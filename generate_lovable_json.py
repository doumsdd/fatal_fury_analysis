#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère le JSON Lovable pour Fatal Fury COTW avec les images disponibles sur le wiki
"""

import json
import os
from config import PORTRAITS_DIR

def load_analysis_data():
    """Charge les données d'analyse des images."""
    if os.path.exists('ffcow_full_analysis.json'):
        with open('ffcow_full_analysis.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def extract_character_names(data):
    """Extrait la liste des personnages depuis les données analysées."""
    characters = []
    
    # Les personnages principaux identifiés
    main_characters = [
        "Terry Bogard", "Rock Howard", "Andy Bogard", "Joe Higashi", 
        "Billy Kane", "B.Jenet", "Gato", "Kevin Rian", "Kain R. Heinlein",
        "Marco Rodrigues", "Salvatore Ganacci", "Vox Reaper",
        "Duck King", "Rick Strowd", "Preecha", "Laocorn Gaudeamus"
    ]
    
    # DLC Characters (confirmed releases)
    dlc_characters = [
        "Kim Jae Hoon", "Nightmare Geese", "Blue Mary", 
        "Wolfgang Krauser", "Mr. Karate", "Kenshiro",
        "Kim Kaphwan", "Cristiano Ronaldo"
    ]
    
    all_characters = main_characters + dlc_characters
    
    # Filtrer ceux qui ont des images
    if data and 'characters' in data:
        visible_chars = [c for c in all_characters if c in data['characters'] or 
                        any(c.lower() in k.lower() for k in data['characters'].keys())]
        
        if visible_chars:
            return visible_chars
    
    return all_characters

def select_placeholder_image(char_name):
    """Sélectionne une image placeholder selon le personnage."""
    # Essayer de trouver une image correspondante dans l'analyse
    image_mapping = {
        "Terry Bogard": "Terry",
        "Rock Howard": "Rock",
        "Andy Bogard": "Andy",
        "Joe Higashi": "Joe",
        "Billy Kane": "Billy",
        "Kevin Rian": "Kevin",
        "Marco Rodrigues": "Marco",
        "Salvatore Ganacci": "Salvatore",
        "Kain R. Heinlein": "Kain",
        "Vox Reaper": "Vox"
    }
    
    simple_name = image_mapping.get(char_name, char_name.split()[0])
    
    # Vérifier si des images existent pour ce personnage
    if os.path.exists(PORTRAITS_DIR):
        for filename in os.listdir(PORTRAITS_DIR):
            if simple_name.lower() in filename.lower():
                return filename
    
    return None

def generate_lovable_json():
    """Génère le fichier JSON final pour Lovable."""
    
    # Charger les données d'analyse
    analysis_data = load_analysis_data()
    
    # Liste des personnages à inclure
    characters = extract_character_names(analysis_data)
    
    print(f"🐺 Génération du JSON Lovable pour FFCOTW")
    print(f"   Personnages inclus : {len(characters)}\n")
    
    output_data = []
    
    for i, char_name in enumerate(sorted(characters), 1):
        # Sélectionner une image si disponible
        image_file = select_placeholder_image(char_name)
        
        entry = {
            "id": i,
            "name": char_name,
            "image": image_file,
            "stats": {
                "role": "Fighter",
                "faction": "Fatal Fury Universe",
                "game": "Fatal Fury: City of the Wolves"
            },
            "availability": "Released" if i <= 17 else "DLC"
        }
        
        output_data.append(entry)
        
        status = "✅" if image_file else "⚠️"
        print(f"   [{i}/{len(characters)}] {status} {char_name}" + (f" ({image_file})" if image_file else ""))
    
    # Sauvegarder le JSON
    with open("lovable_data.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*70}")
    print(f"✨ lovable_data.json généré avec succès !")
    print(f"   Total personnages : {len(output_data)}")
    print(f"   Avec images : {sum(1 for e in output_data if e['image'])}")
    print(f"   Sans images : {sum(1 for e in output_data if not e['image'])}")
    print(f"   Fichier sauvegardé : lovable_data.json")
    print(f"{'='*70}\n")
    
    return output_data

if __name__ == "__main__":
    generate_lovable_json()