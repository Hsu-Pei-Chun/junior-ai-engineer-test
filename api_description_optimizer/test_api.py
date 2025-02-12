from fastapi.testclient import TestClient
from optimize_description import app
import pytest
import time
from concurrent.futures import ThreadPoolExecutor

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