
import sqlite3
import uuid

from pathlib import Path
from datetime import datetime, timezone


class ConversationMemory:

    def __init__(self):

        # Resolve the database path relative to the project.
        self.db_dir = Path(__file__).resolve().parent.parent / "data"
        self.db_dir.mkdir(parents=True, exist_ok=True)

        self.db_path = self.db_dir / "memory.db"

        self.initialize_database()

        # Each application launch gets a new session.
        self.session_id = str(uuid.uuid4())

        self.create_session()

    def get_connection(self):

        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        return connection

    def initialize_database(self):

        with self.get_connection() as connection:

            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL,

                    FOREIGN KEY(session_id)
                    REFERENCES sessions(id)
                )
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_created
                ON messages(created_at)
            """)

            connection.commit()

    def create_session(self):

        with self.get_connection() as connection:

            connection.execute("""
                INSERT INTO sessions (id, created_at)
                VALUES (?, ?)
            """, (
                self.session_id,
                datetime.now(timezone.utc).isoformat()
            ))

    def add_message(self, role, content):

        with self.get_connection() as connection:

            connection.execute("""
                INSERT INTO messages (
                    session_id,
                    role,
                    content,
                    created_at
                )
                VALUES (?, ?, ?, ?)
            """, (
                self.session_id,
                role,
                content,
                datetime.now(timezone.utc).isoformat()
            ))

    def get_recent_messages(self, limit=12):

        with self.get_connection() as connection:

            cursor = connection.execute("""
                SELECT role, content
                FROM messages
                ORDER BY id DESC
                LIMIT ?
            """, (limit,))

            messages = cursor.fetchall()

        # Reverse so the oldest message comes first.
        return [
            {
                "role": message["role"],
                "content": message["content"]
            }
            for message in reversed(messages)
        ]

    def get_message_count(self):

        with self.get_connection() as connection:

            cursor = connection.execute("""
                SELECT COUNT(*) AS total
                FROM messages
            """)

            return cursor.fetchone()["total"]

    def get_recent_sessions(self, limit=5):

        with self.get_connection() as connection:

            cursor = connection.execute("""
                SELECT
                    s.id,
                    s.created_at,
                    COUNT(m.id) AS message_count
                FROM sessions s
                LEFT JOIN messages m
                    ON s.id = m.session_id
                GROUP BY s.id
                ORDER BY s.created_at DESC
                LIMIT ?
            """, (limit,))

            return [dict(row) for row in cursor.fetchall()]
