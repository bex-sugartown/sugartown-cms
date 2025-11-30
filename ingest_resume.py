import pdfplumber
import pandas as pd
import re
import os

# --- CONFIGURATION ---
# Update this path if needed
DRIVE_FOLDER = "/Users/beckyalice/Library/CloudStorage/GoogleDrive-becky.head@gmail.com/My Drive/04 Resumes & Job Search/01 Resumes/Resume 2026"
SOURCE_FILE = "MASTER_RESUME.pdf"
source_path = os.path.join(DRIVE_FOLDER, SOURCE_FILE)

def parse_resume_to_granular_csv(file_path):
    all_rows = []
    full_text = ""
    row_id = 1  # Initialize Row ID counter
    
    # Applicant Info (Hardcoded as requested)
    applicant = {
        "Applicant Name": "Becky Prince Head",
        "Applicant Title": "Content Management & Design Systems Product Leader",
        "Applicant Location": "San Francisco Bay Area",
        "Applicant Email": "bex@sugartown.io",
        "Applicant Phone": "(510) 679-4580",
        "Applicant LinkedIn": "https://www.linkedin.com/in/beckyhead/", # Explicitly set
        "Applicant Portfolio": "https://sugartown.io/", # Explicitly set
        "Applicant Summary": ""
    }

    with pdfplumber.open(file_path) as pdf:
        # 1. EXTRACT TEXT (We skip link extraction since we hardcoded them)
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"

    # 2. PARSE SUMMARY
    summary_match = re.search(r"Summary\s+(.*?)\s+Professional Experience", full_text, re.DOTALL)
    if summary_match:
        applicant["Applicant Summary"] = summary_match.group(1).replace("\n", " ").strip()

    # 3. PARSE EXPERIENCE (With "Buffer Logic" for Bullets)
    exp_section_match = re.search(r"Professional Experience\s+(.*?)\s+Education", full_text, re.DOTALL)
    
    if exp_section_match:
        exp_text = exp_section_match.group(1)
        job_headers = re.split(r"([A-Z][a-zA-Z0-9\s\.]+)(?:-|–)\s+([A-Z][a-zA-Z\s]+)\n", exp_text)
        
        i = 1
        while i < len(job_headers) - 2:
            company = job_headers[i].strip()
            role = job_headers[i+1].strip()
            content_block = job_headers[i+2].strip()
            
            lines = content_block.split('\n')
            meta_line = lines[0]
            
            dates, location, work_type, currently_employed = "", "", "Hybrid", "No"
            date_loc_match = re.match(r"(.*?)\s*\|\s*(.*)", meta_line)
            
            if date_loc_match:
                dates = date_loc_match.group(1).strip()
                location_raw = date_loc_match.group(2).strip()
                if "PRESENT" in dates.upper(): currently_employed = "Yes"
                if "(" in location_raw:
                    location = location_raw.split("(")[0].strip()
                    work_type = location_raw.split("(")[1].replace(")", "").strip()
                else: location = location_raw

            intro_text = []
            active_bullet_text = None 

            for line in lines[1:]:
                clean_line = line.strip()
                if not clean_line: continue
                
                is_bullet_start = clean_line.startswith("•") or clean_line.startswith("-")
                
                if is_bullet_start:
                    # Save previous bullet if exists
                    if active_bullet_text is not None:
                        all_rows.append({
                            "Row ID": row_id,
                            **applicant,
                            "Record Type": "Experience",
                            "Organization/School/Category": company,
                            "Role/Degree": role,
                            "Dates": dates,
                            "Currently Employed?": currently_employed,
                            "Location": location,
                            "Type/Mode": work_type,
                            "Intro": " ".join(intro_text),
                            "Content List": active_bullet_text,
                            "Experience Skills": ""
                        })
                        row_id += 1
                    
                    # Start NEW bullet
                    text_part = clean_line.lstrip("•- ").strip()
                    active_bullet_text = text_part if text_part else ""
                        
                elif active_bullet_text is not None:
                    # Continuation
                    active_bullet_text = clean_line if active_bullet_text == "" else active_bullet_text + " " + clean_line
                else:
                    intro_text.append(clean_line)

            # Save the final bullet of the job
            if active_bullet_text is not None:
                all_rows.append({
                    "Row ID": row_id,
                    **applicant,
                    "Record Type": "Experience",
                    "Organization/School/Category": company,
                    "Role/Degree": role,
                    "Dates": dates,
                    "Currently Employed?": currently_employed,
                    "Location": location,
                    "Type/Mode": work_type,
                    "Intro": " ".join(intro_text),
                    "Content List": active_bullet_text,
                    "Experience Skills": ""
                })
                row_id += 1
            
            # Catch jobs with ONLY intro (no bullets)
            if not any(r['Organization/School/Category'] == company for r in all_rows):
                 all_rows.append({
                        "Row ID": row_id,
                        **applicant,
                        "Record Type": "Experience",
                        "Organization/School/Category": company,
                        "Role/Degree": role,
                        "Dates": dates,
                        "Currently Employed?": currently_employed,
                        "Location": location,
                        "Type/Mode": work_type,
                        "Intro": " ".join(intro_text),
                        "Content List": " ".join(intro_text),
                        "Experience Skills": ""
                    })
                 row_id += 1
            i += 3

    # 4. PARSE EDUCATION
    edu_section_match = re.search(r"Education\s+(.*?)\s+Skills", full_text, re.DOTALL)
    if edu_section_match:
        edu_lines = edu_section_match.group(1).strip().split('\n')
        for line in edu_lines:
            if "|" in line:
                parts = line.split("|")
                all_rows.append({
                    "Row ID": row_id,
                    **applicant,
                    "Record Type": "Education",
                    "Organization/School/Category": parts[0].strip(),
                    "Role/Degree": parts[1].strip(),
                    "Dates": "", "Currently Employed?": "", "Location": "", "Type/Mode": "", "Intro": "", "Content List": "", "Experience Skills": ""
                })
                row_id += 1

    # 5. PARSE SKILLS
    skills_section_match = re.search(r"Skills\s+(.*)", full_text, re.DOTALL)
    if skills_section_match:
        skills_text = skills_section_match.group(1)
        known_categories = [ "Content Platforms & Architecture", "Commerce & Product Data Systems", "APIs, Integrations & Architecture", "Design Systems & Experience Delivery", "Al, Personalization & Automation", "Product Leadership & Execution" ]
        current_cat = "Skills"
        current_content = []
        
        for line in skills_text.split('\n'):
            line = line.strip()
            if not line: continue
            is_header = False
            for cat in known_categories:
                if cat in line:
                    if current_content:
                        all_rows.append({ 
                            "Row ID": row_id,
                            **applicant, 
                            "Record Type": "Skills", 
                            "Organization/School/Category": current_cat, 
                            "Role/Degree": "", "Dates": "", "Currently Employed?": "", "Location": "", "Type/Mode": "", "Intro": "", 
                            "Content List": ", ".join(current_content), 
                            "Experience Skills": "" 
                        })
                        row_id += 1
                    current_cat = line
                    current_content = []
                    is_header = True
                    break
            if not is_header: current_content.append(line)
        if current_content:
            all_rows.append({ 
                "Row ID": row_id,
                **applicant, 
                "Record Type": "Skills", 
                "Organization/School/Category": current_cat, 
                "Role/Degree": "", "Dates": "", "Currently Employed?": "", "Location": "", "Type/Mode": "", "Intro": "", 
                "Content List": ", ".join(current_content), 
                "Experience Skills": "" 
            })
            row_id += 1

    return pd.DataFrame(all_rows)

# --- EXECUTE ---
if os.path.exists(source_path):
    print(f"📄 Found Master Resume at: {source_path}")
    print("⏳ Parsing with Row IDs...")
    df = parse_resume_to_granular_csv(source_path)
    output_csv = "resume_data.csv"
    df.to_csv(output_csv, index=False)
    print(f"✅ Success! Data extracted to: {output_csv}")
    print(f"   (Found {len(df)} rows of data)")
else:
    print(f"❌ ERROR: Could not find '{SOURCE_FILE}'")
