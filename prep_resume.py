import shutil
import os
from datetime import date

# --- 1. CONFIGURATION (Your Real Paths) ---
# We define the base folder so we don't have to type it twice
DRIVE_FOLDER = "/Users/beckyalice/Library/CloudStorage/GoogleDrive-becky.head@gmail.com/My Drive/04 Resumes & Job Search/01 Resumes/Resume 2026"

# The file you downloaded from Google Docs (Must be PDF!)
SOURCE_FILENAME = "Becky-Head_Product-Leader_CMS-Design-System_2026_figma.pdf" 

# Your Target Naming Convention
NAME = "Becky-Head"
ROLE = "Product-Leader_CMS-Design-System"
YEAR = "2026" # Updated to match your folder year

# --- 2. SETUP PATHS ---
# Combine the folder + filename to get the full path
source_path = os.path.join(DRIVE_FOLDER, SOURCE_FILENAME)

# Define where the "Sent" versions go (I created a subfolder for you)
archive_folder = os.path.join(DRIVE_FOLDER, "Sent_Versions")

# --- 3. LOGIC ---
today = date.today()
date_stamp = today.strftime("%Y-%m-%d")

# The clean name for the recruiter (e.g., Becky-Head_Product-Leader_2026.pdf)
external_filename = f"{NAME}_{ROLE}_{YEAR}.pdf"
external_path = os.path.join(DRIVE_FOLDER, external_filename)

# The backup name for your records (e.g., 2025-11-25_Becky-Head_Variant.pdf)
internal_filename = f"{date_stamp}_{NAME}_{ROLE}.pdf"
internal_path = os.path.join(archive_folder, internal_filename)

# --- 4. EXECUTION ---
# Check if the source PDF exists first
if not os.path.exists(source_path):
    print(f"❌ ERROR: Could not find '{SOURCE_FILENAME}'")
    print(f"   Looked in: {DRIVE_FOLDER}")
    print("   Did you download the Google Doc as a PDF yet?")
    exit()

# Create the Archive folder if it doesn't exist
if not os.path.exists(archive_folder):
    os.makedirs(archive_folder)
    print(f"ue402 Created new folder: Sent_Versions")

# Copy the files
shutil.copy(source_path, external_path)
print(f"✅ READY TO SEND: {external_filename}")
print(f"   (Located in your main Resume 2026 folder)")

shutil.copy(source_path, internal_path)
print(f"ue402 ARCHIVED:     {internal_filename}")
print(f"   (Saved to 'Sent_Versions' folder)")
