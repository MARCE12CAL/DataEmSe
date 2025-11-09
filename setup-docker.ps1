# ============================================
# Script de Configuración Docker para Excel Data Mapper
# Ejecutar en PowerShell desde la raíz del proyecto
# ============================================

Write-Host "=== Iniciando configuración Docker ===" -ForegroundColor Green

# Verificar que estamos en el directorio correcto
if (-Not (Test-Path "backend") -or -Not (Test-Path "frontend")) {
    Write-Host "ERROR: Debes ejecutar este script desde la raíz del proyecto excel-data-mapper" -ForegroundColor Red
    Write-Host "Estructura esperada: excel-data-mapper/backend y excel-data-mapper/frontend" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n[1/10] Creando Dockerfile para Backend..." -ForegroundColor Cyan

# Crear backend/Dockerfile
@"
# Backend Dockerfile para Flask
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py \
    FLASK_ENV=development

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorios necesarios para almacenamiento
RUN mkdir -p /app/uploads /app/profiles /app/temp

# Exponer puerto
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "run.py"]
"@ | Out-File -FilePath "backend/Dockerfile" -Encoding UTF8

Write-Host "[OK] backend/Dockerfile creado" -ForegroundColor Green

Write-Host "`n[2/10] Creando .dockerignore para Backend..." -ForegroundColor Cyan

# Crear backend/.dockerignore
@"
# Python
__pycache__/
*.py[cod]
*`$py.class
*.so
.Python
venv/
env/
ENV/
*.egg-info/
dist/
build/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Datos temporales
uploads/
temp/
*.log

# Git
.git/
.gitignore
"@ | Out-File -FilePath "backend/.dockerignore" -Encoding UTF8

Write-Host "[OK] backend/.dockerignore creado" -ForegroundColor Green

Write-Host "`n[3/10] Creando Dockerfile para Frontend (Desarrollo)..." -ForegroundColor Cyan

# Crear frontend/Dockerfile
@"
# Frontend Dockerfile para Angular (Desarrollo)
FROM node:18-alpine

# Establecer directorio de trabajo
WORKDIR /app

# Copiar package files
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar código fuente
COPY . .

# Exponer puerto
EXPOSE 4200

# Comando para desarrollo con hot-reload
CMD ["npm", "start", "--", "--host", "0.0.0.0", "--poll", "2000"]
"@ | Out-File -FilePath "frontend/Dockerfile" -Encoding UTF8

Write-Host "[OK] frontend/Dockerfile creado" -ForegroundColor Green

Write-Host "`n[4/10] Creando Dockerfile para Frontend (Producción)..." -ForegroundColor Cyan

# Crear frontend/Dockerfile.prod
@"
# Frontend Dockerfile para Angular (Producción)
# Etapa 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build -- --configuration production

# Etapa 2: Nginx
FROM nginx:alpine

# Copiar archivos compilados
COPY --from=builder /app/dist/excel-data-mapper /usr/share/nginx/html

# Copiar configuración de nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
"@ | Out-File -FilePath "frontend/Dockerfile.prod" -Encoding UTF8

Write-Host "[OK] frontend/Dockerfile.prod creado" -ForegroundColor Green

Write-Host "`n[5/10] Creando .dockerignore para Frontend..." -ForegroundColor Cyan

# Crear frontend/.dockerignore
@"
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build
dist/
.angular/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
coverage/
*.spec.ts

# Git
.git/
.gitignore

# Environment
.env
.env.local
"@ | Out-File -FilePath "frontend/.dockerignore" -Encoding UTF8

Write-Host "[OK] frontend/.dockerignore creado" -ForegroundColor Green

Write-Host "`n[6/10] Creando nginx.conf para Frontend..." -ForegroundColor Cyan

# Crear frontend/nginx.conf
@"
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Compresión
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Configuración para Angular routing
    location / {
        try_files `$uri `$uri/ /index.html;
    }

    # Proxy para el backend
    location /api/ {
        proxy_pass http://backend:5000/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade `$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host `$host;
        proxy_cache_bypass `$http_upgrade;
        proxy_set_header X-Real-IP `$remote_addr;
        proxy_set_header X-Forwarded-For `$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto `$scheme;
    }

    # Cache para archivos estáticos
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)`$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
"@ | Out-File -FilePath "frontend/nginx.conf" -Encoding UTF8

Write-Host "[OK] frontend/nginx.conf creado" -ForegroundColor Green

Write-Host "`n[7/10] Creando docker-compose.yml (Desarrollo)..." -ForegroundColor Cyan

