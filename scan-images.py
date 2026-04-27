#!/usr/bin/env python3
"""
Run this from your website2026 folder:
  python3 scan-images.py

It scans all project folders, finds the first image in each,
and writes images/manifest.json — the site uses this to find images.
"""
import os, json, re

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images', 'projects')
manifest = {}
extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.JPG', '.JPEG', '.PNG', '.WEBP'}

if not os.path.exists(base):
    print(f"Folder not found: {base}")
    exit(1)

for folder in sorted(os.listdir(base)):
    folder_path = os.path.join(base, folder)
    if not os.path.isdir(folder_path):
        continue
    
    # Find all images in folder, sorted (1.jpg first if exists)
    images = sorted([
        f for f in os.listdir(folder_path)
        if os.path.splitext(f)[1] in extensions
        and not f.startswith('.')
    ])
    
    if images:
        # Use 1.jpg/png if exists, otherwise first image found
        preferred = next((img for img in images if os.path.splitext(img)[0] == '1'), images[0])
        manifest[folder] = f"images/projects/{folder}/{preferred}"
        print(f"✓ {folder} → {preferred}")
    else:
        print(f"  {folder} — no images")

# Write manifest
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images', 'manifest.json')
with open(out, 'w') as f:
    json.dump(manifest, f, indent=2)

print(f"\n✓ Wrote {len(manifest)} entries to images/manifest.json")
print(f"  Missing images: {len([f for f in os.listdir(base) if os.path.isdir(os.path.join(base,f))]) - len(manifest)} folders")
