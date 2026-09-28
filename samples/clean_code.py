"""
Clean, optimized, and secure reference implementation following PEP8 standards.
"""
import sqlite3
import os

# Secrets loaded securely from environment variables
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")

def get_user_records(db_path: str, username: str) -> list:
    """
    Safely retrieves user records using parameterized queries to prevent SQL injection.
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        query = "SELECT id, username, email FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        return cursor.fetchall()

def find_common_elements(list1: list, list2: list) -> list:
    """
    Computes common elements with O(N + M) complexity using set intersection.
    """
    return list(set(list1).intersection(set(list2)))

def log_activity(message: str) -> None:
    """
    Appends an activity log safely using a context manager.
    """
    with open("activity.log", "a", encoding="utf-8") as f:
        f.write(message + "\n")
