#!/usr/bin/env python3
import pandas as pd
import json
from difflib import SequenceMatcher
from pathlib import Path
import sys

# --- CONFIGURATION ---
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_CSV = BASE_DIR / "data" / "source" / "resume_data.csv"
OUTPUT_JSON = BASE_DIR / "data" / "json" / "master_resume_data.json"

# Column Headers
COL_RECORD_TYPE = 'Record Type'
COL_SLOT_ID = 'Slot_ID'
COL_VARIANT = 'Variant Type'
COL_CONTENT = 'Content'
COL_ORG = 'Organization'
COL_ROLE = 'Role/Degree'
COL_DATES = 'Dates'
COL_LOC = 'Location'
COL_SKILLS_HEADER = 'Skills'

# Metadata Headers (The new stuff)
COL_ROLE_TITLE = 'Role Title'
COL_ROLE_SUMMARY = 'Role Summary'
COL_APP_NAME = 'Applicant Name'
COL_APP_LOC = 'Applicant Location'
COL_APP_EMAIL = 'Applicant Email'
COL_APP_PHONE = 'Applicant Phone'
COL_APP_LINKEDIN = 'Applicant LinkedIn'
COL_APP_PORTFOLIO = 'Applicant Portfolio'

SIMILARITY_THRESHOLD = 0.45

def similar(a, b):
    return SequenceMatcher(None, str(a), str(b)).ratio()

def process_slots(df_subset, context_name):
    """Cluster rows into Slots -> Variants."""
    slots_output = []
    manual_slots = {}
    orphans = []

    for _, row in df_subset.iterrows():
        content = row[COL_CONTENT]
        if pd.isna(content): continue

        variant_type = row[COL_VARIANT] if pd.notna(row[COL_VARIANT]) else "CMS-DS-PDM-01"
        slot_id = row[COL_SLOT_ID] if pd.notna(row[COL_SLOT_ID]) else None
        
        # Capture Skill Header if available
        skill_header = row[COL_SKILLS_HEADER] if COL_SKILLS_HEADER in row and pd.notna(row[COL_SKILLS_HEADER]) else None

        bullet_obj = {
            "type": variant_type,
            "content": content,
            "manual_id": slot_id,
            "header": skill_header 
        }

        if slot_id:
            if slot_id not in manual_slots:
                manual_slots[slot_id] = []
            manual_slots[slot_id].append(bullet_obj)
        else:
            orphans.append(bullet_obj)

    final_clusters = []

    # 1. Add Manual Slots
    for s_id, variants in manual_slots.items():
        final_clusters.append({"id": s_id, "variants": variants})

    # 2. Auto-Cluster Orphans
    for orphan in orphans:
        matched = False
        for cluster in final_clusters:
            centroid = cluster['variants'][0]['content']
            if similar(orphan['content'], centroid) > SIMILARITY_THRESHOLD:
                cluster['variants'].append(orphan)
                matched = True
                break
        
        if not matched:
            slug = str(context_name).lower().split()[0].replace(',', '').replace('.', '')
            new_id = f"{slug}_auto_{len(final_clusters)+1:02d}"
            final_clusters.append({"id": new_id, "variants": [orphan]})

    # 3. Format Output
    for cluster in final_clusters:
        header_title = None
        for v in cluster['variants']:
            if v.get('header'):
                header_title = v['header']
                break
        
        slot_obj = {
            "id": cluster['id'], 
            "header": header_title,
            "variants": []
        }
        
        seen_types = set()
        for v in cluster['variants']:
            if v['type'] not in seen_types:
                slot_obj['variants'].append({"type": v['type'], "content": v['content']})
                seen_types.add(v['type'])
        slots_output.append(slot_obj)
        
    return slots_output

