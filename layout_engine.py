def generate_st_card_grid(cards_data, *, wrapper_class="st-grid", dark_trigger_slugs=None):
    """
    Generates Sugartown v5+ ST-Card grid HTML (<article class="st-card">…</article>)
    suitable for injecting into a Gem body.

    Goals:
    - Emit markup that matches the Knowledge Graph archive card structure closely.
    - Support optional dark variant via `.st-card--dark`
      - Per-card override: card["is_dark"] = True/False
      - Tag-triggered: if any tag matches dark_trigger_slugs, card becomes dark
    - Use current tag pill class: `.st-card__tag`

    Args:
        cards_data (list[dict]): Each dict describes one card.
        wrapper_class (str): Grid wrapper class. Defaults to "st-grid".
        dark_trigger_slugs (set|list|tuple|None): Tag slugs that trigger dark mode.
            Example: {"system", "meta", "architecture", "dx"}

    Card dict keys (recommended):
        id (int|str)              Optional
        title (str)               Required
        link (str)                Optional (defaults "#")
        eyebrow (str)             Optional (e.g., "PROJ-002 • THE RESUME FACTORY")
        subtitle (str)            Optional (e.g., "Documentation | Meta | System")
        categories (list[str])    Optional (display lines under title)
        tags (list[str])          Optional (tag pills)
        status (str)              Optional (badge text: ACTIVE / LIVE / SHIPPED)
        next_step (str)           Optional
        date (str)                Optional (e.g., "December 13, 2025")
        is_dark (bool)            Optional explicit override
        data (dict)               Optional data-* attributes (e.g., {"project":"PROJ-002"})

    Returns:
        str: Raw HTML string.
    """
    import html

    def esc(s: str) -> str:
        return html.escape(str(s), quote=True)

    def slugify(s: str) -> str:
        # light slug normalizer for tag-trigger matching (not for URLs)
        s = str(s).strip().lower()
        return (
            s.replace("&", "and")
             .replace("—", "-")
             .replace("–", "-")
             .replace(" ", "-")
        )

    dark_trigger = set(slugify(t) for t in (dark_trigger_slugs or []))

    out = [f'<div class="{esc(wrapper_class)}">']

    for card in cards_data:
        title = card.get("title", "").strip()
        if not title:
            # Skip invalid cards silently; you can raise if you prefer.
            continue

        link = card.get("link", "#")
        eyebrow = card.get("eyebrow", "")
        subtitle = card.get("subtitle", "")
        categories = card.get("categories") or []
        tags = card.get("tags") or []
        status = card.get("status", "")
        next_step = card.get("next_step", "")
        date = card.get("date", "")

        # Determine dark mode
        is_dark = bool(card.get("is_dark", False))
        if not is_dark and dark_trigger and tags:
            tag_slugs = {slugify(t) for t in tags}
            if tag_slugs.intersection(dark_trigger):
                is_dark = True

        classes = ["st-card"]
        if is_dark:
            classes.append("st-card--dark")

        # Optional data-* attributes
        data_attrs = []
        if isinstance(card.get("data"), dict):
            for k, v in card["data"].items():
                if v is None:
                    continue
                data_attrs.append(f' data-{esc(k)}="{esc(v)}"')

        # Categories: render as stacked lines like your archive (“A | B” per line)
        categories_html = ""
        if categories:
            lines = []
            for line in categories:
                if not line:
                    continue
                # allow either a string "A | B" or a list/tuple ["A","B"]
                if isinstance(line, (list, tuple)):
                    line_text = " | ".join(str(x).strip() for x in line if str(x).strip())
                else:
                    line_text = str(line).strip()
                if line_text:
                    lines.append(esc(line_text))
            if lines:
                categories_html = (
                    '<div class="st-card__subtitle">'
                    + "<br>".join(lines) +
                    "</div>"
                )

        # Tags: “current tag pill classes”
        tags_html = ""
        if tags:
            pills = []
            for t in tags:
                t = str(t).strip()
                if not t:
                    continue
                pills.append(f'<a class="st-card__tag" href="#tag-{esc(slugify(t))}">{esc(t)}</a>')
            if pills:
                tags_html = (
                    '<div class="st-card__tags">'
                    + "".join(pills) +
                    "</div>"
                )

        # Badge
        badge_html = ""
        if status:
            badge_html = f'<span class="st-badge">{esc(status)}</span>'

        # Footer / next step
        footer_html = ""
        if next_step or date:
            footer_bits = []
            footer_bits.append('<div class="st-card__footer">')
            footer_bits.append('<div class="st-card__footer-title">Next Step:</div>')
            if next_step:
                footer_bits.append(f'<div class="st-card__action-text">{esc(next_step)}</div>')
            if date:
                footer_bits.append(f'<div class="st-card__date">{esc(date)}</div>')
            footer_bits.append("</div>")
            footer_html = "".join(footer_bits)

        card_html = f"""
<article class="{' '.join(classes)}"{''.join(data_attrs)}>
  <div class="st-card__header">
    <div class="st-card__eyebrow">{esc(eyebrow)}</div>
    {badge_html}
  </div>

  <h2 class="st-card__title"><a href="{esc(link)}">{esc(title)}</a></h2>

  {categories_html}

  {('<div class="st-card__subtitle">' + esc(subtitle) + '</div>') if subtitle and not categories_html else ''}

  {('<div class="st-card__tags-label st-label">Tags:</div>') if tags_html else ''}
  {tags_html}

  {footer_html}
</article>""".strip()

        out.append(card_html)

    out.append("</div>")
    return "\n".join(out)


# ==========================================
# EXAMPLE USAGE
# ==========================================
# cards = [
#   {
#     "title": "Architecture Deep Dive: Resume Factory v3.0",
#     "link": "/gem/resume-factory-v3",
#     "eyebrow": "PROJ-002 • THE RESUME FACTORY",
#     "categories": ["Product & Platform Strategy | Engineering & DX | ProductOps"],
#     "tags": ["architecture", "headless cms", "migration", "sanity"],
#     "status": "ACTIVE",
#     "next_step": "Finalize monorepo strategy",
#     "date": "December 13, 2025",
#     "data": {"project": "PROJ-002", "status": "active", "category": "architecture"},
#     # Optional dark toggle:
#     # "is_dark": True,
#   }
# ]
#
# html = generate_st_card_grid(cards, dark_trigger_slugs={"system", "meta", "architecture", "dx"})
