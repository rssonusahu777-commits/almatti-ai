from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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
