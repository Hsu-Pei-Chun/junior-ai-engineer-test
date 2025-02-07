import json
import time
from generate_quick_replies import generate_quick_replies

# 測試數據
test_data = {
    "chat_history": [
        {"role": "user", "content": "我要買送給愛好 3C 產品的朋友的禮物，該選哪個好？"},
        {"role": "assistant", "content": "推薦這幾款熱門 3C 產品：1. MacBook Pro 💻 2. iPad 0 元 📱"}
    ],
    "faq_list": ["如何成為會員", "如何取得優惠券", "退貨政策是什麼"],
    "product_list": ["MacBook Pro", "iPad 0 元", "高效保濕面膜", "無痕內衣"]
}

# 測試次數
TEST_RUNS = 50
test_results = []
success_count = 0
fail_count = 0
response_times = []

for i in range(TEST_RUNS):
    print(f"測試 {i+1}/{TEST_RUNS} ...")
    start_time = time.time()

    try:
        replies = generate_quick_replies(
            test_data["chat_history"],
            test_data["faq_list"],
            test_data["product_list"]
        )
        end_time = time.time()
        response_time = round(end_time - start_time, 2)  # 計算生成時間

        # 確保回應是 JSON 並有 5 個 Quick Replies
        assert isinstance(replies, list), "輸出格式錯誤，應該為 JSON 陣列"
        assert len(replies) == 5, f"輸出數量錯誤，應該是 5 個，但收到 {len(replies)} 個"

        test_results.append({
            "test_case": i + 1,
            "quick_replies": replies,
            "response_time": response_time
        })

        success_count += 1  # 成功計數 +1
        response_times.append(response_time)  # 記錄 response time

    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        test_results.append({
            "test_case": i + 1,
            "error": str(e),
            "response_time": None
        })
        fail_count += 1  # 失敗計數 +1

# 計算測試總覽數據
summary = {
    "total_tests": TEST_RUNS,  # 測試總次數
    "success_count": success_count,  # 成功測試數
    "fail_count": fail_count,  # 失敗測試數
    "avg_response_time": round(sum(response_times) / len(response_times), 2) if response_times else None,  # 平均生成時間
    "min_response_time": min(response_times) if response_times else None,  # 最快生成時間
    "max_response_time": max(response_times) if response_times else None  # 最慢生成時間
}

# 讓 summary 放在最上方
final_data = {
    "summary": summary,  # ✅ 先放總覽
    "tests": test_results  # ✅ 再放詳細測試案例
}

# 覆蓋原本的 test_results.json
with open("test_results.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=4)

print("✅ 測試完成，結果已儲存至 test_results.json")
