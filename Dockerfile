# 使用官方的 Python 3.10 基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 将当前目录内容复制到工作目录中
COPY . /app

# 安装系统依赖项
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 安装 ta-lib
RUN pip install TA-Lib==0.5.1

# 安装其他 Python 依赖项
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# 暴露应用运行的端口（如果有需要的话）
# EXPOSE 8080

# 设置环境变量
ENV PYTHONPATH=/app

# 运行主程序
CMD ["python", "main.py"]