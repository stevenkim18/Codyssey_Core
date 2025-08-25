import subprocess
import string
import random

def generate_password(length=6):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# 비밀번호는 숫자+소문자 6자리
password = generate_password()

# 테스트용 txt 파일 생성
with open("hello.txt", "w", encoding="utf-8") as f:
    f.write("안녕하세요! Finder에서 바로 열리는 zip 예제입니다.\n")

# subprocess로 zip 실행 (ZipCrypto 방식)
subprocess.run(["zip", "-e", "-P", password, "hello.zip", "hello.txt"], check=True)

print("hello.zip 생성 완료!")
print("비밀번호:", password)