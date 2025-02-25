from fastapi import FastAPI, Request
from datetime import datetime, timedelta
import asyncio

app = FastAPI()
messages = []  # ذخیره پیام‌ها

@app.get("/")
async def index(request: Request):
    """ok p 5 m akhir"""
    now = datetime.utcnow()
    recent_messages = [msg["text"] for msg in messages if now - msg["time"] <= timedelta(minutes=5)]
    
    # نمایش پیام‌های اخیر در ترمینال
    print("\n📩 پیام‌های ۵ دقیقه اخیر:")
    for msg in recent_messages:
        print(f" - {msg}")

    return ""  # صفحه سفید

@app.post("/send_message/")
async def send_message(msg: str):
    """ثبت پیام در سرور"""
    messages.append({"text": msg, "time": datetime.utcnow()})
    return {"status": "message received"}