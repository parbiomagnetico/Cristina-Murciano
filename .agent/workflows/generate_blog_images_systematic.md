---
description: Sistema para generar imágenes premium del blog sin duplicaciones
---

# Workflow: Generar Imágenes del Blog (Sistema Definitivo)

## Pre-requisitos
1. Verificar que existe el archivo `.agent/PLAN_IMAGENES_BLOG.md`
2. Confirmar que la cuota de generación de imágenes está disponible

## Paso 1: Consultar el estado actual
```bash
# Revisar el plan maestro
cat .agent/PLAN_IMAGENES_BLOG.md
```

## Paso 2: Identificar el siguiente batch a ejecutar
- **Batch 1**: Wellness (9 imágenes) - Romper duplicación de `blog_wellness_lifestyle_premium.png`
- **Batch 2**: Fisioterapia (8 imágenes) - Romper duplicación de `blog_joint_assessment_premium.png`
- **Batch 3**: Circulación (3 imágenes) - Especializaciones de `blog_drainage_legs_premium.png`
- **Batch 4**: Finales (3 imágenes) - Reemplazar `blog-massage.png` placeholders

## Paso 3: Generar imágenes del batch seleccionado

### Estructura del prompt (NO CAMBIAR):
```
close-up of [DESCRIPCIÓN ESPECÍFICA], premium high-key photography, clinical but warm atmosphere, minimalist composition, airy and ethereal feel, soft natural lighting, color palette of clean white, soft teal, and gentle lilac, soft ethereal light leaks, diffused holographic color washes in pastel magenta and teal, dreamy aura-like glow, [AÑADIR SI APLICA: female therapist dressed entirely in professional white, anonymous and faceless (face is NOT visible, head is cropped or turned away)], focus is strictly on [OBJETO PRINCIPAL], 8k resolution, cinematic lighting, professional wellness aesthetic --no sharp rainbow prisms, distinct rainbow lines, faces, facial features, eyes, looking at camera, gloves, latex gloves, medical gloves, surgical gloves, male therapist, dark gloomy atmosphere, neon, cyberpunk, low quality, cartoon, illustration, busy background, messy room, text, watermark, signature
```

## Paso 4: Mover imágenes generadas
```bash
mv "C:/Users/facto/.gemini/antigravity/brain/[ID]/[ARCHIVO_GENERADO].png" "c:/Users/facto/Desktop/Cristinamurciano/src/assets/images/[NOMBRE_FINAL].png"
```

## Paso 5: Actualizar posts.json
Usar `multi_replace_file_content` para actualizar SOLO los slugs especificados en el plan para ese batch.

**IMPORTANTE**: Verificar en el plan qué artículos deben usar la nueva imagen y cuáles pueden seguir compartiendo la genérica.

## Paso 6: Verificar
```bash
# Verificar que la imagen existe
ls src/assets/images/blog-[nombre]-premium.png

# Verificar que el JSON la referencia
grep "[nombre]-premium.png" src/data/posts.json
```

## Paso 7: Marcar batch como completado
Actualizar el archivo `.agent/PLAN_IMAGENES_BLOG.md` añadiendo:
```
✅ Batch [N] completado - [FECHA]
```

## REGLAS CRÍTICAS
1. **NUNCA** regenerar una imagen que ya existe con nombre `-premium.png`
2. **SIEMPRE** consultar el plan antes de generar
3. **NO** generar todas las imágenes de golpe - hacerlo por batches
4. **RESPETAR** las decisiones de compartir imagen genérica cuando el plan lo indica
5. **ACTUALIZAR** el plan después de cada batch

## Control de Duplicaciones
Antes de generar, ejecutar:
```powershell
$posts = Get-Content src/data/posts.json | ConvertFrom-Json
$slug = "nombre-del-slug"
$currentImage = ($posts | Where-Object { $_.slug -eq $slug }).image
Write-Host "Artículo '$slug' usa actualmente: $currentImage"
```

Si ya tiene una imagen `-premium.png` específica → **NO REGENERAR**

## Ejemplo de Ejecución (Batch 1, Primera Imagen)

1. **Consultar plan**: Verificar que `blog-autocuidado-premium.png` no existe
2. **Generar**:
   ```
   ImageName: blog-autocuidado-premium
   Prompt: close-up of hands in meditation mudra position on lap, peaceful self-care moment, premium high-key photography...
   ```
3. **Mover**:
   ```bash
   mv "C:/Users/facto/.gemini/.../blog_autocuidado_premium_[ID].png" "c:/Users/facto/Desktop/Cristinamurciano/src/assets/images/blog-autocuidado-premium.png"
   ```
4. **Actualizar JSON**: Cambiar `cuidar-cuerpo` de `blog_wellness_lifestyle_premium.png` → `blog-autocuidado-premium.png`
5. **Verificar**: Comprobar que el archivo existe y el JSON apunta correctamente

## Resumen
- Total de imágenes pendientes: **23**
- Dividido en: **4 batches**
- Tiempo estimado: **~2 horas** (respetando límites de cuota)
- Ahorro vs generar todo: **~40% de tokens**
