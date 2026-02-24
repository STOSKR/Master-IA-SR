# 🎬 Buscador de Películas

Una aplicación web moderna para buscar y explorar películas, construida con JavaScript vanilla y buenas prácticas de desarrollo.

## ✨ Características

- 🔍 **Búsqueda en tiempo real** por título de película
- 🎭 **Filtrado por género** con 21 géneros disponibles
- 📊 **Ordenamiento múltiple**: por puntuación, votos o título
- 🎨 **Diseño moderno y responsive** - funciona en móviles, tablets y desktop
- ⚡ **Carga rápida** - sin base de datos, todo en el cliente
- 🧩 **Arquitectura modular** - componentes separados y reutilizables

## 📁 Estructura del Proyecto

```
web/
├── index.html              # Página principal
├── styles.css              # Estilos globales
├── app.js                  # Orquestador principal
├── components/             # Componentes UI
│   ├── movieCard.js        # Tarjeta de película
│   ├── searchBar.js        # Barra de búsqueda
│   └── filterPanel.js      # Panel de filtros
└── utils/                  # Utilidades
    ├── csvParser.js        # Parser de archivos CSV
    └── dataLoader.js       # Cargador de datos
```

## 🚀 Cómo Usar

### Opción 1: Servidor Python (Recomendado)

```bash
cd web
python -m http.server 8000
```

Abre tu navegador en: `http://localhost:8000`

### Opción 2: Servidor Node.js

```bash
cd web
npx http-server -p 8000
```

Abre tu navegador en: `http://localhost:8000`

### Opción 3: Live Server (VS Code)

1. Instala la extensión "Live Server" en VS Code
2. Click derecho en `index.html`
3. Selecciona "Open with Live Server"

## 🎯 Funcionalidades

### Búsqueda
- Escribe en la barra de búsqueda para filtrar películas por título
- La búsqueda es en tiempo real con debounce de 300ms
- Presiona Enter para buscar inmediatamente

### Filtros
- **Género**: Filtra por género cinematográfico
- **Ordenar por**: 
  - Mejor puntuación (predeterminado)
  - Más votadas
  - Título alfabético

### Visualización
- Tarjetas con póster de película
- Puntuación promedio (⭐)
- Número de votos
- Enlace directo a IMDb

## 🛠️ Tecnologías

- **HTML5** - Estructura semántica
- **CSS3** - Estilos modernos con variables CSS, Grid y Flexbox
- **JavaScript ES6+** - Módulos, clases, async/await
- **Sin frameworks** - JavaScript vanilla puro

## 📊 Datos

La aplicación carga datos de:
- `peliculas.csv` - 27,841 películas
- `generos.csv` - 21 géneros

Los datos se cargan dinámicamente desde los archivos CSV sin necesidad de base de datos.

## 🎨 Diseño

- **Tema oscuro** inspirado en plataformas de streaming
- **Responsive** - adaptado para móviles, tablets y desktop
- **Animaciones suaves** - transiciones y efectos hover
- **Accesibilidad** - contraste adecuado y navegación por teclado

## 🔧 Buenas Prácticas Implementadas

### Arquitectura
- ✅ Separación de responsabilidades (MVC-like)
- ✅ Componentes modulares y reutilizables
- ✅ Utilidades separadas para lógica común

### Código
- ✅ Código documentado con JSDoc
- ✅ Nomenclatura descriptiva y consistente
- ✅ Manejo de errores apropiado
- ✅ Validación de datos

### Performance
- ✅ Lazy loading de imágenes
- ✅ Debouncing en búsqueda
- ✅ CSS optimizado con variables
- ✅ Minimización de re-renderizados

### UX/UI
- ✅ Feedback visual inmediato
- ✅ Estados de carga
- ✅ Mensajes de error amigables
- ✅ Diseño intuitivo

## 📝 Notas

- Las imágenes de pósters se cargan desde TMDb (The Movie Database)
- Si una imagen no está disponible, se muestra un placeholder
- Los archivos CSV deben estar en el directorio padre de `web/`

## 🚀 Próximas Mejoras Posibles

- Paginación para mejorar performance con muchos resultados
- Favoritos guardados en LocalStorage
- Vista detallada de película (modal)
- Más filtros (año, puntuación mínima, etc.)
- Export/share de resultados
- Modo claro/oscuro toggle

---

**Desarrollado con ❤️ y buenas prácticas**
