
import hmac
import json
import logging
import os

from flask import Flask, jsonify, render_template, request
from publisher import process_queue

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BioHub")

app = Flask(__name__)


def load_links():
    """Safely load social links, with a fallback for file errors."""
    json_path = os.path.join(os.path.dirname(__file__), "links.json")

    if not os.path.exists(json_path):
        logger.error("Links file does not exist: %s", json_path)
        return []

    try:
        with open(json_path, "r", encoding="utf-8") as file:
            links = json.load(file)

        if not isinstance(links, list):
            logger.error("links.json content is not a JSON list.")
            return []

        return links

    except (json.JSONDecodeError, OSError) as error:
        logger.error("Unable to load links: %s", error)
        return []


@app.route("/")
def index():
    """Render the homepage."""
    return render_template(
        "index.html",
        name="Antenyi Joseph Ochohepo",
        title="Full-Stack Software Engineer & Backend Developer",
        links=load_links(),
    )


@app.route("/run-publisher-job", methods=["POST"])
def run_publisher_job():
    """Authorize a publisher job using a secret request header."""
    expected_secret = os.environ.get("PUBLISHER_SECRET_KEY")
    supplied_secret = request.headers.get("X-Publisher-Secret", "")

    if not expected_secret or not supplied_secret:
        return jsonify(error="Unauthorized"), 403

    if not hmac.compare_digest(supplied_secret, expected_secret):
        return jsonify(error="Unauthorized"), 403

    process_queue()
    return jsonify(message="Publisher job executed."), 200


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "").lower() == "true")
