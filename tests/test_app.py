
from unittest.mock import patch

import app as application


def test_homepage_returns_success():
    client = application.app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_get_request_cannot_trigger_publisher():
    client = application.app.test_client()

    with patch.object(application, "process_queue") as mock_process:
        response = client.get("/run-publisher-job")

    assert response.status_code == 405
    mock_process.assert_not_called()


def test_missing_secret_is_rejected():
    client = application.app.test_client()

    with (
        patch.dict("os.environ", {}, clear=False),
        patch.object(application.os.environ, "get", return_value=None),
        patch.object(application, "process_queue") as mock_process,
    ):
        response = client.post("/run-publisher-job")

    assert response.status_code == 403
    mock_process.assert_not_called()


def test_incorrect_header_secret_is_rejected():
    client = application.app.test_client()

    with (
        patch.dict(
            "os.environ",
            {"PUBLISHER_SECRET_KEY": "test-secret"},
        ),
        patch.object(application, "process_queue") as mock_process,
    ):
        response = client.post(
            "/run-publisher-job",
            headers={"X-Publisher-Secret": "wrong-secret"},
        )

    assert response.status_code == 403
    mock_process.assert_not_called()


def test_valid_header_secret_triggers_publisher():
    client = application.app.test_client()

    with (
        patch.dict(
            "os.environ",
            {"PUBLISHER_SECRET_KEY": "test-secret"},
        ),
        patch.object(application, "process_queue") as mock_process,
    ):
        response = client.post(
            "/run-publisher-job",
            headers={"X-Publisher-Secret": "test-secret"},
        )

    assert response.status_code == 200
    mock_process.assert_called_once_with()
