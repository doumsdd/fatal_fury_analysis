#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fatal Fury: City of the Wolves - Frame Data Scraper (HTML)"""

import re, json, time, pandas as pd, requests, os
from bs4 import BeautifulSoup
from pathlib import Path
from config import API_ENDPOINT, CHARACTERS_LIST, PAGES_HTML_DIR, OUTPUT_CSV_RAW, OUTPUT_CSV_CLEAN, REQUEST_DELAY

def get_character_html(character_name):
    # Normaliser le nom de personnage pour l'API wiki (. -> _)
    slug = character_name.replace(' ', '_').replace('.', '_')
    page_title = f"Fatal_Fury:_City_of_the_Wolves/{slug}"
    try:
        params = {'action': 'parse', 'page': page_title, 'prop': 'text', 'format': 'json'}
        response = requests.get(API_ENDPOINT, params=params, timeout=30)
        data = response.json()
        # Structure: {"parse": {"text": {"*": "HTML"}}}
        if 'parse' in data and 'text' in data['parse']:
            return data['parse']['text']['*']
    except Exception as e:
        print(f"  Error for {character_name}: {e}")
    return None

def extract_table_data(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    moves = []
    
    # Chercher tous les tableaux avec class "wikitable" ou contenant des données de frames
    tables = soup.find_all('table', class_=re.compile(r'wikitable|frame'))
    
    for table in tables:
        headers = []
        rows = table.find_all('tr')
        
        for i, row in enumerate(rows):
            # Headers
            if i == 0:
                ths = row.find_all(['th', 'header'])
                headers = [th.get_text(strip=True).lower() for th in ths]
                continue
            
            tds = row.find_all('td')
            if len(tds) >= 3:
                move_data = {}
                
                # Extraire les valeurs selon l'ordre des headers
                text_cells = [td.get_text(strip=True) for td in tds]
                
                # Chercher patterns spécifiques
                move_name = ''
                damage = ''
                startup = ''
                active = ''
                recovery = ''
                hit_adv = ''
                block_adv = ''
                
                # Heuristique pour extraire les données
                for j, cell in enumerate(text_cells):
                    # Le nom du coup est généralement dans la première colonne
                    if j == 0:
                        move_name = cell
                    
                    # Chercher des patterns numériques
                    nums = re.findall(r'\d+', cell)
                    if nums:
                        if not damage and j < 2:
                            damage = nums[0]
                        elif not startup:
                            startup = nums[0]
                        elif not active:
                            active = nums[0]
                        elif not recovery:
                            recovery = nums[0]
                        elif not hit_adv:
                            hit_adv = nums[0]
                
                if move_name or damage or startup:
                    moves.append({
                        'Character': '',
                        'name': move_name,
                        'damage': damage,
                        'startup': startup,
                        'active_frames': active,
                        'recovery': recovery,
                        'adv_on_hit': hit_adv
                    })
    
    return moves

def main():
    print("=" * 70)
    print("FATAL FURY COTW - FRAME DATA SCRAPER")
    print("=" * 70)
    print(f"\nCharacters to scrape: {len(CHARACTERS_LIST)}\n")
    os.makedirs(PAGES_HTML_DIR, exist_ok=True)
    all_moves = []
    
    for i, char in enumerate(CHARACTERS_LIST, 1):
        print(f"[{i}/{len(CHARACTERS_LIST)}] Scraping {char}...")
        html = get_character_html(char)
        if not html:
            print(f"  Skipped: no HTML\n")
            continue
        
        slug = char.replace(' ', '_')
        with open(PAGES_HTML_DIR / f"{slug}.html", 'w', encoding='utf-8') as f:
            f.write(html)
        
        moves = extract_table_data(html)
        if moves:
            for m in moves:
                m['Character'] = char
            all_moves.extend(moves)
            print(f"  OK: {len(moves)} moves extracted\n")
        else:
            print(f"  No frame data found\n")
        if i < len(CHARACTERS_LIST):
            time.sleep(REQUEST_DELAY)
    
    if all_moves:
        df = pd.DataFrame(all_moves)
        df = df.drop_duplicates().sort_values(by=['Character', 'name']).reset_index(drop=True)
        df.to_csv(OUTPUT_CSV_RAW, index=False, encoding='utf-8-sig')
        essential = [c for c in ['Character', 'name', 'damage', 'startup', 'active_frames', 'recovery'] if c in df.columns]
        df[essential].to_csv(OUTPUT_CSV_CLEAN, index=False, encoding='utf-8-sig')
        print("\n" + "=" * 70)
        print("SCRAPING COMPLETE!")
        print(f"  Characters processed: {len(set(df['Character']))}")
        print(f"  Total moves scraped: {len(df)}")
        print(f"  Files generated:")
        print(f"    - {OUTPUT_CSV_RAW}")
        print(f"    - {OUTPUT_CSV_CLEAN}")
        print("=" * 70)
    else:
        print("\nNo data found!")

if __name__ == "__main__":
    main()