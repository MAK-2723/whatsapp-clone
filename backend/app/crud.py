from app.database import messages
from app.models import Message
from bson.objectid import ObjectId

async def process_payload(payload):
    if "messages" in payload:
        for msg in payload["messages"]:
            await messages.insert_one({
                "wa_id": msg["from"],
                "name": payload["contacts"][0]["profile"]["name"],
                "text": msg["text"]["body"],
                "timestamp": msg["timestamp"],
                "status": "sent",
                "meta_msg_id": msg["id"]
            })
    elif "statuses" in payload:
        for status in payload["statuses"]:
            await messages.update_one({"meta_msg_id":status["id"]}.{"$set":{"status":status["status"]}})

async def get_messages_by_user(wa_id):
    return await messages.find({"wa_id":wa_id}).to_list(100)

async def get_all_conversations():
    return await messages.aggregate([
        {"$group":{"_id":"$wa_id","last_msg":{"$last":"$text"}, "timestamp": {"$last":"$timestamp"}}},
        {"$sort":{"timestamp":-1}}
    ]).to_list(100)

async def insert_message(data):
    await messages.insert_one(data)