# Crear docker-compose.yml
@"
version: '3.8'

services:
  # Backend Flask
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: excel-mapper-backend
    ports:
      - "5000:5000"
    volumes:
      - ./backend:/app
      - backend-uploads:/app/uploads
      - backend-profiles:/app/profiles
    environment:
      - FLASK_APP=run.py
      - FLASK_ENV=development
      - PYTHONUNBUFFERED=1
    networks:
      - excel-mapper-network
    restart: unless-stopped

  # Frontend Angular
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: excel-mapper-frontend
    ports:
      - "4200:4200"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    depends_on:
      - backend
    networks:
      - excel-mapper-network
    restart: unless-stopped

volumes:
  backend-uploads:
  backend-profiles:

networks:
  excel-mapper-network:
    driver: bridge
"@ | Out-File -FilePath "docker-compose.yml" -Encoding UTF8

Write-Host "[OK] docker-compose.yml creado" -ForegroundColor Green

Write-Host "`n[8/10] Creando docker-compose.prod.yml (Producción)..." -ForegroundColor Cyan

# Crear docker-compose.prod.yml
@"
version: '3.8'

services:
  # Backend Flask
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: excel-mapper-backend-prod
    ports:
      - "5000:5000"
    volumes:
      - backend-uploads:/app/uploads
      - backend-profiles:/app/profiles
    environment:
      - FLASK_APP=run.py
      - FLASK_ENV=production
      - PYTHONUNBUFFERED=1
    networks:
      - excel-mapper-network
    restart: always

  # Frontend Angular con Nginx
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    container_name: excel-mapper-frontend-prod
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - excel-mapper-network
    restart: always

volumes:
  backend-uploads:
  backend-profiles:

networks:
  excel-mapper-network:
    driver: bridge
"@ | Out-File -FilePath "docker-compose.prod.yml" -Encoding UTF8

Write-Host "[OK] docker-compose.prod.yml creado" -ForegroundColor Green

Write-Host "`n[9/10] Creando .dockerignore en raíz..." -ForegroundColor Cyan

# Crear .dockerignore en raíz
@"
# Git
.git/
.gitignore
.gitattributes

# Documentation
*.md
LICENSE
docs/

# Docker
Dockerfile
docker-compose*.yml
.dockerignore

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
.env.*.local
"@ | Out-File -FilePath ".dockerignore" -Encoding UTF8

Write-Host "[OK] .dockerignore creado" -ForegroundColor Green

Write-Host "`n[10/10] Creando .env.example..." -ForegroundColor Cyan

# Crear .env.example
@"
# Backend Configuration
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1

# Database (si usas una en el futuro)
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# API Configuration
API_HOST=0.0.0.0
API_PORT=5000

# Frontend Configuration
ANGULAR_PORT=4200

# CORS
CORS_ORIGINS=http://localhost:4200,http://localhost:80

# Upload Configuration
MAX_UPLOAD_SIZE=50MB
ALLOWED_EXTENSIONS=xlsx,xls,csv

# Logging
LOG_LEVEL=INFO
"@ | Out-File -FilePath ".env.example" -Encoding UTF8

Write-Host "[OK] .env.example creado" -ForegroundColor Green

Write-Host "`n[BONUS] Creando scripts de ayuda..." -ForegroundColor Cyan

# Crear start.ps1
@"
# Script para iniciar el proyecto en modo desarrollo
Write-Host "Iniciando Excel Data Mapper en modo DESARROLLO..." -ForegroundColor Green
docker-compose up -d
Write-Host "`nEsperando que los servicios estén listos..." -ForegroundColor Yellow
Start-Sleep -Seconds 10
docker-compose ps
Write-Host "`n=== Servicios Disponibles ===" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:4200" -ForegroundColor White
Write-Host "Backend:  http://localhost:5000" -ForegroundColor White
Write-Host "`nPara ver logs: docker-compose logs -f" -ForegroundColor Yellow
"@ | Out-File -FilePath "start.ps1" -Encoding UTF8

