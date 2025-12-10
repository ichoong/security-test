import sqlite3
import subprocess
from flask import Flask, request
import pickle
import os

app = Flask(__name__)

# ----------------------------------------------------------
# 1. GITLEAKS가 100% 탐지하는 하드코딩 Secret
# ----------------------------------------------------------

# GitHub Personal Token
GITHUB_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuv"

# JWT Secret key (규칙에 걸림)
JWT_SECRET = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.SECRET123.SECRET456"

tes = "sss"
# Private key 조각
PRIVATE_KEY = """
-----BEGIN PRIVATE KEY-----
MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAMRANDOM12345EXAMPLE
-----END PRIVATE KEY-----
"""


# ----------------------------------------------------------
# 2. CODEQL 탐지: SQL Injection
# ----------------------------------------------------------
@app.route("/user")
def get_user():
    username = request.args.get("username", "")
    query = "SELECT * FROM users WHERE username = '" + username + "';"  # ❌ SQL Injection
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
    return {"result": result}


# ----------------------------------------------------------
# 3. CODEQL 탐지: Command Injection
# ----------------------------------------------------------
@app.route("/run")
def run_cmd():
    cmd = request.args.get("cmd", "ls")
    result = subprocess.check_output("sh -c " + cmd, shell=True)  # ❌ Command Injection
    return {"output": result.decode()}


# ----------------------------------------------------------
# 4. CODEQL 탐지: Insecure Deserialization
# ----------------------------------------------------------
@app.route("/load")
def load_obj():
    data = request.args.get("data", "")  # base64 string이라고 가정
    obj = pickle.loads(bytes(data, "utf-8"))  # ❌ Unsafe Deserialization
    return {"loaded": str(obj)}


# ----------------------------------------------------------
# 5. CODEQL 탐지: Path Traversal
# ----------------------------------------------------------
@app.route("/read")
def read_file():
    filename = request.args.get("file", "test.txt")
    filepath = "/tmp/uploads/" + filename  # ❌ Path Traversal
    with open(filepath, "r") as f:
        return f.read()


if __name__ == "__main__":
    app.run(debug=True)
