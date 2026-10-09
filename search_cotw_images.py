#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recherche exhaustive des portraits et splash arts Fatal Fury COTW
"""

import requests
import json
from config import API_ENDPOINT

def fetch_images_by_prefix(prefix, limit=500):
    """Récupère les images avec un préfixe donné."""
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'allimages',
        'aiprefix': prefix,
        'ailimit': limit
    }
    
    response = requests.get(API_ENDPOINT, params=params, timeout=15)
    return response.json()

def main():
    print("🔍 Recherche approfondie des portraits Fatal Fury COTW\n")
    
    # Rechercher TOUTES les images contenant "CotW" ou préfixe CotW_
    print("📥 Récupération de TOUS les fichiers d'images FFCOTW...")
    
    all_imgs = []
    
    # Essayer plusieurs prefixes
    search_prefixes = ['CotW_', 'CotW']
    
    for prefix in search_prefixes:
        data = fetch_images_by_prefix(prefix, 1000)
        imgs = data.get('query', {}).get('allimages', [])
        print(f"  → Préfixe '{prefix}': {len(imgs)} images")
        all_imgs.extend(imgs)
    
    # Dédupliquer
    unique_names = set()
    unique_imgs = []
    for img in all_imgs:
        if img['name'] not in unique_names:
            unique_names.add(img['name'])
            unique_imgs.append(img)
    
    print(f"\n✅ Total unique : {len(unique_imgs)} images\n")
    
    # Analyser la distribution par personnage
    characters = {}
    for img in unique_imgs:
        name = img['name']
        
        # Extraire le nom du personnage
        # Format attendu: CotW_[CharacterName]_[MoveName].png
        parts = name.replace('CotW_', '').replace('CotW', '', 1).split('_')
        
        if len(parts) > 0:
            char_name = parts[0]
            
            # Filtrer les noms invalides (ceux qui sont des numéros de coups)
            if char_name and not any(kw in char_name for kw in ['214', '236', '2A', '2B', '2C', '2D', '28', '3A', '3B', '3C', '4A', '4B', '4C', '4D', '5C', '6A', '6B', '6C', 'CD']):
                if char_name not in characters:
                    characters[char_name] = []
                characters[char_name].append(img)
    
    print("📊 Personnages identifiés :")
    for char in sorted(characters.keys()):
        count = len(characters[char])
        # Trouver le type d'image dominant
        types = {'moves': 0, 'other': 0}
        for img in characters[char]:
            n = img['name']
            if any(kw in n for kw in ['214', '236', '2A', '2B', '2C', '2D', '28', '3A', '3B', '3C', 
                                       '4A', '4B', '4C', '4D', '5C', '6A', '6B', '6C', '7B', '7C', 'CD']):
                types['moves'] += 1
            else:
                types['other'] += 1
        
        type_str = f"{types['moves']} moves" if types['moves'] > types['other'] else f"{types['other']} static"
        print(f"  • {char:20s}: {count:3d} images ({type_str})")
    
    print("\n" + "="*70)
    print("🎨 RECHERCHE DE PORTRAITS / SPLASH ARTS")
    print("="*70 + "\n")
    
    # Chercher spécifiquement des images statiques (non-animations)
    portrait_candidates = {}
    
    for char, imgs in characters.items():
        for img in imgs:
            name = img['name']
            
            # Exclure les animations de coups (numéros de commandes)
            is_move = any(kw in name for kw in [
                '214', '236', '2A', '2B', '2C', '2D', '28', '3A', '3B', '3C',
                '4A', '4B', '4C', '4D', '5C', '6A', '6B', '6C', '7B', '7C', 'CD',
                '~B', '~C', 'detonate', 'hitbox', 'Rev'
            ])
            
            # Si ce n'est pas une animation, c'est potentiellement un portrait/splash
            if not is_move:
                if char not in portrait_candidates:
                    portrait_candidates[char] = []
                portrait_candidates[char].append(img)
    
    print(f"✨ {len(portrait_candidates)} personnages ont des images statiques:\n")
    
    for char in sorted(portrait_candidates.keys())[:20]:  # Limiter l'affichage
        imgs = portrait_candidates[char]
        print(f"  • {char}")
        for img in imgs[:3]:  # Afficher les 3 premières
            print(f"    - {img['name']}")
        if len(imgs) > 3:
            print(f"    ... et {len(imgs)-3} autres")
        print()
    
    # Sauvegarder toutes les données
    output_data = {
        'total_images': len(unique_imgs),
        'characters': {k: len(v) for k, v in characters.items()},
        'portrait_candidates': {k: [{'filename': i['name'], 'url': i['url']} for i in v] 
                                for k, v in portrait_candidates.items()}
    }
    
    with open('ffcow_full_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*70}")
    print("💾 Analyse complète sauvegardée dans: ffcow_full_analysis.json")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()