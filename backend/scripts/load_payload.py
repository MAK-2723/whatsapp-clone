import os, json, asyncio
import httpx

async def load():
    folder= "../../sample_payloads"
    async with httpx.AsyncClient() as client:
        for filename in os.listdir(folder):
            with open(os.path.join(folder,filename)) as f:
                payload=json.load(f)
                await client.post("http://loacalhost:8000/webhooks/", json=payload)

if __name__=="__main__":
    asyncio.run(load())
