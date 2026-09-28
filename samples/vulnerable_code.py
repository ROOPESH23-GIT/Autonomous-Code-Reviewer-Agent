# Sample script with intentional security vulnerabilities, performance bugs, and bad practices
import sqlite3
import os

# Security Issue: Hardcoded API secret
JWT_SECRET_KEY = "super_secret_jwt_token_12345_do_not_share"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"

def get_user_records(db_path, user_input_username):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Security Issue: Critical SQL Injection vulnerability
    query = "SELECT id, username, email FROM users WHERE username = '" + user_input_username + "'"
    cursor.execute(query)
    results = cursor.fetchall()

    # Security Issue: Insecure execution
    eval("print('Fetched records count: ' + str(len(results)))")

    return results

def find_common_elements(list1, list2):
    # Performance Issue: Quadratic O(N^2) complexity with nested loops
    common = []
    for i in list1:
        for j in list2:
            if i == j:
                if i not in common:
                    common.append(i)
    return common

def log_activity(message):
    # Resource Leak Issue: File opened without 'with' statement
    f = open("activity.log", "a")
    f.write(message + "\n")
    # Missing f.close()
