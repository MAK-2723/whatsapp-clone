from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, HTTPException
from app.middleware import http_exception_handler, validation_exception_handler
from app import database, crud, websocket
from dotenv import load_dotenv
import os
import logging
import uvicorn

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger("backend")

FRONTEND_URL=os.getenv("FRONTEND_URL") #set on Render
origins=[FRONTEND_URL,"http://localhost:8000"]
    
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

@app.post("/webhook/")
async def receive_payload(request: Request):
    payload=await request.json()
    logger.info("Recieved /webhook payload: %s", str(payload)[:500])
    try: 
        await crud.process_payload(payload)
        await websocket.manager.broadcast("new_data")
        return {"status": "processed"}
    except Exception as e:
        logger.exception("Error processing webhook: %s",e)
        return {"status": "error", "detail": str(e)}        

@app.get("/messages/{wa_id}")
async def get_messages(wa_id: str):
    logger.inso("Get /messages %s",wa_id)
    return await crud.get_messages_by_user(wa_id)

@app.get("/conversations")
async def get_conversations():
    logger.info("Get /conversations")
    return await crud.get_all_conversations()

@app.post("/send")
async def send_message(request: Request):
    data= await request.json()
    logger.info("Recieved /send data: %s", data)
    try:
        await crud.insert_message(data)
        await websocket.manager.broadcast("new_data")
        return {"status":"saved"}
    except Exception as e:
        logger.exception("Error saving message: %s", e)
        return {"status": "error", "detail": str(e)}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await websocket.manager.connect(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        websocket.manager.disconnect(ws)

if __name__=="__main__":
    uvicorn.run("app.main:app",host="0.0.0.0",port=8000)
