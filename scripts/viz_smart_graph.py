import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import glob
import os
import re

# ==========================================
# 1. CONFIGURATION & THEMING
# ==========================================

# Define Palettes (Refined for "Dark Mode Engineering")
THEMES = {
    'dark': {
        'bg_color': '#0D1226',      # Deep Void
        'node_project': '#FE1295',  # Sugartown Pink (Hubs)
        'node_category': '#00695C', # Dark Emerald (Categories)
        'node_gem': '#880E4F',      # Deep Raspberry (Gems)
        'edge_color': (1, 1, 1, 0.15), # Subtle White transparency
        'text_color': '#FFFFFF',       # Force White
    },
    'light': {
        'bg_color': '#FFFFFF',
        'node_project': '#FE1295', 
        'node_category': '#2BD4AA', 
        'node_gem': '#C2185B',
        'edge_color': (0, 0, 0, 0.1),
        'text_color': '#000000'
    }
}

OUTPUT_DIR = 'output/visuals'

# ==========================================
# 2. DATA LOADING
# ==========================================
def get_latest_report():
    if not os.path.exists('output/reports'):
        print("❌ Directory 'output/reports' not found.")
        return None
    list_of_files = glob.glob('output/reports/gems_report_*.csv')
    if not list_of_files:
        print("❌ No CSV reports found.")
        return None
    return max(list_of_files, key=os.path.getctime)

def clean_svg(filename):
    """
    Post-processes the SVG to make it responsive.
    Removes hardcoded height/width so it scales with the container.
    """
    with open(filename, 'r') as f:
        content = f.read()
    
    # Regex to remove width="pt" and height="pt"
    content = re.sub(r'width="[^"]+"', '', content, count=1)
    content = re.sub(r'height="[^"]+"', '', content, count=1)
    
    with open(filename, 'w') as f:
        f.write(content)
    print(f"   ✨ Made SVG Responsive: {filename}")

# ==========================================
# 3. GRAPH BUILDER
# ==========================================
def build_graph(df):
    G = nx.Graph()
    print(f"🕸️  Building Network from {len(df)} Gems...")

    for index, row in df.iterrows():
        # 1. GEM NODE
        gem_id = row['id']
        title = str(row['title'])
        if len(title) > 20:
            title = title[:20] + "..."
            
        G.add_node(gem_id, label=title, type='gem', size=300)
        
        # 2. PROJECT NODE (Dynamic Lookup from CSV)
        raw_proj_id = row.get('project_id')
        proj_name = row.get('project_name')
        
        if pd.notna(raw_proj_id) and raw_proj_id:
            label = proj_name if pd.notna(proj_name) else raw_proj_id
            if isinstance(label, str) and len(label) > 10 and ' ' in label:
                label = label.replace(' ', '\n', 1)

            G.add_node(raw_proj_id, label=label, type='project', size=2500)
            G.add_edge(gem_id, raw_proj_id, weight=3)
            
        # 3. CATEGORY NODES
        cats = str(row.get('wp_categories', '')).split(',')
        for cat in cats:
            cat = cat.strip()
            if cat and cat.lower() != 'nan':
                G.add_node(cat, label=cat, type='category', size=1200)
                G.add_edge(gem_id, cat, weight=1)
    return G

# ==========================================
# 4. RENDERER (Multi-Theme)
# ==========================================
def draw_graph(G, theme_name='dark'):
    config = THEMES[theme_name]
    
    # 1. Setup Canvas
    # Slightly rectangular helps with wide labels
    plt.figure(figsize=(14, 10)) 
    ax = plt.gca()
    plt.gcf().set_facecolor(config['bg_color']) 
    ax.axis('off')

    # 2. Physics Layout
    pos = nx.spring_layout(G, k=0.8, iterations=60, seed=42)

    # --- FIX: MANUAL LIMITS ---
    # Find the exact coordinates of the nodes
    x_values, y_values = zip(*pos.values())
    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)

    # Add a 15% buffer to ensure labels don't get cut off
    x_margin = (x_max - x_min) * 0.15
    y_margin = (y_max - y_min) * 0.15
    
    ax.set_xlim(x_min - x_margin, x_max + x_margin)
    ax.set_ylim(y_min - y_margin, y_max + y_margin)
    # --------------------------

    # 3. Draw Edges
    nx.draw_networkx_edges(G, pos, edge_color=config['edge_color'], width=1)

    # 4. Draw Nodes & Labels
    node_types = [
        ('project', config['node_project'], 2500),
        ('category', config['node_category'], 1200),
        ('gem', config['node_gem'], 300)
    ]

    for n_type, n_color, n_size in node_types:
        nodelist = [n for n, d in G.nodes(data=True) if d.get('type') == n_type]
        if not nodelist: continue
        
        # Draw Nodes
        nx.draw_networkx_nodes(G, pos, 
                               nodelist=nodelist, 
                               node_color=n_color, 
                               node_size=n_size, 
                               linewidths=0)
        
        # Only label Projects and Categories
        if n_type in ['project', 'category']:
            labels = {n: d['label'] for n, d in G.nodes(data=True) if n in nodelist}
            
            nx.draw_networkx_labels(G, pos, labels, 
                                    font_size=9, 
                                    font_color=config['text_color'], 
                                    font_family='Monospace',
                                    font_weight='bold',
                                    verticalalignment='center')

    # 5. Save
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"{OUTPUT_DIR}/knowledge_graph_{theme_name}.svg"
    
    # bbox_inches='tight' + pad_inches=0 = Crop to exact content
    plt.savefig(filename, 
                format='svg', 
                bbox_inches='tight', 
                pad_inches=0, 
                facecolor=config['bg_color'])
    plt.close()
    
    print(f"✅ Generated {theme_name.upper()} Graph: {filename}")
    clean_svg(filename)

def main():
    csv_path = get_latest_report()
    if not csv_path: return
    
    df = pd.read_csv(csv_path)
    G = build_graph(df)
    
    draw_graph(G, 'dark')
    draw_graph(G, 'light')

if __name__ == "__main__":
    main()