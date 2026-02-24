# 🚀 Deploy en Vercel

Guía rápida para desplegar tu buscador de películas en Vercel.

## Método 1: Deploy desde la Terminal (Recomendado)

### 1. Instalar Vercel CLI

```bash
npm install -g vercel
```

### 2. Ir a la carpeta del proyecto

```bash
cd web
```

### 3. Deploy

```bash
vercel
```

Sigue los pasos:
- Login con tu cuenta de Vercel (GitHub, GitLab o email)
- Confirma el nombre del proyecto
- Confirma el directorio (debe ser `.` o `./`)
- ¡Listo! Te dará una URL

### 4. Deploy a Producción

```bash
vercel --prod
```

---

## Método 2: Deploy desde GitHub

### 1. Crear repositorio en GitHub

```bash
cd web
git init
git add .
git commit -m "Initial commit - Buscador de películas"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/TU-REPO.git
git push -u origin main
```

### 2. Importar en Vercel

1. Ve a [vercel.com](https://vercel.com)
2. Click en "New Project"
3. Importa tu repositorio de GitHub
4. Vercel detectará automáticamente la configuración
5. Click en "Deploy"

---

## Método 3: Deploy con GUI de Vercel

### 1. Subir carpeta directamente

1. Ve a [vercel.com/new](https://vercel.com/new)
2. Arrastra la carpeta `web` completa
3. Click en "Deploy"

---

## ⚙️ Configuración Automática

El archivo `vercel.json` ya está configurado para:
- ✅ Servir archivos estáticos
- ✅ Rutas correctas para todos los recursos
- ✅ Sin necesidad de build

## 🌐 URLs

Después del deploy obtendrás:
- **Preview**: `https://tu-proyecto-xxxxx.vercel.app`
- **Producción**: `https://tu-proyecto.vercel.app`

## 📝 Notas Importantes

- Los archivos CSV se despliegan junto con la app
- No necesitas backend ni base de datos
- Cada push a main/main desplegará automáticamente (si usas GitHub)
- Vercel es gratis para proyectos personales

## 🔄 Actualizar el Deploy

```bash
# Hacer cambios en tu código
git add .
git commit -m "Actualización"
git push

# O desde CLI de Vercel
vercel --prod
```

## 🛠️ Troubleshooting

### Error: "Module not found"
- Verifica que todos los archivos estén en la carpeta `web`
- Revisa que las rutas de importación usen `./` (relativas)

### CSV no se cargan
- Asegúrate de que `peliculas.csv` y `generos.csv` están en `web/`
- Verifica las rutas en `dataLoader.js` (`./peliculas.csv`, `./generos.csv`)

### Deploy falla
```bash
# Limpiar caché de Vercel
vercel --force
```

---

**¡Tu app estará online en menos de 1 minuto! 🎉**
