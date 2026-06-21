import json
import os
import subprocess

def add_design():
    print("=== Add a New Design ===")
    card_id = input("ID (e.g. terminal_design_2): ").strip()
    title = input("Title: ").strip()
    category = input("Category (e.g. UI Inspiration, Product Interfaces): ").strip()
    
    print("Paste the HTML for the Visual (press Ctrl+D on empty line to finish):")
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break
    visual_html = "\n".join(lines).strip()
    
    # We can provide empty metadata by default or ask for it
    metadata_html = """
    <div class="mb-4">
        <h4 class="font-medium font-sans text-[var(--text-primary)] text-sm mb-2">Why I saved this:</h4>
        <ul class="list-disc pl-5 font-sans text-sm text-[var(--arsenal-text)] space-y-1">
            <li>Reason 1</li>
            <li>Reason 2</li>
        </ul>
    </div>
    <div class="mb-4">
        <h4 class="font-medium font-sans text-[var(--text-primary)] text-sm mb-2">What I can learn:</h4>
        <ul class="list-disc pl-5 font-sans text-sm text-[var(--arsenal-text)] space-y-1">
            <li>Takeaway 1</li>
            <li>Takeaway 2</li>
        </ul>
    </div>
    """

    data = {
        "id": card_id,
        "title": title,
        "category": category,
        "visual_html": visual_html,
        "metadata_html": metadata_html.strip()
    }

    out_path = f"src/designs/{card_id}.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        
    print(f"\nSaved {out_path}")
    print("Rebuilding index.html...")
    subprocess.run(["python3", "build.py"])

if __name__ == "__main__":
    add_design()
