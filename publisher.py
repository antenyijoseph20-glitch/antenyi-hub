import json
from datetime import datetime

QUEUE_FILE = "queue.json"

def process_queue():
    try:
        with open(QUEUE_FILE, "r") as f:
            queue = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {QUEUE_FILE}: {e}")
        return

    published_count = 0
    for item in queue:
        # Publish the first "Ready" item found
        if item.get("status") == "Ready":
            print("=" * 50)
            print(f"🚀 PUBLISHING POST #{item['id']}: {item['topic']}")
            print("=" * 50)
            print(item['content'])
            print("=" * 50)
            
            # Update status
            item["status"] = "Published"
            item["published_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            published_count += 1
            break  # Publish one post per execution

    if published_count > 0:
        with open(QUEUE_FILE, "w") as f:
            json.dump(queue, f, indent=2)
        print("\n✅ queue.json updated successfully!")
    else:
        print("ℹ️ No pending posts with status 'Ready' found.")

if __name__ == "__main__":
    process_queue()
