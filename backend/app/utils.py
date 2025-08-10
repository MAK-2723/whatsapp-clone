from datetime import datetime

def parse_message_payload(payload: dict) -> list:
    """Extracts messages from a WhatsApp webhook payload."""
    messages = []
    # Unwrap if 'metaData' key exists
    data = payload.get("metaData", payload)
    # WhatsApp payload structure
    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            contacts = value.get("contacts", [{}])
            contact = contacts[0] if contacts else {}
            for msg in value.get("messages", []):
                messages.append({
                    "wa_id": msg.get("from"),
                    "name": contact.get("profile", {}).get("name", "Unknown"),
                    "text": msg.get("text", {}).get("body", ""),
                    "timestamp": format_timestamp(msg.get("timestamp")),
                    # Determine status dynamically
                    "status": "sent" if msg.get("from") == value.get("metadata", {}).get("display_phone_number") else "received",
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
