import json
import pandas as pd
import os

EXCEL_FILE = "DeepSeekAPI用量.xlsx"
SHEET_DETAIL = "每日明细"
SHEET_SUMMARY = "月度汇总"

def usage_dict(usage_list):
    """将 usage 列表转为字典"""
    return {item["type"]: item["amount"] for item in usage_list}

def load_and_merge(amount_file="amount.json", cost_file="cost.json"):
    """读取 amount.json 和 cost.json，返回融合后的明细 DataFrame（包含全零行）"""
    with open(amount_file, "r", encoding="utf-8") as f:
        amount_data = json.load(f)
    with open(cost_file, "r", encoding="utf-8") as f:
        cost_data = json.load(f)

    amount_biz = amount_data["data"]["biz_data"]
    cost_biz_raw = cost_data["data"]["biz_data"]
    if isinstance(cost_biz_raw, list):
        cost_biz = cost_biz_raw[0]
    else:
        cost_biz = cost_biz_raw

    amount_days = {day["date"]: day["data"] for day in amount_biz["days"]}
    cost_days = {day["date"]: day["data"] for day in cost_biz["days"]}
    all_dates = set(amount_days.keys()) | set(cost_days.keys())

    rows = []
    for date in sorted(all_dates):
        amount_day_data = {item["model"]: usage_dict(item["usage"]) for item in amount_days.get(date, [])}
        cost_day_data = {item["model"]: usage_dict(item["usage"]) for item in cost_days.get(date, [])}
        all_models = set(amount_day_data.keys()) | set(cost_day_data.keys())
        for model in all_models:
            a = amount_day_data.get(model, {})
            c = cost_day_data.get(model, {})
            rows.append({
                "日期": date,
                "模型": model,
                "输入Token": int(a.get("PROMPT_TOKEN", 0)),
                "缓存命中Token": int(a.get("PROMPT_CACHE_HIT_TOKEN", 0)),
                "缓存未命中Token": int(a.get("PROMPT_CACHE_MISS_TOKEN", 0)),
                "输出Token": int(a.get("RESPONSE_TOKEN", 0)),
                "请求次数": int(a.get("REQUEST", 0)),
                "输入费用(元)": float(c.get("PROMPT_TOKEN", 0)),
                "缓存命中费用(元)": float(c.get("PROMPT_CACHE_HIT_TOKEN", 0)),
                "缓存未命中费用(元)": float(c.get("PROMPT_CACHE_MISS_TOKEN", 0)),
                "输出费用(元)": float(c.get("RESPONSE_TOKEN", 0)),
                "请求费用(元)": float(c.get("REQUEST", 0))
            })
    return pd.DataFrame(rows)

def recompute_summary(detail_df):
    """根据明细 DataFrame 重新计算汇总表"""
    if detail_df.empty:
        return pd.DataFrame()
    numeric_cols = ["输入Token", "缓存命中Token", "缓存未命中Token", "输出Token", "请求次数",
                    "输入费用(元)", "缓存命中费用(元)", "缓存未命中费用(元)", "输出费用(元)", "请求费用(元)"]
    summary = detail_df.groupby("模型")[numeric_cols].sum().reset_index()
    return summary

def update_excel(new_detail_df, excel_path=EXCEL_FILE):
    """将新明细数据合并到现有 Excel，覆盖同一天同模型的数据，并过滤全零行"""
    if os.path.exists(excel_path):
        try:
            old_detail = pd.read_excel(excel_path, sheet_name=SHEET_DETAIL)
            old_detail["日期"] = old_detail["日期"].astype(str)
        except Exception as e:
            print(f"读取旧 Excel 失败，将创建新文件: {e}")
            old_detail = pd.DataFrame()
    else:
        old_detail = pd.DataFrame()

    new_detail_df["日期"] = new_detail_df["日期"].astype(str)
    if not old_detail.empty:
        old_detail = old_detail[~old_detail.set_index(["日期", "模型"]).index.isin(
            new_detail_df.set_index(["日期", "模型"]).index
        )]
        combined = pd.concat([old_detail, new_detail_df], ignore_index=True)
    else:
        combined = new_detail_df

    numeric_cols_filter = ["输入Token", "缓存命中Token", "缓存未命中Token", "输出Token", "请求次数",
                           "输入费用(元)", "缓存命中费用(元)", "缓存未命中费用(元)", "输出费用(元)", "请求费用(元)"]
    keep_mask = (combined[numeric_cols_filter] != 0).any(axis=1)
    combined = combined[keep_mask].copy()

    combined["日期"] = pd.to_datetime(combined["日期"])
    combined = combined.sort_values("日期").reset_index(drop=True)
    combined["日期"] = combined["日期"].dt.strftime("%Y-%m-%d")

    summary_df = recompute_summary(combined)

    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        combined.to_excel(writer, sheet_name=SHEET_DETAIL, index=False)
        summary_df.to_excel(writer, sheet_name=SHEET_SUMMARY, index=False)

    print(f"更新成功！明细表共 {len(combined)} 条非零记录，汇总表共 {len(summary_df)} 个模型。")
    print(f"文件保存为: {excel_path}")


if __name__ == "__main__":
    new_data = load_and_merge("amount.json", "cost.json")
    if new_data.empty:
        print("未读取到任何有效数据，请检查 JSON 文件。")
    else:
        update_excel(new_data)
