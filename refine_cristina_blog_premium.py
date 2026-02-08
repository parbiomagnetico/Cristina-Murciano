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

# ⚠️ RUTA DEL BLOG
DIRECTORIO_BLOG = "./src/content/blog" 

if not API_KEY:
    raise ValueError("❌ ERROR: No se encontró GOOGLE_API_KEY en el archivo .env")

# --- SEGURIDAD ---
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

genai.configure(api_key=API_KEY)
# Usamos gemini-2.5-flash como solicitó el usuario
model = genai.GenerativeModel(
    'gemini-2.5-flash', 
    generation_config={"response_mime_type": "application/json"},
    safety_settings=safety_settings
)

# --- EL CEREBRO (TERAPEUTA CERCANA) ---
SYSTEM_INSTRUCTION = """
ACTÚA COMO: Cristina Murciano, Fisioterapeuta y Osteópata experta en Monzón.
TU ESTILO: Premium, profesional pero cercano, empático y sosegado. Transmitiendo calma y autoridad técnica sin ser pedante.

OBJETIVO:
Reescribir un artículo de blog para elevar su calidad al nivel de "parbiomagnetico.es/blog".
Debe ser interesante, fácil de leer y exquisitamente estructurado.

LONGITUD OBJETIVO: 
Alrededor de 400 palabras. (Concisión y valor).

REGLAS DE ORO DE REDACCIÓN:
1.  **Estructura Impecable:** Usa H2 y párrafos cortos. El texto debe "respirar".
2.  **SEO Natural:** El artículo debe posicionar por el tema (ej: "Dolor muscular"), pero SIN repetir palabras clave robóticamente.
3.  **Toque Local Sutil:** Menciona "Monzón" o "mi consulta en Monzón" **SOLO UNA VEZ** y preferiblemente en el cierre o CTA final. NO lo repitas por todo el texto.
4.  **Enfoque Holístico:** No hables solo de músculos; habla de bienestar, estrés y conexión cuerpo-mente si el tema lo permite.
5.  **Sin Relleno:** Elimina frases vacías como "En el vertiginoso mundo de hoy...". Ve al grano con elegancia.
6.  **Formato:** Markdown limpio. No uses H1 (el título ya va en el frontmatter).

ESTRUCTURA SUGERIDA (No pongas los nombres de las secciones literales, fluye):
- **Introducción empática:** Conecta con el problema del lector.
- **El porqué (Cuerpo):** Explicación técnica sencilla de lo que ocurre.
- **La Solución (Tratamiento):** Cómo lo abordamos en consulta (técnicas manuales, ambiente, etc.).
- **Beneficios:** Qué sentirá el paciente después.
- **Cierre/CTA:** Invitación suave a reservar en Monzón.

SALIDA JSON:
{
  "new_title": "Título H1 Atractivo y SEO-Friendly",
  "seo_excerpt": "Meta descripción (150-160 chars) persuasiva para Google.",
  "social_caption": "Texto breve y atractivo para compartir en Instagram/Facebook con hashtags.",
  "category": "Categoría principal (ej: Fisioterapia, Bienestar, Osteopatía)",
  "tags": ["tag1", "tag2", "tag3"],
  "markdown_content": "[El contenido completo del artículo en Markdown sin el título H1]"
}
"""

def limpiar_json(texto_sucio):
    texto_limpio = re.sub(r'```json\s*|\s*```', '', texto_sucio)
    return texto_limpio.strip()

def procesar_blog_premium():
    if not os.path.exists(DIRECTORIO_BLOG):
         print(f"❌ Error: No existe el directorio: {DIRECTORIO_BLOG}")
         return
 
    # Abrir archivo de log para salida en tiempo real
    log_file = open("refinement_output_live.txt", "w", encoding="utf-8")
    
    def log(mensaje):
        print(mensaje)
        log_file.write(mensaje + "\n")
        log_file.flush()  # Forzar escritura inmediata
 
    archivos = [f for f in os.listdir(DIRECTORIO_BLOG) if f.endswith(".md")]
    archivos.sort()
    
    log(f"Iniciando Reescritura (Estilo Conciso) en {len(archivos)} archivos...")
    log(f"Hora de inicio: {time.strftime('%H:%M:%S')}")
    log("")
    
    procesados = 0
    saltados = 0
    
    for nombre_archivo in archivos:
        ruta_completa = os.path.join(DIRECTORIO_BLOG, nombre_archivo)
        log(f"Procesando: {nombre_archivo}")
        
        try:
            post = frontmatter.load(ruta_completa)
            
            if post.get('optimized', False): 
                log(f"  → Saltando {nombre_archivo} (ya optimizado)")
                saltados += 1
                continue

            prompt_usuario = f"POST ORIGINAL:\nTítulo: {post.get('title', '')}\nContenido:\n{post.content}"
 
            log(f"  → Enviando a IA...")
            response = model.generate_content(f"{SYSTEM_INSTRUCTION}\n\n{prompt_usuario}")
            datos_ia = json.loads(limpiar_json(response.text))
            
            # Actualizar frontmatter
            post['title'] = datos_ia['new_title']
            post['excerpt'] = datos_ia['seo_excerpt']
            post['social_caption'] = datos_ia['social_caption']
            post['category'] = datos_ia['category']
            post['tags'] = datos_ia['tags']
            
            # Actualizar contenido
            post.content = datos_ia['markdown_content']
            post['active'] = True # Mantener artículo visible
            post['optimized'] = True 
            
            with open(ruta_completa, "w", encoding="utf-8") as f:
                f.write(frontmatter.dumps(post))
            
            procesados += 1
            log(f"  ✓ Éxito! {nombre_archivo} reescrito con nuevo estilo.")
            log(f"  Progreso: {procesados} procesados, {saltados} saltados")
            log("")
            time.sleep(2) # Pausa reducida para ir más rápido

        except Exception as e:
            log(f"  ✗ Error: {e}")
            if "429" in str(e):
                log("  Cuota excedida, esperando 60s...")
                time.sleep(60)
            log("")
    
    log(f"\n{'='*50}")
    log(f"RESUMEN FINAL:")
    log(f"  Total procesados: {procesados}")
    log(f"  Total saltados: {saltados}")
    log(f"  Hora de fin: {time.strftime('%H:%M:%S')}")
    log(f"{'='*50}")
    log_file.close()

if __name__ == "__main__":
    procesar_blog_premium()