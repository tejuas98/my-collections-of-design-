import os
from bs4 import BeautifulSoup
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# We need to preserve exactly the layout from index.html.
# Using bs4 might mess with spacing, so let's use string manipulation to replace the contents of #card-grid
start_str = '<div class="grid grid-cols-1 lg:grid-cols-2 gap-10" id="card-grid">'
end_str = '</div>\n</main>'

start_idx = html.find(start_str)
end_idx = html.find(end_str, start_idx)

if start_idx != -1 and end_idx != -1:
    template_html = html[:start_idx + len(start_str)] + '\n<!-- INJECT_CARDS_HERE -->\n' + html[end_idx:]
    with open('src/template.html', 'w', encoding='utf-8') as f:
        f.write(template_html)
    print("Created src/template.html")
else:
    print("Could not find #card-grid")
