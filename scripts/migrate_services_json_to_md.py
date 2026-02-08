import json
import os

INPUT_FILE = "src/data/services.json"
OUTPUT_DIR = "src/content/services"

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Read JSON
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    services = json.load(f)

for service in services:
    slug = service['id']
    title = service['title'].replace('"', '\\"')
    short_desc = service['shortDescription'].replace('"', '\\"')
    image = service['image']
    full_desc = service['fullDescription']
    
    md_content = f"""---
title: "{title}"
shortDescription: "{short_desc}"
image: "{image}"
---

{full_desc}
"""
    
    filename = os.path.join(OUTPUT_DIR, f"{slug}.md")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    print(f"Created {filename}")
