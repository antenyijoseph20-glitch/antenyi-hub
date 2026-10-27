
import json

import publisher


def test_preview_does_not_mark_post_as_published(tmp_path, monkeypatch):
    queue_path = tmp_path / "queue.json"
    original_queue = [
        {
            "id": 101,
            "topic": "Test post",
            "content": "This is test content.",
            "status": "Ready",
        }
    ]
    queue_path.write_text(
        json.dumps(original_queue),
        encoding="utf-8",
    )

    monkeypatch.setattr(publisher, "QUEUE_FILE", str(queue_path))

    publisher.process_queue()

    updated_queue = json.loads(queue_path.read_text(encoding="utf-8"))

    assert updated_queue[0]["status"] == "Ready"
    assert "published_at" not in updated_queue[0]
