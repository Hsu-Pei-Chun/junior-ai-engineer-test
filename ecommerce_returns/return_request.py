import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def load_prompt():
    """ 讀取 AI 提示詞 """
    with open("return_request_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def ask_ai(prompt, collected_info):
    """ 與 AI 互動，取得下一個問題或驗證輸入 """
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"目前已收集的資訊: {json.dumps(collected_info, ensure_ascii=False)}"}
        ],
        max_tokens=200
    )
    
    try:
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析錯誤: {e}")
        print(f"❌ OpenAI API 回應: {response.choices[0].message.content}")
        return None  # 避免程式崩潰

def collect_return_info():
    """ 與 AI 互動，逐步蒐集退貨資訊 """
    prompt = load_prompt()
    collected_info = {}
    required_fields = ["customer_name", "customer_phone", "order_id", "product_name", "return_reason"]

    while len(collected_info) < len(required_fields):
        parsed_result = ask_ai(prompt, collected_info)
        if not parsed_result:
            continue  # 若 API 回應解析錯誤，跳過這次循環

        # 處理 AI 回傳的錯誤訊息
        if "error_message" in parsed_result:
            print(f"❌ {parsed_result['error_message']}")
            continue  # 讓 AI 重新詢問，避免錯誤的資料被存入

        # 取得下一個問題的鍵
        if "next_question" in parsed_result:
            key = required_fields[len(collected_info)]
            while True:
                user_input = input(parsed_result["next_question"] + " ")
                
                # 把使用者輸入傳回 AI，再次請求驗證
                collected_info[key] = user_input
                validation_result = ask_ai(prompt, collected_info)

                if "error_message" in validation_result:
                    print(f"❌ {validation_result['error_message']} 請重新輸入！")
                    collected_info.pop(key)  # 移除錯誤的輸入，重新詢問
                else:
                    break  # 只有當 AI 確認輸入正確後，才跳出迴圈

            print("✅ 目前已收集的資訊：", collected_info)

        # 若 AI 已確認所有資訊齊全
    while "return_info" not in parsed_result:
        print("⚠️ AI 回應未包含 return_info，請求 AI 再次確認資訊...")
        parsed_result = ask_ai(prompt, collected_info)
        
    return parsed_result["return_info"]
 

# ✅ 測試函式
if __name__ == "__main__":
    return_info = collect_return_info()
    print("✅ 最終蒐集的退貨資訊:")
    print(json.dumps(return_info, ensure_ascii=False, indent=4))
