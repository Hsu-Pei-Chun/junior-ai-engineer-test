from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from tenacity import retry, stop_after_attempt, wait_fixed
from dotenv import load_dotenv
import json
import logging
from aiocache import cached
from aiocache.serializers import JsonSerializer

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 初始化 FastAPI
app = FastAPI(title="商品描述優化 API")

# 定義請求 Body
class DescriptionRequest(BaseModel):
    description: str

# 讀取 Prompt 文件
def load_prompt():
    with open("optimize_description_prompt.txt", "r", encoding="utf-8") as file:
        return file.read()

# 使用 aiocache 快取結果，避免重複呼叫 OpenAI API
# Retry 機制（API 失敗時最多重試 3 次，每次間隔 2 秒）
@cached(ttl=3600, key_builder=lambda func, *args, **kwargs: f"{args[0]}", serializer=JsonSerializer())
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def optimize_description(text: str) -> str:
    prompt = load_prompt().replace("{商品描述}", text)

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(  
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": prompt}],
            max_tokens=500
        )

        logging.info(f"OpenAI API 回應: {response}")
        print(f"🔍 OpenAI API 回應: {response}")

        if not response.choices or not response.choices[0].message.content:
            raise HTTPException(status_code=500, detail="❌ OpenAI API 回應為空")

        optimized_text =response.choices[0].message.content.strip() if response.choices else ""

        if not optimized_text:
            raise HTTPException(status_code=500, detail="❌ OpenAI API 回應為空")
        
        try:
            return json.loads(optimized_text)
        except json.JSONDecodeError as e:
            logging.error(f"❌ JSON 解析錯誤: {e}")
            raise HTTPException(status_code=500, detail=f"OpenAI API 回應格式錯誤: {str(e)}")

    except Exception as e:
        logging.error(f"❌ OpenAI API 失敗: {e}")
        raise HTTPException(status_code=500, detail=f"OpenAI API 失敗: {str(e)}")

@app.post("/summarized-description")
async def summarize_description(request: DescriptionRequest):
    if not request.description.strip():
        raise HTTPException(status_code=400, detail="❌ 商品描述不可為空")

    optimized_text = await optimize_description(request.description)
    return optimized_text

# 啟動方式（開發模式）
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
