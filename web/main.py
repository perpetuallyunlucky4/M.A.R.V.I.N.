from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from runner import generate_chat_completion
from runner import get_history
import uvicorn
from threading import Thread
import asyncio
import json
from fastapi.responses import JSONResponse

test = True

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/history")
async def get_hist():
    try:
        history = get_history()
        return JSONResponse(content=history)
    except FileNotFoundError:
        return JSONResponse(content=[])

@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    while True:
        user_input = await websocket.receive_text()
        async for token in stream_async(user_input):
            await websocket.send_text(token)

async def stream_async(user_input):
    queue = asyncio.Queue()
    loop = asyncio.get_running_loop()  # get main event loop
    
    def worker():
        # In this worker thread, schedule putting tokens into the main loop's queue
        for token in generate_chat_completion(user_input):
            asyncio.run_coroutine_threadsafe(queue.put(token), loop)
        asyncio.run_coroutine_threadsafe(queue.put(None), loop)  # signal end

    Thread(target=worker, daemon=True).start()

    while True:
        token = await queue.get()
        if token is None:
            break
        yield token
        
if __name__ == "__main__":
    print("starting up....")
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

