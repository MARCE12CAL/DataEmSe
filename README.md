# Excel Data Mapper

Sistema completo para mapeo, normalización y procesamiento de archivos Excel utilizando Flask (Backend) y Angular (Frontend).

---

## Características Principales

### 7 Módulos Funcionales

1. Auto-Detección - Detecta campos automáticamente en archivos Excel
2. Gestión de Perfiles - CRUD completo de perfiles de mapeo
3. Procesamiento Batch - Procesamiento masivo de archivos
4. Scanner - Escanea directorios completos
5. Unificador - Combina múltiples archivos Excel
6. Comparador - Compara archivos contra modelos
7. Exportador - Exporta a CSV, JSON, SQL

---

## Inicio Rápido

### Requisitos Previos

- Python 3.8+
- Node.js 18+ y npm
- pip

### 1. Clonar o Descomprimir
```bash
tar -xzf excel-data-mapper.tar.gz
cd excel-data-mapper
```

### 2. Iniciar Backend (Flask)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Backend corriendo en: `http://localhost:5000`

### 3. Iniciar Frontend (Angular)
```bash
# En otra terminal
cd frontend
npm install
npm start
```

Frontend corriendo en: `http://localhost:4200`

---

## Documentación

- QUICKSTART.md - Guía de 5 minutos
- backend/README.md - API y endpoints
- frontend/README.md - Desarrollo frontend

---

## Tecnologías

### Backend:
- Flask 3.0.3
- pandas 2.2.2
- openpyxl 3.1.2
- Flask-CORS 5.0.0

### Frontend:
- Angular 17
- TypeScript 5.2
- RxJS 7.8

---

## Estructura del Proyecto
```
excel-data-mapper/
├── backend/              # API Flask
│   ├── app/
│   │   ├── models/      # Modelos de datos
│   │   ├── routes/      # Endpoints API
│   │   ├── services/    # Lógica de negocio
│   │   └── utils/       # Utilidades
│   ├── config.py
│   ├── run.py
│   └── requirements.txt
│
├── frontend/            # App Angular
│   ├── src/
│   │   └── app/
│   │       ├── core/services/  # Servicios HTTP
│   │       └── features/       # Componentes
│   ├── package.json
│   └── angular.json
│
└── README.md
```

---

## Uso Básico

1. Accede a `http://localhost:4200`
2. Navega a Auto-Detección
3. Sube 2-5 archivos Excel de muestra
4. El sistema detectará campos automáticamente
5. Crea un perfil desde el análisis
6. Usa el perfil para procesamiento batch

---

## API Endpoints

### Perfiles
- GET /api/profiles - Listar perfiles
- POST /api/profiles - Crear perfil
- PUT /api/profiles/:id - Actualizar perfil
- DELETE /api/profiles/:id - Eliminar perfil

### Auto-Detección
- POST /api/autodetect/analyze - Analizar archivos

### Batch
- POST /api/batch/generate-script - Generar script Python

Ver documentación completa en backend/README.md

---

## Ejemplos

### Crear un Perfil
```json
{
  "nombre": "Clientes Ecuador",
  "descripcion": "Perfil para datos de clientes",
  "campos": [
    {
      "nombre": "cedula",
      "palabras_clave": ["cédula", "ci", "identificación"],
      "tipo_dato": "texto",
      "requerido": true
    }
  ]
}
```

---


