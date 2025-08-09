from app.database import messages
from app.models import Message
from app.utils import parse_message_payload, parse_status_payload, format_timestamp
from bson.objectid import ObjectId

async def process_payload(payload):
    msgs= parse_message_payload(payload)
    statuses= parse_status_payload(payload)
    if msgs:
        await messages.insert_many(msgs)
    if statuses:
        for status in statuses:
            await messages.update_one(
                {"meta_msg_id": status["meta_msg_id"]},
                {"$set": {"status": status["status"]}}
            )

async def get_messages_by_user(wa_id):
    return await messages.find({"wa_id":wa_id}).to_list(100)

async def get_all_conversations():
    return await messages.aggregate([
        {"$group":{"_id":"$wa_id","last_msg":{"$last":"$text"}, "timestamp": {"$last":"$timestamp"}}},
        {"$sort":{"timestamp":-1}}
    ]).to_list(100)

async def insert_message(data):
    await messages.insert_one(data)
