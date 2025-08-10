from app.database import messages
from app.models import Message
from app.utils import parse_message_payload, parse_status_payload, format_timestamp
from bson.objectid import ObjectId
import logging

logger=logging.getLogger("crud")

async def process_payload(payload):
    logger.info("process_payload called")
    try:
        msgs= parse_message_payload(payload)
        statuses= parse_status_payload(payload)
        if msgs:
            logger.info("Inserting messages: %s", msgs)
            await messages.insert_many(msgs)
            logger.info("Inserted messages!")
        if statuses:
            for status in statuses:
                logger.info("Updating statuses: %s", status)
                result= await messages.update_one(
                    {"meta_msg_id": status["meta_msg_id"]},
                    {"$set": {"status": status["status"]}}
                )
            logger.info("Matched %s Modified %s", result.matched_count, result.modified_count)
    except Exception as e:
        logger.error("Error in process_payload: %s", e)
        raise

async def get_messages_by_user(wa_id):
    try:
        return await messages.find({"wa_id":wa_id}).to_list(100)
    except Exception as e:
        logger.error("Error fetching messages: %s", e)
        return []

async def get_all_conversations():
    try:
        pipelines=[
            {"$group":{"_id":"$wa_id","last_msg":{"$last":"$text"}, "timestamp": {"$last":"$timestamp"}}},
            {"$sort":{"timestamp":-1}}
        ]
        res= await messages.aggregate(pipeline).to_list(100)
        return res
    except Exception as e:
        logger.error("Error fetching conversations: %s", e)
        return []

async def insert_message(data):
    try:
        if wa_id not in data or text not in data:
            raise ValueError("wa_id and text required")
        await messages.insert_one(data)
    except Exception as e:
        logger.error("Error inserting message: %s", e)
        raise
