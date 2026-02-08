import json
import os
import re

# Paths
posts_json_path = r'c:\Users\facto\Desktop\Cristinamurciano\src\data\posts.json'
output_dir = r'c:\Users\facto\Desktop\Cristinamurciano\src\content\blog'

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Read JSON
with open(posts_json_path, 'r', encoding='utf-8') as f:
    posts = json.load(f)

print(f"Found {len(posts)} posts to convert.")

for post in posts:
    slug = post.get('slug')
    title = post.get('title').replace('"', '\\"') # Escape quotes in title
    date = post.get('date')
    image = post.get('image')
    image_alt = post.get('image_alt', '').replace('"', '\\"')
    excerpt = post.get('excerpt', '').replace('"', '\\"')
    content = post.get('content', '')
    active = str(post.get('active', True)).lower()
    optimized = str(post.get('optimized', False)).lower()

    # Create frontmatter
    md_content = f"""---
title: "{title}"
date: "{date}"
image: "{image}"
image_alt: "{image_alt}"
excerpt: "{excerpt}"
active: {active}
optimized: {optimized}
---

{content}
"""
    
    # Write to file
    file_path = os.path.join(output_dir, f"{slug}.md")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

print("Conversion complete!")
