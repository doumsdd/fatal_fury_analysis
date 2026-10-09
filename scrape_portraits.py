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
    # Mapping exact des caractères de recherche vers les noms complets
    # et les préfixes d'image car certains utilisent un format différent
    character_mapping = {
        "Terry": ("Terry Bogard", "FF_COTW_Terry_Icon"),
        "Rock": ("Rock Howard", "FF_COTW_Rock_Icon"),
        "Andy": ("Andy Bogard", "FF_COTW_Andy_Icon"),
        "Joe": ("Joe Higashi", "FF_COTW_Joe_Icon"),
        "Billy": ("Billy Kane", "FF_COTW_Billy_Icon"),
        "BJenet": ("B.Jenet", "FF_COTW_B_Jenet_Icon"),
        "Gato": ("Gato", "FF_COTW_Gato_Icon"),
        "Hokutomaru": ("Hokutomaru", "FF_COTW_Hokutomaru_Icon"),
        "HotaruFutaba": ("Hotaru Futaba", "FF_COTW_Hotaru_Futaba_Icon"),
        "KimDongHwan": ("Kim Dong Hwan", "FF_COTW_Kim_Dong_Hwan_Icon"),
        "KainRHeinlein": ("Kain R. Heinlein", "FF_COTW_Kain_R_Heinlein_Icon"),
        "Kevin": ("Kevin Rian", "FF_COTW_Kevin_Icon"),
        "Marco": ("Marco Rodrigues", "FF_COTW_Marco_Icon"),
        "MrBig": ("Mr. Big", "FF_COTW_Mr_Big_Icon"),
        "Salvatore": ("Salvatore Ganacci", "FF_COTW_Salvatore_Icon"),
        "Vox Reaper": ("Vox Reaper", "FF_COTW_Vox_Icon"),
        "DuckKing": ("Duck King", "FF_COTW_Duck_King_Icon"),
        "Rick": ("Rick Strowd", "FF_COTW_Rick_Icon"),
        "Preecha": ("Preecha", "FF_COTW_Preecha_Icon"),
        "KenMasters": ("Ken Masters", "FF_COTW_Ken_Icon"),
        "ChunLi": ("Chun-Li", "FF_COTW_Chun-Li_Icon"),
        "JaeHoon": ("Kim Jae Hoon", "COTW_Jae_Hoon_Icon"),
        "Kim": ("Kim Kaphwan", "FF_COTW_Kim_Icon"),
        "Mary": ("Blue Mary", "FF_COTW_Mary_Icon"),
        "CR7": ("Cristiano Ronaldo", "FF_COTW_CR7_Icon"),
        "Krauser": ("Wolfgang Krauser", "FF_COTW_Krauser_Icon"),
        "MrKarate": ("Mr. Karate", "FF_COTW_Mr_Karate_Icon"),
        "Kenshiro": ("Kenshiro", "FF_COTW_Kenshiro_Icon"),
        "Mai": ("Mai Shiranui", "FF_COTW_Mai_Icon"),
        "Tizoc": ("Tizoc", "FF_COTW_Tizoc_Icon"),
        "NightmareGeese": ("Nightmare Geese", "FF_COTW_Nightmare_Geese_Icon")
    }
    
    # Personnages exclus car non sortis sur le wiki:
    # - Laocorn Gaudeamus (Sortie: Novembre 2026)
    # - Manjiro & Ken (Sortie: Octobre 2026)
    
    # Personnages sans icônes disponibles sur le wiki à ce jour:
    # - Hotaru Futaba, Kain R. Heinlein, Kim Dong Hwan
    
    all_chars = {}
    
    for search_key in character_mapping.keys():
        display_name, image_prefix = character_mapping[search_key]
        
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'allimages',
            'aiprefix': f'{image_prefix}',
            'ailimit': '5'
        }
        
        try:
            response = requests.get(API_ENDPOINT, params=params, timeout=10)
            data = response.json()
            
            if 'query' in data and data['query']['allimages']:
                img = data['query']['allimages'][0]
                all_chars[display_name] = {
                    'filename': img['name'],
                    'url': img['url']
                }
                print(f"  ✅ {display_name}: {img['name']}")
        except Exception as e:
            print(f"  ⚠️ Error fetching {display_name}: {e}")
    
    print(f"\n📊 Total trouvé: {len(all_chars)} icônes\n")
    
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