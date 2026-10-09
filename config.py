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

# URLs candidates pour la page système (essayées dans l'ordre)
SYSTEM_PAGE_CANDIDATES = [
    f"{GAME_PREFIX}/System",
    f"{GAME_PREFIX}/Controls",
    f"{GAME_PREFIX}/Movement",
]

# ============================================================================
# Fichiers
# ============================================================================

OUTPUT_CSV = "ffcow_frame_data_raw.csv"
COOKIE_FILE = "cookie.txt"
PAGES_HTML_DIR = Path("pages_html")
PORTRAITS_DIR = Path("portraits")

# ============================================================================
# Liste fallback des personnages (basée sur le wiki DreamCancel)
# ============================================================================

CHARACTERS_FALLBACK = [
    # Base Roster + DLC (Full list from DreamCancel Wiki)
    "Terry Bogard", "Rock Howard", "Billy Kane", "B.Jenet", "Gato", 
    "Hokutomaru", "Hotaru Futaba", "Kim Dong Hwan", "Kain R. Heinlein", 
    "Kevin Rian", "Marco Rodrigues", "Mr. Big", "Salvatore Ganacci", 
    "Vox Reaper", "Duck King", "Rick Strowd", "Preecha", "Laocorn Gaudeamus",
    # Additional Characters listed in navigation
    "Andy Bogard", "Joe Higashi", "Ken Masters", "Chun-Li", "Manjiro & Ken",
    "Kim Jae Hoon", "Nightmare Geese", "Kim Kaphwan", "Blue Mary",
    "Cristiano Ronaldo", "Wolfgang Krauser", "Mr. Karate", "Kenshiro",
    "Mai Shiranui"
]

# ============================================================================
# Mapping des colonnes
# ============================================================================

COLUMN_MAP = {
    'move_name': ['name', 'move', 'move name', 'technique', 'attack'],
    'damage': ['damage', 'dmg'],
    'startup': ['startup', 'start-up'],
    'active_frames': ['active', 'active frames'],
    'recovery': ['recovery'],
    'adv_on_block': ['on block', 'block adv'],
    'adv_on_hit': ['on hit', 'hit adv'],
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

LOG_LEVEL = logging.DEBUG