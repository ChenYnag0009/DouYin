from flask import Flask, request
import requests
from douyin_scraper import download_from_douyin_wtf
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

def send_message(chat_id, text):
    requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": text})

def send_video(chat_id, video_url):
    requests.post(f"{URL}/sendVideo", json={"chat_id": chat_id, "video": video_url})

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if "douyin.com" in text or "v.douyin.com" in text:
            send_message(chat_id, "🔄 កំពុងតភ្ជាប់ទៅ Douyin.wtf...")

            video_url = download_from_douyin_wtf(text)

            if video_url:
                send_video(chat_id, video_url)
            else:
                send_message(chat_id, "❌ មិនអាចទាញយកវីដេអូបានទេ។ សូមពិនិត្យលីងរបស់អ្នក!")
        else:
            send_message(chat_id, "📥 សូមផ្ញើលីង Douyin មក!")
    return {"ok": True}

@app.route('/')
def home():
    return "Douyin Bot is running!"
