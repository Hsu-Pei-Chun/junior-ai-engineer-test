from fastapi.testclient import TestClient
from optimize_description import app

client = TestClient(app)

def test_summarize_description():
    payload = {"description": "這款智能手錶具備心率監測與 GPS 追蹤，適合運動健身。"}
    response = client.post("/summarized-description", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "summarized_description" in data  # 確保回應包含 `summarized_description`
    assert "title" in data ["summarized_description"]  # 確保有 `title`
    assert "summary" in data["summarized_description"]  # 確保有 `summary`
    assert "bullet_points" in data["summarized_description"]  # 確保有 `bullet_points`


def test_invalid_json():
        """ 測試 JSON 格式錯誤時 API 是否能處理 """
        response = client.post("/summarized-description", content="invalid json")
        assert response.status_code == 422  # FastAPI 內建的請求格式錯誤代碼