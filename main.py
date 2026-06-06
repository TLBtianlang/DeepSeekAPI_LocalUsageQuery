import requests
import json
import api_get
import organize

api_get.get_api(save=True)
new_data = organize.load_and_merge("amount.json", "cost.json")
if new_data.empty:
    print("未读取到任何有效数据，请检查 JSON 文件。")
else:
    organize.update_excel(new_data)