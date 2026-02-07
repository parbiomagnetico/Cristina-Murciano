import os
import time
import frontmatter
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv
from tqdm import tqdm
import json
import re

# --- CONFIGURACIÓN ---
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# ⚠️ RUTA DEL BLOG (Ajusta si es necesario)
DIRECTORIO_BLOG = "./src/content/blog" 

if not API_KEY:
    raise ValueError("❌ ERROR: No se encontró GOOGLE_API_KEY en el archivo .env")

# --- SEGURIDAD (ANTIBLOQUEO) ---
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(
    'gemini-2.5-pro', # ⚠️ USAMOS PRO PARA MAYOR CALIDAD EN TEXTOS LARGOS (Si da error 429, cambia a flash)
    generation_config={"response_mime_type": "application/json"},
    safety_settings=safety_settings
)

# --- EL CEREBRO (TERAPEUTA MANUAL SENIOR) ---
SYSTEM_INSTRUCTION = """
ACTÚA COMO: Cristina Murciano, Terapeuta Manual Experta (Quiromasaje, Osteopatía, Drenaje). 
Tu consulta está en Monzón (Huesca).

OBJETIVO: Convertir un borrador básico en un ARTÍCULO PILAR SEO (1.000 - 1.200 palabras).
El artículo debe posicionarte como la mayor autoridad local en bienestar y alivio del dolor.

TONO:
- Profesional pero cálido (como si hablaras con un paciente en la camilla).
- Educativo: Usa términos anatómicos correctos (fascia, cortisol, sistema linfático) pero explicados sencillos.
- Persuasivo: El lector debe sentir que "entiendes su dolor".

ESTRUCTURA OBLIGATORIA DEL CONTENIDO (Markdown):
1.  **H1: Título Gancho** (Ej: "Ciática: Por qué ocurre y cómo calmarla sin pastillas").
2.  **Introducción Empática:** "Sé cómo te sientes...". Describe los síntomas cotidianos.
3.  **H2: La Raíz del Problema (Anatomía y Emoción):**
    - Explica qué pasa dentro del cuerpo (contractura, inflamación, estrés).
    - Menciona la conexión cuerpo-mente (somatización).
4.  **H2: Cómo te ayuda la Terapia Manual:**
    - No hables de "masajes genéricos". Habla de "liberación miofascial", "descontracturante", "equilibrio".
    - Explica el mecanismo de alivio.
5.  **H2: Beneficios Concretos:**
    - Lista con bullet points (Mejora sueño, movilidad, reduce ansiedad...).
6.  **H2: ¿Por qué elegirnos en Monzón?**
    - Autoridad local y trato personalizado.
7.  **Conclusión y CTA:** Invitación directa a reservar cita.

SALIDA JSON (Estricta):
{
  "new_title": "Título H1 optimizado SEO",
  "seo_excerpt": "Meta descripción (155 car) con palabra clave + Monzón",
  "social_caption": "Texto para Instagram: Problema + Solución + Hashtags (#Monzon #Bienestar #Masaje)",
  "category": "Categoría sugerida (ej: Dolor de Espalda, Bienestar, Estrés)",
  "tags": ["tag1", "tag2", "tag3"],
  "markdown_content": "# Título H1\n\n[Contenido completo del artículo siguiendo la estructura]..."
}
"""

def limpiar_json(texto_sucio):
    texto_limpio = re.sub(r'```json\s*|\s*```', '', texto_sucio)
    return texto_limpio.strip()

def procesar_blog_premium():
    if not os.path.exists(DIRECTORIO_BLOG):
         print(f"❌ Error: No existe el directorio: {DIRECTORIO_BLOG}")
         return

    archivos = [f for f in os.listdir(DIRECTORIO_BLOG) if f.endswith(".md")]
    print(f"🌟 Iniciando Reescritura PREMIUM en {len(archivos)} artículos...")
    
    procesados = 0
    omitidos = 0

    pbar = tqdm(archivos, desc="Creando Artículos Pilar")

    for nombre_archivo in pbar:
        ruta_completa = os.path.join(DIRECTORIO_BLOG, nombre_archivo)
        
        # --- BUCLE TANQUE (Retry Infinito) ---
        while True:
            try:
                post = frontmatter.load(ruta_completa)
                
                # --- FILTROS ---
                # 1. Solo procesar si active es False (Borradores)
                #if post.get('active', False) is True:
                #    omitidos += 1
                #    break 

                # 2. Si ya está optimizado, saltar
                #if post.get('optimized', False) is True:
                #    omitidos += 1
                #    break

                # --- GENERAR ---
                pbar.set_description(f"✍️ Escribiendo: {nombre_archivo[:10]}...")
                
                # Le pasamos título y contenido actual
                prompt_usuario = f"BORRADOR ORIGINAL:\nTítulo: {post.get('title', '')}\nContenido:\n{post.content}"

                response = model.generate_content(f"{SYSTEM_INSTRUCTION}\n\n{prompt_usuario}")
                datos_ia = json.loads(limpiar_json(response.text))
                
                # --- ACTUALIZACIÓN FRONTMATTER ---
                post['title'] = datos_ia['new_title']
                post['excerpt'] = datos_ia['seo_excerpt']
                post['social_caption'] = datos_ia['social_caption']
                post['category'] = datos_ia['category']
                post['tags'] = datos_ia['tags']
                
                # Mantenemos layout e imagen si existen, si no, los dejamos igual
                if not post.get('layout'):
                     post['layout'] = '../../layouts/BlogPost.astro'
                
                # Marcas de control
                post['active'] = False # Seguimos en borrador para revisión
                post['optimized'] = True # Marca de calidad
                
                # Reemplazo total del cuerpo
                post.content = datos_ia['markdown_content']
                
                with open(ruta_completa, "w", encoding="utf-8") as f:
                    f.write(frontmatter.dumps(post))
                    
                procesados += 1
                
                # Pausa de seguridad (Al usar PRO, necesitamos más pausa)
                time.sleep(10) 
                break 

            except Exception as e:
                error_str = str(e)
                if "429" in error_str:
                    pbar.set_description(f"⛔ 429 (Cuota). Esperando 60s...")
                    time.sleep(60) # Espera larga para modelo Pro
                elif "Safety" in error_str:
                    print(f"\n⚠️ Bloqueo de seguridad en {nombre_archivo}. Reintentando...")
                    time.sleep(5)
                else:
                    print(f"\n⚠️ Error en {nombre_archivo}: {e}")
                    time.sleep(15)

    print(f"\n✅ FINALIZADO: {procesados} Artículos Pilar creados. {omitidos} ignorados.")

if __name__ == "__main__":
    procesar_blog_premium()