from fastapi.testclient import TestClient
from optimize_description import app
import pytest
import time
import openai
from concurrent.futures import ThreadPoolExecutor
from optimize_description import optimize_description
from types import SimpleNamespace


client = TestClient(app)
URL = "/summarized-description"

def test_summarize_description():
    payload = {"description": "這款智能手錶具備心率監測與 GPS 追蹤，適合運動健身。"}
    response = client.post(URL, json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "summarized_description" in data  # 確保回應包含 `summarized_description`
    assert "title" in data ["summarized_description"]  # 確保有 `title`
    assert "summary" in data["summarized_description"]  # 確保有 `summary`
    assert "bullet_points" in data["summarized_description"]  # 確保有 `bullet_points`

def test_invalid_json():
        """ 測試 JSON 格式錯誤時 API 是否能處理 """
        response = client.post(URL, content="invalid json")
        assert response.status_code == 422  # FastAPI 內建的請求格式錯誤代碼

@pytest.mark.benchmark
def test_async_api_performance(benchmark):
    payload = {"description": "這款智能手錶具備心率監測與 GPS 追蹤，適合運動健身。"}

    def send_request():
        start_time = time.perf_counter()
        response = client.post(URL, json=payload)
        end_time = time.perf_counter()

        assert response.status_code == 200
        return end_time - start_time
    
    avg_time = 0 
    
    try:
    
        # 先測量單一請求的效能
        execution_time = benchmark(send_request)

        # 使用多執行緒來模擬並發請求
        with ThreadPoolExecutor(max_workers=10) as executor:
            execution_times = list(executor.map(lambda _: send_request(), range(30)))


        avg_time = sum(execution_times) / len(execution_times)

    finally:
        with open("benchmark.log", "a", encoding="utf-8") as f:
            f.write(f"非同步 API 50 個請求平均執行時間: {avg_time}\n")

    print(f"🚀 50 個請求的平均執行時間: {avg_time:.4f} 秒")

def test_cache_mechanism(monkeypatch):

    import asyncio
    asyncio.run(optimize_description.cache.clear())

    # 用來記錄 fake API 呼叫次數
    call_count = {"calls": 0}

    # 定義 fake 的 completions.create 方法
    class FakeChatCompletions:
        def create(self, *args, **kwargs):
            call_count["calls"] += 1
            # 回傳模擬的 API 回應（格式需與原本程式相符）
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        message=SimpleNamespace(
                            content='{"summarized_description": {"title": "Test Title", "summary": "Test Summary", "bullet_points": ["A", "B"]}}'
                        )
                    )
                ]
            )

    # 定義 fake 的 chat 物件
    class FakeChat:
        completions = FakeChatCompletions()

    # 定義 fake 的 OpenAI 類別，回傳 FakeChat
    class FakeOpenAI:
        def __init__(self, api_key):
            self.api_key = api_key
            self.chat = FakeChat()

    # 使用 monkeypatch 將 openai.OpenAI 替換成我們的 FakeOpenAI
    monkeypatch.setattr(openai, "OpenAI", FakeOpenAI)

    payload = {"description": "這款智能手錶具備心率監測與 GPS 追蹤，適合運動健身。"}

    # 第一次呼叫：會真正執行 API 呼叫
    response1 = client.post(URL, json=payload)
    assert response1.status_code == 200

    # 第二次呼叫相同輸入：應該從快取取得，不會再呼叫 FakeOpenAI 的 create 方法
    response2 = client.post(URL, json=payload)
    assert response2.status_code == 200

    # 若快取機制正常，FakeChatCompletions.create 應只被呼叫一次
    assert call_count["calls"] == 1