# Crear stop.ps1
@"
# Script para detener el proyecto
Write-Host "Deteniendo Excel Data Mapper..." -ForegroundColor Yellow
docker-compose down
Write-Host "Servicios detenidos correctamente" -ForegroundColor Green
"@ | Out-File -FilePath "stop.ps1" -Encoding UTF8

# Crear logs.ps1
@"
# Script para ver logs
param(
    [string]`$service = ""
)

if (`$service -eq "") {
    Write-Host "Mostrando logs de todos los servicios..." -ForegroundColor Cyan
    docker-compose logs -f
} else {
    Write-Host "Mostrando logs de: `$service" -ForegroundColor Cyan
    docker-compose logs -f `$service
}
"@ | Out-File -FilePath "logs.ps1" -Encoding UTF8

# Crear rebuild.ps1
@"
# Script para reconstruir contenedores
Write-Host "Reconstruyendo contenedores..." -ForegroundColor Yellow
docker-compose down
docker-compose build --no-cache
docker-compose up -d
Write-Host "`nContenedores reconstruidos y reiniciados" -ForegroundColor Green
docker-compose ps
"@ | Out-File -FilePath "rebuild.ps1" -Encoding UTF8

Write-Host "[OK] Scripts de ayuda creados" -ForegroundColor Green

# Crear README-DOCKER.md con instrucciones
@"
#  Guía Docker - Excel Data Mapper

##  Archivos Creados

Todos los archivos Docker han sido creados automáticamente:

\`\`\`
excel-data-mapper/
├── docker-compose.yml           # Configuración desarrollo
├── docker-compose.prod.yml      # Configuración producción
├── .dockerignore                # Archivos a ignorar
├── .env.example                 # Variables de entorno ejemplo
├── start.ps1                    # Script inicio rápido
├── stop.ps1                     # Script detener servicios
├── logs.ps1                     # Script ver logs
├── rebuild.ps1                  # Script reconstruir
│
├── backend/
│   ├── Dockerfile               # Imagen Flask
│   └── .dockerignore
│
└── frontend/
    ├── Dockerfile               # Imagen Angular (desarrollo)
    ├── Dockerfile.prod          # Imagen Angular + Nginx (producción)
    ├── nginx.conf               # Configuración Nginx
    └── .dockerignore
\`\`\`

##  Inicio Rápido

### Opción 1: Usar scripts de PowerShell

\`\`\`powershell
# Iniciar todo
./start.ps1

# Ver logs
./logs.ps1

# Ver logs de un servicio específico
./logs.ps1 backend
./logs.ps1 frontend

# Detener todo
./stop.ps1

# Reconstruir desde cero
./rebuild.ps1
\`\`\`

### Opción 2: Comandos Docker Compose

\`\`\`powershell
# Construir imágenes
docker-compose build

# Iniciar servicios
docker-compose up -d

# Ver estado
docker-compose ps

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
\`\`\`

##  Acceso a los Servicios

Después de ejecutar \`./start.ps1\` o \`docker-compose up -d\`:

- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:5000/api
- **Documentación API**: http://localhost:5000/api/docs (si está configurado)

##  Modo Producción

\`\`\`powershell
# Construir para producción
docker-compose -f docker-compose.prod.yml build

# Iniciar en producción
docker-compose -f docker-compose.prod.yml up -d

# Acceder en: http://localhost
\`\`\`

## 🔧 Comandos Útiles

\`\`\`powershell
# Ver contenedores en ejecución
docker-compose ps

# Ejecutar comando en contenedor
docker-compose exec backend bash
docker-compose exec frontend sh

# Reiniciar un servicio
docker-compose restart backend

# Ver uso de recursos
docker stats

# Limpiar todo (¡CUIDADO! Elimina volúmenes)
docker-compose down -v

# Reconstruir sin caché
docker-compose build --no-cache
\`\`\`

##  Troubleshooting

### Puerto en uso
\`\`\`powershell
# Ver qué está usando el puerto
netstat -ano | findstr :4200
netstat -ano | findstr :5000

# Cambiar puertos en docker-compose.yml
# Buscar la sección "ports:" y modificar
\`\`\`

### Cambios no se reflejan
\`\`\`powershell
# Reconstruir
./rebuild.ps1

# O manualmente
docker-compose down
docker-compose build --no-cache
docker-compose up -d
\`\`\`

### Ver errores detallados
\`\`\`powershell
# Logs del backend
docker-compose logs -f backend

# Logs del frontend
docker-compose logs -f frontend

# Logs de ambos
docker-compose logs -f
\`\`\`

##  Limpieza

\`\`\`powershell
# Detener y eliminar contenedores
docker-compose down

# Además eliminar volúmenes
docker-compose down -v

# Limpiar sistema completo
docker system prune -a
```\`

##  Notas Importantes

1. **Hot Reload**: En modo desarrollo, los cambios se reflejan automáticamente
2. **Volúmenes**: Los datos se persisten en volúmenes Docker
3. **Red**: Los servicios se comunican a través de una red Docker privada
4. **CORS**: Ya está configurado para localhost:4200

##  ¿Necesitas Ayuda?

- Ver logs: \`./logs.ps1\`
- Estado: \`docker-compose ps\`
- Reiniciar: \`./rebuild.ps1\`

¡Listo para usar! 
"@ | Out-File -FilePath "README-DOCKER.md" -Encoding UTF8

Write-Host "[OK] README-DOCKER.md creado" -ForegroundColor Green

Write-Host "`n============================================" -ForegroundColor Green
Write-Host " CONFIGURACIÓN DOCKER COMPLETADA" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green

Write-Host "`n Archivos creados:" -ForegroundColor Cyan
Write-Host "  ✓ backend/Dockerfile" -ForegroundColor White
Write-Host "  ✓ backend/.dockerignore" -ForegroundColor White
Write-Host "  ✓ frontend/Dockerfile" -ForegroundColor White
Write-Host "  ✓ frontend/Dockerfile.prod" -ForegroundColor White
Write-Host "  ✓ frontend/.dockerignore" -ForegroundColor White
Write-Host "  ✓ frontend/nginx.conf" -ForegroundColor White
Write-Host "  ✓ docker-compose.yml" -ForegroundColor White
Write-Host "  ✓ docker-compose.prod.yml" -ForegroundColor White
Write-Host "  ✓ .dockerignore" -ForegroundColor White
Write-Host "  ✓ .env.example" -ForegroundColor White
Write-Host "  ✓ start.ps1" -ForegroundColor White
Write-Host "  ✓ stop.ps1" -ForegroundColor White
Write-Host "  ✓ logs.ps1" -ForegroundColor White
Write-Host "  ✓ rebuild.ps1" -ForegroundColor White
Write-Host "  ✓ README-DOCKER.md" -ForegroundColor White

Write-Host "`n Próximos pasos:" -ForegroundColor Yellow
Write-Host "  1. Ejecuta: ./start.ps1" -ForegroundColor White
Write-Host "  2. Espera unos segundos mientras los contenedores inician" -ForegroundColor White
Write-Host "  3. Accede a: http://localhost:4200" -ForegroundColor White
Write-Host "  4. Para ver logs: ./logs.ps1" -ForegroundColor White
Write-Host "  5. Para detener: ./stop.ps1" -ForegroundColor White

Write-Host "`n Lee README-DOCKER.md para más información" -ForegroundColor Cyan

Write-Host "`n¿Deseas iniciar los contenedores ahora? (S/N): " -ForegroundColor Yellow -NoNewline
$respuesta = Read-Host

if ($respuesta -eq "S" -or $respuesta -eq "s") {
    Write-Host "`nIniciando contenedores..." -ForegroundColor Green
    docker-compose up -d
    Start-Sleep -Seconds 5
    Write-Host "`n=== Estado de los contenedores ===" -ForegroundColor Cyan
    docker-compose ps
    Write-Host "`n Servicios iniciados!" -ForegroundColor Green
    Write-Host "Frontend: http://localhost:4200" -ForegroundColor White
    Write-Host "Backend:  http://localhost:5000" -ForegroundColor White
} else {
    Write-Host "`nPuedes iniciar los contenedores más tarde con: ./start.ps1" -ForegroundColor Yellow
}

Write-Host "`n¡Configuración completada! 🎉" -ForegroundColor Green