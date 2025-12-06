import sys
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, 'output', 'reports')
VISUALS_DIR = os.path.join(BASE_DIR, 'output', 'visuals')
OUTPUT_FILE = os.path.join(VISUALS_DIR, 'category_dist_latest.png')

def get_latest_csv():
    list_of_files = glob.glob(os.path.join(REPORTS_DIR, '*.csv'))
    if not list_of_files: return None
    return max(list_of_files, key=os.path.getctime)

def main():
    print("------------------------------------------------")
    print("📊 VIZ ENGINE: Category Distribution")
    print("------------------------------------------------")

    # 1. Load Data
    latest_csv = get_latest_csv()
    if not latest_csv: return
    print(f"   📂 Source: {os.path.basename(latest_csv)}")
    
    df = pd.read_csv(latest_csv)

    # 2. Process Categories
    all_cats = []
    for cats in df['categories'].dropna():
        # Split "Engineering, Ways of Working" -> ["Engineering", "Ways of Working"]
        # Also clean HTML entities if present (e.g. &amp;)
        clean_cats = [c.strip().replace('&amp;', '&') for c in cats.split(',')]
        all_cats.extend(clean_cats)

    # Count frequencies
    counts = Counter(all_cats)
    
    # 3. Plot
    plt.figure(figsize=(10, 6))
    
    # Sort for aesthetics
    labels, values = zip(*sorted(counts.items(), key=lambda x: x[1], reverse=True))
    
    bars = plt.barh(labels, values, color='#ff007f') # Sugartown Pink
    plt.xlabel('Number of Gems')
    plt.title('Content Distribution by Category')
    plt.gca().invert_yaxis() # Highest on top
    
    # Style tweaks
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    
    # 4. Save
    os.makedirs(VISUALS_DIR, exist_ok=True)
    plt.savefig(OUTPUT_FILE, dpi=120, bbox_inches='tight')
    plt.close()

    print(f"   ✨ Generated: output/visuals/{os.path.basename(OUTPUT_FILE)}")
    print("------------------------------------------------")

if __name__ == "__main__":
    main()
