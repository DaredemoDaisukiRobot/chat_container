from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # 將使用者資訊寫入 user.csv
    with open('module/role/player/user.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])
    
    return redirect(url_for('chat'))

@app.route('/chat')
def chat():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")