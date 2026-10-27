
import json
import logging
from pathlib import Path

QUEUE_FILE = Path(__file__).resolve().parent / "queue.json"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BioHub.Publisher")


def process_queue():
    """Preview the next ready post without marking it as published."""
    queue_path = Path(QUEUE_FILE)

    try:
        with queue_path.open("r", encoding="utf-8") as file:
            queue = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, OSError) as error:
        logger.error("Unable to read %s: %s", queue_path, error)
        return

    if not isinstance(queue, list):
        logger.error("The queue must contain a JSON list.")
        return

    for item in queue:
        if not isinstance(item, dict):
            continue

        if item.get("status") == "Ready":
            logger.info(
                "Previewing post #%s: %s",
                item.get("id", "unknown"),
                item.get("topic", "Untitled"),
            )
            print("=" * 50)
            print(item.get("content", ""))
            print("=" * 50)
            logger.info(
                "Preview only: no social platform integration is configured. "
                "The post remains Ready."
            )
            return

    logger.info("No pending posts with status 'Ready' found.")


if __name__ == "__main__":
    process_queue()
