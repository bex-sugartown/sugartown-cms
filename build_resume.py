import json
import os

# ==========================================
# CONFIGURATION
# ==========================================
SOURCE_FILE = 'master_resume_data.json'
OUTPUT_DIR = 'builds'

# ==========================================
# TEMPLATE: MARKDOWN
# ==========================================
def render_markdown(resume, applicant):
    """Generates a Markdown string from resume data"""
    md = []
    
    # --- HEADER ---
    md.append(f"# {applicant['name']}")
    md.append(f"**{resume['role_title']}**")
    md.append(f"{applicant['location']} | {applicant['email']} | {applicant['phone']}")
    md.append(f"[LinkedIn]({applicant['linkedin']}) | [Portfolio]({applicant['portfolio']})")
    md.append("\n---")

    # --- SUMMARY ---
    md.append("\n## Professional Summary")
    md.append(f"{resume['role_summary']}")

    # --- SKILLS (Table Format for readability) ---
    if resume.get('skills'):
        md.append("\n## Skills & Technologies")
        md.append("| Category | Skills |")
        md.append("| :--- | :--- |")
        for skill in resume['skills']:
            # Clean up content if it's a list or string
            content = skill['content']
            md.append(f"| **{skill['category']}** | {content} |")

    # --- EXPERIENCE ---
    md.append("\n## Professional Experience")
    
    for job in resume['experience']:
        # Header: Role at Company
        dates = job['dates'] if job['dates'] else "Dates N/A"
        md.append(f"\n### {job['role']} | **{job['organization']}**")
        md.append(f"*{dates} | {job['location']}*")
        
        # Category Summary (The "Theme" of the role)
        if job.get('category_summary'):
            md.append(f"\n> *Focus: {job['category_summary']}*")
        
        # Bullet Points
        for highlight in job['highlights']:
            md.append(f"* {highlight['content']}")

    # --- EDUCATION ---
    md.append("\n## Education")
    for edu in applicant['education']:
        dates = edu['dates'] if edu['dates'] else ""
        md.append(f"* **{edu['degree_certification']}** — {edu['institution']} {dates}")

    return "\n".join(md)

# ==========================================
# MAIN ENGINE
# ==========================================
def main():
    print("------------------------------------------------")
    print("📄 SUGARTOWN RESUME BUILDER v1.0")
    print("------------------------------------------------")

    # 1. Load Data
    try:
        with open(SOURCE_FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Could not find {SOURCE_FILE}")
        return

    # 2. Get Applicant (Assuming Single User 'applicant_1')
    applicant = data['applicants'][0] 
    resumes = data['resumes']
    
    print(f"👤 Applicant: {applicant['name']}")
    print(f"📚 Found {len(resumes)} resume versions.")

    # 3. Create Output Directory
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 4. Generate Builds
    for res in resumes:
        rid = res['id']
        print(f"   ⚙️  Building: {rid}...")
        
        # Render
        markdown_content = render_markdown(res, applicant)
        
        # Save
        filename = f"{OUTPUT_DIR}/{rid}_Resume.md"
        with open(filename, 'w') as f:
            f.write(markdown_content)
            
    print(f"\n✨ Success! Generated {len(resumes)} resumes in /{OUTPUT_DIR}")
    print("------------------------------------------------")

if __name__ == "__main__":
    main()