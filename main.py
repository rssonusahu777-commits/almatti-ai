from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all (for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Request model
class ChatRequest(BaseModel):
    message: str

# Health route
@app.get("/")
def home():
    return {
        "status": "ok",
        "service": "Almatti AI Workforce"
    }

# Chat API
@app.post("/api/chats")
def chat(req: ChatRequest):
    return {
        "reply": f"You said: {req.message}"
    }
