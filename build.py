import os
import json
import glob

def build():
    # Load template
    with open('src/template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    # Find all design JSON files
    design_files = glob.glob('src/designs/*.json')
    
    # Sort files by numerical ID (if visual_X format) or just alphabetically
    # To maintain some order, let's try to extract numbers
    def sort_key(f):
        basename = os.path.basename(f)
        name = basename.replace('.json', '')
        if name.startswith('visual_'):
            try:
                return int(name.split('_')[1])
            except ValueError:
                return 9999
        return 9999
        
    design_files.sort(key=sort_key)

    cards_html = []
    catalog = {}

    for filepath in design_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            design = json.load(f)
            
        card_id = design['id']
        cat = design['category']
        title = design['title']
        visual_html = design.get('visual_html', '')
        metadata_html = design.get('metadata_html', '')

        catalog[card_id] = {
            "id": card_id,
            "title": title,
            "cat": cat
        }

        # Build card HTML
        card_html = f"""
        <div class="product-card p-6 flex flex-col justify-between research-card relative cursor-pointer hover:border-[var(--text-primary)] transition-all" data-category="{cat}" onclick="openPreviewModal('{card_id}')">
            <div>
                <div class="mb-4">
                    <h3 class="font-serif font-bold text-2xl text-[var(--arsenal-title)] mb-1">{title}</h3>
                    <div class="font-mono text-[11px] font-bold tracking-widest text-[var(--arsenal-text)] uppercase">{cat}</div>
                </div>
                <!-- 3D FLIP CONTAINER -->
                <div class="group perspective-1000 w-full mb-2 cursor-pointer" onclick="flipCard('{card_id}')" title="Click to flip or edit">
                    <div class="relative w-full transition-transform duration-700 preserve-3d grid" id="flip-inner-{card_id}">
                        <!-- FRONT FACE: The Visual -->
                        <div class="col-start-1 row-start-1 backface-hidden w-full flex justify-center items-center bg-transparent p-6 rounded-lg bg-[var(--bg-primary)] border border-[var(--arsenal-border)] hover:border-[var(--arsenal-title)] transition-colors relative overflow-hidden" id="visual-front-{card_id}">
                            <!-- Hint Icon -->
                            <div class="absolute top-2 right-2 bg-black/10 text-[var(--arsenal-title)] rounded-full w-6 h-6 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity z-50">
                                <svg fill="none" height="14" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="14" xmlns="http://www.w3.org/2000/svg"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.59-9.21l-3.23 3.23"></path></svg>
                            </div>
                            <!-- Normal Card Visual -->
                            <div class="visual-wrapper w-full flex justify-center items-center pointer-events-none">
                                {visual_html}
                            </div>
                        </div>
                        <!-- BACK FACE: The Metadata -->
                        <div class="col-start-1 row-start-1 backface-hidden rotate-y-180 w-full flex flex-col justify-center items-start p-6 rounded-lg bg-[var(--bg-primary)] border border-[var(--arsenal-border)] overflow-y-auto z-20">
                            <div class="w-full">
                                {metadata_html}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Utility Bar -->
            <div class="flex justify-end items-center gap-3 mt-6 pt-4 border-t border-[var(--arsenal-border)] relative z-20 bg-[var(--arsenal-card-bg)] utility-bar" onclick="event.stopPropagation()">
                <button class="bg-transparent border border-[var(--arsenal-border)] text-[var(--text-primary)] hover:bg-[var(--border-primary)] rounded-full p-2.5 transition-all duration-300 z-10 relative flex items-center justify-center overflow-hidden" id="copy-btn-{card_id}" onclick="copyCode('{card_id}', event)" title="Copy HTML Code" style="min-width: 36px; height: 36px;">
                    <div class="flex items-center justify-center transition-all duration-300" id="copy-icon-container-{card_id}">
                        <svg fill="none" height="16" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="16"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                    </div>
                </button>
                <button class="download-btn bg-transparent border border-[var(--arsenal-border)] text-[var(--text-primary)] hover:bg-[var(--border-primary)] rounded-full p-2.5 transition-colors z-10 relative" onclick="downloadPNG('{card_id}')" title="Download PNG">
                    <svg fill="none" height="16" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="16"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" x2="12" y1="15" y2="3"></line></svg>
                </button>
            </div>
        </div>
"""
        cards_html.append(card_html)

    # Join cards into the grid
    grid_content = '\n'.join(cards_html)
    
    # Replace markers
    output_html = template.replace('<!-- INJECT_CARDS_HERE -->', grid_content)
    output_html = output_html.replace('/* INJECT_CATALOG_HERE */', json.dumps(catalog))

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(output_html)

    print(f"Successfully built index.html with {len(design_files)} designs.")

if __name__ == "__main__":
    build()
