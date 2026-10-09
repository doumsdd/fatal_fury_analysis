#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scrape B.Jenet frame data specifically"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = 'https://dreamcancel.com/w/api.php'
r = requests.get(url, params={'action': 'parse', 'page': 'Fatal_Fury:_City_of_the_Wolves/B._Jenet', 'prop': 'text', 'format': 'json'})
html = r.json()['parse']['text']['*']
soup = BeautifulSoup(html, 'html.parser')

moves = []
for table in soup.find_all('table'):
    rows = table.find_all('tr')
    if len(rows) > 1:
        for row in rows[1:]:
            tds = row.find_all('td')
            if len(tds) >= 3:
                cells = [td.get_text(strip=True) for td in tds]
                move_name = cells[0] if cells else ''
                nums = re.findall(r'\d+', ' '.join(cells))
                moves.append({'name': move_name, 'nums': nums})

df_bjenet = pd.DataFrame(moves)
print(f"B.Jenet moves extracted: {len(df_bjenet)}")
print(df_bjenet.head())

# Load existing CSVs
raw = pd.read_csv('ffcow_frame_data_raw.csv')
clean = pd.read_csv('ffcow_frame_data_clean.csv')

# Clean B.Jenet data into proper columns
bj_cols = ['Character', 'name', 'damage', 'startup', 'active_frames', 'recovery', 'adv_on_hit']
bj_rows = []
for _, row in df_bjenet.iterrows():
    entry = {'Character': 'B.Jenet', 'name': str(row['name'])}
    raw_nums = row.get('nums', [])
    if isinstance(raw_nums, list):
        nums = raw_nums
    else:
        nums = [int(x) for x in re.findall(r'\d+', str(raw_nums))] if pd.notnull(raw_nums) else []
    if len(nums) > 0: entry['damage'] = str(nums[0])
    if len(nums) > 1: entry['startup'] = str(nums[1])
    if len(nums) > 2: entry['active_frames'] = str(nums[2])
    if len(nums) > 3: entry['recovery'] = str(nums[3])
    if len(nums) > 4: entry['adv_on_hit'] = str(nums[4])
    bj_rows.append(entry)

if bj_rows:
    df_new = pd.DataFrame(bj_rows)
    combined_raw = pd.concat([raw, df_new], ignore_index=True)
    combined_raw.to_csv('ffcow_frame_data_raw.csv', index=False, encoding='utf-8-sig')
    
    essential = [c for c in ['Character', 'name', 'damage', 'startup', 'active_frames', 'recovery'] if c in df_new.columns]
    combined_clean = pd.concat([clean, df_new[essential]], ignore_index=True)
    combined_clean.to_csv('ffcow_frame_data_clean.csv', index=False, encoding='utf-8-sig')
    print("CSVs updated successfully!")
else:
    print("No data to add.")