from datetime import datetime

def make_conversation_id(num1, num2):
    """Create a stable conversation ID for two numbers."""
    return "_".join(sorted([str(num1), str(num2)]))

def parse_message_payload(payload: dict) -> list:
    """Extracts messages from a WhatsApp webhook payload with conversation_id."""
    messages = []
    # Unwrap if 'metaData' key exists
    data = payload.get("metaData", payload)
    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            contacts = value.get("contacts", [{}])
            contact = contacts[0] if contacts else {}
            business_number = value.get("metadata", {}).get("display_phone_number")
            for msg in value.get("messages", []):
                from_num = msg.get("from")
                # Generate conversation ID
                conversation_id = make_conversation_id(from_num, business_number)
                messages.append({
                    "conversation_id": conversation_id,
                    "wa_id": from_num,
                    "name": contact.get("profile", {}).get("name", "Unknown"),
                    "text": msg.get("text", {}).get("body", ""),
                    "timestamp": format_timestamp(msg.get("timestamp")),
                    "status": "sent" if from_num == business_number else "received",
                    "meta_msg_id": msg.get("id")
                })
    return messages


def parse_status_payload(payload: dict) -> list:
    """Extracts status updates from a webhook payload."""
    statuses = []
    # Unwrap if 'metaData' key exists
    data = payload.get("metaData", payload)
    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            for status in value.get("statuses", []):
                statuses.append({
                    "meta_msg_id": status.get("id"),
                    "status": status.get("status")
                })
    return statuses
    
def format_timestamp(ts: str) -> str:
    """Converts UNIX timestamp (as string) to ISO format."""
    try:
        return datetime.utcfromtimestamp(int(ts)).isoformat()
    except:
        return ts  # fallback if already formatted

