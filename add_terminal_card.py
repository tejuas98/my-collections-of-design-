import re
import os

cyber_html_path = '../CyberSecurity/ps1.html'
lab_html_path = 'index.html'

# 1. Read ps1.html and extract the terminal snippet (lines ~416 to ~452)
with open(cyber_html_path, 'r', encoding='utf-8') as f:
    ps1_content = f.read()

# We can find it using string matching or regex
# Let's extract the terminal block
start_str = '<div class="terminal"'
end_str = '<!-- Bottom: Project Title & Pipeline -->'

start_idx = ps1_content.find(start_str)
end_idx = ps1_content.find(end_str)

if start_idx == -1 or end_idx == -1:
    print("Could not find terminal block")
    exit(1)

terminal_html = ps1_content[start_idx:end_idx].strip()
# Let's wrap it in a flex container so it doesn't try to inherit the 40% width from its parent,
# or we can remove the width: 40% if it has one. The terminal itself has width: 100%.
terminal_html = f'<div style="width: 100%; max-width: 600px; font-family: var(--font-main);">{terminal_html}</div>'

# 2. Extract CSS styles related to terminal just in case
styles = """
<style>
    /* Terminals */
    .terminal {
        background-color: #0a0a10;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 6px;
        overflow: hidden;
        font-family: var(--font-code);
        font-size: 10px;
    }
    .term-header {
        background-color: #1a1a24;
        padding: 4px 8px;
        display: flex;
        align-items: center;
        gap: 6px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .term-dot { width: 8px; height: 8px; border-radius: 50%; }
    .term-title { color: #94A3B8; font-family: var(--font-main); font-size: 10px; margin-left: 8px; font-weight: 600;}
    .term-body { padding: 12px; color: #E2E8F0; line-height: 1.5; }
</style>
"""

# 3. Read index.html and update
with open(lab_html_path, 'r', encoding='utf-8') as f:
    lab_content = f.read()

# Remove dark-theme
lab_content = lab_content.replace('class="font-sans antialiased min-h-screen pb-24 dark-theme"', 'class="font-sans antialiased min-h-screen pb-24 light-theme"')

# Inject styles in <head>
head_end = lab_content.find("</head>")
lab_content = lab_content[:head_end] + styles + lab_content[head_end:]

# Create the new card
slide_id = "terminal_design_1"
card = f"""
        <div class="product-card p-6 flex flex-col justify-between research-card relative cursor-pointer hover:border-[var(--text-primary)] transition-all" data-category="Product Interfaces" onclick="openPreviewModal('{slide_id}')">
            <div>
                <div class="mb-4">
                    <h3 class="font-serif font-bold text-2xl text-[var(--arsenal-title)] mb-1">Terminal Design</h3>
                    <div class="font-mono text-[11px] font-bold tracking-widest text-[var(--arsenal-text)] uppercase">Product Interfaces</div>
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
                                <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden font-sans max-w-full mx-auto" style="width: 100%; aspect-ratio: 16/9; position: relative; overflow: hidden; transform: scale(0.8); display: flex; justify-content: center; align-items: center; padding: 20px;">
                                    {terminal_html}
                                </div>
                            </div>
                        </div>
                        <!-- BACK FACE: The Metadata -->
                        <div class="col-start-1 row-start-1 backface-hidden rotate-y-180 w-full flex flex-col justify-center items-start p-6 rounded-lg bg-[var(--bg-primary)] border border-[var(--arsenal-border)] overflow-y-auto z-20">
                            <div class="w-full">
                                <div class="mb-4">
                                    <h4 class="font-medium font-sans text-[var(--text-primary)] text-sm mb-2">Why I saved this:</h4>
                                    <ul class="list-disc pl-5 font-sans text-sm text-[var(--arsenal-text)] space-y-1">
                                        <li>Keyword chip design</li>
                                        <li>Clear conversational structure</li>
                                        <li>Subtle border styling</li>
                                    </ul>
                                </div>
                                <div class="mb-4">
                                    <h4 class="font-medium font-sans text-[var(--text-primary)] text-sm mb-2">What I can learn:</h4>
                                    <ul class="list-disc pl-5 font-sans text-sm text-[var(--arsenal-text)] space-y-1">
                                        <li>Structuring LLM outputs visually</li>
                                        <li>Tag system UI patterns</li>
                                    </ul>
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

# Insert the new card
main_idx = lab_content.find("</main>")
insert_idx = lab_content.rfind("</div>", 0, main_idx)
new_lab_content = lab_content[:insert_idx] + card + lab_content[insert_idx:]

with open(lab_html_path, 'w', encoding='utf-8') as f:
    f.write(new_lab_content)

print("Injected Terminal card and removed dark theme.")
