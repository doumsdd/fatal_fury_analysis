import json

with open('lovable_data.json', 'r') as f:
    data = json.load(f)

print(f"Total entries in lovable_data.json: {len(data)}\n")
for d in data:
    print(f"{d['id']:2d}. {d['name']} ({d.get('image', 'N/A')})")
