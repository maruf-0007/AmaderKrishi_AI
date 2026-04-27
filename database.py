import mysql.connector
import os
import uuid
import hashlib
from datetime import datetime

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "amaderkrishi"),
    "charset": "utf8mb4",
    "use_unicode": True,
}

def init_db():
    config_no_db = {k: v for k, v in DB_CONFIG.items() if k != "database"}
    conn = mysql.connector.connect(**config_no_db)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    conn.commit()
    cursor.close()
    conn.close()

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(36) PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            phone VARCHAR(20),
            password_hash VARCHAR(64) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id VARCHAR(36) PRIMARY KEY,
            user_id VARCHAR(36) NOT NULL,
            title VARCHAR(200) DEFAULT 'নতুন কথোপকথন',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id VARCHAR(36) PRIMARY KEY,
            session_id VARCHAR(36) NOT NULL,
            user_id VARCHAR(36) NOT NULL,
            user_message TEXT NOT NULL,
            ai_response LONGTEXT NOT NULL,
            message_type VARCHAR(20) DEFAULT 'text',
            image_data LONGTEXT,
            image_mime VARCHAR(50),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ ডেটাবেস প্রস্তুত!")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(dictionary=True)

    def close(self):
        self.cursor.close()
        self.conn.close()

    def create_user(self, first_name: str, last_name: str, email: str, phone: str, password: str):
        try:
            user_id = str(uuid.uuid4())
            pw_hash = hash_password(password)
            self.cursor.execute(
                "INSERT INTO users (id, first_name, last_name, email, phone, password_hash) VALUES (%s, %s, %s, %s, %s, %s)",
                (user_id, first_name, last_name, email.lower().strip(), phone, pw_hash)
            )
            self.conn.commit()
            return user_id
        except mysql.connector.IntegrityError:
            return None

    def verify_user(self, email: str, password: str):
        pw_hash = hash_password(password)
        self.cursor.execute(
            "SELECT id, first_name, last_name, email FROM users WHERE email=%s AND password_hash=%s",
            (email.lower().strip(), pw_hash)
        )
        return self.cursor.fetchone()

    def create_session(self, user_id: str, title: str = "নতুন কথোপকথন"):
        session_id = str(uuid.uuid4())
        self.cursor.execute(
            "INSERT INTO sessions (id, user_id, title) VALUES (%s, %s, %s)",
            (session_id, user_id, title)
        )
        self.conn.commit()
        return session_id

    def update_session_title(self, session_id: str, title: str):
        self.cursor.execute(
            "UPDATE sessions SET title=%s WHERE id=%s",
            (title[:200], session_id)
        )
        self.conn.commit()

    def get_user_sessions(self, user_id: str):
        self.cursor.execute(
            "SELECT id, title, created_at, updated_at FROM sessions WHERE user_id=%s ORDER BY updated_at DESC",
            (user_id,)
        )
        rows = self.cursor.fetchall()
        for row in rows:
            row["created_at"] = row["created_at"].isoformat() if row["created_at"] else None
            row["updated_at"] = row["updated_at"].isoformat() if row["updated_at"] else None
        return rows

    def get_session_history(self, session_id: str):
        self.cursor.execute(
            "SELECT id, user_message, ai_response, message_type, image_data, image_mime, created_at "
            "FROM messages WHERE session_id=%s ORDER BY created_at ASC",
            (session_id,)
        )
        rows = self.cursor.fetchall()
        for row in rows:
            row["created_at"] = row["created_at"].isoformat() if row["created_at"] else None
        return rows

    def save_message(self, session_id: str, user_id: str, user_msg: str, ai_resp: str,
                     msg_type: str = "text", image_data: str = None, image_mime: str = None):
        msg_id = str(uuid.uuid4())
        self.cursor.execute(
            "INSERT INTO messages (id, session_id, user_id, user_message, ai_response, message_type, image_data, image_mime) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (msg_id, session_id, user_id, user_msg, ai_resp, msg_type, image_data, image_mime)
        )
        self.conn.commit()
        return msg_id

    def delete_session(self, session_id: str):
        self.cursor.execute("DELETE FROM sessions WHERE id=%s", (session_id,))
        self.conn.commit()