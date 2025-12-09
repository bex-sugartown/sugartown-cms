import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import ast

# --- CONFIGURATION (The "Sugartown Pink" Palette) ---
STYLE_CONFIG = {
    'bg_color': '#0D1226',        # Deep Void
    'bar_color': '#FE1295',       # Sugartown Pink
    'text_color': '#FFFFFF',      # White
    'accent_color': '#00E5FF',    # Electric Cyan (for edges/ticks)
    'font': 'Monospace',          # Tech aesthetic
    'output_dir': 'output/visuals',
    'output_filename': 'category_dist_latest.png'
}

def get_latest_report():
    """Finds the most recently generated Gems Report CSV."""
    list_of_files = glob.glob('output/reports/gems_report_*.csv')
    if not list_of_files:
        print("❌ No CSV reports found in output/reports/")
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    print(f"📂 Loading data from: {latest_file}")
    return latest_file

def clean_categories(df):
    """
    Parses the 'categories' column. 
    Handles cases where categories are stored as list-strings like "['Strategy', 'Ops']".
    """
    # If the CSV saved the list as a string, evaluate it back to a list
    # Otherwise, assume it's a comma-separated string or single value
    cleaned_cats = []
    
    for entry in df['categories']:
        try:
            # Try to parse string representation of list "['A', 'B']"
            items = ast.literal_eval(entry)
            if isinstance(items, list):
                cleaned_cats.extend(items)
            else:
                cleaned_cats.append(str(entry))
        except (ValueError, SyntaxError):
            # Fallback for plain strings
            cleaned_cats.append(str(entry))
            
    return pd.Series(cleaned_cats)

def generate_chart():
    # 1. Load Data
    csv_path = get_latest_report()
    if not csv_path:
        return

    df = pd.read_csv(csv_path)

    # 2. Process Data (Explode lists so a Gem counts for ALL its categories)
    all_categories = clean_categories(df)
    category_counts = all_categories.value_counts().sort_values(ascending=True)

    # 3. Setup Plot (Sugartown Theming)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Apply Sugartown Backgrounds
    fig.patch.set_facecolor(STYLE_CONFIG['bg_color'])
    ax.set_facecolor(STYLE_CONFIG['bg_color'])

    # 4. Draw Bars
    bars = ax.barh(
        category_counts.index, 
        category_counts.values, 
        color=STYLE_CONFIG['bar_color'],
        edgecolor=STYLE_CONFIG['accent_color'],
        linewidth=1,
        height=0.6
    )

    # 5. Typography & Labels
    ax.set_title("Gem Distribution by Category", 
                 fontsize=16, 
                 fontname=STYLE_CONFIG['font'], 
                 color=STYLE_CONFIG['text_color'], 
                 pad=20)
    
    ax.set_xlabel("Number of Gems", 
                  fontsize=10, 
                  fontname=STYLE_CONFIG['font'], 
                  color=STYLE_CONFIG['accent_color'])

    # 6. Clean Up Axes (Remove top/right spines)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(STYLE_CONFIG['accent_color'])
    ax.spines['left'].set_color(STYLE_CONFIG['accent_color'])
    
    ax.tick_params(axis='x', colors=STYLE_CONFIG['text_color'])
    ax.tick_params(axis='y', colors=STYLE_CONFIG['text_color'])

    # 7. Add Value Labels to ends of bars
    for bar in bars:
        width = bar.get_width()
        label_y = bar.get_y() + bar.get_height() / 2
        ax.text(width + 0.3, label_y, s=f'{int(width)}', 
                va='center', 
                color=STYLE_CONFIG['text_color'], 
                fontname=STYLE_CONFIG['font'])

    # 8. Save
    os.makedirs(STYLE_CONFIG['output_dir'], exist_ok=True)
    output_path = os.path.join(STYLE_CONFIG['output_dir'], STYLE_CONFIG['output_filename'])
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, facecolor=STYLE_CONFIG['bg_color'])
    print(f"✅ Visualization generated: {output_path}")

if __name__ == "__main__":
    generate_chart()