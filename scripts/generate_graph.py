import networkx as nx
import matplotlib.pyplot as plt
import textwrap
from PIL import Image  # Requires: pip3 install Pillow
from content_store import all_gems

# --- CONFIGURATION ---
MAX_LABEL_LENGTH = 20  # Hard limit for characters before truncation
WRAP_WIDTH = 10        # Break lines after this many characters
MAX_IMAGE_WIDTH = 3000 # WordPress safety limit

# --- SUGARTOWN BRAND PALETTE ---
COLORS = {
    'pink': '#FE1295',    # Hero / Projects
    'green': '#2BD4AA',   # Categories
    'gold': '#FFB749',    # Accents
    'midnight': '#0D1226',# Deep Content / Gems
    'white': '#FFFFFF',
    'grey': '#F0F2F5'
}

def generate_knowledge_graph():
    # 1. Initialize Graph
    G = nx.Graph()
    node_sizes = {}
    node_colors = []

    print("🕸️  Building Sugartown Knowledge Graph...")

    # 2. Build Nodes & Count Frequencies
    frequency_map = {}
    node_types = {}

    for gem in all_gems:
        # --- TITLE CLEANING LOGIC ---
        full_title = gem['title']
        clean_title = full_title.replace('Project: ', '').replace('Market Scan: ', '').replace('Strategy: ', '').replace('Architecture Decision: ', '')
        
        if len(clean_title) > MAX_LABEL_LENGTH:
            clean_title = clean_title[:MAX_LABEL_LENGTH] + "..."
            
        wrapped_title = textwrap.fill(clean_title, width=WRAP_WIDTH)
        
        # Add Gem Node
        G.add_node(wrapped_title, type='gem', color=COLORS['midnight'])
        frequency_map[wrapped_title] = frequency_map.get(wrapped_title, 1)
        node_types[wrapped_title] = 'gem'

        # Extract Meta
        meta = gem.get('meta', {})
        category = meta.get('gem_category')
        project = meta.get('gem_related_project')

        # Add Category Node
        if category:
            clean_cat = category[:15] + ".." if len(category) > 15 else category
            wrapped_cat = textwrap.fill(clean_cat, width=WRAP_WIDTH)
            G.add_node(wrapped_cat, type='category', color=COLORS['green'])
            G.add_edge(wrapped_title, wrapped_cat)
            frequency_map[wrapped_cat] = frequency_map.get(wrapped_cat, 1) + 1
            node_types[wrapped_cat] = 'category'

        # Add Project Node
        if project:
            clean_proj = project[:15] + ".." if len(project) > 15 else project
            wrapped_proj = textwrap.fill(clean_proj, width=WRAP_WIDTH)
            G.add_node(wrapped_proj, type='project', color=COLORS['pink'])
            G.add_edge(wrapped_title, wrapped_proj)
            frequency_map[wrapped_proj] = frequency_map.get(wrapped_proj, 1) + 1
            node_types[wrapped_proj] = 'project'

    # 3. Calculate Dynamic Sizes
    for node in G.nodes():
        freq = frequency_map.get(node, 1)
        n_type = node_types.get(node, 'gem')
        
        if n_type == 'gem':
            size = 4500 
        elif n_type == 'category':
            size = 5500 + (freq * 500)
        elif n_type == 'project':
            size = 7000 + (freq * 500)
        else:
            size = 3000

        node_sizes[node] = size
        node_colors.append(nx.get_node_attributes(G, 'color')[node])

    # 4. Setup Layout
    print(f"   Nodes: {G.number_of_nodes()} | Edges: {G.number_of_edges()}")
    
    # --- LAYOUT TWEAKS ---
    # Changed seed from 42 to 24 to "shake" the box and fill gaps.
    # Increased iterations to 150 to let the physics settle more naturally.
    # Decreased 'k' slightly to pull the graph tighter together.
    pos = nx.spring_layout(G, k=1.0, iterations=150, seed=24)

    # 5. Draw the Graph
    # We render HUGE first (high quality), then downsize.
    plt.figure(figsize=(24, 20), facecolor=COLORS['white'])
    ax = plt.gca()
    ax.set_facecolor(COLORS['white'])

    nx.draw_networkx_edges(G, pos, width=2.0, alpha=0.4, edge_color='#BDC3C7')
    
    nx.draw_networkx_nodes(G, pos, 
                           node_size=[node_sizes[n] for n in G.nodes()], 
                           node_color=node_colors, 
                           alpha=1.0, 
                           linewidths=0)
    
    nx.draw_networkx_labels(G, pos, 
                            font_size=12, 
                            font_family='sans-serif', 
                            font_weight='bold', 
                            font_color=COLORS['white'])

    plt.axis('off')
    
    # 6. Save Initial High-Res Image
    output_file = "knowledge_graph.png"
    plt.savefig(output_file, format="PNG", dpi=300, bbox_inches='tight')
    print(f"✨ Graph Generated: {output_file}")

    # 7. Resize for Web (WordPress Safety)
    try:
        with Image.open(output_file) as img:
            if img.width > MAX_IMAGE_WIDTH:
                print(f"   📉 Resizing image (Width: {img.width}px -> {MAX_IMAGE_WIDTH}px)...")
                # Calculate new height to maintain aspect ratio
                aspect_ratio = img.height / img.width
                new_height = int(MAX_IMAGE_WIDTH * aspect_ratio)
                
                # Resize and Overwrite
                img_resized = img.resize((MAX_IMAGE_WIDTH, new_height), Image.Resampling.LANCZOS)
                img_resized.save(output_file)
                print(f"   ✅ Image optimized for Web: {MAX_IMAGE_WIDTH}x{new_height}")
    except Exception as e:
        print(f"   ⚠️ Warning: Image resizing failed. Do you have Pillow installed? Error: {e}")

if __name__ == "__main__":
    generate_knowledge_graph()
