import json
from bs4 import BeautifulSoup
import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

cards = soup.find_all('div', class_='product-card')
print(f"Found {len(cards)} cards.")

for card in cards:
    cat = card.get('data-category')
    onclick = card.get('onclick', '')
    # Extract ID from openPreviewModal('visual_1')
    try:
        card_id = onclick.split("'")[1]
    except IndexError:
        continue
    
    title_tag = card.find('h3')
    title = title_tag.text.strip() if title_tag else "Untitled"
    
    # Visual HTML
    visual_wrapper = card.find('div', class_='visual-wrapper')
    visual_html = visual_wrapper.decode_contents().strip() if visual_wrapper else ""
    
    # Metadata HTML
    back_face = card.find('div', class_='rotate-y-180')
    metadata_html = ""
    if back_face:
        # The inner div holds the metadata
        inner_w_full = back_face.find('div', class_='w-full')
        if inner_w_full:
            metadata_html = inner_w_full.decode_contents().strip()
    
    data = {
        "id": card_id,
        "title": title,
        "category": cat,
        "visual_html": visual_html,
        "metadata_html": metadata_html
    }
    
    out_path = f"src/designs/{card_id}.json"
    with open(out_path, 'w', encoding='utf-8') as out_f:
        json.dump(data, out_f, indent=4)
    
print("Extraction complete.")
