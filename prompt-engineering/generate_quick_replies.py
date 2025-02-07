import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def load_prompt():
    with open("quick_replies_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

# 生成 Quick Replies 的函式
def generate_quick_replies(chat_history, faq_list, product_list):
    prompt = load_prompt()

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"這是過去的對話歷史: {json.dumps(chat_history, ensure_ascii=False)}"},
                {"role": "user", "content": f"FAQ 清單: {json.dumps(faq_list, ensure_ascii=False)}"},
                {"role": "user", "content": f"產品清單: {json.dumps(product_list, ensure_ascii=False)}"},
            ],
            max_tokens=100
        )

        quick_replies = response.choices[0].message.content
        return quick_replies

    except Exception as e:
        print(f"發生錯誤: {e}")
        return None

# 測試函式
if __name__ == "__main__":
    test_data = {
        "chat_history": [
            {"role": "user", "content": "我要買送給愛好 3C 產品的朋友的禮物，該選哪個好？"},
            {"role": "assistant", "content": "推薦這幾款熱門 3C 產品：1. MacBook Pro 💻 2. iPad 0 元 📱"}
        ],
        "faq_list": ["如何成為會員", "如何取得優惠券", "退貨政策是什麼"],
        "product_list": ["MacBook Pro", "iPad 0 元", "高效保濕面膜", "無痕內衣"]
    }

    replies = generate_quick_replies(
        test_data["chat_history"], test_data["faq_list"], test_data["product_list"]
    )

    print("產生的 Quick Replies:")
    print(replies)
