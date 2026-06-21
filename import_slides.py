import os
from bs4 import BeautifulSoup

cyber_html_path = '../CyberSecurity/ps1.html'
lab_html_path = 'index.html'

with open(cyber_html_path, 'r', encoding='utf-8') as f:
    cyber_soup = BeautifulSoup(f, 'html.parser')

slides = cyber_soup.find_all('div', class_=lambda c: c and 'slide' in c.split())

with open(lab_html_path, 'r', encoding='utf-8') as f:
    lab_content = f.read()

# Instead of using BeautifulSoup for writing (which can mess up formatting), 
# we'll inject the new cards as a string just before the closing </div> of #card-grid.

# Let's find the closing tag of <div id="card-grid" ...>
# Since #card-grid contains all the cards, we can find the end of it by looking for the section after it.
# In index.html, #card-grid is followed by:
# </div>
# </main>
# We can search for "\n</div>\n<!-- END MAIN -->" or similar.
# Let's just use a unique split point.

end_grid_marker = "</div>\n</main>"
if end_grid_marker not in lab_content:
    # try another marker
    end_grid_marker = "</div>\n<!-- Utility Bar -->" # Actually, wait. Let's look for </main>
    # We can use rfind to find the last </div> before </main>

main_idx = lab_content.find("</main>")
if main_idx == -1:
    print("Could not find </main>")
    exit(1)

insert_idx = lab_content.rfind("</div>", 0, main_idx)

new_cards_html = ""

for i, slide in enumerate(slides):
    slide_id = f"cyber_slide_{i+1}"
    slide_html = str(slide)
    
    # We need to wrap it so it scales properly, since slides are often fixed size or expect 100vw/100vh.
    # The slides in CyberSecurity are likely styled with Tailwind.
    
    card = f"""
        <div class="product-card p-6 flex flex-col justify-between research-card relative cursor-pointer hover:border-[var(--text-primary)] transition-all" data-category="Presentations" onclick="openPreviewModal('{slide_id}')">
            <div>
                <div class="mb-4">
                    <h3 class="font-serif font-bold text-2xl text-[var(--arsenal-title)] mb-1">CyberSecurity Slide {i+1}</h3>
                    <div class="font-mono text-[11px] font-bold tracking-widest text-[var(--arsenal-text)] uppercase">Presentations</div>
                </div>
                <!-- 3D FLIP CONTAINER -->
                <div class="group perspective-1000 w-full mb-2 cursor-pointer" onclick="flipCard('{slide_id}')" title="Click to flip or edit">
                    <div class="relative w-full transition-transform duration-700 preserve-3d grid" id="flip-inner-{slide_id}">
                        <!-- FRONT FACE: The Visual -->
                        <div class="col-start-1 row-start-1 backface-hidden w-full flex justify-center items-center bg-transparent p-6 rounded-lg bg-[var(--bg-primary)] border border-[var(--arsenal-border)] hover:border-[var(--arsenal-title)] transition-colors relative overflow-hidden" id="visual-front-{slide_id}">
                            <!-- Hint Icon -->
                            <div class="absolute top-2 right-2 bg-black/10 text-[var(--arsenal-title)] rounded-full w-6 h-6 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity z-50">
                                <svg fill="none" height="14" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="14" xmlns="http://www.w3.org/2000/svg"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.59-9.21l-3.23 3.23"></path></svg>
                            </div>
                            <!-- Normal Card Visual -->
                            <div class="visual-wrapper w-full flex justify-center items-center pointer-events-none">
                                <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden font-sans max-w-full mx-auto" style="width: 100%; aspect-ratio: 16/9; position: relative; overflow: hidden; transform: scale(0.8);">
                                    {slide_html}
                                </div>
                            </div>
                        </div>
                        <!-- BACK FACE: The Metadata -->
                        <div class="col-start-1 row-start-1 backface-hidden rotate-y-180 w-full flex flex-col justify-center items-start p-6 rounded-lg bg-[var(--bg-primary)] border border-[var(--arsenal-border)] overflow-y-auto z-20">
                            <div class="w-full">
                                <div class="mb-4">
                                    <h4 class="font-medium font-sans text-white text-sm mb-2">Why I saved this:</h4>
                                    <ul class="list-disc pl-5 font-sans text-sm text-[var(--arsenal-text)] space-y-1"><li>Presentation layout</li><li>Slide design from CyberSecurity</li></ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Utility Bar -->
            <div class="flex justify-end items-center gap-3 mt-6 pt-4 border-t border-[var(--arsenal-border)] relative z-20 bg-[var(--arsenal-card-bg)] utility-bar" onclick="event.stopPropagation()">
                <button class="bg-transparent border border-[var(--arsenal-border)] text-[var(--text-primary)] hover:bg-[var(--border-primary)] rounded-full p-2.5 transition-all duration-300 z-10 relative flex items-center justify-center overflow-hidden" id="copy-btn-{slide_id}" onclick="copyCode('{slide_id}', event)" title="Copy HTML Code" style="min-width: 36px; height: 36px;">
                    <div class="flex items-center justify-center transition-all duration-300" id="copy-icon-container-{slide_id}">
                        <svg fill="none" height="16" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="16"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                    </div>
                </button>
                <button class="download-btn bg-transparent border border-[var(--arsenal-border)] text-[var(--text-primary)] hover:bg-[var(--border-primary)] rounded-full p-2.5 transition-colors z-10 relative" onclick="downloadPNG('{slide_id}')" title="Download PNG">
                    <svg fill="none" height="16" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="16"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" x2="12" y1="15" y2="3"></line></svg>
                </button>
            </div>
        </div>
"""
    new_cards_html += card

new_lab_content = lab_content[:insert_idx] + new_cards_html + lab_content[insert_idx:]

with open(lab_html_path, 'w', encoding='utf-8') as f:
    f.write(new_lab_content)

print(f"Injected {len(slides)} slides into Visual Research Lab.")
