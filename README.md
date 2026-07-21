# 🌾 আমাদের কৃষি AI (AmaderKrishi AI)

বাংলাদেশের কৃষকদের জন্য একটি বাংলা ভাষার AI সহায়ক — টেক্সট, ছবি ও ভয়েসের মাধ্যমে কৃষি সংক্রান্ত প্রশ্নের উত্তর দেয়, ফসলের রোগ শনাক্ত করে, এবং চ্যাট ইতিহাস সংরক্ষণ করে। **FastAPI** ব্যাকএন্ড, **Google Gemini** AI, এবং vanilla HTML/CSS/JS ফ্রন্টএন্ড দিয়ে তৈরি।

## ফিচার তালিকা

| ফিচার | বিবরণ |
|---|---|
| 💬 টেক্সট চ্যাট | বাংলায় কৃষি প্রশ্ন করুন |
| 📷 ছবি আপলোড | ফসলের ছবি দিয়ে রোগ শনাক্ত করুন |
| 🎤 ভয়েস চ্যাট | বাংলায় কথা বলুন (Chrome ব্রাউজার প্রয়োজন) |
| 📚 ইতিহাস | ChatGPT-এর মতো কথোপকথন সংরক্ষণ |
| 👤 মাল্টি-ইউজার | আলাদা লগইন ও ডেটা |

## প্রজেক্ট স্ট্রাকচার

```
.
├── main.py           # FastAPI অ্যাপ — সব রুট
├── database.py       # MySQL ডেটাবেস ও কুয়েরি
├── requirements.txt  # Python প্যাকেজ
├── .env.example      # পরিবেশ ভেরিয়েবলের টেমপ্লেট
└── frontend/
    └── index.html    # সম্পূর্ণ UI
```

## সেটআপ গাইড

### ধাপ ১ — রিপোজিটরি ক্লোন ও প্যাকেজ ইনস্টল

```bash
git clone https://github.com/<your-username>/AmaderKrishi_AI.git
cd AmaderKrishi_AI
pip install -r requirements.txt
```

### ধাপ ২ — Gemini API Key নিন (বিনামূল্যে)

1. [aistudio.google.com](https://aistudio.google.com) এ যান
2. Google অ্যাকাউন্ট দিয়ে লগইন করুন
3. "Get API Key" ক্লিক করুন
4. API Key কপি করুন

### ধাপ ৩ — MySQL সেটআপ

```sql
CREATE DATABASE amaderkrishi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### ধাপ ৪ — এনভায়রনমেন্ট ভেরিয়েবল সেট করুন

```bash
cp .env.example .env
```

তারপর `.env` ফাইলে আপনার তথ্য দিন:
```
GEMINI_API_KEY=আপনার_gemini_api_key
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=আপনার_mysql_পাসওয়ার্ড
DB_NAME=amaderkrishi
```

> ⚠️ `.env` ফাইলটি কখনোই GitHub-এ কমিট করবেন না — এটি ইতিমধ্যে `.gitignore`-এ যুক্ত আছে।

### ধাপ ৫ — Backend চালু করুন

```bash
uvicorn main:app --reload
```

✅ সফল হলে দেখাবে: `আমাদের কৃষি AI চালু হয়েছে!`

### ধাপ ৬ — Frontend খুলুন

`frontend/index.html` ফাইলটি যেকোনো ব্রাউজারে খুলুন, অথবা VS Code Live Server দিয়ে চালু করুন।

**গুরুত্বপূর্ণ**: ভয়েস ইনপুটের জন্য Chrome ব্যবহার করুন।

## API Endpoints

| Method | URL | কাজ |
|---|---|---|
| POST | `/api/register` | নিবন্ধন |
| POST | `/api/login` | লগইন |
| POST | `/api/sessions` | নতুন সেশন |
| GET | `/api/sessions/{user_id}` | সেশন তালিকা |
| GET | `/api/history/{session_id}` | চ্যাট ইতিহাস |
| POST | `/api/chat` | টেক্সট চ্যাট |
| POST | `/api/chat-image` | ছবি বিশ্লেষণ |
| DELETE | `/api/sessions/{id}` | সেশন মুছুন |

## সমস্যা সমাধান

**CORS Error**: Backend চালু আছে কিনা চেক করুন (`http://localhost:8000`)

**DB Error**: MySQL চালু আছে কিনা এবং `.env`-এ পাসওয়ার্ড ঠিক আছে কিনা দেখুন

**ভয়েস কাজ করছে না**: Chrome ব্রাউজার ব্যবহার করুন এবং মাইক্রোফোন পারমিশন দিন

**API Key Error**: `.env` ফাইলে সঠিক Gemini API Key দিন

## টেক স্ট্যাক

- **Backend:** FastAPI, google-generativeai (Gemini), MySQL Connector
- **Frontend:** Vanilla HTML/CSS/JS, Web Speech API (ভয়েস ইনপুট)
- **Database:** MySQL

## লাইসেন্স

এই প্রজেক্টটি শিক্ষামূলক ব্যবহারের জন্য উন্মুক্ত।
