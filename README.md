# 🌾 AmaderKrishi AI

An AI-powered Bengali-language agricultural assistant designed for farmers in Bangladesh. It answers agriculture-related questions through **text, images, and voice**, detects crop diseases, and stores chat history. The project is built using a **FastAPI** backend, **Google Gemini AI**, and a **Vanilla HTML/CSS/JS** frontend.

## Features

| Feature         | Description                                |
| --------------- | ------------------------------------------ |
| 💬 Text Chat    | Ask agricultural questions in Bengali      |
| 📷 Image Upload | Upload crop images to detect diseases      |
| 🎤 Voice Chat   | Speak in Bengali (Chrome browser required) |
| 📚 Chat History | Store conversations like ChatGPT           |
| 👤 Multi-User   | Separate login and user data               |

## Project Structure

```text
.
├── main.py           # FastAPI application — all routes
├── database.py       # MySQL database and queries
├── requirements.txt  # Python packages
├── .env.example      # Environment variable template
└── frontend/
    └── index.html    # Complete UI
```

## Setup Guide

### Step 1 — Clone the Repository and Install Packages

```bash
git clone https://github.com/<your-username>/AmaderKrishi_AI.git
cd AmaderKrishi_AI
pip install -r requirements.txt
```

### Step 2 — Get a Gemini API Key (Free)

1. Visit [Google AI Studio](https://aistudio.google.com)
2. Sign in with your Google account
3. Click **"Get API Key"**
4. Copy your API key

### Step 3 — Set Up MySQL

```sql
CREATE DATABASE amaderkrishi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Step 4 — Configure Environment Variables

```bash
cp .env.example .env
```

Then add your information to the `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=amaderkrishi
```

> ⚠️ **Never commit the `.env` file to GitHub** — it is already included in `.gitignore`.

### Step 5 — Start the Backend

```bash
uvicorn main:app --reload
```

If successful, you should see:

```text
AmaderKrishi AI is running!
```

### Step 6 — Open the Frontend

Open the `frontend/index.html` file in any browser, or run it using **VS Code Live Server**.

> **Important:** Use Google Chrome for voice input.

## API Endpoints

| Method | URL                         | Description               |
| ------ | --------------------------- | ------------------------- |
| POST   | `/api/register`             | Register a new user       |
| POST   | `/api/login`                | User login                |
| POST   | `/api/sessions`             | Create a new chat session |
| GET    | `/api/sessions/{user_id}`   | Get user's session list   |
| GET    | `/api/history/{session_id}` | Get chat history          |
| POST   | `/api/chat`                 | Text chat                 |
| POST   | `/api/chat-image`           | Analyze an image          |
| DELETE | `/api/sessions/{id}`        | Delete a chat session     |

## Troubleshooting

**CORS Error:** Check whether the backend is running at `http://localhost:8000`.

**Database Error:** Make sure MySQL is running and the password in `.env` is correct.

**Voice Input Not Working:** Use Google Chrome and allow microphone permission.

**API Key Error:** Make sure you have entered the correct Gemini API key in the `.env` file.

## Tech Stack

* **Backend:** FastAPI, Google Generative AI (Gemini), MySQL Connector
* **Frontend:** Vanilla HTML/CSS/JS, Web Speech API (Voice Input)
* **Database:** MySQL

## License

This project is open for educational use.
