#!/usr/bin/env python3
"""
Publish AI Ethics & Operations page from GitHub to WordPress
Part of Sugartown CMS publishing pipeline
"""

import requests
import re
import base64  # ← ADDED: Missing import
from datetime import datetime
import config

# ==========================================
# CONFIGURATION
# ==========================================
BASE_URL = config.BASE_URL
USER = config.USER
PASSWORD = config.PASSWORD

# Pages endpoint (different from gems)
PAGES_ENDPOINT = f"{BASE_URL}/wp-json/wp/v2/pages"

# Auth
creds = f"{USER}:{PASSWORD}"
token = base64.b64encode(creds.encode())
headers = {
    'Authorization': f'Basic {token.decode("utf-8")}',
    'Content-Type': 'application/json'
}


def convert_markdown_to_html(markdown_text):
    """
    Enhanced markdown to HTML conversion
    Handles: headers, bold, italic, links, nested lists, code blocks, hr, metadata blocks
    """
    lines = markdown_text.split('\n')
    html_lines = []
    in_code_block = False
    code_language = ''
    list_stack = []  # Track nested list levels
    metadata_buffer = []  # Buffer for metadata lines
    
    for i, line in enumerate(lines):
        # Code blocks
        if line.startswith('```'):
            # Flush any metadata buffer
            if metadata_buffer:
                html_lines.append('<p>' + '<br>\n'.join(metadata_buffer) + '</p>')
                metadata_buffer = []
            
            if in_code_block:
                html_lines.append('</code></pre>')
                in_code_block = False
            else:
                code_language = line.replace('```', '').strip()
                html_lines.append(f'<pre><code class="language-{code_language}">')
                in_code_block = True
            continue
        
        if in_code_block:
            html_lines.append(line)
            continue
        
        # Detect metadata block (lines starting with **Key:** value)
        metadata_match = re.match(r'^\*\*([^:]+):\*\*\s+(.+)$', line)
        if metadata_match and i < 5:  # Only first 5 lines can be metadata
            metadata_buffer.append(f'<strong>{metadata_match.group(1)}:</strong> {convert_inline_markdown(metadata_match.group(2))}')
            continue
        
        # Flush metadata buffer if we hit non-metadata content
        if metadata_buffer:
            html_lines.append('<p class="st-metadata">' + '<br>\n'.join(metadata_buffer) + '</p>')
            metadata_buffer = []
        
        # Calculate indentation level for nested lists
        indent_match = re.match(r'^(\s*)', line)
        indent_level = len(indent_match.group(1)) // 2 if indent_match else 0
        
        # Unordered lists with nesting support
        ul_match = re.match(r'^(\s*)[\-\*]\s+(.+)$', line)
        if ul_match:
            # Close deeper lists if we've dedented
            while list_stack and list_stack[-1]['level'] > indent_level:
                html_lines.append(f'</{list_stack.pop()["type"]}>')
            
            # Open new list if needed
            if not list_stack or list_stack[-1]['level'] < indent_level:
                html_lines.append('<ul>')
                list_stack.append({'type': 'ul', 'level': indent_level})
            
            html_lines.append(f'<li>{convert_inline_markdown(ul_match.group(2))}</li>')
            continue
        
        # Ordered lists with nesting support
        ol_match = re.match(r'^(\s*)\d+\.\s+(.+)$', line)
        if ol_match:
            # Close deeper lists if we've dedented
            while list_stack and list_stack[-1]['level'] > indent_level:
                html_lines.append(f'</{list_stack.pop()["type"]}>')
            
            # Open new list if needed
            if not list_stack or list_stack[-1]['level'] < indent_level:
                html_lines.append('<ol>')
                list_stack.append({'type': 'ol', 'level': indent_level})
            
            html_lines.append(f'<li>{convert_inline_markdown(ol_match.group(2))}</li>')
            continue
        
        # Close all open lists if we're not in a list anymore
        if list_stack and not re.match(r'^\s*[\-\*\d]', line):
            while list_stack:
                html_lines.append(f'</{list_stack.pop()["type"]}>')
        
        # Headers with proper anchor IDs
        header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if header_match:
            level = len(header_match.group(1))
            text = header_match.group(2)
            # Create URL-friendly ID that matches markdown link patterns
            # 1. Lowercase
            anchor_id = text.lower()
            # 2. Remove special chars (leaves spaces where they were)
            anchor_id = re.sub(r'[^\w\s-]', '', anchor_id)
            # 3. Replace whitespace (including multiple spaces) with hyphens
            #    This creates -- where & was removed (matches existing links)
            anchor_id = re.sub(r'\s+', '-', anchor_id)
            # 4. Clean up but DON'T normalize multiple hyphens (needed for linking)
            anchor_id = anchor_id.strip('-')
            
            html_lines.append(f'<h{level} id="{anchor_id}">{convert_inline_markdown(text)}</h{level}>')
            continue
        
        # Horizontal rule
        if re.match(r'^[\-\*]{3,}$', line.strip()):
            html_lines.append('<hr>')
            continue
        
        # Empty lines
        if not line.strip():
            continue
        
        # Regular paragraphs
        html_lines.append(f'<p>{convert_inline_markdown(line)}</p>')
    
    # Close any remaining open lists
    while list_stack:
        html_lines.append(f'</{list_stack.pop()["type"]}>')
    
    return '\n'.join(html_lines)

