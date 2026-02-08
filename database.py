import sqlite3

class Database:
    def __init__(self, db_name="conversations.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Create table for storing conversations
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')

        # Create table for storing messages
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            content TEXT,
            sender TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id)
        )''')

        # Create table for storing user preferences
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_preferences (
            user_id TEXT PRIMARY KEY,
            preference_key TEXT,
            preference_value TEXT
        )''')

    def save_conversation(self, user_id, message):
        self.cursor.execute('''INSERT INTO conversations (user_id, message) VALUES (?, ?)''', (user_id, message))
        self.conn.commit()

    def save_message(self, conversation_id, content, sender):
        self.cursor.execute('''INSERT INTO messages (conversation_id, content, sender) VALUES (?, ?, ?)''', (conversation_id, content, sender))
        self.conn.commit()

    def set_user_preference(self, user_id, key, value):
        self.cursor.execute('''REPLACE INTO user_preferences (user_id, preference_key, preference_value) VALUES (?, ?, ?)''', (user_id, key, value))
        self.conn.commit()

    def get_user_preference(self, user_id, key):
        self.cursor.execute('''SELECT preference_value FROM user_preferences WHERE user_id = ? AND preference_key = ?''', (user_id, key))
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()