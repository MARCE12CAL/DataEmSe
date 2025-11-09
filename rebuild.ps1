# Script para reconstruir contenedores
Write-Host "Reconstruyendo contenedores..." -ForegroundColor Yellow
docker-compose down
docker-compose build --no-cache
docker-compose up -d
Write-Host "
Contenedores reconstruidos y reiniciados" -ForegroundColor Green
docker-compose ps
