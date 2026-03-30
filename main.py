import os
import uuid
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import sqlite3
import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from agents.controller import ControllerAgent
from agents.web_agent import WebAgent
from agents.content_agent import ContentAgent
from agents.communication_agent import CommunicationAgent
from agents.file_manager_agent import FileManagerAgent
from agents.chat_agent import ChatAgent

app = FastAPI(
    title="Almatti AI Workforce API",
    description="Multi-Agent AI System with 5 specialized agents",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure output directories exist
os.makedirs("output/websites", exist_ok=True)
os.makedirs("output/presentations", exist_ok=True)
os.makedirs("output/communications", exist_ok=True)
os.makedirs("output/files", exist_ok=True)


class TaskRequest(BaseModel):
    task: str

class ChatCreate(BaseModel):
    title: str = "New Chat"

class ChatUpdate(BaseModel):
    title: str = None
    messages: list = None

def get_db():
    conn = sqlite3.connect("almatti.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@app.on_event("startup")
def startup():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS chats (
        id TEXT PRIMARY KEY,
        title TEXT,
        messages TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS files (
        id TEXT PRIMARY KEY,
        name TEXT,
        type TEXT,
        url TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Almatti AI Workforce", "agents": 5}

@app.get("/api/chats")
def list_chats():
    conn = get_db()
    rows = conn.execute("SELECT id, title, created_at, updated_at FROM chats ORDER BY updated_at DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/api/chats")
def create_chat(chat: ChatCreate):
    conn = get_db()
    chat_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO chats (id, title, messages) VALUES (?, ?, ?)",
        (chat_id, chat.title, "[]")
    )
    conn.commit()
    new_chat = conn.execute("SELECT * FROM chats WHERE id = ?", (chat_id,)).fetchone()
    conn.close()
    row = dict(new_chat)
    row["messages"] = json.loads(row["messages"])
    return row

@app.get("/api/chats/{chat_id}")
def get_chat(chat_id: str):
    conn = get_db()
    row = conn.execute("SELECT * FROM chats WHERE id = ?", (chat_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Chat not found")
    res = dict(row)
    res["messages"] = json.loads(res["messages"])
    return res

@app.patch("/api/chats/{chat_id}")
def update_chat(chat_id: str, update: ChatUpdate):
    conn = get_db()
    row = conn.execute("SELECT * FROM chats WHERE id = ?", (chat_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Chat not found")
    
    current_title = update.title if update.title is not None else row["title"]
    current_msgs = json.dumps(update.messages) if update.messages is not None else row["messages"]
    
    conn.execute(
        "UPDATE chats SET title = ?, messages = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (current_title, current_msgs, chat_id)
    )
    conn.commit()
    updated_row = conn.execute("SELECT * FROM chats WHERE id = ?", (chat_id,)).fetchone()
    conn.close()
    res = dict(updated_row)
    res["messages"] = json.loads(res["messages"])
    return res

@app.get("/api/files")
def list_files():
    # Sync with local directory
    conn = get_db()
    # Simple mockup to always return the physical files in output directory 
    # Or just returning db contents. We'll return DB and mock ones for now
    import glob
    files_list = []
    for filepath in glob.glob("output/**/*.*", recursive=True):
        files_list.append({
            "id": str(uuid.uuid4())[:8],
            "name": os.path.basename(filepath),
            "type": filepath.split('.')[-1],
            "url": f"/{filepath}",
            "created_at": datetime.utcnow().isoformat()
        })
    return files_list


@app.post("/execute")
def execute_task(request: TaskRequest):
    if not request.task.strip():
        raise HTTPException(status_code=400, detail="Task description cannot be empty.")

    task_id = str(uuid.uuid4())[:8]
    start_time = datetime.utcnow()

    # Step 1: Controller Agent parses and plans
    controller = ControllerAgent()
    plan = controller.parse_task(request.task)

    results = {
        "task_id": task_id,
        "original_task": request.task,
        "timestamp": start_time.isoformat() + "Z",
        "controller_log": plan["log"],
        "agents": {},
    }

    # Step 2: Run agents in parallel based on detected tasks
    agent_map = {
        "chat": (ChatAgent(), plan.get("run_chat", True)),
        "web": (WebAgent(), plan.get("run_web", False)),
        "content": (ContentAgent(), plan.get("run_content", False)),
        "communication": (CommunicationAgent(), plan.get("run_communication", False)),
        "file_manager": (FileManagerAgent(), True),  # always runs
    }

    def run_agent(name, agent, task_text):
        try:
            return name, agent.run(task_text)
        except Exception as e:
            return name, {"status": "error", "error": str(e)}

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(run_agent, name, agent, request.task): name
            for name, (agent, should_run) in agent_map.items()
            if should_run
        }
        for future in as_completed(futures):
            name, result = future.result()
            results["agents"][name] = result

    results["duration_ms"] = int(
        (datetime.utcnow() - start_time).total_seconds() * 1000
    )
    results["status"] = "completed"
    return JSONResponse(content=results)
