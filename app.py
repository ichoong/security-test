import os
import subprocess
import sqlite3
import requests

#--- test#
# --- GITLEAKS TEST ---
DB_PASSWORD = "hardcoded_password_123"   # ❌ Gitleaks가 탐지할 비밀정보

# --- DEPENDENCY SCAN TEST ---
# requests==2.19.1 는 알려진 취약점(CVE-2018-18074)이 있음
def download_data():
    url = "http://example.com/data"
    response = requests.get(url)
    return response.text

# --- SQL INJECTION TEST ---
def get_user(username):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    # ❌ SQL injection
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)

    return cursor.fetchall()

# --- COMMAND INJECTION TEST ---
def run_system_cmd(cmd):
    # ❌ 잠재적 OS Command Injection
    return subprocess.check_output(f"echo {cmd}", shell=True)

if __name__ == "__main__":
    print(download_data())
    print(get_user("admin' OR '1'='1"))
    print(run_system_cmd("test"))

