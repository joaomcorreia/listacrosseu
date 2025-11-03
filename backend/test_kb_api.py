import requests
import json

# Test KB list endpoint
response = requests.get("http://127.0.0.1:8000/api/assistant/kb")
print("KB List API:")
print(json.dumps(response.json(), indent=2))

# Test KB embed endpoint
embed_data = {"id": 1}
response = requests.post(
    "http://127.0.0.1:8000/api/assistant/kb/embed",
    json=embed_data
)
print("\nKB Embed API:")
print(json.dumps(response.json(), indent=2))

# Check if the document was updated
response = requests.get("http://127.0.0.1:8000/api/assistant/kb")
print("\nUpdated KB List (should show embedded_at timestamp):")
for doc in response.json()["items"]:
    if doc["id"] == 1:
        print(f"Document {doc['slug']}: embedded_at = {doc['embedded_at']}")