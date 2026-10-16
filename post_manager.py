import json
import os


def load_queue():
  path = "queue.json"
  if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
      return json.load(f)
  return []


def save_queue(queue):
  with open("queue.json", "w", encoding="utf-8") as f:
    json.dump(queue, f, indent=4)


def view_ready_posts():
  queue = load_queue()
  ready_posts = [p for p in queue if p["status"] == "Ready"]

  print(f"\n--- Content Queue Status ({len(ready_posts)} posts ready) ---")
  for post in ready_posts:
    print(f"\n[ID: {post['id']}] Topic: {post['topic']}")
    print(f"Content: {post['content']}")
    print("-" * 40)


if __name__ == "__main__":
  # Quick terminal interface to check your content bank
  while True:
    print("\n--- Antenyi's Social Content Manager ---")
    print("1. View Ready Posts in Queue")
    print("2. Exit")
    choice = input("Choose an option (1-2): ").strip()

    if choice == "1":
      view_ready_posts()
    elif choice == "2":
      print("Exiting content manager. Keep building!")
      break
    else:
      print("Invalid choice. Try again.")