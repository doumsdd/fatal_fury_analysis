#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraping des portraits et donnÃ©es pour Fatal Fury: City of the Wolves
"""

import requests
import os
import json
from config import API_ENDPOINT, CHARACTERS_FALLBACK, PORTRAITS_DIR

# CrÃ©er le dossier portraits s'il n'existe pas
os.makedirs(PORTRAITS_DIR, exist_ok=True)

def get_page_image(page_name):
    """RÃ©cupÃ¨re l'image principale d'une page wiki via l'API."""
    url = f"{API_ENDPOINT}?action=query&titles={page_name}&prop=images&format=json"
    try:
        response = requests.get(url)
        data = response.json()
        if 'query' in data and 'pages' in data['query']:
            pages = data['query']['pages']
            page_id = list(pages.keys())[0]
            images = pages[page_id].get('images', [])
            # Cherche un fichier image dans les liens de la page
            for img in images:
                if img['title'].startswith("File:") or img['title'].startswith("File :"):
                    return img['title'].replace("File:", "").replace("File :", "")
        return None
    except Exception as e:
        print(f"Error fetching {page_name}: {e}")
        return None

def download_wiki_image(file_name, save_path):
    """TÃ©lÃ©charge une image depuis le wiki."""
    thumb_url = f"https://dreamcancel.com/wiki/Special:FilePath/{file_name}"
    try:
        res = requests.get(thumb_url, stream=True)
        if res.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in res.iter_content(1024):
                    f.write(chunk)
            return True
    except Exception as e:
        print(f"Failed to download {file_name}: {e}")
    return False

if __name__ == "__main__":
    portraits_map = {}
    
    # Liste des personnages principaux pour FFCOTW (peut Ãªtre enrichie)
    ff_characters = [
        "Terry Bogard", "Rock Howard", "Billy Kane", "B.Jenet", "Gato", 
        "Hokutomaru", "Hotaru Futaba", "Kim Dong Hwan", "Kain R. Heinlein", 
        "Kevin Rian", "Marco Rodrigues", "Mr. Big", "Salvatore Ganacci", 
        "Vox Reaper", "Duck King", "Rick Strowd", "Preecha", "Laocorn Gaudeamus",
        "Andy Bogard", "Joe Higashi", "Ken Masters", "Chun-Li", "Manjiro & Ken",
        "Kim Jae Hoon", "Nightmare Geese", "Kim Kaphwan"
    ]

    print("Starting FFCOTW Portrait Extraction...")
    
    for char in ff_characters:
        file_name = get_page_image(char)
        if file_name:
            safe_name = char.replace(" ", "_").replace("&", "and")
            filename = f"{safe_name}.png"
            filepath = os.path.join(PORTRAITS_DIR, filename)
            
            if not os.path.exists(filepath):
                print(f"Downloading {filename}...")
                success = download_wiki_image(file_name, filepath)
                if success:
                    portraits_map[char] = filename
                else:
                    portraits_map[char] = None # Failed download
            else:
                portraits_map[char] = filename
        
        # Petit delay pour Ãªtre gentil avec le serveur
        import time
        time.sleep(0.5)

    # Sauvegarde du mapping
    with open("portraits_mapping.json", "w", encoding="utf-8") as f:
        json.dump(portraits_map, f, ensure_ascii=False, indent=2)
        
    print(f"\nDone! Found {len([k for v in portraits_map.values() if v])} portraits.")