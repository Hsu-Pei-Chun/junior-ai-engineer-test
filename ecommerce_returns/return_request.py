import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def load_prompt():
    with open("return_request_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def collect_return_info():
    """ 與 AI 互動，逐步蒐集退貨資訊 """
    prompt = load_prompt()
    collected_info = {}  # 存儲用戶填寫的資訊
    required_fields = ["customer_name", "customer_phone", "order_id", "product_name", "return_reason"]

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    while len(collected_info) < len(required_fields):
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"目前已收集的資訊: {json.dumps(collected_info, ensure_ascii=False)}"}
            ],
            max_tokens=200
        )

        result = response.choices[0].message.content
        print("🔍 AI 回應：", result)

        try:
            parsed_result = json.loads(result)
            
            # 如果 AI 要求下一個問題
            if "next_question" in parsed_result:
                user_input = input(parsed_result["next_question"] + " ")  # 讓用戶輸入
                key = required_fields[len(collected_info)]
                collected_info[key] = user_input
                print("✅ 目前已收集的資訊：", collected_info)
            # 如果所有資訊齊全
            if len(collected_info) == len(required_fields):
                return collected_info
        
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析錯誤: {e}")
            print(f"❌ OpenAI API 回應: {result}")

    return None

# ✅ 測試函式
if __name__ == "__main__":
    return_info = collect_return_info()
    print("✅ 最終蒐集的退貨資訊:")
    print(json.dumps(return_info, ensure_ascii=False, indent=4))
