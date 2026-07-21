from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai
import base64
import os
from pathlib import Path
from dotenv import load_dotenv
from database import Database, init_db

# Load variables from a local .env file if present (no-op in production
# environments that inject real env vars directly)
load_dotenv()

app = FastAPI(title="আমাদের কৃষি API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Resolve paths relative to this file ─────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

# Mount static files for the frontend
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

# ─── Gemini Setup ─────────────────────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY environment variable is not set. "
        "Copy .env.example to .env and add your key from https://aistudio.google.com/apikey"
    )
genai.configure(api_key=GEMINI_API_KEY)
# FIX: correct model name (gemini-2.5-flash does not exist yet)
text_model   = genai.GenerativeModel("gemini-2.5-flash")
vision_model = genai.GenerativeModel("gemini-2.5-flash")

# ─── Pydantic Models ──────────────────────────────────────────────────────────
class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str

class CreateSessionRequest(BaseModel):
    user_id: str
    title: Optional[str] = "নতুন কথোপকথন"

# ─── System Prompt ────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
তুমি "আমাদের কৃষি AI" — বাংলাদেশের কৃষকদের জন্য একটি বিশেষজ্ঞ কৃষি সহায়তাকারী।

ভূমিকা:
- বাংলাদেশের কৃষকদের ফসল সংক্রান্ত সমস্যায় সাহায্য করা
- স্থানীয় ও বাস্তবিক কৃষি পরামর্শ দেওয়া
- রোগ-বালাই, সার, সেচ, আবহাওয়া বিষয়ে পরামর্শ দেওয়া

নিয়মাবলী:
- সর্বদা সহজ ও সাবলীল বাংলায় উত্তর দাও
- সংক্ষিপ্ত, স্পষ্ট ও কার্যকর পরামর্শ দাও
- রোগ বিষয়ক প্রশ্নে: কারণ + সমাধান + প্রতিরোধ উল্লেখ করো
- বাংলাদেশের স্থানীয় কীটনাশক ও সার-এর নাম ব্যবহার করো
- কৃষকের ভাষায় কথা বলো, জটিল শব্দ এড়াও
- ইমোজি ব্যবহার করো যেন বোঝা সহজ হয় 🌾
"""

def build_prompt(user_message: str) -> str:
    return f"{SYSTEM_PROMPT}\n\nকৃষকের প্রশ্ন:\n{user_message}"

def build_image_prompt(user_message: str) -> str:
    return f"""{SYSTEM_PROMPT}

কৃষক একটি ছবি পাঠিয়েছেন এবং জিজ্ঞেস করেছেন: {user_message if user_message else "এই ফসলের কী সমস্যা হয়েছে?"}

ছবি দেখে বলো:
🔍 **রোগের নাম**: 
🦠 **কারণ**: 
💊 **সমাধান**: 
🛡️ **প্রতিরোধ**: 
"""

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    # FIX: use absolute resolved path
    return FileResponse(str(FRONTEND_DIR / "index.html"))

@app.post("/api/register")
async def register(req: RegisterRequest):
    if not req.first_name.strip() or not req.last_name.strip():
        raise HTTPException(status_code=400, detail="নাম দিন")
    if not req.email.strip() or "@" not in req.email:
        raise HTTPException(status_code=400, detail="সঠিক ইমেইল দিন")
    if len(req.password) < 6:
        raise HTTPException(status_code=400, detail="পাসওয়ার্ড কমপক্ষে ৬ অক্ষর হতে হবে")

    db = Database()
    try:
        user_id = db.create_user(
            req.first_name.strip(),
            req.last_name.strip(),
            req.email.strip(),
            req.phone.strip(),
            req.password
        )
        if not user_id:
            raise HTTPException(status_code=400, detail="এই ইমেইল দিয়ে আগেই অ্যাকাউন্ট আছে")
        full_name = f"{req.first_name.strip()} {req.last_name.strip()}"
        return {"success": True, "user_id": user_id, "username": full_name, "email": req.email.strip()}
    finally:
        db.close()

@app.post("/api/login")
async def login(req: LoginRequest):
    if not req.email.strip() or not req.password:
        raise HTTPException(status_code=400, detail="ইমেইল ও পাসওয়ার্ড দিন")

    db = Database()
    try:
        user = db.verify_user(req.email.strip(), req.password)
        if not user:
            raise HTTPException(status_code=401, detail="ইমেইল বা পাসওয়ার্ড ভুল")
        full_name = f"{user['first_name']} {user['last_name']}"
        return {"success": True, "user_id": user["id"], "username": full_name, "email": user["email"]}
    finally:
        db.close()

@app.post("/api/sessions")
async def create_session(req: CreateSessionRequest):
    db = Database()
    try:
        session_id = db.create_session(req.user_id, req.title)
        return {"session_id": session_id, "title": req.title}
    finally:
        db.close()

@app.get("/api/sessions/{user_id}")
async def get_sessions(user_id: str):
    db = Database()
    try:
        sessions = db.get_user_sessions(user_id)
        return {"sessions": sessions}
    finally:
        db.close()

@app.get("/api/history/{session_id}")
async def get_history(session_id: str):
    db = Database()
    try:
        history = db.get_session_history(session_id)
        return {"history": history}
    finally:
        db.close()

@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    db = Database()
    try:
        db.delete_session(session_id)
        return {"success": True}
    finally:
        db.close()

@app.post("/api/chat")
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="বার্তা খালি রাখা যাবে না")
    db = Database()
    try:
        prompt = build_prompt(req.message)
        response = text_model.generate_content(prompt)
        answer = response.text
        db.save_message(req.session_id, req.user_id, req.message, answer, "text")
        db.update_session_title(req.session_id, req.message[:50])
        return {"reply": answer, "session_id": req.session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI সমস্যা: {str(e)}")
    finally:
        db.close()

@app.post("/api/chat-image")
async def chat_image(
    user_id: str = Form(...),
    session_id: str = Form(...),
    message: str = Form(""),
    image: UploadFile = File(...)
):
    db = Database()
    try:
        image_bytes = await image.read()
        b64_image = base64.b64encode(image_bytes).decode()
        mime = image.content_type or "image/jpeg"
        prompt = build_image_prompt(message)
        # FIX: pass image parts correctly to Gemini
        response = vision_model.generate_content([
            {"mime_type": mime, "data": b64_image},
            prompt
        ])
        answer = response.text
        user_msg = message if message else "📷 ছবি পাঠালাম, রোগ শনাক্ত করুন"
        db.save_message(session_id, user_id, user_msg, answer, "image", b64_image, mime)
        db.update_session_title(session_id, "🖼️ " + (message[:40] if message else "ছবি বিশ্লেষণ"))
        return {"reply": answer, "session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ছবি বিশ্লেষণে সমস্যা: {str(e)}")
    finally:
        db.close()

@app.on_event("startup")
async def startup():
    try:
        init_db()
        print("✅ আমাদের কৃষি AI চালু হয়েছে!")
    except Exception as e:
        print(f"⚠️ ডেটাবেস সংযোগ সমস্যা: {e}")
        print("ℹ️ দয়া করে MySQL চালু আছে কিনা এবং DB_PASSWORD সঠিক কিনা যাচাই করুন।")
