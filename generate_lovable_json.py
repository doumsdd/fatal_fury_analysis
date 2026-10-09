#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère le JSON pour Lovable à partir des données scrapées de Fatal Fury COTW
"""

import json
import os
import csv

def main():
    data = []
    
    # Liste des personnages (peut être mise à jour dynamiquement si scrape_portraits.py est exécuté)
    characters_file = "portraits_mapping.json"
    portraits = {}
    if os.path.exists(characters_file):
        with open(characters_file, 'r', encoding='utf-8') as f:
            portraits = json.load(f)

    # Exemple de structure de données (à compléter par l'analyse frame data)
    sample_stats = [
        {"character": "Terry Bogard", "archetype": "Balanced", "avg_startup": 15},
        {"character": "Rock Howard", "archetype": "Rushdown", "avg_startup": 10},
        {"character": "Billy Kane", "archetype": "Zoner", "avg_startup": 20}
    ]

    output_data = []
    for char in sample_stats:
        entry = {
            "name": char["character"],
            "role": char["archetype"],
            "stats": {"speed": char["avg_startup"]},
            "image": None
        }
        
        # Associer le portrait si disponible
        if char["character"] in portraits and portraits[char["character"]]:
            entry["image"] = portraits[char["character"]] # On garde juste le nom du fichier
        
        output_data.append(entry)

    with open("lovable_data.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print("lovable_data.json généré avec succès !")

if __name__ == "__main__":
    main()