def convert_inline_markdown(text):
    """Convert inline markdown: bold, italic, links, code, escape sequences"""
    # Handle escaped characters (remove backslashes before special chars)
    text = re.sub(r'\\([*~`$\[\]<>{}|^&])', r'\1', text)
    
    # Links [text](url) - simple direct conversion
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
    
    # Bold **text**
    text = re.sub(r'\*\*([^\*]+)\*\*', r'<strong>\1</strong>', text)
    
    # Italic *text*
    text = re.sub(r'\*([^\*]+)\*', r'<em>\1</em>', text)
    
    # Inline code `code`
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    return text

def fetch_github_markdown(repo, file_path):
    """Fetch raw markdown from GitHub"""
    url = f"https://raw.githubusercontent.com/{repo}/main/{file_path}"
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def publish_to_wordpress(html_content, page_slug='ai-ethics'):
    """Publish or update WordPress page"""
    
    # Add Sugartown styling wrapper (hide WP page title since we use markdown H1)
    styled_html = f'''
<style>
    /* Hide WordPress auto-generated page title when this content exists */
    body:has(.st-ethics-page) h1.wp-block-post-title {{
        display: none !important;
    }}
</style>
<div class="st-ethics-page st-github-content">
    {html_content}
    <footer class="st-ethics-footer">
        <p><em>Last synced from GitHub: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</em></p>
        <p><a href="https://github.com/bex-sugartown/sugartown-cms/blob/main/docs/ai_ethics_and_operations.md" target="_blank">View source on GitHub</a></p>
    </footer>
</div>
'''
    
    # Page data
    page_data = {
        'slug': page_slug,
        'title': 'AI Ethics & Operations',  # Keep for SEO/admin but hide visually
        'content': styled_html,
        'status': 'publish'
    }
    
    # Check if page exists
    check_response = requests.get(
        PAGES_ENDPOINT,
        params={'slug': page_slug},
        headers=headers
    )
    
    if check_response.json():
        # Update existing page
        page_id = check_response.json()[0]['id']
        response = requests.post(
            f"{PAGES_ENDPOINT}/{page_id}",
            json=page_data,
            headers=headers
        )
        print(f"✓ Updated page ID {page_id}")
        print(f"  URL: {BASE_URL}/{page_slug}/")
    else:
        # Create new page
        response = requests.post(
            PAGES_ENDPOINT,
            json=page_data,
            headers=headers
        )
        page_id = response.json().get('id')
        print(f"✓ Created new page ID {page_id}")
        print(f"  URL: {BASE_URL}/{page_slug}/")
    
    response.raise_for_status()
    return response.json()

def main():
    """Main execution"""
    import sys
    
    print("🦄 Sugartown Ethics Page Publisher")
    print("=" * 50)
    
    try:
        # Check if local markdown file provided as argument
        if len(sys.argv) > 1:
            local_file = sys.argv[1]
            print(f"📥 Reading markdown from local file: {local_file}")
            with open(local_file, 'r', encoding='utf-8') as f:
                markdown = f.read()
        else:
            # Fetch from GitHub
            print("📥 Fetching markdown from GitHub...")
            markdown = fetch_github_markdown(
                repo='bex-sugartown/sugartown-cms',
                file_path='docs/ai_ethics_and_operations.md'
            )
        
        # Convert to HTML
        print("🔄 Converting markdown to HTML...")
        html = convert_markdown_to_html(markdown)
        
        # Publish to WordPress
        print("📤 Publishing to WordPress...")
        result = publish_to_wordpress(html)
        
        print("\n✨ Success! Page published.")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: File not found - {e}")
        return 1
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())