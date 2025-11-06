# ⚡ Inicio Rápido - Excel Data Mapper

Esta guía te ayudará a tener el proyecto funcionando en menos de 5 minutos.

## 📋 Pre-requisitos

Asegúrate de tener instalado:

- ✅ Python 3.8 o superior
- ✅ Node.js 18+ y npm
- ✅ pip (gestor de paquetes de Python)

Para verificar:

```bash
python3 --version
node --version
npm --version
```

## 🚀 Pasos de Instalación

### Paso 1: Descomprimir el Proyecto

```bash
tar -xzf excel-data-mapper.tar.gz
cd excel-data-mapper
```

### Paso 2: Configurar el Backend

```bash
cd backend

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor
python run.py
```

✅ **El backend estará corriendo en:** `http://localhost:5000`

No cierres esta terminal. El servidor debe seguir corriendo.

### Paso 3: Configurar el Frontend

Abre una **nueva terminal** y ejecuta:

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm start
```

✅ **El frontend estará corriendo en:** `http://localhost:4200`

El navegador se abrirá automáticamente.

## 🎉 ¡Listo!

Ahora puedes:

1. Abrir tu navegador en `http://localhost:4200`
2. Explorar las diferentes funcionalidades
3. Subir archivos Excel de prueba
4. Crear perfiles de mapeo
5. Generar scripts de procesamiento batch

## 🧪 Primer Uso

### Probar la Auto-Detección

1. Ve a **Auto-Detección** en el menú
2. Sube 2-3 archivos Excel de muestra
3. Haz clic en "Analizar Archivos"
4. Verás los campos detectados automáticamente
5. Opcionalmente, crea un perfil desde el análisis

### Crear un Perfil Manualmente

1. Ve a **Gestión de Perfiles**
2. Haz clic en "Nuevo Perfil"
3. Completa el formulario:
   - Nombre: "Clientes Ecuador"
   - Descripción: "Perfil para datos de clientes"
4. Guarda el perfil

### Generar Script Batch

1. Ve a **Procesamiento Batch**
2. Completa la configuración:
   - Nombre del perfil: (el que creaste)
   - Ruta del CSV: `/path/to/config.csv`
   - Carpeta de salida: `/path/to/output`
3. Haz clic en "Generar Script"
4. Descarga el script Python generado

## 🔧 Solución de Problemas

### Error: "No module named 'flask'"

Asegúrate de que el entorno virtual esté activado:

```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

Luego reinstala:

```bash
pip install -r requirements.txt
```

### Error: "ng: command not found"

Instala Angular CLI globalmente:

```bash
npm install -g @angular/cli
```

### Puerto 5000 o 4200 ya en uso

Cambia el puerto en el backend:

```bash
PORT=5001 python run.py
```

O en el frontend (edita `package.json`):

```json
"start": "ng serve --port 4201"
```

### Error al instalar pandas en Windows

Ver `INSTALACION_WINDOWS.md` para soluciones específicas de Windows.

## 📚 Siguientes Pasos

- Lee el [README.md](README.md) completo
- Explora la documentación de la API en `backend/README.md`
- Revisa los ejemplos de uso
- Personaliza los perfiles según tus necesidades

## 🆘 ¿Necesitas Ayuda?

- Revisa la sección de **Solución de Problemas** arriba
- Consulta los archivos README en backend y frontend
- Verifica que todos los requisitos estén instalados

## ⏱️ Resumen de Tiempo

- ⏰ Descomprimir: 30 segundos
- ⏰ Backend setup: 2-3 minutos
- ⏰ Frontend setup: 2-3 minutos
- ⏰ **Total: ~5 minutos**

¡Disfruta usando Excel Data Mapper! 🎊
