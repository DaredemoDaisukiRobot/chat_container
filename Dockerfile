FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製應用程式檔案到容器中
COPY . /app

# 安裝必要的套件
RUN pip install --no-cache-dir flask requests

# 暴露 Flask 預設埠
EXPOSE 5000

# 啟動應用程式
CMD ["python", "app.py"]