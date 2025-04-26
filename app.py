from flask import Flask, render_template, request, redirect, url_for, session
import csv
import requests
import socket

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 設置一個隨機的 secret key

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # 檢查使用者資訊是否存在於 user.csv
    with open('user.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username and row[1] == password:
                session['username'] = username  # 設置 session
                return redirect(url_for('chat'))
    
    # 如果登入失敗，重新導向到登入頁面
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 檢查使用者是否已存在
        with open('user.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username:
                    return redirect(url_for('register'))  # 使用者已存在，重新導向到註冊頁面
        
        # 新增使用者到 user.csv
        with open('user.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password])
        
        return redirect(url_for('index'))  # 註冊成功，重新導向到登入頁面
    
    return render_template('register.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('index'))  # 如果沒有登入，重新導向到登入頁面
    initial_message = "hello " + session['username']
    return render_template('index.html', initial_message=initial_message)

@app.route('/submit', methods=['POST'])
def submit():
    if 'username' not in session:
        return redirect(url_for('index'))  # 如果沒有登入，重新導向到登入頁面
    
    user_input = request.form.get('user_input')
    if user_input.lower() == 'logout':
        return redirect(url_for('logout'))  # 處理登出指令

    # 分析指令格式 <IP> <message>
    try:
        target_ip, message = user_input.split(' ', 1)
    except ValueError:
        return "指令格式錯誤，請使用 '<IP> <message>' 格式"

    # 傳送訊息到目標 IP
    sender_ip = socket.gethostbyname(socket.gethostname())  # 取得傳送者 IP
    payload = {"sender_ip": sender_ip, "message": message}
    try:
        response = requests.post(f"http://{target_ip}:5000/receive", json=payload)
        if response.status_code == 200:
            return f"訊息已傳送到 {target_ip}"
        else:
            return f"無法傳送訊息到 {target_ip}，錯誤碼：{response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"傳送失敗，錯誤：{e}"

@app.route('/receive', methods=['POST'])
def receive():
    data = request.get_json()
    sender_ip = data.get("sender_ip", "未知 IP")
    message = data.get("message", "")
    return f"{sender_ip} {message}", 200

@app.route('/logout')
def logout():
    session.pop('username', None)  # 清除 session
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # 明確指定埠為 5000