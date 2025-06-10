#!/bin/bash

# CollabW 开发环境快速启动脚本

echo "🚀 启动 CollabW 开发环境..."

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker 未运行，请先启动 Docker"
    exit 1
fi

# 创建日志目录
mkdir -p logs/backend logs/frontend

# 构建并启动服务
echo "📦 构建并启动服务..."
docker-compose up --build -d

# 等待服务健康检查
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "📊 检查服务状态..."
docker-compose ps

# 显示日志
echo "📋 显示最近日志..."
docker-compose logs --tail=20

echo ""
echo "✅ CollabW 开发环境启动完成!"
echo ""
echo "🌐 服务地址:"
echo "   前端: http://localhost:3000"
echo "   后端: http://localhost:8000"
echo "   API文档: http://localhost:8000/docs"
echo ""
echo "📝 常用命令:"
echo "   查看日志: docker-compose logs -f"
echo "   停止服务: docker-compose down"
echo "   重启服务: docker-compose restart"
echo "   清理环境: docker-compose down -v --remove-orphans"
echo ""
