#!/usr/bin/env python3
import json
import argparse
from pathlib import Path
import sys

# --- CONFIGURATION ---
BASE_DIR = Path(__file__).resolve().parent
INPUT_JSON = BASE_DIR / "data" / "json" / "master_resume_data.json"
OUTPUT_DIR = BASE_DIR / "output" / "resumes"
MASTER_VARIANT = "CMS-DS-PDM-01" 

def get_variant_content(slot, target_role):
    # 1. Exact Match
    for v in slot['variants']:
        if v['type'] == target_role:
            return v['content']
    # 2. Master Fallback
    if target_role != MASTER_VARIANT:
        for v in slot['variants']:
            if v['type'] == MASTER_VARIANT:
                return v['content']
    return None

def build_resume(target_role):
    if not INPUT_JSON.exists():
        print(f"❌ ERROR: Data file not found. Run 'python3 scripts/ingest_resume.py' first.")
        sys.exit(1)

    print(f"🏭 SUGARTOWN FACTORY: Building Resume for target '{target_role}'")
    
    with open(INPUT_JSON, 'r') as f:
        data = json.load(f)

    # --- 1. HEADER (The Screencap Match) ---
    basics = data['basics']
    md = f"# {basics['name']}\n"
    # Pipe separated contact info
    contact_info = [
        basics['location'],
        basics['email'],
        basics['phone'],
        basics['linkedin'],
        basics['portfolio']
    ]
    # Filter out empty strings/NaNs
    contact_line = " | ".join([str(c) for c in contact_info if c and str(c) != 'nan'])
    md += f"{contact_line}\n\n"
    
    # --- 2. DYNAMIC SUMMARY (Role Title + Summary) ---
    # Look for metadata specific to this Variant (e.g. CMS-DS-PDM-01)
    # If not found, fall back to Master variant metadata
    summary_meta = data['variant_summaries'].get(target_role)
    if not summary_meta:
        summary_meta = data['variant_summaries'].get(MASTER_VARIANT)
        
    if summary_meta:
        md += f"## {summary_meta['title']}\n\n"
        md += f"{summary_meta['summary']}\n\n"
        md += "---\n\n" # Separator
    
    # --- 3. EXPERIENCE ---
    md += "## EXPERIENCE\n\n"
    for job in data['work_history']:
        job_content = ""
        for slot in job['slots']:
            content = get_variant_content(slot, target_role)
            if content:
                job_content += f"- {content}\n"
        
        if job_content:
            md += f"### {job['company']} — {job['role']}\n"
            md += f"*{job['dates']} | {job['location']}*\n\n"
            md += job_content + "\n"

    # --- 4. EDUCATION ---
    if data.get('education'):
        md += "## EDUCATION\n\n"
        for edu in data['education']:
            md += f"**{edu['institution']}**\n"
            details = [d for d in [edu.get('area'), edu.get('location')] if d]
            md += f"{' | '.join(details)}\n\n"

    # --- 5. SKILLS ---
    if data.get('skills'):
        md += "## SKILLS\n\n"
        for slot in data['skills']:
            content = get_variant_content(slot, target_role)
            if content:
                if slot.get('header'):
                    md += f"**{slot['header']}**: "
                md += f"{content}\n\n"

    # Save Output
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filename = OUTPUT_DIR / f"Resume_{target_role}.md"
    
    with open(filename, 'w') as f:
        f.write(md)
    
    print(f"✅ ARTIFACT CREATED: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--role', type=str, default=MASTER_VARIANT, help='Target Variant ID')
    args = parser.parse_args()
    
    build_resume(args.role)