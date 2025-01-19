from flask import Flask, render_template, request, redirect, url_for, session
import csv

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
    with open('module/role/player/user.csv', mode='r') as file:
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
        with open('module/role/player/user.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username:
                    return redirect(url_for('register'))  # 使用者已存在，重新導向到註冊頁面
        
        # 新增使用者到 user.csv
        with open('module/role/player/user.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password])
        
        return redirect(url_for('index'))  # 註冊成功，重新導向到登入頁面
    
    return render_template('register.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('index'))  # 如果沒有登入，重新導向到登入頁面
    initial_message = "hello " + session['username'] + "\n" + "welcome to Die Dungeons"
    return render_template('index.html', initial_message=initial_message)

@app.route('/submit', methods=['POST'])
def submit():
    if 'username' not in session:
        return redirect(url_for('index'))  # 如果沒有登入，重新導向到登入頁面
    user_input = request.form.get('user_input')
    if user_input.lower() == 'logout':
        return redirect(url_for('logout'))  # 處理登出指令
    return user_input

@app.route('/logout')
def logout():
    session.pop('username', None)  # 清除 session
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")