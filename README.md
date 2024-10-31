# Taiwan E-Hospital Crawler

這是一個用於抓取台灣e院 (https://sp1.hso.mohw.gov.tw/doctor/) 問答資料的爬蟲專案。此爬蟲可以擷取從網站第一筆到 2024/10/31 之間的所有問答紀錄（僅包含有問有答，若問題被刪除則無法抓取到），內容包含提問者資訊與醫生回覆內容。

## 爬取資訊

- 提問者基本資訊（化名、性別、年齡範圍）
- 提問內容與日期
- 回覆醫生資訊（醫院、科別、姓名）
- 醫生回覆內容與日期

## 環境設置

### 1. 建立虛擬環境

#### macOS/Linux
```bash
# 建立虛擬環境
python3 -m venv .venv
```

### 2 安裝相依套件
```bash
# 安裝所需套件
pip install scrapy beautifulsoup4 lxml

# 匯出相依套件清單（optional）
pip freeze > requirements.txt
```

如果有 requirements.txt，也可以直接安裝所有相依套件：
```bash
pip install -r requirements.txt
```

## 專案結構

```
.
├── README.md
├── scrapy.cfg
└── taiwan_e_hospital
    ├── __init__.py
    ├── items.py                # 定義資料結構
    ├── middlewares.py
    ├── pipelines.py            # 資料處理與儲存邏輯
    ├── settings.py
    └── spiders                 # 主要爬蟲邏輯
        ├── __init__.py
        └── get_question_response.py
```

## 資料欄位

- `question_id`: 問題編號
- `questioner_name`: 提問者姓名
- `questioner_gender`: 提問者性別
- `questioner_age_range`: 提問者年齡範圍
- `question_date`: 提問日期
- `question_text`: 提問內容
- `doctor_hospital`: 回覆醫師所屬醫院
- `doctor_department`: 回覆醫師科別
- `doctor_name`: 回覆醫師姓名
- `reply_date`: 回覆日期
- `answer_text`: 回覆內容

具體輸出結構可參考 [Demo File](https://github.com/iamalex33329/chatgpt-develop-guide-zhtw/blob/master/demo.json)

## 資料庫結構

資料會被儲存在 `tw_e_hospital.sqlite` 資料庫中的 `qanda` 表格，包含所有上述欄位。

## 執行爬蟲

```bash
# 執行這行會直接把資料寫進資料庫
scrapy crawl taiwan_e_hospital

# 執行這行會多輸出一份 json 檔案
scrapy crawl taiwan_e_hospital -o output.json -t json
```