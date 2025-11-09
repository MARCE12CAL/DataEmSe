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
