import os

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output', 'visuals')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'roadmap_2025.html')

def generate_mermaid_gantt():
    return """<pre class="mermaid">
gantt
    title Sugartown Launch Roadmap (12 Weeks)
    dateFormat  YYYY-MM-DD
    axisFormat  %m/%d
    
    section Phase 1 The Factory
    Infrastructure and Repo Split     :done,    p1_infra, 2025-11-24, 4d
    Pink Stink Theme and CSS          :done,    p1_design, after p1_infra, 4d
    Headless Resume Engine            :done,    p1_resume, after p1_design, 3d
    
    section Phase 2 Viz Ops
    Visualization Engine Python       :active,  p2_viz,    2025-12-06, 5d
    Automated Cover Letters           :         p2_cov,    after p2_viz, 5d
    Smart Merge On Hold               :crit,    p2_merge,  after p2_cov, 1w
    
    section Phase 3 Frontend
    React Nextjs Evaluation           :         p3_react,  2026-01-05, 2w
    Full Headless Migration           :         p3_mig,    after p3_react, 4w
</pre>"""

def main():
    print("------------------------------------------------")
    print("🧜‍♀️ VIZ ENGINE: Mermaid Gantt Chart (WP Safe Mode)")
    print("------------------------------------------------")

    mermaid_code = generate_mermaid_gantt()
    
    # Save to file
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        f.write(mermaid_code)
    
    print(f"   ✨ Generated: output/visuals/{os.path.basename(OUTPUT_FILE)}")
    print("------------------------------------------------")
    print("   📋 Preview:\n")
    print(mermaid_code)

if __name__ == "__main__":
    main()
