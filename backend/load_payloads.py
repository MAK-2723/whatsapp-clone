import os, json, asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

WEBHOOK_ENDPOINT = f"{BACKEND_URL.rstrip('/')}/webhooks/"

folder = os.path.join(os.path.dirname(__file__), "sample_payloads")

async def load():
    if not os.path.exists(folder):
        print(f"❌ Payload folder not found: {folder}")
        return

    async with httpx.AsyncClient() as client:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if not filename.lower().endswith(".json"):
                print(f"⚠️ Skipping non-JSON file: {filename}")
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    payload = json.load(f)

                response = await client.post(WEBHOOK_ENDPOINT, json=payload)

                if response.status_code == 200:
                    print(f"✅ Sent payload from {filename} successfully")
                else:
                    print(f"⚠️ Failed to send {filename}: {response.status_code} - {response.text}")

            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")

if __name__ == "__main__":
    asyncio.run(load())
