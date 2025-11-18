from .core.qkd_engine import run_bb84
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import router

app = FastAPI(
    title="QuantX Secure Communication Backend",
    version="0.1.0"
)
# Allow frontend (web) to access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/simulate")
def simulate():
    try:
        # Use 'n' instead of 'total_bits'
        result = run_bb84(n=50)
        return JSONResponse(content=result)
    except Exception as e:
        return {"error": str(e)}


# Attach API routes
app.include_router(router)


@app.get("/")
def root():
    return {"message": "QuantX Backend is Running"}


# ----------------------------------------------------
# Live Chat WebSocket (for MVP messaging demonstration)
# ----------------------------------------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


@app.websocket("/ws/chat")
async def chat_socket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
