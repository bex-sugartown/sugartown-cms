# Knowledge Graph Visualization Options

**Project:** Sugartown.io Knowledge Graph  
**Date:** December 2025  
**Status:** Decision needed

---

## Option 1: Force-Directed Network Graph (RECOMMENDED)

### Visual Concept
```
        [PROJ-001: Sugartown CMS]
       /        |        \        \
      /         |         \        \
  [Gem 1]   [Gem 2]   [Gem 3]   [Gem 4]
     |          |         |         |
     └──────────┴─────────┴─────────┘
              [Tag: Python]


        [PROJ-002: Resume Factory]
           /              \
       [Gem 5]          [Gem 6]
          |                |
          └────────────────┘
           [Tag: AI-assisted]
```

### What It Shows
- **Large pink nodes** = Projects
- **Small cyan nodes** = Gems
- **Lines** = Relationships (gem → project, gem → tag)
- **Clusters** = Naturally groups related content
- **Distance** = Semantic similarity (shared tags pull gems closer)

### Interactions
- **Click project** → Filter to show only that project's gems
- **Click gem** → Navigate to gem detail page
- **Hover node** → Show tooltip (title, status, tags)
- **Click tag** → Highlight all gems with that tag
- **Zoom/Pan** → Explore large graphs
- **Search** → Find and highlight nodes

### Technical Stack
- **D3.js** (v7) - Force simulation
- **Or Vis.js Network** - Pre-built network graphs
- **Data format:** JSON (nodes + edges)

### Pros
✅ Best for showing "topology over chronology"  
✅ Naturally clusters by project/tags  
✅ Scales to 100+ gems  
✅ Interactive and exploratory  
✅ Aligns with "Knowledge Graph" branding  
✅ Can layer multiple relationship types  

### Cons
❌ Can get messy with many connections  
❌ Requires good physics tuning (repulsion/attraction)  
❌ Not great for showing hierarchy  
❌ Performance can degrade with 500+ nodes  

### Best For
- Showing semantic relationships
- Exploring connections between gems
- "How does X relate to Y?"
- Discovery and serendipity

### Code Snippet
```javascript
// Using Vis.js Network
const nodes = new vis.DataSet([
  {id: 'PROJ-001', label: 'Sugartown CMS', group: 'project'},
  {id: 1335, label: 'Pre-Design System', group: 'gem'}
]);

const edges = new vis.DataSet([
  {from: 1335, to: 'PROJ-001'}
]);

const network = new vis.Network(container, {nodes, edges}, options);
network.on('click', params => {
  if (params.nodes.length > 0) {
    const nodeId = params.nodes[0];
    // Handle click
  }
});
```

---

## Option 2: Hierarchical Tree / Sunburst

### Visual Concept
```
                    Sugartown Digital
                    /       |        \
                   /        |         \
          PROJ-001      PROJ-002    PROJ-003
         /    |    \       |   \        |
        /     |     \      |    \       |
   Eng  Content  Ops   Career  Eng   Design
    |      |      |      |      |       |
  [Gems] [Gems] [Gems] [Gems] [Gems]  [Gem]
```

**Or as Sunburst (circular hierarchy):**
```
         ┌─────────────┐
         │   Center:   │
         │  Knowledge  │
         │    Graph    │
         └─────────────┘
        /       |       \
   Ring 1:   Projects
      /          |          \
 Ring 2:    Categories
    /             |             \
Ring 3:         Gems
```

### What It Shows
- **Levels:** Root → Projects → Categories → Gems
- **Size:** Proportional to number of gems
- **Color:** By project or category
- **Angle:** Distribution of gems across categories

### Interactions
- **Click segment** → Zoom into that branch
- **Hover** → Show stats (count, status breakdown)
- **Breadcrumbs** → Navigate back up hierarchy
- **Filter** → Show only Active/Shipped gems

### Technical Stack
- **D3.js Hierarchy** - Collapsible tree
- **D3.js Partition** - Sunburst diagram
- **Data format:** Nested JSON

### Pros
✅ Clear hierarchy (Projects → Categories → Gems)  
✅ Shows proportions visually  
✅ Good for understanding structure  
✅ Familiar pattern (file explorer, org chart)  
✅ Easy to navigate (zoom in/out)  

