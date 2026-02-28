# AI WhatsApp Business Automation System

A production-ready AI-powered WhatsApp automation engine built using:

- WhatsApp Web (whatsapp-web.js)
- FastAPI (Python backend)
- Ollama (Local LLM)
- Google Sheets (Lead CRM)
- Zero monthly API cost

This system automatically responds to WhatsApp inquiries, detects lead intent, and stores qualified leads in Google Sheets — all running locally.

---

## 🚀 Overview

This project is designed to automate WhatsApp-based business communication.

It performs:

- AI-powered responses to customer queries
- Intent detection (fee, admission, demo, etc.)
- Automatic lead capture
- Duplicate lead prevention
- Rate limiting & spam protection
- Status/newsletter filtering
- Google Sheets CRM integration

Built for small businesses such as:

- Coaching centers
- IELTS academies
- Gyms
- Clinics
- Real estate agents

---

## 🏗 Architecture
Customer WhatsApp
↓
whatsapp-web.js (Node.js bot)
↓
FastAPI Backend
↓
Ollama (Local LLM)
↓
Google Sheets (Lead CRM)

No external paid APIs required.

---

## 🔒 Production Safeguards

- Ignores status updates
- Ignores newsletters
- Ignores group chats
- Ignores empty messages
- Rate limiting (anti-spam)
- Safe intent detection (word-boundary matching)
- Google Sheets failure protection
- AI timeout handling
- Backend global error shielding

---

## 📊 Lead Capture Format

Leads are stored in Google Sheets with the following structure:

| Phone | Message | Intent | Status | Timestamp |

- Status defaults to: `New Lead`
- Duplicate leads are prevented

---

## 🧠 AI Behavior Control

The system uses a structured business context file to:

- Prevent hallucinations
- Enforce response length
- Maintain professional tone
- Encourage demo booking
- Redirect unrelated queries

---

## ⚙️ Setup Instructions

### 1️⃣ Backend Setup (Python)
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

Ensure:
- `business_context.txt` exists
- `credentials.json` (Google Service Account) exists
- Google Sheet is shared with service account email

---

### 2️⃣ WhatsApp Bot Setup (Node)
cd whatsapp-bot
npm install
node bot.js

Scan QR when prompted.

---

### 3️⃣ Ollama

Ensure Ollama is running locally:
ollama run llama3

Or start the Ollama service before launching backend.

---

## 🛡 Security Notes

- `credentials.json` must never be committed to GitHub
- Repository should remain private
- Use `.gitignore` properly
- Avoid exposing service account keys

---

## 💰 Monetization Model

Recommended pricing model:

- Setup Fee: ₹3,000 – ₹5,000
- Monthly Maintenance: ₹1,000 – ₹2,000

Suitable for local service businesses handling WhatsApp inquiries daily.

---

## 📌 Current Version

v1.0 – Stable Lead Capture System

Core Features:
- AI replies
- Intent detection
- Google Sheets CRM
- Spam filtering
- Stability hardening

---

## 📈 Roadmap

Planned Upgrades:

- Conversation logging sheet
- Admin dashboard
- Multi-business support
- Auto-follow-up system
- Deployment-ready Docker version
- Cloud VPS deployment
- Role-based access
- Analytics dashboard

---

## 👤 Author - Priyatham/Heisenberg

Private repository — internal business automation system.


© 2026 Heisenberg Agency. All rights reserved. Confidential and Proprietary.
---
