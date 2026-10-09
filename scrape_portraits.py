#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recherche et téléchargement des portraits Fatal Fury COTW
Les images sont au format FF_COTW_<CharacterName>_Icon.png
Ex: https://dreamcancel.com/w/images/thumb/f/f6/FF_COTW_Andy_Icon.png/85px-FF_COTW_Andy_Icon.png
"""

import requests
import json
import os
from config import API_ENDPOINT, PORTRAITS_DIR

def get_all_ff_cotw_icons():
    """Récupère toutes les icônes de personnages FFCOTW."""
    # Mapping des noms courts vers les noms complets
    character_mapping = {
        "Terry": "Terry Bogard",
        "Rock": "Rock Howard",
        "Andy": "Andy Bogard",
        "Joe": "Joe Higashi",
        "Billy": "Billy Kane",
        "BJenet": "B.Jenet",
        "Gato": "Gato",
        "Hokutomaru": "Hokutomaru",
        "Hotaru Futaba": "Hotaru Futaba",
        "KimDongHwan": "Kim Dong Hwan",
        "KainRHeinlein": "Kain R. Heinlein",
        "Kevin Rian": "Kevin Rian",
        "MarcoRodrigues": "Marco Rodrigues",
        "MrBig": "Mr. Big",
        "Salvatore Ganacci": "Salvatore Ganacci",
        "Vox Reaper": "Vox Reaper",
        "DuckKing": "Duck King",
        "RickStrowd": "Rick Strowd",
        "Preecha": "Preecha",
        "LaocornGaudeamus": "Laocorn Gaudeamus",
        "Ken Masters": "Ken Masters",
        "ChunLi": "Chun-Li",
        "KimJaeHoon": "Kim Jae Hoon",
        "Nightmare Geese": "Nightmare Geese",
        "Kim Kaphwan": "Kim Kaphwan",
        "Blue Mary": "Blue Mary",
        "Cristiano Ronaldo": "Cristiano Ronaldo",
        "Wolfgang Krauser": "Wolfgang Krauser",
        "Mr Karate": "Mr. Karate",
        "Kenshiro": "Kenshiro",
        "Mai Shiranui": "Mai Shiranui"
    }
    
    # Liste des personnages à rechercher (espaces remplacés par rien)
    characters_to_search = list(character_mapping.keys())
    
    all_chars = {}
    
    for char_key in characters_to_search:
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'allimages',
            'aiprefix': f'FF_COTW_{char_key}_Icon',
            'ailimit': '10'
        }
        
        try:
            response = requests.get(API_ENDPOINT, params=params, timeout=10)
            data = response.json()
            
            if 'query' in data and data['query']['allimages']:
                img = data['query']['allimages'][0]
                display_name = character_mapping[char_key]
                all_chars[display_name] = {
                    'filename': img['name'],
                    'url': img['url']
                }
        except Exception as e:
            print(f"  ⚠️ Error fetching {char_key}: {e}")
    
    print(f"\n✅ {len(all_chars)} icônes trouvées:")
    for name, info in sorted(all_chars.items()):
        print(f"  • {name}: {info['filename']}")
    
    return all_chars

def extract_character_icon(images):
    """Extrait le nom du personnage depuis le nom d'image."""
    characters = {}
    
    for img in images:
        name = img['name']  # Ex: FF_COTW_Andy_Icon.png
        
        # Extraire le nom du personnage
        # Format: FF_COTW_<Name>_Icon.png
        parts = name.split('_')
        
        if len(parts) >= 4:
            # Enlever 'FF' et 'COTW' du début, et '_Icon.png' de la fin
            char_name_parts = parts[2:-2]  # Prend entre 'COTW' et 'Icon'
            
            # Rejoindre pour créer le nom complet
            char_name = ' '.join(p.capitalize() for p in char_name_parts)
            
            characters[char_name] = {
                'filename': name,
                'url': img['url']
            }
    
    return characters

def download_image(url, filename):
    """Télécharge une image depuis une URL."""
    filepath = os.path.join(PORTRAITS_DIR, filename)
    try:
        res = requests.get(url, stream=True, timeout=10)
        if res.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in res.iter_content(8192):
                    f.write(chunk)
            return True
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")
    return False

def generate_lovable_json(characters):
    """Génère le JSON Lovable avec les icônes téléchargées."""
    output_data = []
    
    sorted_chars = sorted(characters.keys())
    
    for i, char_name in enumerate(sorted_chars, 1):
        info = characters[char_name]
        
        # Créer un nom de fichier lisible
        safe_name = char_name.replace(" ", "_").replace("&", "and")
        download_filename = f"{safe_name}.png"
        
        downloaded = download_image(info['url'], download_filename)
        
        entry = {
            "id": i,
            "name": char_name,
            "image": download_filename if downloaded else None,
            "stats": {
                "role": "Fighter",
                "faction": "Fatal Fury Universe",
                "game": "Fatal Fury: City of the Wolves"
            },
            "availability": "Released"
        }
        
        output_data.append(entry)
    
    # Sauvegarder
    with open("lovable_data.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    return output_data

def main():
    print("🐺 Scraping des ICÔNES Fatal Fury COTW\n")
    print("   Pattern recherché : FF_COTW_<Character>_Icon.png\n")
    
    os.makedirs(PORTRAITS_DIR, exist_ok=True)
    
    print("📥 Récupération des icônes depuis DreamCancel Wiki...")
    characters = get_all_ff_cotw_icons()
    
    if not characters:
        print("\n⚠️ Aucune icône trouvée ! Vérifiez les patterns.\n")
        return
    
    print(f"\n{'='*70}")
    print(f"💾 Génération des fichiers...\n")
    
    output_data = generate_lovable_json(characters)
    
    # Compter les succès
    success_count = sum(1 for e in output_data if e['image'])
    
    print(f"\n{'='*70}")
    print(f"✨ SCRAPING TERMINÉ AVEC SUCCÈS !")
    print(f"   Personnages identifiés : {len(characters)}")
    print(f"   Icônes téléchargées : {success_count}")
    print(f"   Fichier JSON : lovable_data.json")
    print(f"   Portraits dans : {PORTRAITS_DIR}/")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()