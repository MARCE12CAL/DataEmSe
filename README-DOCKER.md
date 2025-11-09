#  Guía Docker - Excel Data Mapper

##  Archivos Creados

Todos los archivos Docker han sido creados automáticamente:

\\\
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
\\\

##  Inicio Rápido

### Opción 1: Usar scripts de PowerShell

\\\powershell
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
\\\

### Opción 2: Comandos Docker Compose

\\\powershell
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
\\\

##  Acceso a los Servicios

Después de ejecutar \./start.ps1\ o \docker-compose up -d\:

- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:5000/api
- **Documentación API**: http://localhost:5000/api/docs (si está configurado)

##  Modo Producción

\\\powershell
# Construir para producción
docker-compose -f docker-compose.prod.yml build

# Iniciar en producción
docker-compose -f docker-compose.prod.yml up -d

# Acceder en: http://localhost
\\\

## 🔧 Comandos Útiles

\\\powershell
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
\\\

##  Troubleshooting

### Puerto en uso
\\\powershell
# Ver qué está usando el puerto
netstat -ano | findstr :4200
netstat -ano | findstr :5000

# Cambiar puertos en docker-compose.yml
# Buscar la sección "ports:" y modificar
\\\

### Cambios no se reflejan
\\\powershell
# Reconstruir
./rebuild.ps1

# O manualmente
docker-compose down
docker-compose build --no-cache
docker-compose up -d
\\\

### Ver errores detallados
\\\powershell
# Logs del backend
docker-compose logs -f backend

# Logs del frontend
docker-compose logs -f frontend

# Logs de ambos
docker-compose logs -f
\\\

##  Limpieza

\\\powershell
# Detener y eliminar contenedores
docker-compose down

# Además eliminar volúmenes
docker-compose down -v

# Limpiar sistema completo
docker system prune -a
`\

##  Notas Importantes

1. **Hot Reload**: En modo desarrollo, los cambios se reflejan automáticamente
2. **Volúmenes**: Los datos se persisten en volúmenes Docker
3. **Red**: Los servicios se comunican a través de una red Docker privada
4. **CORS**: Ya está configurado para localhost:4200

##  ¿Necesitas Ayuda?

- Ver logs: \./logs.ps1\
- Estado: \docker-compose ps\
- Reiniciar: \./rebuild.ps1\

¡Listo para usar! 
