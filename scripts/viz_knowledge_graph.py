import pandas as pd
import networkx as nx
import os
import glob
import html
import math

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, 'output', 'reports')
VISUALS_DIR = os.path.join(BASE_DIR, 'output', 'visuals')
OUTPUT_FILE = os.path.join(VISUALS_DIR, 'knowledge_graph_smart.svg')

# Canvas Settings (Increased for spacing)
WIDTH = 1400 
HEIGHT = 1000
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

# 🎨 PALETTE: "Pink Stink" Tech Mode
COLORS = {
    'bg': '#0D1226',        # Sugartown Midnight
    'root': '#FE1295',      # Sugartown Pink
    'category': '#00F0FF',  # Electric Cyan
    'gem': '#FFD700',       # Hard Gold
    'edge': 'rgba(255, 255, 255, 0.08)', 
    'text': '#FFFFFF',
    'text_dim': '#8A9BA8'   # Muted Blue-Grey
}

def get_latest_csv():
    list_of_files = glob.glob(os.path.join(REPORTS_DIR, '*.csv'))
    if not list_of_files: return None
    return max(list_of_files, key=os.path.getctime)

def split_label(text, max_chars=20):
    """Wraps text more aggressively."""
    if not text: return ["", ""]
    if len(text) <= max_chars: return [text, ""]
    words = text.split()
    mid = len(words) // 2
    return [" ".join(words[:mid]), " ".join(words[mid:])]

def generate_svg(G, pos):
    # Note: Using triple quotes avoids most f-string conflicts
    svg = [f'''<svg class="sugartown-graph" viewBox="0 0 {WIDTH} {HEIGHT}" aria-labelledby="title" role="img" xmlns="http://www.w3.org/2000/svg">
    <title id="title">Sugartown Knowledge Graph</title>
    
    <rect width="100%" height="100%" fill="{COLORS["bg"]}"/>
    
    <style>
        .sugartown-graph {{ 
            font-family: 'Menlo', 'Monaco', 'Consolas', monospace; 
        }}
        
        .node-group {{ 
            cursor: pointer; 
            transform-origin: center; 
            transform-box: fill-box; 
            transition: transform 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }}
        
        .node-group:hover {{ transform: scale(1.15); }}
        
        .node-group:hover text {{ 
            fill: {COLORS["text"]} !important; 
            font-weight: 700;
            text-shadow: 0 0 5px {COLORS["bg"]};
        }}
        
        .edge {{ stroke: {COLORS["edge"]}; stroke-width: 1.2; }}
        
        text {{ 
            font-weight: 300; 
            letter-spacing: 0.04em; 
            pointer-events: none;
        }}
        
        .label-root {{ fill: {COLORS["text"]}; font-size: 16px; font-weight: 700; text-transform: uppercase; }}
        .label-cat {{ fill: {COLORS["category"]}; font-size: 13px; font-weight: 400; }}
        .label-gem {{ fill: {COLORS["text_dim"]}; font-size: 11px; }}
        
    </style>''']

    # 2. Draw Edges
    for u, v in G.edges():
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        svg.append(f'<line class="edge" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"></line>')

    # 3. Draw Nodes
    for node, data in G.nodes(data=True):
        x, y = pos[node]
        node_type = data.get('type', 'gem')
        
        # Styles
        if node_type == 'root':
            r = 45
            fill = COLORS['root']
            css_class = "label-root"
            label = ["SUGARTOWN", "OS"]
            stroke = "none"
        elif node_type == 'category':
            r = 10
            fill = COLORS['bg']
            # ✨ FIX: Use DOUBLE QUOTES for the dictionary key here
            stroke = f'stroke="{COLORS["category"]}" stroke-width="2"'
            css_class = "label-cat"
            label = split_label(str(node).replace('&amp;', '&'))
        else: # Gem
            r = 5
            fill = COLORS['gem']
            stroke = "none"
            css_class = "label-gem"
            label = split_label(str(node))

        # Node Group
        svg.append(f'''
        <g class="node-group" transform="translate({x},{y})">
            <circle r="{r + 10}" fill="transparent"></circle> 
            <circle r="{r}" fill="{fill}" {stroke}></circle>
            <text class="{css_class}" text-anchor="middle">
                <tspan x="0" dy="-{r + 10}">{html.escape(label[0])}</tspan>
                <tspan x="0" dy="14">{html.escape(label[1])}</tspan>
            </text>
        </g>''')

    svg.append('</svg>')
    return "\n".join(svg)

def main():
    print("------------------------------------------------")
    print("🕸️  VIZ ENGINE: Smart Graph (Syntax Fix)")
    print("------------------------------------------------")

    csv_file = get_latest_csv()
    if not csv_file: return

    print(f"   📂 Reading: {os.path.basename(csv_file)}")
    df = pd.read_csv(csv_file)
    G = nx.Graph()
    
    G.add_node("ROOT", type='root')

    for _, row in df.iterrows():
        title = row['title']
        cat = str(row['categories']).split(',')[0].strip()
        if not cat or cat == 'nan': cat = "Uncategorized"

        G.add_node(cat, type='category')
        G.add_node(title, type='gem')
        G.add_edge("ROOT", cat)
        G.add_edge(cat, title)

    print(f"   🧮 Simulating Physics ({G.number_of_nodes()} nodes)...")

    # PHYSICS SETTINGS
    pos = nx.spring_layout(G, k=1.2, iterations=200, scale=450, center=[CENTER_X, CENTER_Y])

    svg_content = generate_svg(G, pos)

    os.makedirs(VISUALS_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        f.write(svg_content)
        
    print(f"   ✨ Generated: output/visuals/{os.path.basename(OUTPUT_FILE)}")
    print("------------------------------------------------")

if __name__ == "__main__":
    main()
