# CollabW 开发环境快速启动脚本 (Windows PowerShell)

Write-Host "🚀 启动 CollabW 开发环境..." -ForegroundColor Green

# 检查Docker是否运行
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker 未运行，请先启动 Docker" -ForegroundColor Red
    exit 1
}

# 创建日志目录
if (!(Test-Path "logs")) { New-Item -ItemType Directory -Path "logs" }
if (!(Test-Path "logs/backend")) { New-Item -ItemType Directory -Path "logs/backend" }
if (!(Test-Path "logs/frontend")) { New-Item -ItemType Directory -Path "logs/frontend" }

# 构建并启动服务
Write-Host "📦 构建并启动服务..." -ForegroundColor Yellow
docker-compose up --build -d

# 等待服务健康检查
Write-Host "⏳ 等待服务启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# 检查服务状态
Write-Host "📊 检查服务状态..." -ForegroundColor Yellow
docker-compose ps

# 显示日志
Write-Host "📋 显示最近日志..." -ForegroundColor Yellow
docker-compose logs --tail=20

Write-Host ""
Write-Host "✅ CollabW 开发环境启动完成!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 服务地址:" -ForegroundColor Cyan
Write-Host "   前端: http://localhost:3000" -ForegroundColor White
Write-Host "   后端: http://localhost:8000" -ForegroundColor White
Write-Host "   API文档: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "📝 常用命令:" -ForegroundColor Cyan
Write-Host "   查看日志: docker-compose logs -f" -ForegroundColor White
Write-Host "   停止服务: docker-compose down" -ForegroundColor White
Write-Host "   重启服务: docker-compose restart" -ForegroundColor White
Write-Host "   清理环境: docker-compose down -v --remove-orphans" -ForegroundColor White
Write-Host ""
