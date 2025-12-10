import os
import subprocess
import sqlite3
import requests

# [Gitleaks Test]
# 실제 AWS 키 형식(AKIA...)을 흉내 낸 가짜 키입니다.
# Gitleaks는 이 패턴을 보고 "AWS Secret Key가 코드에 있다"고 경고합니다.
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE" 
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

def vulnerable_logic(user_input):
    # [CodeQL Test 1: SQL Injection]
    # 사용자 입력을 검증 없이 f-string으로 쿼리에 넣는 전형적인 취약점
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{user_input}'" 
    cursor.execute(query) 
    a = 100
    b = 200

    # [CodeQL Test 2: Command Injection]
    # 사용자 입력을 쉘 명령어에 그대로 전달 (shell=True)
    subprocess.call(f"echo {user_input}", shell=True)

if __name__ == "__main__":
    vulnerable_logic("admin' OR '1'='1")
