# 🌾 আমাদের কৃষি AI — সম্পূর্ণ সেটআপ গাইড

## প্রজেক্ট স্ট্রাকচার
```
amader_krishi/
├── backend/
│   ├── main.py          ← FastAPI অ্যাপ
│   ├── database.py      ← MySQL ডেটাবেস
│   ├── requirements.txt ← Python প্যাকেজ
│   └── .env             ← আপনার API Keys
└── frontend/
    └── index.html       ← সম্পূর্ণ UI
```

---

## ধাপ ১ — Gemini API Key নিন (বিনামূল্যে)

1. https://aistudio.google.com এ যান
2. Google অ্যাকাউন্ট দিয়ে লগইন করুন
3. "Get API Key" ক্লিক করুন
4. API Key কপি করুন

---

## ধাপ ২ — MySQL সেটআপ

```sql
-- MySQL এ লগইন করুন এবং রান করুন:
CREATE DATABASE amader_krishi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## ধাপ ৩ — .env ফাইল আপডেট করুন

`backend/.env` ফাইলে আপনার তথ্য দিন:
```
GEMINI_API_KEY=আপনার_gemini_api_key
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=আপনার_mysql_পাসওয়ার্ড
DB_NAME=amaderkrishi
```

---

## ধাপ ৪ — Python প্যাকেজ ইনস্টল করুন

```bash
cd backend
pip install -r requirements.txt
```

---

## ধাপ ৫ — Backend চালু করুন

```bash
uvicorn main:app --reload
```

✅ সফল হলে দেখাবে: `আমাদের কৃষি AI চালু হয়েছে!`

---

## ধাপ ৬ — Frontend খুলুন

`frontend/index.html` ফাইলটি যেকোনো ব্রাউজারে খুলুন।
অথবা VS Code Live Server দিয়ে চালু করুন।

**গুরুত্বপূর্ণ**: ভয়েস ইনপুটের জন্য Chrome ব্যবহার করুন।

---

## ফিচার তালিকা

| ফিচার | বিবরণ |
|---|---|
| 💬 টেক্সট চ্যাট | বাংলায় কৃষি প্রশ্ন করুন |
| 📷 ছবি আপলোড | ফসলের ছবি দিয়ে রোগ শনাক্ত করুন |
| 🎤 ভয়েস চ্যাট | বাংলায় কথা বলুন (Chrome) |
| 📚 ইতিহাস | ChatGPT-এর মতো কথোপকথন সংরক্ষণ |
| 👤 মাল্টি-ইউজার | আলাদা লগইন ও ডেটা |

---

## API Endpoints

| Method | URL | কাজ |
|---|---|---|
| POST | /api/register | নিবন্ধন |
| POST | /api/login | লগইন |
| POST | /api/sessions | নতুন সেশন |
| GET | /api/sessions/{user_id} | সেশন তালিকা |
| GET | /api/history/{session_id} | চ্যাট ইতিহাস |
| POST | /api/chat | টেক্সট চ্যাট |
| POST | /api/chat-image | ছবি বিশ্লেষণ |
| DELETE | /api/sessions/{id} | সেশন মুছুন |

---

## সমস্যা সমাধান

**CORS Error**: Backend চালু আছে কিনা চেক করুন (`http://localhost:8000`)

**DB Error**: MySQL চালু আছে কিনা এবং `.env`-এ পাসওয়ার্ড ঠিক আছে কিনা দেখুন

**ভয়েস কাজ করছে না**: Chrome ব্রাউজার ব্যবহার করুন এবং মাইক্রোফোন পারমিশন দিন

**API Key Error**: `.env` ফাইলে সঠিক Gemini API Key দিন
