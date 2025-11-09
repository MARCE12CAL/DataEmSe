# Script para detener el proyecto
Write-Host "Deteniendo Excel Data Mapper..." -ForegroundColor Yellow
docker-compose down
Write-Host "Servicios detenidos correctamente" -ForegroundColor Green