### Cons
❌ Doesn't show cross-cutting relationships (tags)  
❌ Forces single hierarchy (what if gem has 2 categories?)  
❌ Less "exploratory" feeling  
❌ Doesn't align with "topology" philosophy  

### Best For
- Showing project organization
- Understanding content distribution
- "How many gems in each project/category?"
- Executive overview / dashboards

### Code Snippet
```javascript
// D3.js Collapsible Tree
const hierarchy = d3.hierarchy(data);
const treeLayout = d3.tree().size([height, width]);
const root = treeLayout(hierarchy);

svg.selectAll('.link')
  .data(root.links())
  .enter().append('path')
  .attr('d', d3.linkHorizontal());

svg.selectAll('.node')
  .data(root.descendants())
  .enter().append('circle')
  .on('click', (event, d) => {
    // Toggle children
  });
```

---

## Option 3: Tag-Based Semantic Network

### Visual Concept
```
    [Python] ──┬── Architecture Update
               ├── Data Science Viz
               ├── DevOps Undo Button
               └── CSV Reality Check

    [Headless CMS] ──┬── System Contract
                     ├── Market Scan
                     └── Two-Repo Solution

    [Automation] ──┬── Resume Factory
                   ├── AI Assistant
                   └── Gemini 3

         (Tags connect gems with shared topics)
```

### What It Shows
- **Tag nodes** = Central hubs (larger)
- **Gem nodes** = Satellites (smaller)
- **Lines** = "Gem uses this tag"
- **Clusters** = Topics that often co-occur
- **Distance** = Tag frequency (popular tags are central)

### Interactions
- **Click tag** → Show all gems with that tag
- **Click gem** → Navigate to detail
- **Hover tag** → Highlight connected gems
- **Filter by project** → Gray out other projects
- **Slider** → Min tag frequency (hide rare tags)

### Technical Stack
- **Cytoscape.js** - Network analysis library
- **Sigma.js** - Fast graph rendering
- **Data format:** Graph (nodes + edges)

### Pros
✅ Shows semantic relationships (shared topics)  
✅ Great for discovering related content  
✅ Answers "What else talks about X?"  
✅ Visualizes tag co-occurrence  
✅ Useful for content strategy (identify gaps)  

### Cons
❌ Can be overwhelming with many tags  
❌ Doesn't show project structure  
❌ Requires tag cleanup (synonyms, stemming)  
❌ Gems with no tags are isolated  

### Best For
- Content discovery
- Finding related gems
- "Show me everything about Python"
- Identifying content clusters

### Code Snippet
```javascript
// Cytoscape.js
const cy = cytoscape({
  container: document.getElementById('graph'),
  elements: [
    {data: {id: 'python', type: 'tag', label: 'Python'}},
    {data: {id: '1335', type: 'gem', label: 'Pre-Design System'}},
    {data: {source: '1335', target: 'python'}}
  ],
  style: [
    {selector: 'node[type="tag"]', style: {size: 30}},
    {selector: 'node[type="gem"]', style: {size: 10}}
  ]
});
```

---

## Comparison Matrix

| Feature | Force-Directed | Hierarchical | Tag Network |
|---------|---------------|--------------|-------------|
| **Shows Projects** | ✅ Large nodes | ✅ Top level | ⚠️ Can add as filter |
| **Shows Hierarchy** | ❌ Flat network | ✅ Clear levels | ❌ Flat network |
| **Shows Tags** | ⚠️ Can add | ❌ Not typically | ✅ Primary feature |
| **Shows Connections** | ✅ Multi-type | ⚠️ Parent-child only | ✅ Tag-based |
| **Exploration** | ✅ Excellent | ⚠️ Limited to path | ✅ Excellent |
| **Scalability** | ✅ 100+ nodes | ✅ 500+ nodes | ⚠️ 50+ tags max |
| **Learning Curve** | ⚠️ Medium | ✅ Low (familiar) | ⚠️ Medium |
| **Implementation** | ⚠️ Medium | ⚠️ Medium | ❌ Complex |
| **Performance** | ✅ Good | ✅ Excellent | ⚠️ Good |
| **Mobile Friendly** | ⚠️ Touch gestures | ✅ Zoom/pan | ⚠️ Touch gestures |

