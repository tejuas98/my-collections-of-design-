import os
from bs4 import BeautifulSoup

cyber_html_path = '../CyberSecurity/ps1.html'
lab_html_path = 'index.html'

with open(cyber_html_path, 'r', encoding='utf-8') as f:
    cyber_soup = BeautifulSoup(f, 'html.parser')

styles = cyber_soup.find_all('style')

with open(lab_html_path, 'r', encoding='utf-8') as f:
    lab_content = f.read()

# Instead of injecting globally, we can just scope or append them.
# There is a </head> tag where we can append them.
head_end = lab_content.find("</head>")

styles_html = ""
for style in styles:
    # Wrap in a special class or just inject
    styles_html += str(style) + "\n"

new_lab_content = lab_content[:head_end] + "\n<!-- CYBERSECURITY STYLES -->\n" + styles_html + lab_content[head_end:]

with open(lab_html_path, 'w', encoding='utf-8') as f:
    f.write(new_lab_content)

print(f"Injected {len(styles)} style tags.")
