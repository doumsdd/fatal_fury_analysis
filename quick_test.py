#!/usr/bin/env python3
# Quick test: search for FFCOTW character icons
import requests

chars = ['Terry', 'Rock', 'Andy', 'Joe', 'Billy', 'Gato', 'Kevin']
base_url = "https://dreamcancel.com/w/api.php"

for char in chars:
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'allimages',
        'aiprefix': f'FF_COTW_{char}_Icon'
    }
    r = requests.get(base_url, params=params)
    data = r.json()
    imgs = data['query']['allimages'] if 'query' in data else []
    status = imgs[0]['name'] if imgs else "NOT FOUND"
    print(f"{char:15s} : {status}")