def run_ingestion():
    print(f"🏭 SUGARTOWN FACTORY: Ingestion Sequence Started")
    
    if not INPUT_CSV.exists():
        print(f"❌ ERROR: Source file not found at {INPUT_CSV}")
        sys.exit(1)

    try:
        df = pd.read_csv(INPUT_CSV)
    except Exception as e:
        print(f"❌ ERROR reading CSV: {e}")
        sys.exit(1)

    # 1. Capture Static Basics (From the first valid row)
    first_valid = df.iloc[0] # Assuming first row has contact info
    golden_record = {
        "basics": {
            "name": str(first_valid[COL_APP_NAME]),
            "location": str(first_valid[COL_APP_LOC]),
            "email": str(first_valid[COL_APP_EMAIL]),
            "phone": str(first_valid[COL_APP_PHONE]),
            "linkedin": str(first_valid[COL_APP_LINKEDIN]),
            "portfolio": str(first_valid[COL_APP_PORTFOLIO])
        },
        "variant_summaries": {}, # NEW: Stores Title/Summary per variant
        "work_history": [],
        "education": [],
        "skills": []
    }

    # 2. Capture Dynamic Summaries (Iterate all rows to find unique Variant Types)
    if COL_ROLE_TITLE in df.columns and COL_ROLE_SUMMARY in df.columns:
        # Group by Variant Type to get unique summaries
        # We drop duplicates to just get one row per variant type
        meta_df = df[[COL_VARIANT, COL_ROLE_TITLE, COL_ROLE_SUMMARY]].drop_duplicates(subset=[COL_VARIANT])
        
        for _, row in meta_df.iterrows():
            v_type = row[COL_VARIANT]
            if pd.notna(v_type):
                golden_record['variant_summaries'][v_type] = {
                    "title": row[COL_ROLE_TITLE] if pd.notna(row[COL_ROLE_TITLE]) else "Product Leader",
                    "summary": row[COL_ROLE_SUMMARY] if pd.notna(row[COL_ROLE_SUMMARY]) else ""
                }

    # --- PART 3: EDUCATION ---
    if COL_RECORD_TYPE in df.columns:
        edu_df = df[df[COL_RECORD_TYPE] == 'Education']
        seen_edu = set()
        for _, row in edu_df.iterrows():
            inst = row[COL_ORG] if pd.notna(row[COL_ORG]) else ""
            degree = row[COL_ROLE] if pd.notna(row[COL_ROLE]) else ""
            unique_key = (inst, degree)
            if unique_key not in seen_edu and (inst or degree):
                golden_record['education'].append({
                    "institution": inst,
                    "area": degree,
                    "dates": row[COL_DATES] if pd.notna(row[COL_DATES]) else "",
                    "location": row[COL_LOC] if pd.notna(row[COL_LOC]) else ""
                })
                seen_edu.add(unique_key)
    
    # --- PART 4: SKILLS ---
    if COL_RECORD_TYPE in df.columns:
        skill_df = df[df[COL_RECORD_TYPE] == 'Skills']
        golden_record['skills'] = process_slots(skill_df, "skills")

    # --- PART 5: EXPERIENCE ---
    if COL_RECORD_TYPE in df.columns:
        exp_df = df[(df[COL_RECORD_TYPE] == 'Experience') | (df[COL_RECORD_TYPE].isna())]
    else:
        exp_df = df 

    processed_jobs = 0
    for org_name in exp_df[COL_ORG].unique():
        if pd.isna(org_name): continue
        
        org_rows = exp_df[exp_df[COL_ORG] == org_name]
        first_row = org_rows.iloc[0]

        job_entry = {
            "company": org_name,
            "role": first_row[COL_ROLE] if pd.notna(first_row[COL_ROLE]) else "Product Leader",
            "dates": first_row[COL_DATES] if pd.notna(first_row[COL_DATES]) else "",
            "location": first_row[COL_LOC] if pd.notna(first_row[COL_LOC]) else "",
            "slots": process_slots(org_rows, org_name)
        }
        golden_record['work_history'].append(job_entry)
        processed_jobs += 1

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(golden_record, f, indent=2)
    
    print(f"✅ SUCCESS: Ingested metadata for {len(golden_record['variant_summaries'])} variants.")

if __name__ == "__main__":
    run_ingestion()