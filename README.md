# 🤖 Chatbot Docker

## 🌿 Control de Versiones y Flujo de Trabajo

Este proyecto utiliza Git con un flujo de trabajo basado en ramas para mantener el código organizado y estable.

### Estructura de Ramas

- **`main`**: Contiene el código estable y listo para producción. Solo se actualiza mediante Pull Requests desde `develop`.
- **`develop`**: Rama de integración donde se fusionan las nuevas funcionalidades antes de pasar a `main`.
- **`feature/*`**: Ramas temporales para desarrollar nuevas características (ej: `feature/interfaz-grafica`).

### Cómo contribuir al proyecto

#### 1. Crear una nueva funcionalidad
```bash
# Asegúrate de estar en develop y actualizado
git checkout develop
git pull origin develop

# Crear rama para tu feature
git checkout -b feature/nombre-de-la-feature

# Ejemplo real:
git checkout -b feature/mejora-documentacion
