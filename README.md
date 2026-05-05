# Chatbot Docker

API REST de chatbot desarrollada en Flask, contenerizada con Docker y orquestada con Docker Compose.

## Descripción

Este proyecto es una aplicación web de chatbot desarrollada en Python con Flask. Permite interactuar con un bot básico a través de una interfaz web o mediante peticiones a su API REST. El chatbot responde a preguntas simples y almacena el historial completo de conversaciones en un archivo JSON, garantizando la persistencia de datos incluso cuando los contenedores se reinician.

**Características:**
- Interfaz web responsive
- API REST con endpoints `/api/chat` y `/api/history`
- Persistencia de datos en volumen Docker
- Hot-reload para desarrollo

**Funcionalidades**

Recibe mensajes del usuario vía navegador o API.
Procesa el mensaje y devuelve una respuesta predefinida según palabras clave (hola, hora, docker, git, adiós, etc.).
Guarda cada interacción (timestamp, mensaje del usuario, respuesta del bot) en un archivo JSON.
Expone el historial completo a través del endpoint /api/history.

 **Funcionamiento**

1. El usuario accede a la aplicación web en el navegador o envía una petición POST a /api/chat.
2. Flask recibe el mensaje, lo procesa con la lógica del chatbot y genera una respuesta.
3. La conversación se registra en data/conversaciones.json.
4. Docker Compose levanta el servicio, mapea el puerto 5000 y monta un volumen para persistir los datos fuera del contenedor.

## Instlacion y Despliegue

### Prerrequisitos

- Docker
- Docker Compose instalados
- Git

### Paso a paso

1. Clonar repositorio
1. Contruir la imagen con Docker
1. Levantar los servicios con Docker Compose
1. Acceder a la app
1. Ver los logs (si necesario)

## Explicacion de los archivos Docker

### Dockerfile

FROM python:3.11-slim       				# Imagen base ligera de Python 3.11
WORKDIR /app                				# Directorio de trabajo dentro del contenedor
COPY requirements.txt .     				# Copiamos dependencias primero (optimiza caché)
RUN pip install --no-cache-dir -r requirements.txt  	# Instalamos Flask
COPY app.py .               				# Copiamos el código fuente
RUN mkdir -p /app/data      				# Creamos carpeta para datos persistentes
EXPOSE 5000                 				# Declaramos que el contenedor escucha en el puerto 5000
ENV FLASK_APP=app.py        				# Variable de entorno para Flask
ENV PYTHONUNBUFFERED=1      				# Evita buffering en logs para verlos en tiempo real
CMD ["python", "app.py"]    				# Comando que se ejecuta al iniciar el contenedor

**Decisiones clave**

1. python:3.11-slim: Imagen reducida (~45 MB vs ~900 MB de la imagen completa), ideal para producción y transferencias rápidas.
2. --no-cache-dir: Evita almacenar caché de pip, reduciendo el tamaño final de la imagen.
3. Copiar requirements.txt antes que app.py: Si solo cambia el código, Docker reutiliza la capa de instalación de dependencias, acelerando builds posteriores.

### docker-compose.yml

version: '3.8'

services:
  chatbot:
    build: .                          # Construye la imagen desde el Dockerfile local
    container_name: chatbot-app       # Nombre fácil de recordar para el contenedor
    ports:
      - "5000:5000"                   # Mapea puerto 5000 del host → 5000 del contenedor
    volumes:
      - ./data:/app/data              # Volumen bind: carpeta local data/ → /app/data en contenedor
      - .:/app                         # Volumen para hot-reload en desarrollo
    environment:
      - FLASK_ENV=development
      - FLASK_DEBUG=1
    restart: unless-stopped           # Reinicia automáticamente si falla, excepto si se detiene manualmente
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/"]
      interval: 30s
      timeout: 10s
      retries: 3

**Puntos Clave**

1. ports: "5000:5000": Expone la aplicación para que sea accesible desde fuera del contenedor (navegador, curl, etc.).
2. volumes: ./data:/app/data: Garantiza que conversaciones.json se guarde en el disco del host. Si el contenedor se destruye, los datos permanecen.
3. volumes: .:/app: Permite el hot-reload: cualquier cambio en el código local se refleja inmediatamente en el contenedor sin reconstruir la imagen.
4. healthcheck: Docker verifica cada 30 segundos que la app responda correctamente. Si falla 3 veces seguidas, marca el contenedor como unhealthy.



### Posibles problemas y soluciones

**Puerto 5000 ya está en uso**

Síntoma: Al ejecutar docker compose up, aparece un error como bind: address already in use o port is already allocated.
Causa: Otra aplicación está usando el puerto 5000. En macOS, por ejemplo, el servicio AirPlay lo utiliza por defecto. También puede ocurrir si tienes otra instancia de Flask o Docker corriendo.
Solución: Edita el archivo docker-compose.yml y cambia el mapeo de puertos. Por ejemplo, usa el puerto 8080 del host en lugar del 5000
Luego accede a la aplicación en http://localhost:8080 en vez de http://localhost:5000.

**Error de permisos con Docker**

Síntoma: Aparece el mensaje permission denied while trying to connect to the Docker daemon socket al ejecutar cualquier comando de Docker.
Causa: Tu usuario de sistema no pertenece al grupo docker, por lo que no tiene permisos para interactuar con el daemon de Docker.
Solución: Añade tu usuario al grupo docker y despues ierra la sesión actual y vuelve a iniciarla (o reinicia el equipo).

**Los datos no se guardan tras reiniciar el contenedor**

Síntoma: Envías mensajes al chatbot, pero al detener y volver a levantar los contenedores con docker compose down && docker compose up -d, el historial de conversaciones aparece vacío.
Causa: La carpeta data/ no existe en el directorio del proyecto o no tiene permisos de escritura, por lo que el volumen de Docker no puede sincronizar los datos entre el contenedor y el host.
Solución: Crea la carpeta manualmente y asegúrate de que tenga permisos de escritura

**El build usa caché obsoleta**

Síntoma: Has modificado el archivo requirements.txt para añadir una nueva librería, pero al ejecutar docker compose up --build, la nueva dependencia no se instala o el contenedor sigue comportándose como antes.
Causa: Docker almacena en caché las capas de la imagen para acelerar las construcciones posteriores. Si detecta que no ha cambiado nada en las primeras capas, reutiliza la caché en lugar de reconstruir.
Solución: Fuerza una reconstrucción completa sin usar la caché

**No puedo acceder desde otra máquina en la red**

Síntoma: La aplicación funciona perfectamente en localhost de tu propio equipo, pero otro ordenador de la misma red no puede acceder a http://tu-ip:5000.
Causa: Por defecto, Flask escucha solo en la interfaz de red local (127.0.0.1), lo que impide conexiones externas. También puede deberse a que el firewall del sistema bloquea el puerto 5000.
Solución: Asegúrate de que en app.py la aplicación se inicie con el host 0.0.0.0. Además, abre el puerto 5000 en el firewall de tu sistema operativo

### Contribuciones y organizacion del proyecto

Este repositorio sigue un flujo de trabajo basado en **Git Flow simplificado**, utilizando ramas para separar el desarrollo activo del código estable.

**Estructura de ramas**

1. **main** Código estable y listo para el entorno productivo
2. **develop** Rama de integracion donde se fusionan nuevas funcionalidades antes de pasar a main (entorno productivo)
3. **feature/** Ramas temporales para cada nueva funcionalidad o correcion


