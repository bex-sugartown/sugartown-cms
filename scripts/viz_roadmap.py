import os

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output', 'visuals')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'roadmap_2025.html')

def generate_mermaid_gantt():
    # Includes WordPress Block Comments for "Wide" alignment
    return """<div class="wp-block-group alignwide">
<pre class="mermaid">
gantt
    title Sugartown Launch Roadmap (12 Weeks)
    dateFormat  YYYY-MM-DD
    axisFormat  %m/%d
    
    section Phase 1 The Factory
    Infrastructure and Repo Split     :done,    p1_infra, 2025-11-24, 4d
    Sugartown Pink Theme and CSS      :done,    p1_design, after p1_infra, 4d
    Headless Resume Engine            :done,    p1_resume, after p1_design, 3d
    
    section Phase 2 Viz Ops
    Visualization Engine Python       :active,  p2_viz,    2025-12-06, 5d
    Web Resume Publishing             :         p2_web,    after p2_viz, 3d
    Skills Cloud Visualization        :         p2_skills, after p2_web, 3d
    Automated Cover Letters           :         p2_cov,    after p2_skills, 5d
    Smart Merge On Hold               :crit,    p2_merge,  2026-04-01, 1w
    
    section Phase 3 Frontend
    React Nextjs Evaluation           :         p3_react,  2026-01-05, 2w
    Full Headless Migration           :         p3_mig,    after p3_react, 4w
</pre>
</div>
"""

def main():
    print("------------------------------------------------")
    print("🧜‍♀️ VIZ ENGINE: Mermaid Gantt (Terminal Output)")
    print("------------------------------------------------")

    mermaid_code = generate_mermaid_gantt()
    
    # Save to file
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        f.write(mermaid_code)
    
    print(f"   ✨ Generated: output/visuals/{os.path.basename(OUTPUT_FILE)}")
    print("------------------------------------------------")
    
    # ✨ FIX: Print to console for easy copy/paste
    print("   📋 COPY BELOW:\n")
    print(mermaid_code)
    print("\n------------------------------------------------")

if __name__ == "__main__":
    main()