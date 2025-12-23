#!/usr/bin/env python3
"""
Merge clean content from git version with new taxonomy v4 structure
- Takes 'content' blobs from OLD (git, no mojibake)
- Takes everything else from NEW (taxonomy v4 updates)
"""

import sys
import re

def extract_gems(content):
    """Extract all gem dictionaries from a content_store.py file."""
    # Find all_gems list
    match = re.search(r'all_gems\s*=\s*\[(.*?)\n\]', content, re.DOTALL)
    if not match:
        print("ERROR: Could not find all_gems list")
        return []
    
    gems_text = match.group(1)
    
    # Split by gem boundaries (each starts with opening brace at start of line)
    gem_blocks = re.split(r'\n\s*{', gems_text)
    
    gems = []
    for block in gem_blocks:
        if not block.strip():
            continue
        
        # Add back the opening brace
        if not block.strip().startswith('{'):
            block = '{' + block
        
        gems.append(block)
    
    return gems

def get_gem_title(gem_text):
    """Extract title from a gem block."""
    match = re.search(r"'title':\s*['\"](.+?)['\"]", gem_text)
    return match.group(1) if match else None

def get_gem_content(gem_text):
    """Extract content blob from a gem block."""
    # Match content with triple quotes
    match = re.search(r"'content':\s*\"\"\"(.*?)\"\"\"", gem_text, re.DOTALL)
    if match:
        return match.group(1)
    
    # Try single quotes
    match = re.search(r"'content':\s*'''(.*?)'''", gem_text, re.DOTALL)
    if match:
        return match.group(1)
    
    # Debug: check if content exists but in different format
    if "'content':" in gem_text or '"content":' in gem_text:
        # Content exists but we can't parse it - maybe single line string?
        return None
    
    return None

def replace_content_in_gem(gem_text, new_content):
    """Replace the content blob in a gem."""
    # Find where content starts and ends
    if '"""' in gem_text:
        # Find the content section with triple quotes
        start_match = re.search(r"'content':\s*\"\"\"", gem_text)
        if not start_match:
            return gem_text
        
        start_pos = start_match.end()
        
        # Find the closing triple quotes
        end_pos = gem_text.find('"""', start_pos)
        if end_pos == -1:
            return gem_text
        
        # Reconstruct: before + new content + after
        before = gem_text[:start_pos]
        after = gem_text[end_pos:]
        return before + new_content + after
    
    # Try triple single quotes
    start_match = re.search(r"'content':\s*'''", gem_text)
    if not start_match:
        return gem_text
    
    start_pos = start_match.end()
    end_pos = gem_text.find("'''", start_pos)
    if end_pos == -1:
        return gem_text
    
    before = gem_text[:start_pos]
    after = gem_text[end_pos:]
    return before + new_content + after

def main():
    print("🔄 Merging clean content from git with new taxonomy structure...")
    
    # Read OLD version (git, clean content)
    print("\n1️⃣ Reading OLD version (from git)...")
    with open('content_store_old.py', 'r', encoding='utf-8') as f:
        old_content = f.read()
    
    # Read NEW version (taxonomy v4, mojibake content)
    print("2️⃣ Reading NEW version (taxonomy v4)...")
    with open('content_store.py', 'r', encoding='utf-8') as f:
        new_content = f.read()
    
    # Extract gems from both
    print("3️⃣ Extracting gems from both files...")
    old_gems = extract_gems(old_content)
    new_gems = extract_gems(new_content)
    
    print(f"   Found {len(old_gems)} gems in OLD")
    print(f"   Found {len(new_gems)} gems in NEW")
    
    # Build mapping of old content by title
    print("4️⃣ Building content mapping...")
    old_content_map = {}
    for gem_text in old_gems:
        title = get_gem_title(gem_text)
        content = get_gem_content(gem_text)
        if title and content:
            old_content_map[title] = content
    
    print(f"   Mapped {len(old_content_map)} content blobs")
    
    # Replace content in new gems
    print("5️⃣ Merging content...")
    merged_gems = []
    matched = 0
    unmatched = []
    
    for gem_text in new_gems:
        title = get_gem_title(gem_text)
        
        if title and title in old_content_map:
            # Replace mojibake content with clean content
            clean_content = old_content_map[title]
            merged_gem = replace_content_in_gem(gem_text, clean_content)
            merged_gems.append(merged_gem)
            matched += 1
            print(f"   ✓ Merged: {title}")
        else:
            # Keep as-is (new gem or title mismatch)
            merged_gems.append(gem_text)
            if title:
                unmatched.append(title)
                # Don't print warning yet
    
    print(f"\n   ✅ Matched and merged: {matched}/{len(new_gems)} gems")
    if unmatched:
        print(f"   ⚠️  Kept as-is (no clean content found): {len(unmatched)} gems")
        for title in unmatched:
            print(f"      - {title}")
    
    # Rebuild the file
    print("6️⃣ Rebuilding file...")
    
    # Get everything before all_gems
    pre_gems = re.split(r'all_gems\s*=\s*\[', new_content)[0]
    
    # Get everything after all_gems
    post_match = re.search(r'\n\]\s*\n(.*)$', new_content, re.DOTALL)
    post_gems = post_match.group(1) if post_match else ""
    
    # Reconstruct
    merged_content = pre_gems + 'all_gems = [\n'
    
    for i, gem in enumerate(merged_gems):
        # Clean up the gem text
        gem_clean = gem.strip()
        if not gem_clean.startswith('{'):
            gem_clean = '{' + gem_clean
        if not gem_clean.endswith(','):
            gem_clean = gem_clean + ','
        
        merged_content += '    ' + gem_clean.replace('\n', '\n    ') + '\n'
    
    merged_content += ']\n' + post_gems
    
    # Save
    with open('content_store_merged.py', 'w', encoding='utf-8') as f:
        f.write(merged_content)
    
    print("\n✅ Merge complete!")
    print(f"   Saved to: content_store_merged.py")
    print("\n📋 Next steps:")
    print("   1. python3 -c \"import content_store_merged; print('✅ Syntax OK')\"")
    print("   2. mv content_store.py content_store_backup.py")
    print("   3. mv content_store_merged.py content_store.py")

if __name__ == '__main__':
    main()
