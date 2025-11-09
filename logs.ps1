# Script para ver logs
param(
    [string]$service = ""
)

if ($service -eq "") {
    Write-Host "Mostrando logs de todos los servicios..." -ForegroundColor Cyan
    docker-compose logs -f
} else {
    Write-Host "Mostrando logs de: $service" -ForegroundColor Cyan
    docker-compose logs -f $service
}
