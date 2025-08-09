from pydantic import BaseModel
from typing import Optional

class Message(BaseModel):
    wa_id: str
    name: str
    text: str
    timestamp: str
    status: str="sent"
    meta_msg_id: Optional[str]