# 使用官方 Python 运行时作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# 复制应用代码到容器
COPY . .

# 声明容器运行时监听的端口 (文档作用)
EXPOSE 5000

# 容器启动时运行的命令
CMD ["python", "app.py"]