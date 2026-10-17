import json
import logging
import os
from flask import Flask, render_template
from publisher import process_queue

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BioHub")

app = Flask(__name__)


def load_links():
  """Safely loads social links with fallbacks for filesystem and parsing edge cases."""
  json_path = os.path.join(os.path.dirname(__file__), "links.json")

  if not os.path.exists(json_path):
    logger.error(f"Edge Case Triggered: {json_path} does not exist.")
    return []

  try:
    with open(json_path, "r", encoding="utf-8") as f:
      links = json.load(f)
      if not isinstance(links, list):
        logger.error(
            "Edge Case Triggered: links.json content is not a JSON list."
        )
        return []
      return links
  except json.JSONDecodeError as e:
    logger.error(f"Edge Case Triggered: Syntax error in links.json: {e}")
    return []
  except Exception as e:
    logger.error(f"Unexpected error loading links: {e}")
    return []


@app.route("/")
def index():
  links = load_links()
  return render_template(
      "index.html",
      name="Antenyi Joseph Ochohepo",
      title="Full-Stack Software Engineer & Backend Developer",
      links=links,
  )
@app.route("/run-publisher-job")
def run_publisher_job():
    # You can add basic token protection here if you want security
    process_queue()
    return "Publisher executed successfully!" 


if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=5000)