---
description: How to generate consistent, premium images for blog posts
---

# Generar Imágenes para el Blog

Este workflow garantiza que todas las imágenes del blog mantengan la estética "premium/etérea" de la marca.

## 1. Preparación
Asegúrate de tener claro el sujeto de la imagen (ej: "manos masajeando pie", "aceites esenciales lavanda", etc.).

## 2. Generar el Prompt
Usa el script automatizado para obtener un prompt que cumple con la guía de estilo.

// turbo
```bash
npm run gen:prompt -- "TU DECIPCION AQUI"
```

## 3. Generar la Imagen
Copia el output del paso anterior y úsalo en tu herramienta de generación de imágenes favorita (Midjourney, DALL-E 3, o el agente de IA si tiene quota).

**Nota:** Si usas el agente, simplemente pídele:
"Genera una imagen usando este prompt: [PEGAR PROMPT]"

## 4. Guardar
Guarda la imagen en `src/assets/images/` con el formato `blog-[slug].png`.
