# Script para iniciar el proyecto en modo desarrollo
Write-Host "Iniciando Excel Data Mapper en modo DESARROLLO..." -ForegroundColor Green
docker-compose up -d
Write-Host "
Esperando que los servicios estén listos..." -ForegroundColor Yellow
Start-Sleep -Seconds 10
docker-compose ps
Write-Host "
=== Servicios Disponibles ===" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:4200" -ForegroundColor White
Write-Host "Backend:  http://localhost:5000" -ForegroundColor White
Write-Host "
Para ver logs: docker-compose logs -f" -ForegroundColor Yellow
