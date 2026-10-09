#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour lister toutes les images Fatal Fury COTW sur le wiki DreamCancel
"""

import requests
import json
import os
from config import API_ENDPOINT

def get_all_cotw_images():
    """Récupère toutes les images avec le préfixe CotW_"""
    all_images = []
    continuation = None
    
    while True:
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'allimages',
            'aiprefix': 'CotW_',
            'ailimit': '500'
        }
        
        if continuation:
            params['aicontinue'] = continuation
        
        response = requests.get(API_ENDPOINT, params=params, timeout=10)
        data = response.json()
        
        if 'query' in data and 'allimages' in data:
            all_images.extend(data['query']['allimages'])
        
        if 'continue' in data:
            continuation = data['continue'].get('aicontinue')
        else:
            break
    
    return all_images

def extract_portrait_info(images):
    """Extrait les informations de portraits des images."""
    # Patterns typiques pour les portraits FFCOTW
    portrait_patterns = [
        '_Portrait',
        'Portrait_',
        '_Prt',
        '_Icon',
        '_Splash',
        '_TitleScreen',
        '_Win',
        '_Select'
    ]
    
    portraits = {}
    for img in images:
        name = img['name']
        url = img['url']
        
        # Vérifier si c'est un portrait ou splash art
        for pattern in portrait_patterns:
            if pattern in name:
                # Extraire le nom du personnage (ex: CotW_Terry_Portrait.png -> Terry)
                parts = name.split('_')
                # Skip 'CotW' prefix and find character name
                char_name = ''
                found_cotw = False
                for part in parts:
                    if part == 'CotW':
                        found_cotw = True
                        continue
                    if found_cotw:
                        char_name += part + ' '
                
                if char_name:
                    char_name = char_name.strip().rstrip('PrtIconSelectWinTitleScreen').strip()
                    portraits[char_name] = {
                        'filename': name,
                        'url': url
                    }
                break
    
    return portraits

def main():
    print("🐺 Listing all Fatal Fury COTW images from DreamCancel Wiki...")
    
    images = get_all_cotw_images()
    print(f"Total images found with 'CotW_' prefix: {len(images)}")
    
    # Sauvegarder toutes les images dans un fichier pour analyse
    with open('all_cotw_images.json', 'w', encoding='utf-8') as f:
        json.dump(images, f, ensure_ascii=False, indent=2)
    
    # Extraire les portraits
    portraits = extract_portrait_info(images)
    print(f"\nPortraits/Splash arts trouvés: {len(portraits)}")
    
    # Afficher les portraits uniques par personnage
    unique_chars = set()
    for char_name in portraits.keys():
        # Normaliser le nom (enlever les parties techniques)
        clean_name = char_name.split('Portrait')[0].split('Prt')[0].split('Icon')[0].strip()
        unique_chars.add(clean_name)
    
    print(f"Personnages identifiés: {len(unique_chars)}")
    print("\nListe des personnages:")
    for char in sorted(unique_chars):
        print(f"  - {char}")
    
    print("\nFichier sauvegardé: all_cotw_images.json")

if __name__ == "__main__":
    main()