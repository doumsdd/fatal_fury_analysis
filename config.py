#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration centralisée pour le scraper Fatal Fury: City of the Wolves.
"""

import logging
from pathlib import Path

# ============================================================================
# URLs et endpoints
# ============================================================================

WIKI_BASE_URL = "https://dreamcancel.com"
GAME_PREFIX = "Fatal_Fury:_City_of_the_Wolves"
API_ENDPOINT = f"{WIKI_BASE_URL}/w/api.php"

# ============================================================================
# Fichiers
# ============================================================================

OUTPUT_CSV_RAW = "ffcow_frame_data_raw.csv"
OUTPUT_CSV_CLEAN = "ffcow_frame_data_clean.csv"
PAGES_HTML_DIR = Path("pages_html")

# ============================================================================
# Liste des personnages (basée sur le wiki DreamCancel)
# ============================================================================

CHARACTERS_LIST = [
    "Terry Bogard", "Rock Howard", "Andy Bogard", "Joe Higashi", "Billy Kane",
    "B.Jenet", "Gato", "Hokutomaru", "Hotaru Futaba", "Kim Dong Hwan",
    "Kain R. Heinlein", "Kevin Rian", "Marco Rodrigues", "Mr. Big",
    "Salvatore Ganacci", "Vox Reaper", "Duck King", "Rick Strowd", "Preecha",
    "Ken Masters", "Chun-Li", "Kim Jae Hoon", "Nightmare Geese",
    "Kim Kaphwan", "Blue Mary", "Cristiano Ronaldo", "Wolfgang Krauser",
    "Mr. Karate", "Kenshiro", "Mai Shiranui", "Tizoc"
]

# ============================================================================
# Mapping des colonnes (variantes possibles dans les tables wiki)
# ============================================================================

COLUMN_MAP = {
    'move_name': ['name', 'move', 'move name', 'technique', 'attack'],
    'input': ['input', 'command', 'notation', 'motion'],
    'damage': ['damage', 'dmg', 'power'],
    'startup': ['startup', 'start-up', 'su'],
    'active_frames': ['active', 'active frames', 'active_frames'],
    'recovery': ['recovery', 'rec'],
    'adv_on_block': ['on block', 'block adv', 'guard adv', 'block advantage'],
    'adv_on_hit': ['on hit', 'hit adv', 'hit advantage', 'hit advantage']
}

# ============================================================================
# Configuration HTTP
# ============================================================================

HEADERS = {
    'User-Agent': 'FFCOV-FrameData-Scraper/1.0',
    'Accept': 'application/json',
}

REQUEST_TIMEOUT = 30
REQUEST_DELAY = 1.0
MAX_RETRIES = 3

LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_FILE = 'scraper.log'