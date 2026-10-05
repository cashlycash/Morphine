def test_transform_generates_outputs(client):
    payload = {
        "content": "Morphine helps teams repurpose content quickly for multiple channels.",
        "input_type": "text",
        "output_formats": ["linkedin", "twitter", "executive_summary", "video_script"],
        "parameters": {
            "tone": "Professional",
            "audience": "C-suite",
            "length": "Medium",
            "style": "Data-driven",
            "language": "English",
            "detail_level": "Overview",
            "quality_cost_balance": 0.8,
        },
    }

    response = client.post("/api/v1/transform", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "completed"
    assert len(data["outputs"]) == 4


def test_history_lists_transformations(client):
    payload = {
        "content": "Test history path",
        "input_type": "text",
        "output_formats": ["linkedin"],
        "parameters": {
            "tone": "Professional",
            "audience": "General Public",
            "length": "Short",
            "style": "Formal",
            "language": "English",
            "detail_level": "Overview",
            "quality_cost_balance": 0.5,
        },
    }

    client.post("/api/v1/transform", json=payload)
    history = client.get("/api/v1/history")
    assert history.status_code == 200
    assert len(history.json()["items"]) >= 1
