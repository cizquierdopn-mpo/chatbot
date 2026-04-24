#  Chatbot Docker

##  Control de Versiones y Flujo de Trabajo

Este proyecto utiliza Git con un flujo de trabajo basado en ramas para mantener el codigo organizado.

### Estructura de Ramas

- **`main`**: Contiene el codigo estable y listo para produccion. Solo se actualiza mediante Pull Requests desde `develop`.
- **`develop`**: Rama de integracion donde se fusionan las nuevas funcionalidades antes de pasar a `main`.
- **`feature/*`**: Ramas temporales para desarrollar nuevas características.

### Como contribuir al proyecto

#### 1. Crear una nueva funcionalidad
```bash
# Asegurate de estar en develop y actualizado
git checkout develop
git pull origin develop

# Crear rama para tu feature
git checkout -b feature/nombre-de-la-feature

# Ejemplo real:
git checkout -b feature/mejora-documentacion

---

## Paso 2: Docker (Dockerfile)

Crea el `Dockerfile`:
```dockerfile
# Imagen base ligera de Python
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias (para Flask)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY src/ ./src/
COPY templates/ ./templates/
COPY data/ ./data/

# Puerto expuesto (documentación, no publicación real)
EXPOSE 5000

# Variable de entorno
ENV FLASK_APP=src/app.py
ENV PYTHONUNBUFFERED=1

# Comando de inicio
CMD ["python", "src/app.py"]

# Chatbot API con Docker

---

API REST de chatbot desarrollada en Flask, contenerizada con Docker y 
orquestada con Docker Compose.

## Descripcion

Aplicacion web que permite interactuar con un chatbot básico via navegador.
Almacena el historial de conversaciones en JSON.

**Características:**
- Interfaz web responsive
- API REST con endpoints /api/chat y /api/history
- Persistencia de datos en volumen Docker
- Hot-reload para desarrollo

## Instalacion y Despliegue

### Prerrequisitos
- Docker y Docker Compose instalados
- Git

### Paso a paso

1. **Clonar repositorio**
```bash
git clone https://github.com/tu-usuario/chatbot-docker.git
cd chatbot-docker
