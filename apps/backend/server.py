import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
import uuid

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents import AgentOrchestrator, TaskContext, AgentResult
from integrations.whatsapp import router as whatsapp_router

# Configuração de Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("server")

app = FastAPI(title="Cleudocode Gemini API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(whatsapp_router)

# Gerenciador de terminais ativos
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)

    def disconnect(self, websocket: WebSocket, session_id: str):
        if session_id in self.active_connections:
            self.active_connections[session_id].remove(websocket)

    async def broadcast(self, session_id: str, message: dict):
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                await connection.send_json(message)

manager = ConnectionManager()
orchestrator = AgentOrchestrator()

class TaskRequest(BaseModel):
    title: str
    description: str
    requirements: List[str] = []

@app.get("/status")
async def get_status():
    return orchestrator.get_all_agents_status()

@app.post("/tasks")
async def create_task(request: TaskRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    context = TaskContext(
        task_id=task_id,
        title=request.title,
        description=request.description,
        requirements=request.requirements
    )
    
    background_tasks.add_task(run_task, context)
    return {"task_id": task_id}

async def run_task(context: TaskContext):
    # Aqui poderíamos injetar um logger customizado para o orchestrator
    # Por enquanto, vamos simular o stream via manager se soubermos o session_id
    # No futuro, o task_id pode ser vinculado a um session_id do terminal
    logger.info(f"Iniciando tarefa {context.task_id}")
    await manager.broadcast(context.task_id, {"type": "system", "content": f"Iniciando: {context.title}"})
    
    result = await orchestrator.execute_task(context)
    
    status = "success" if result.success else "error"
    await manager.broadcast(context.task_id, {"type": status, "content": result.output})
    
    if result.errors:
        for err in result.errors:
            await manager.broadcast(context.task_id, {"type": "error", "content": f"Erro: {err}"})

@app.websocket("/ws/terminal/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    try:
        await websocket.send_json({"type": "system", "content": "Conectado ao terminal do agente."})
        while True:
            data = await websocket.receive_text()
            # Echo ou processar comandos do terminal aqui
            await websocket.send_json({"type": "input", "content": f"{data}"})
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
