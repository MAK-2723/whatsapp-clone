from datetime import datetime

def parse_message_payload(payload: dict) -> list:
    """Extracts messages from a WhatsApp webhook payload."""
    messages = []
    if "messages" in payload:
        for msg in payload["messages"]:
            contact = payload.get("contacts", [{}])[0]
            messages.append({
                "wa_id": msg.get("from"),
                "name": contact.get("profile", {}).get("name", "Unknown"),
                "text": msg.get("text", {}).get("body", ""),
                "timestamp": format_timestamp(msg.get("timestamp")),
                "status": "sent",
                "meta_msg_id": msg.get("id")
            })
    return messages

def parse_status_payload(payload: dict) -> list:
    """Extracts status updates from a webhook payload."""
    statuses = []
    if "statuses" in payload:
        for status in payload["statuses"]:
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
