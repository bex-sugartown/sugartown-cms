def generate_pink_card_grid(cards_data):
    """
    Generates the v3.3 'Clean Grid' HTML for Sugartown Pink Cards.
    
    Args:
        cards_data (list): List of dicts containing card content.
        
    Returns:
        str: The raw HTML string to inject into a Gem body.
    """
    html_output = ['<div class="st-grid-wrapper">']
    
    for card in cards_data:
        # 1. Handle Background
        bg_style = ""
        if card.get('bg_image'):
            bg_style = f' style="background-image: url(\'{card["bg_image"]}\');"'
            
        # 2. Handle Tags
        tags_html = ""
        if card.get('tags'):
            tag_spans = [f'<span class="pink-card__tag">{t}</span>' for t in card['tags']]
            tags_html = f'<div class="wp-block-post-terms">{" ".join(tag_spans)}</div>'

        # 3. Assemble Card HTML
        card_html = f"""
    <div class="pink-card">
        <div class="pink-card__bg"{bg_style}></div>
        
        <div class="pink-card__content">
            <p class="pink-card__eyebrow">{card.get('eyebrow', 'SUGARTOWN')}</p>
            <h2 class="pink-card__title"><a href="{card.get('link', '#')}">{card['title']}</a></h2>
            <h3 class="pink-card__subtitle">{card.get('subtitle', '')}</h3>
            <p class="pink-card__body">{card.get('body', '')}</p>
            
            <div class="pink-card__citation">
                {card.get('citation', '')}
            </div>
            
            {tags_html}
        </div>

        <div class="pink-card__media">
            <img src="{card.get('icon_url', '')}" alt="{card['title']} Icon" loading="lazy" />
        </div>
    </div>"""
        html_output.append(card_html)

    html_output.append('</div>')
    return "\n".join(html_output)

# ==========================================
# EXAMPLE USAGE
# ==========================================
# home_cards = [
#     {
#         "title": "CV / Resume",
#         "link": "/cv-resume",
#         "eyebrow": "SUGARTOWN-CMS",
#         "subtitle": "A Systems View of a Career",
#         "body": "The Resume Factory is a rules-based composition engine...",
#         "citation": "<a href='#'>[1] Source: Resume Engine v2.0</a>",
#         "tags": ["p13n", "json", "python"],
#         "icon_url": "https://sugartown.io/.../work_icon.svg",
#         "bg_image": "https://sugartown.io/.../texture.png"
#     },
#     # ... add other cards here
# ]
#
# # In your main content definition:
# homepage_content = f"""
# <h1>Atoms & Ecosystems</h1>
# <p>Intro text...</p>
# {generate_pink_card_grid(home_cards)}
# """