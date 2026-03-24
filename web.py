from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/capture')
def capture():
    # سحب بيانات السيرفر اللي "هجم" على الموقع
    node_ip = request.remote_addr # آيبي النود حق الاستضافة
    headers = dict(request.headers) # معلومات نظام السيرفر
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # حفظ "صيدة السيرفر" في ملف
    with open("node_logs.txt", "a") as f:
        f.write(f"Time: {time} | IP: {node_ip} | Headers: {headers}\n")
    
    return "Node Captured Successfully"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)