import requests
import gspread
import re
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from google.oauth2.service_account import Credentials

app = FastAPI()

# -----------------------------
# Load Business Context
# -----------------------------
try:
    with open("business_context.txt", "r", encoding="utf-8") as f:
        context = f.read()
except FileNotFoundError:
    context = "You are a helpful assistant for a business."

# -----------------------------
# Google Sheets Setup
# -----------------------------
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

gc = gspread.authorize(creds)
sheet = gc.open("AI_Leads_Test").sheet1

# -----------------------------
# Request Model
# -----------------------------
class MessageRequest(BaseModel):
    Body: str
    Sender: str = "Unknown"


# -----------------------------
# Ollama AI Function
# -----------------------------
def ask_ollama(user_message: str):
    try:
        prompt = f"{context}\n\nCustomer Question: {user_message}\nAnswer:"

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=20
        )

        response.raise_for_status()
        return response.json()["response"].strip()

    except Exception as e:
        print("🔥 Ollama Error:", e)
        return "Sorry, I'm currently experiencing technical issues. Please contact our team directly."


# -----------------------------
# Intent Detection (SAFE VERSION)
# -----------------------------
def detect_intent(message: str):
    keywords = [
        "fee",
        "admission",
        "enroll",
        "demo",
        "batch",
        "join",
        "interested",
        "timing",
        "location"
    ]

    message = message.lower()

    for keyword in keywords:
        if re.search(rf"\b{keyword}\b", message):
            return keyword

    return None


# -----------------------------
# Lead Exists Check (Safe)
# -----------------------------
def lead_exists(phone: str):
    try:
        records = sheet.get_all_records()
        for row in records:
            if str(row.get("Phone", "")).strip() == phone:
                return True
        return False
    except Exception as e:
        print("Lead check error:", e)
        return False


# -----------------------------
# Save Lead to Google Sheets
# -----------------------------
def save_lead(phone: str, message: str, intent: str):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([phone, message, intent, "New Lead", timestamp])
        print(f"✅ Lead saved: {phone} | Intent: {intent}")
    except Exception as e:
        print("🔥 Google Sheets Error:", e)


# -----------------------------
# WhatsApp Endpoint
# -----------------------------
@app.post("/whatsapp")
async def whatsapp_reply(request: MessageRequest):
    try:
        user_message = request.Body.strip()
        sender = request.Sender

        # 🔒 Backend safety filters
        if (
            sender == "status@broadcast"
            or "@newsletter" in sender
            or user_message == ""
        ):
            return ""

        # 🤖 Get AI reply
        reply = ask_ollama(user_message)

        # 🎯 Detect intent
        intent = detect_intent(user_message)

        # 💾 Save lead if new
        if intent:
            if not lead_exists(sender):
                save_lead(sender, user_message, intent)

        return reply

    except Exception as e:
        print("🔥 Critical Backend Error:", e)
        return "Sorry, something went wrong. Please contact us directly."
