# DeepSeekAPI LocalUsageQuery

在本地通过Python获取DeepSeekAPI的用量信息

## 功能

- 在本地获取你的DeepSeekAPI用量信息，并支持导出成Excel表格，效果如下:  
![pj5](https://raw.githubusercontent.com/TLBtianlang/DeepSeekAPI_LocalUsageQuery/refs/heads/main/pg/pg5.png)  
![pj6](https://raw.githubusercontent.com/TLBtianlang/DeepSeekAPI_LocalUsageQuery/refs/heads/main/pg/pg6.png)  

## 说明

-   本项目采用 Python 3.12.0版本
-   本项目遵循MIT开源协议

## 配置教程

1.在浏览器打开[DeepSeek开放平台](https://platform.deepseek.com/usage)  
2.打开 开发人员工具(f12)  
3.刷新网页  
4.找到名称为 [https://platform.deepseek.com/api/v0/usage/amount?month=6&year=2026](https://platform.deepseek.com/api/v0/usage/amount?month=6&year=2026) 项  
![pg1](https://raw.githubusercontent.com/TLBtianlang/DeepSeekAPI_LocalUsageQuery/refs/heads/main/pg/pg1.png)  
5.右键并选择 复制 > 复制为 cURL ( bash )  
![pj2](https://raw.githubusercontent.com/TLBtianlang/DeepSeekAPI_LocalUsageQuery/refs/heads/main/pg/pg2.png)  
6.将复制内容复制到记事本中  
7.将复制内容中的 authorization: Bearer 后的内容和 -b 后的内容依次填入到 GET.json 的 Bearer token 值和 cookie 值中  
![pj3](https://raw.githubusercontent.com/TLBtianlang/DeepSeekAPI_LocalUsageQuery/refs/heads/main/pg/pg3.png)  
最终 GET.json 中的格式如下图:  
![pj4](https://raw.githubusercontent.com/TLBtianlang/DeepSeekAPI_LocalUsageQuery/refs/heads/main/pg/pg4.png)  
8.大功告成
