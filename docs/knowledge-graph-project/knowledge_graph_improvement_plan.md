# Knowledge Graph Improvement Plan
**Project:** Sugartown.io Knowledge Graph Homepage Redesign  
**Date:** December 2025  
**Status:** Planning Phase

---

## 🎯 Project Goals

### Current State Issues
- Cards are date-sorted (contradicts "topology over chronology" philosophy)
- Limited metadata visibility (project info missing)
- No filtering/navigation by taxonomy
- Static visualization (not leveraging structured data)

### Target State
1. ✅ Display Project ID + Name on gem cards
2. ✅ Clickable project/category/tag filters → archive pages
3. ✅ Dynamic, interactive knowledge graph visualization from CSV data

---

## 📋 What I Need to Know

### 1. Current Technical Stack
**Questions:**
- [ ] What's generating the homepage? (Python script, WordPress template, static site generator?)
- [ ] Where does the card HTML get rendered? (Template file location?)
- [ ] How is the CSV generated? (Python script that queries WordPress?)
- [ ] Is there a build process or is it dynamic on page load?

**Why this matters:** Determines whether we modify templates, write new Python scripts, or add JavaScript.

---

### 2. Project/Category/Tag Data Structure

**From CSV, I can see:**
- `project_id` (e.g., PROJ-001, PROJ-002)
- `project_name` (e.g., "Sugartown Headless CMS", "The Resume Factory")
- `internal_category` (e.g., "Engineering", "Product Management")
- `wp_categories` (WordPress categories, HTML-encoded)
- `wp_tags` (WordPress tags, HTML-encoded)

**Questions:**
- [ ] Should archive pages filter by:
  - Project ID/Name? (e.g., `/project/PROJ-001/`)
  - Internal Category? (e.g., `/category/engineering/`)
  - WP Categories? (e.g., `/wp-category/content-architecture/`)
  - WP Tags? (e.g., `/tag/python/`)
  - All of the above?
  
- [ ] Do you want a unified taxonomy or separate archive types?
  - Option A: `/archive/?project=PROJ-001` (query params)
  - Option B: `/project/PROJ-001/`, `/category/engineering/`, `/tag/python/` (separate pages)
  
- [ ] Are WordPress category/tag pages already working? (If yes, we just link to them)

---

### 3. Card Layout & Design

**Current cards show (from screenshot):**
- Title
- Project ID (e.g., "Project: PROJ-002")
- Date (e.g., "01_Jun_2025")

**Questions:**
- [ ] Where should Project Name appear? (Below project ID? Replace it? Tooltip?)
- [ ] Should gem_status (Active/Shipped/Draft) be visible?
- [ ] Should action_item be visible? (Or only on detail page?)
- [ ] Do you want status badges (🟢 Active, 🔵 Shipped, 🟡 Draft)?

**Design decision needed:**
```
Option A: Compact
┌─────────────────────────────┐
│ [Title]                     │
│ PROJ-002 • Resume Factory   │
│ Engineering • 01_Jun_2025   │
└─────────────────────────────┘

Option B: Detailed
┌─────────────────────────────┐
│ [Title]                     │
│ Project: PROJ-002           │
│ The Resume Factory          │
│ Category: Engineering       │
│ Status: 🟢 Active           │
│ 01_Jun_2025                 │
└─────────────────────────────┘
```

---

### 4. Archive Page Functionality

**Questions:**
- [ ] Should archive pages have the same card layout as homepage?
- [ ] Should they show count? (e.g., "12 Gems in PROJ-001")
- [ ] Should they be sortable? (By date, title, status?)
- [ ] Should they have breadcrumbs? (e.g., Home > Projects > PROJ-001)

**Example archive page structure:**
```
┌─────────────────────────────────────────┐
│ Home > Projects > PROJ-001              │
│                                         │
│ Sugartown Headless CMS                  │
│ 14 Gems • Status: Active                │
│                                         │
│ [Filters: All | Active | Shipped]       │
│                                         │
│ [Gem Card]  [Gem Card]  [Gem Card]      │
│ [Gem Card]  [Gem Card]  [Gem Card]      │
└─────────────────────────────────────────┘
```

---

### 5. Knowledge Graph Visualization

**From CSV, we have relationships:**
- Project → Gems (one-to-many)
- Category → Gems (one-to-many)
- Tags → Gems (many-to-many)
- Status → Gems (grouping)

**Questions:**
- [ ] What should nodes represent?
  - Projects as large nodes?
  - Gems as smaller nodes?
  - Categories/tags as connectors?
  
- [ ] What should edges represent?
  - Project membership?
  - Tag relationships?
  - Temporal sequence?
  
- [ ] Should it be:
  - **Force-directed graph** (D3.js, like your current viz)
  - **Hierarchical tree** (Project → Category → Gems)
  - **Network diagram** (Gems connected by shared tags)
  - **Timeline with connections** (Date-based with category overlays)

