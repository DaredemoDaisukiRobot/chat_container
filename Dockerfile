# 使用官方 Python 3.9 作為基礎映像
FROM python:3.9-slim

# 設置工作目錄
WORKDIR /app

# 複製當前目錄的所有文件到容器的 /app 目錄
COPY . /app

# 安裝應用所需的依賴包
RUN pip install --no-cache-dir -r requirements.txt

# 開放 Flask 默認運行的端口 5000
EXPOSE 5000

# 設置環境變量，告訴 Flask 運行在 Docker 容器中
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 運行 Flask 應用
CMD ["flask", "run"]