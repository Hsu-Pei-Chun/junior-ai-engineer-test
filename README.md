# Junior AI Engineer Coding Test - 解題說明

## 簡介

此文件記錄我對 **Junior AI Engineer Coding Test** 的解題過程，包括 **Prompt Engineering** 和 **API Development** 兩大類別的題目，涵蓋解題思路、技術選擇、測試結果及改進方向。

## 解題項目

本測試要求完成以下 **三個題目**，我依據需求進行了開發與測試：

1. **Prompt Engineering - Quick Replies**

   - 設計 task prompt 來產生 Quick Replies，以提高用戶留存率與互動性。
   - 測試 prompt 的穩定性，運行 50 次測試，記錄結果與時間。

2. **Prompt Engineering - 退貨流程對話設計**

   - 設計 task prompt，引導用戶提供完整退貨資訊（姓名、電話、訂單單號、退貨品名、理由）。
   - 確保 prompt 的輸出品質與穩定性。

3. **API Development - 商品描述優化 API**

   - 使用 **FastAPI** 開發 API，清理並優化商品描述，使其更精煉且具結構化，以節省 token 使用。
   - 處理 API 錯誤並測試不同輸入情境。

---

## 環境設置

本專案使用 `FastAPI` 並依賴 `openai` API，所有依賴皆透過 `Poetry` 進行管理。

### 1. 安裝依賴

請確保已安裝 `Poetry`，若尚未安裝，可使用以下指令：

```bash
pip install poetry
```

接著，執行以下指令安裝所有專案依賴：

```bash
poetry install
```

### 2. 設定環境變數

請在 `.env` 文件中設置 `OPENAI_API_KEY`。

```env
OPENAI_API_KEY=your_api_key_here
```

若使用 `Poetry` 內建虛擬環境，請執行以下指令進入環境：

```bash
poetry shell
```

---

## 解題實作與技術細節

### **Prompt Engineering - Quick Replies**

- `generate_quick_replies.py`: 生成 Quick Replies。
- `quick_replies_prompt.txt`: Prompt 設計。
- `test_quick_replies.py`: 測試 prompt 穩定性。
- `test_results.json`: 測試結果。

### **Prompt Engineering - 退貨流程對話設計**

- `return_request.py`: 收集退貨資訊的 AI 對話設計。
- `return_request_prompt.txt`: Prompt 設計。

### **API Development - 商品描述優化 API**

- `optimize_description.py`: FastAPI 服務，用於優化商品描述。
- `optimize_description_prompt.txt`: Prompt 設計。

---

## 運行方式

### 1. 運行 FastAPI 服務

```bash
uvicorn optimize_description:app --host 0.0.0.0 --port 8000
```

API 測試請求示例（使用 Postman）：

1. 開啟 Postman，選擇 `POST` 請求。
2. 在 `URL` 欄位輸入：`http://localhost:8000/summarized-description`
3. 切換至 `Body`，選擇 `raw`，格式設為 `JSON`。
4. 輸入以下 JSON 內容：

```json
{
  "id": 10234,
  "uri": "https://sportstore.com/products/xyz123",
  "price": 2500.0,
  "title": "高性能運動跑鞋",
  "status": 1,
  "vendor": "sportstore",
  "summary": "🏃‍♂️ 適合長跑與訓練的專業運動鞋，提供極致舒適與支撐，適應各種地形。",
  "description": "這款運動跑鞋採用透氣網布設計，搭配輕量減震大底，提升跑步體驗。無論是日常訓練還是長距離跑步，都能提供穩定支撐與舒適穿著體驗。",
  "categories": ["運動鞋", "長跑專用", "訓練裝備"]
}
```

### 2. 測試 Quick Replies

```bash
python test_quick_replies.py
```

測試結果將存儲在 `test_results.json`。

其中包含：

- **總測試數** (`total_tests`)
- **成功數** (`success_count`)
- **失敗數** (`fail_count`)
- **平均回應時間** (`avg_response_time`)
- **最短/最長回應時間** (`min_response_time`, `max_response_time`)

### 3. 測試退貨流程對話

```bash
python return_request.py
```