**Visualization library options:**
- D3.js (most flexible, requires custom code)
- Vis.js Network (pre-built graph layouts)
- Cytoscape.js (network analysis focused)
- React Flow (if using React)

**Clickable behavior:**
- Click node → Navigate to gem detail or archive page?
- Hover node → Show tooltip with metadata?
- Filter by project/category → Highlight subgraph?

---

## 🏗️ Technical Implementation Plan

### Phase 1: Data Layer (Week 1)
**Goal:** Ensure CSV has all needed fields

**Tasks:**
1. ✅ Verify CSV contains: `project_id`, `project_name`, `internal_category`, `wp_categories`, `wp_tags`
2. Add `display_order` field to CSV (replace hardcoded order=-1 hack)
3. Add `card_visibility` field (show/hide certain gems from homepage)
4. Generate `project_metadata.json` from CSV:
   ```json
   {
     "PROJ-001": {
       "name": "Sugartown Headless CMS",
       "count": 14,
       "status": "Active",
       "categories": ["Engineering", "Content Strategy"],
       "tags": ["headless cms", "Python", "structured content"]
     }
   }
   ```

**Deliverable:** Updated CSV schema + metadata JSON

---

### Phase 2: Card Layout Update (Week 2)
**Goal:** Display project metadata on cards

**Tasks:**
1. Update card template to include:
   - Project ID + Name (clickable)
   - Internal Category (clickable if filtering enabled)
   - Status badge (optional)
2. Add CSS for new layout
3. Test responsive behavior

**Deliverable:** Updated card HTML/CSS

---

### Phase 3: Archive Pages (Week 3-4)
**Goal:** Create filterable archive views

**Approach A: WordPress Native (if using WP)**
- Create custom page templates for:
  - `archive-project.php` (filters by project_id)
  - `archive-internal-category.php` (filters by internal_category)
- Reuse existing WP category/tag archives
- Modify query to filter gems by metadata

**Approach B: Python-Generated Static Pages**
- Generate HTML for each:
  - `project/PROJ-001/index.html`
  - `category/engineering/index.html`
  - `tag/python/index.html`
- Use Jinja2 templates
- Deploy as static files

**Approach C: Client-Side JavaScript**
- Single-page filter with JS:
  - Load all gems JSON on page
  - Filter/sort client-side
  - Update URL with `?project=PROJ-001`
- Fastest for users, no server changes

**Recommendation:** Start with Approach C (easiest), migrate to A or B if needed.

**Deliverable:** Working archive pages with filters

---

### Phase 4: Knowledge Graph Viz (Week 5-6)
**Goal:** Interactive graph generated from CSV

#### Option 1: Force-Directed Network (Recommended)
**Technology:** D3.js or Vis.js

**Data transformation:**
```python
# graph_generator.py
import pandas as pd
import json

df = pd.read_csv('gems_report_2025-12-10.csv')

nodes = []
edges = []

# Create project nodes
projects = df.groupby('project_id')['project_name'].first()
for proj_id, proj_name in projects.items():
    nodes.append({
        'id': proj_id,
        'label': proj_name,
        'type': 'project',
        'size': 30,
        'color': '#FF69B4'  # Sugartown Pink
    })

# Create gem nodes
for _, row in df.iterrows():
    nodes.append({
        'id': row['id'],
        'label': row['title'],
        'type': 'gem',
        'size': 10,
        'color': '#00CED1',  # Cyan
        'url': row['link']
    })
    
    # Create edge: gem → project
    edges.append({
        'from': row['id'],
        'to': row['project_id']
    })

# Output graph JSON
graph = {'nodes': nodes, 'edges': edges}
with open('knowledge_graph.json', 'w') as f:
    json.dump(graph, f)
```

**Frontend implementation:**
```javascript
// knowledge-graph.js
fetch('knowledge_graph.json')
  .then(res => res.json())
  .then(data => {
    const network = new vis.Network(container, data, options);
    
    network.on('click', function(params) {
      if (params.nodes.length > 0) {
        const nodeId = params.nodes[0];
        const node = data.nodes.find(n => n.id === nodeId);
        
        if (node.type === 'gem') {
          window.location.href = node.url;
        } else if (node.type === 'project') {
          window.location.href = `/project/${node.id}/`;
        }
      }
    });
  });
```

**Interactive features:**
- Click project node → Filter to show only that project's gems
- Click gem node → Navigate to gem detail page
- Hover → Show tooltip with metadata
- Zoom/pan → Explore large graph
- Search box → Highlight matching nodes

**Deliverable:** Interactive graph embedded on homepage

---

#### Option 2: Hierarchical Tree View
**Use case:** If you want clear project hierarchy

```
PROJ-001: Sugartown CMS (14 gems)
  ├── Engineering (8)
  │   ├── Architecture Decision: Two-Repo
  │   └── DevOps: Undo Button
  ├── Content Strategy (4)
  └── ProductOps (2)

PROJ-002: Resume Factory (5 gems)
  ├── Engineering (2)
  └── Career Strategy (3)
```

