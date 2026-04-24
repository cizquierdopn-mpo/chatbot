# Chatbot Docker

API REST de chatbot desarrollada en Flask, contenerizada con Docker y orquestada con Docker Compose.

## Descripción

Aplicacion web que permite interactuar con un chatbot muy basico vía navegador. Almacena el historial de conversaciones en JSON.

**Características:**
- Interfaz web responsive
- API REST con endpoints `/api/chat` y `/api/history`
- Persistencia de datos en volumen Docker
- Hot-reload para desarrollo

## Instlacion y Despliegue

### Prerrequisitos
- Docker y Docker Compose instalados
- Git

### Paso a paso

1. **Clonar repositorio**
```bash
git clone https://github.com/cizquierdopn-mpo/chatbot.git
cd chatbot