---

## Hybrid Approach (Best of All Worlds)

### Concept: Tabbed Views
```
┌──────────────────────────────────────────────┐
│ [Projects] [Tags] [Timeline]                  │
├──────────────────────────────────────────────┤
│                                               │
│   [Force-directed graph showing projects]    │
│                                               │
└──────────────────────────────────────────────┘

User clicks "Tags" tab:
┌──────────────────────────────────────────────┐
│ [Projects] [Tags] [Timeline]                  │
├──────────────────────────────────────────────┤
│                                               │
│   [Tag network showing semantic clusters]    │
│                                               │
└──────────────────────────────────────────────┘
```

**Benefits:**
- ✅ Show multiple perspectives on same data
- ✅ Let users choose preferred view
- ✅ Each view optimized for specific questions

**Drawbacks:**
- ❌ More complex to build
- ❌ Three times the code
- ❌ Requires good tab design

---

## Recommendation: Start with Option 1 (Force-Directed)

### Why Force-Directed Network?
1. **Best fit for "topology over chronology"** - Shows relationships, not timeline
2. **Aligns with Knowledge Graph branding** - Looks like a graph
3. **Flexible** - Can show projects, tags, or both
4. **Interactive** - Click, hover, filter, search
5. **Proven pattern** - Users understand network graphs

### Implementation Plan
**Phase 1:** Basic force-directed graph
- Projects as large nodes
- Gems as small nodes
- Lines = membership

**Phase 2:** Add interactivity
- Click → navigate
- Hover → tooltip
- Filter → highlight

**Phase 3:** Layer in tags
- Tag nodes (medium size)
- Gem-tag edges (dashed lines)
- Toggle layers on/off

**Phase 4:** Polish
- Physics tuning
- Color scheme
- Performance optimization

### Data Transformation
```python
# graph_generator.py (simplified)
import pandas as pd
import json

df = pd.read_csv('gems_report.csv')

nodes = []
edges = []

# Add project nodes
for proj_id in df['project_id'].unique():
    proj_name = df[df['project_id']==proj_id]['project_name'].iloc[0]
    nodes.append({
        'id': proj_id,
        'label': proj_name,
        'type': 'project',
        'size': 40,
        'color': '#FF69B4'  # Sugartown Pink
    })

# Add gem nodes
for _, row in df.iterrows():
    nodes.append({
        'id': row['id'],
        'label': row['title'],
        'type': 'gem',
        'size': 15,
        'color': '#00CED1',  # Cyan
        'url': row['link'],
        'status': row['gem_status']
    })
    
    # Add edge: gem → project
    edges.append({
        'from': row['id'],
        'to': row['project_id']
    })

# Save graph
with open('knowledge_graph.json', 'w') as f:
    json.dump({'nodes': nodes, 'edges': edges}, f)
```

---

## Decision Checklist

Before choosing, answer these:

- [ ] **Primary use case?** Discovery or navigation?
- [ ] **Users more interested in:** Projects or topics?
- [ ] **Number of gems expected:** 50? 100? 500+?
- [ ] **Update frequency:** Static or live data?
- [ ] **Target audience:** Technical (developers) or general (readers)?
- [ ] **Mobile important?** Touch interactions needed?
- [ ] **Development time:** Quick (1 week) or thorough (4 weeks)?

**If you answered:**
- Discovery, Topics, 100+, Live, General → **Force-Directed**
- Navigation, Projects, 500+, Static, Technical → **Hierarchical**
- Discovery, Topics, 50, Static, Technical → **Tag Network**

---

## Next Steps

1. **Choose visualization type** (Force-Directed recommended)
2. **Define interactions** (What happens on click/hover?)
3. **Choose library** (D3.js, Vis.js, Cytoscape.js)
4. **Design color scheme** (Projects vs. Gems vs. Tags)
5. **Generate code** (graph_generator.py + graph.js)

**Once decided, I can generate:**
- Complete Python script to transform CSV → JSON
- Complete JavaScript to render interactive graph
- HTML/CSS to embed on your page
- Documentation on customization

**Ready to decide?** Let me know which option (or hybrid) you prefer!
