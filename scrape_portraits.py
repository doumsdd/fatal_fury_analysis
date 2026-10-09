#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recherche et téléchargement des portraits Fatal Fury COTW
"""

import requests
import json
import os
import time
from config import API_ENDPOINT, PORTRAITS_DIR

def get_all_cotw_images():
    """Récupère toutes les images CotW du wiki."""
    all_images = []
    continuation = None
    
    while True:
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'allimages',
            'aifrom': 'CotW',
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

def find_portraits(images):
    """Extrait les portraits et splash arts des personnages."""
    # Patterns typiques pour les portraits
    portrait_keywords = [
        '_Portrait.',
        '_Splash.',
        '_TitleScreen.',
        '_Select.',
        '_Icon.',
        '_Win.',
        '_Card.',
        '_Banner.'
    ]
    
    portraits = {}
    move_animations = {}
    
    for img in images:
        name = img['name']
        
        # Vérifier si c'est un portrait/splash
        is_portrait = any(kw in name for kw in portrait_keywords)
        
        if is_portrait:
            # Extraire le nom du personnage
            char_name = name.split('_')[1] if len(name.split('_')) > 1 else "Unknown"
            portraits[char_name] = img['url']
        else:
            # Stocker comme animation de coup si pertinent
            if 'CotW_' in name or 'CotW' in name.split('_')[0]:
                parts = name.split('_')
                if len(parts) > 1:
                    char_name = parts[1]
                    if char_name not in move_animations:
                        move_animations[char_name] = []
                    move_animations[char_name].append({
                        'name': name,
                        'url': img['url']
                    })
    
    return portraits, move_animations

def download_image(url, filename):
    """Télécharge une image."""
    filepath = os.path.join(PORTRAITS_DIR, filename)
    try:
        res = requests.get(url, stream=True, timeout=10)
        if res.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in res.iter_content(8192):
                    f.write(chunk)
            return True
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement de {filename}: {e}")
    return False

def main():
    print("🐺 Recherche et récupération des portraits FFCOTW\n")
    
    os.makedirs(PORTRAITS_DIR, exist_ok=True)
    
    # Récupérer toutes les images
    print("📥 Récupération des images du wiki DreamCancel...")
    all_images = get_all_cotw_images()
    print(f"✅ {len(all_images)} images trouvées au total\n")
    
    # Trier les images par personnage
    characters = {}
    for img in all_images:
        name = img['name']
        if 'CotW_' in name or name.startswith('CotW'):
            prefix = name.replace('CotW_', '').replace('CotW', '', 1)
            parts = prefix.split('_')
            if len(parts) > 1:
                char_name = parts[0]
                if char_name not in characters:
                    characters[char_name] = []
                characters[char_name].append(img)
    
    print(f"📊 Personnages identifiés: {len(characters)}\n")
    
    # Essayer de trouver des portraits/spash arts
    print("🔍 Recherche de portraits et splash arts...")
    portraits_found = {}
    
    for char_name, imgs in characters.items():
        # Chercher un portrait ou splash art
        for img in imgs:
            img_name = img['name']
            # Identifier s'il s'agit d'un portrait
            if any(pattern in img_name for pattern in ['.png', '.jpg', '.webp']):
                # Si l'image ne semble pas être une animation de coup
                if not any(kw in img_name for kw in ['214', '236', '28', '5C', '6A', 'CD', '2A', '2B', '2C', '2D', '3A', '3B', '3C', '6B', '6C', '4A', '4B', '4C', '4D', '7B', '7C']):
                    portraits_found[char_name] = img
    
    print(f"✨ {len(portraits_found)} portraits/splash arts potentiels trouvés!\n")
    
    # Afficher la liste des personnages avec images
    print("📋 Liste des personnages et types d'images:\n")
    for char_name in sorted(characters.keys()):
        imgs = characters[char_name]
        img_types = set()
        for img in imgs:
            name = img['name']
            if 'Portrait' in name or 'Splash' in name or 'TitleScreen' in name:
                img_types.add('Portraits/Splash')
            elif any(kw in name for kw in ['214', '236', '28', '5C', '6A', 'CD']):
                img_types.add('Moves/Spécial')
            else:
                img_types.add('Autre')
        print(f"  • {char_name:20s} : {len(imgs)} images - {', '.join(img_types)}")
    
    # Sauvegarder les données brutes
    with open('ffcow_raw_images.json', 'w', encoding='utf-8') as f:
        json.dump({'characters': dict(characters), 'portraits': portraits_found}, 
                  f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*70}")
    print(f"💾 Données sauvegardées dans: ffcow_raw_images.json")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()