import pandas as pd
import math
import os
import glob
import html

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, 'output', 'reports')
VISUALS_DIR = os.path.join(BASE_DIR, 'output', 'visuals')
OUTPUT_FILE = os.path.join(VISUALS_DIR, 'knowledge_graph_latest.svg')

# Canvas Settings
WIDTH = 800
HEIGHT = 520
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

# Ring Radii
R_CATEGORY = 140  # Green nodes distance from center
R_GEM_OFFSET = 80 # How far Gems float from their Category

def get_latest_csv():
    list_of_files = glob.glob(os.path.join(REPORTS_DIR, '*.csv'))
    if not list_of_files: return None
    return max(list_of_files, key=os.path.getctime)

def split_label(text, max_chars=12):
    """Splits text into 2 lines for SVG tspans"""
    if len(text) <= max_chars: return [text, ""]
    words = text.split()
    mid = len(words) // 2
    return [" ".join(words[:mid]), " ".join(words[mid:])]

def generate_svg_content(df):
    svg_elements = []
    
    # 1. PROCESS DATA
    # Group Gems by their Primary Category
    cat_map = {} # { "Engineering": [gem_row, gem_row...] }
    
    for _, row in df.iterrows():
        # Get first category only for the visual grouping
        raw_cats = str(row['categories']).split(',')[0].strip()
        cat_name = raw_cats.replace('&amp;', '&') if raw_cats else "Uncategorized"
        
        if cat_name not in cat_map: cat_map[cat_name] = []
        cat_map[cat_name].append(row)

    categories = list(cat_map.keys())
    total_cats = len(categories)

    # 2. GENERATE NODES & EDGES
    nodes_svg = []
    edges_svg = []

    # Center Node (Sugartown)
    nodes_svg.append(f'''
    <g transform="translate({CENTER_X},{CENTER_Y})">
        <circle r="40" class="node node--pink"></circle>
        <text class="node-label white-label" text-anchor="middle">
            <tspan x="0" dy="-2">Sugartown</tspan>
            <tspan x="0" dy="13">v2</tspan>
        </text>
    </g>''')

    # Loop Categories
    for i, cat_name in enumerate(categories):
        # Calculate Category Position (Inner Ring)
        angle = (2 * math.pi * i) / total_cats
        cat_x = CENTER_X + (R_CATEGORY * math.cos(angle))
        cat_y = CENTER_Y + (R_CATEGORY * math.sin(angle))

        # Edge: Center -> Category
        edges_svg.append(f'<line class="edge" x1="{CENTER_X}" y1="{CENTER_Y}" x2="{cat_x}" y2="{cat_y}"></line>')

        # Category Node
        label_parts = split_label(cat_name)
        nodes_svg.append(f'''
        <g transform="translate({cat_x},{cat_y})">
            <circle r="24" class="node node--green"></circle>
            <text class="node-label" text-anchor="middle">
                <tspan x="0" dy="-2">{html.escape(label_parts[0])}</tspan>
                <tspan x="0" dy="13">{html.escape(label_parts[1])}</tspan>
            </text>
        </g>''')

        # Loop Gems in this Category
        gems = cat_map[cat_name]
        total_gems = len(gems)
        
        # Spread gems in a fan shape *outward* from the category
        # We use the same angle as the category, but add small spread
        gem_spread = 0.5 # Radians width of the fan
        
        for j, gem in enumerate(gems):
            # Calculate Gem Position
            # Base angle is the category's angle. 
            # If multiple gems, spread them around that angle.
            if total_gems == 1:
                gem_angle = angle
            else:
                gem_angle = (angle - gem_spread/2) + (j * (gem_spread / (total_gems-1)))

            gem_x = cat_x + (R_GEM_OFFSET * math.cos(gem_angle))
            gem_y = cat_y + (R_GEM_OFFSET * math.sin(gem_angle))

            # Edge: Category -> Gem
            edges_svg.append(f'<line class="edge" x1="{cat_x}" y1="{cat_y}" x2="{gem_x}" y2="{gem_y}"></line>')

            # Gem Node
            gem_title = gem['title']
            gem_parts = split_label(gem_title, 15)
            nodes_svg.append(f'''
            <g transform="translate({gem_x},{gem_y})">
                <circle r="18" class="node node--gem"></circle>
                <text class="gem-label" text-anchor="middle">
                    <tspan x="0" dy="-5">{html.escape(gem_parts[0])}</tspan>
                    <tspan x="0" dy="8">{html.escape(gem_parts[1])}</tspan>
                </text>
            </g>''')

    # 3. ASSEMBLE FINAL SVG
    return f'''<svg class="sugartown-graph" viewBox="0 0 {WIDTH} {HEIGHT}" aria-labelledby="title desc" role="img" xmlns="http://www.w3.org/2000/svg">
  <title id="title">Sugartown Gems Knowledge Graph</title>
  <style>
    /* Sugartown palette */
    .sugartown-pink {{ color: #FE1295; }}
    .sugartown-green {{ color: #2BD4AA; }}
    .sugartown-gold {{ color: #FFB749; }}
    .sugartown-midnight {{ color: #0D1226; }}

    svg.sugartown-graph {{
        width: 100%;
        max-height: 520px;
        display: block;
        background: #ffffff;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
    }}

    .node {{
        stroke-width: 2.5;
        stroke-linejoin: round;
        transform-origin: center center;
        transition: transform 120ms ease-out, filter 120ms ease-out;
        cursor: pointer;
    }}

    .node--pink {{ fill: #FE1295; stroke: rgba(254, 18, 149, 0.7); }}
    .node--green {{ fill: #2BD4AA; stroke: rgba(43, 212, 170, 0.7); }}
    .node--gold {{ fill: #FFB749; stroke: rgba(255, 183, 73, 0.7); }}
    .node--gem {{ fill: #FFB749; stroke: rgba(255, 183, 73, 0.7); }}

    .node-label {{ font-size: 11px; fill: #0D1226; pointer-events: none; }}
    .white-label {{ fill: #ffffff !important; }}
    .gem-label {{ font-size: 8px; fill: #0D1226; pointer-events: none; }}

    .edge {{
        fill: none;
        stroke-width: 2;
        stroke: rgba(13, 18, 38, 0.16);
        stroke-linecap: round;
        stroke-linejoin: round;
    }}

    .node:hover {{
        transform: scale(1.1);
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.12));
    }}
  </style>

  {"".join(edges_svg)}

  {"".join(nodes_svg)}

</svg>'''

def main():
    print("------------------------------------------------")
    print("🎨 VIZ BUILDER: SVG Knowledge Graph")
    print("------------------------------------------------")

    csv_file = get_latest_csv()
    if not csv_file:
        print("❌ No CSV found. Run export_gems.py first.")
        return

    print(f"   📂 Input: {os.path.basename(csv_file)}")
    
    # Read CSV
    df = pd.read_csv(csv_file)
    
    # Generate
    svg_code = generate_svg_content(df)
    
    # Save
    os.makedirs(VISUALS_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        f.write(svg_code)
        
    print(f"   ✨ Generated: output/visuals/{os.path.basename(OUTPUT_FILE)}")
    print("------------------------------------------------")

if __name__ == "__main__":
    main()