**Technology:** D3.js Collapsible Tree or React Tree View

---

#### Option 3: Tag-Based Network
**Use case:** Show how gems connect via shared tags

```
[Python] ──┬── Architecture Update: Resume Factory
           ├── Data Science: Visualizing the Graph
           └── DevOps: Building the Undo Button

[Headless CMS] ──┬── Sugartown System Contract
                 └── Market Scan: Top Headless CMS
```

**Technology:** Cytoscape.js (best for semantic networks)

---

## 🗂️ Project Tracking Structure

### Documentation You'll Need
Since I don't have persistent memory across months, create these files:

**1. `PROJECT_CONTEXT.md`** (This file - keep updated!)
- Current status
- Decisions made
- Next steps

**2. `TECHNICAL_SPECS.md`**
- CSV schema
- API endpoints (if any)
- File locations

**3. `DESIGN_DECISIONS.md`**
- Card layout choice
- Color scheme
- Interaction patterns

**4. `CHANGELOG.md`**
- Date + what changed
- Links to commits

**5. `OPEN_QUESTIONS.md`**
- Blockers
- Decisions needed

### How to Work with Me Across Months
1. **Start each session:** Upload `PROJECT_CONTEXT.md` + recent work
2. **I'll ask:** "What's changed since last time?"
3. **End each session:** I'll update `PROJECT_CONTEXT.md` with new decisions
4. **You track:** Git commits, implementation progress

---

## 📊 Visualization Recommendation

Based on your data structure, I recommend **Option 1: Force-Directed Network** because:

✅ Shows topology (not chronology)  
✅ Clusters gems by project naturally  
✅ Can layer categories/tags as node colors  
✅ Interactive (click to filter/navigate)  
✅ Scales to 100+ gems  
✅ Aligns with "Knowledge Graph" branding  

**Mockup concept:**
```
     [PROJ-001]          [PROJ-002]
    /    |    \             |    \
 [Gem] [Gem] [Gem]       [Gem] [Gem]
   \     |     /            
    [shared-tag: Python]
```

- Large pink nodes = Projects
- Small cyan nodes = Gems
- Lines = Membership
- Hover = Metadata tooltip
- Click = Navigate

---

## ⏭️ Next Steps (Decision Points)

### 🔴 Critical Decisions Needed:
1. **What generates your homepage?** (Python, WordPress, other?)
2. **Archive page approach:** Client-side JS filter or server-side pages?
3. **Card layout:** Compact or detailed? (See options above)
4. **Graph type:** Force-directed, hierarchical, or tag-network?

### 🟡 Nice-to-Have Decisions:
5. Should gem_status be visible on cards?
6. Should action_items be visible?
7. Color scheme for graph nodes?
8. Should graph replace card view or complement it?

### 🟢 Once Decided, I Can Provide:
- Updated Python scripts for data processing
- HTML/CSS for card layouts
- JavaScript for graph visualization
- Archive page templates
- Testing checklist

---

## 💾 Answering Your Key Questions

### "What do you need to know?"
**See sections above:** Technical stack, data structure, design preferences, archive page behavior, graph type.

### "Are you saving all this info for a months-long project?"
**No, but we can work around it:**

❌ I don't have persistent memory between sessions  
✅ Solution: Keep a `PROJECT_CONTEXT.md` file (this document)  
✅ Each session: Upload context + recent work  
✅ I'll update the context file with decisions made  
✅ You track progress in Git  

**Workflow:**
```
Session 1 (Dec 2025):
- You: Upload current state
- We: Make design decisions
- I: Generate card layout code
- You: Implement + commit

Session 2 (Jan 2026):
- You: Upload PROJECT_CONTEXT.md + "I finished cards, need archive pages"
- I: Review your code, generate archive templates
- You: Implement + commit

Session 3 (Feb 2026):
- You: Upload context + "Archive done, need graph viz"
- I: Generate graph.js code
- You: Implement + ship!
```

---

## 🎯 Recommended Timeline

| Week | Phase | Deliverable |
|------|-------|-------------|
| 1 | Data audit | Updated CSV schema + metadata JSON |
| 2 | Card redesign | New card layout with project info |
| 3-4 | Archive pages | Filterable project/category/tag views |
| 5-6 | Graph viz | Interactive knowledge graph |
| 7 | Polish | Responsive, accessibility, testing |

**Total:** ~7 weeks for all three features

---

## 📁 Files I Can Generate Next

Once you answer the critical questions above, I can create:

1. `card_template_v2.html` - Updated gem card layout
2. `graph_generator.py` - CSV → JSON transformer
3. `knowledge_graph.js` - Interactive graph code
4. `archive_page_template.html` - Filterable gem list
5. `project_metadata_generator.py` - Project stats from CSV
6. `styles_knowledge_graph.css` - Graph + card styling

**What do you want to tackle first?**
