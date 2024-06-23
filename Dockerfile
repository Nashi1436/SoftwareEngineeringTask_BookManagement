# 使用官方 Python 镜像作为基础镜像
FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制项目文件到工作目录
COPY . /app

# 安装项目所需的依赖
RUN pip install -r requirements.txt

# 暴露Django的运行端口
EXPOSE 8000

# 复制启动脚本到容器
COPY entrypoint.sh /app/

# 启动Django应用及执行迁移
CMD ["/app/entrypoint.sh"]
