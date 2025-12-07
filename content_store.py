# --- SUGARTOWN CMS CONTENT STORE ---
# All 14 Gems. 
# Script Logic: New titles = Draft. Existing titles = Publish (Auto-Update).

all_gems = [
# GEM 1: The Hero Story (Architecture)
    {
        'id': 946,
        'title': 'Project: Sugartown CMS Architecture',
        'status': 'publish',
        'categories': ['Engineering & DX', 'Content Architecture'],
        'tags': ['headless CMS', 'content modeling', 'structured content', 'Sugartown'],
        'content': """
        <p>This project began with a simple request: <em>"Write a blog post about Gemini 3."</em> It spiraled into a full-stack engineering challenge because, as a Product Manager, I fundamentally reject unstructured data.</p>
        <h3>The Challenge: Breaking the Blob</h3>
        <p>Standard CMS platforms treat knowledge like a "blob"—a title and a body of text, buried in a chronological feed. I wanted a <strong>Knowledge Graph</strong>: a system where insights are treated as atomic, structured nodes that can be queried, filtered, and reused.</p>
        <h3>The Data Journey</h3>
        <p>We architected a "Headless Ingestion" pipeline. Instead of writing in WordPress, we write in Python (the Source of Truth) and push to the web via REST API. This created immediate conflicts:</p>
        <figure class="wp-block-table is-style-stripes has-small-font-size"><table>
        <thead><tr><th>Decision Point</th><th>The Conflict</th><th>The Resolution</th></tr></thead>
        <tbody>
        <tr><td><strong>Content Model</strong></td><td>Blog posts decay over time.</td><td><strong>Topology over Chronology.</strong> Created <code>Gem</code> Post Type to sort by topic, not date.</td></tr>
        <tr><td><strong>Source Control</strong></td><td>Manual WP edits vs. Script overwrites.</td><td><strong>The "Hybrid" Model.</strong> Script owns the structure; Humans own the "Polish."</td></tr>
        <tr><td><strong>Input Data</strong></td><td><code>.gdoc</code> files are not readable text.</td><td><strong>The ETL Pipeline.</strong> Script exports to PDF -> Text -> JSON before ingestion.</td></tr>
        <tr><td><strong>Presentation</strong></td><td>Theme templates display unwanted meta.</td><td><strong>Headless Templating.</strong> Custom Block Templates stripped of "Bloggy" bylines.</td></tr>
        </tbody></table><figcaption>Fig 1. The Architectural Decision Log.</figcaption></figure>
        <h3>The Outcome: Satisfaction</h3>
        <p>The result is a system that feels alive. I can refactor my entire portfolio by changing one line of Python. The "Green Checkmark" in the terminal has become my favorite UI.</p>
        
        <h3>Live Roadmap (Dec 2025)</h3>
        <p>We have shifted to a 12-week launch sprint. Here is the current status of the build:</p>
        
<pre class="mermaid">
gantt
title Sugartown Launch Roadmap
dateFormat YYYY-MM-DD
axisFormat %m/%d

section Phase 1 The Factory
Infrastructure and Repo Split     :done,    p1_infra, 2025-11-24, 4d
Pink Stink Theme and CSS          :done,    p1_design, after p1_infra, 4d
Headless Resume Engine            :done,    p1_resume, after p1_design, 3d

section Phase 2 Viz Ops
Visualization Engine Python       :active,  p2_viz,    2025-12-06, 5d
Automated Cover Letters           :         p2_cov,    after p2_viz, 5d
Smart Merge On Hold               :crit,    p2_merge,  after p2_cov, 1w

section Phase 3 Frontend
React Nextjs Evaluation           :         p3_react,  2026-01-05, 2w
Full Headless Migration           :         p3_mig,    after p3_react, 4w
</pre>
        """,
        'meta': {'gem_category': 'ProductOps', 'gem_status': 'Active', 'gem_action_item': 'Refine Taxonomy Visualization', 'gem_related_project': 'Sugartown.io v2'}
    },
    # GEM 2: The CSV Reality Check
    {
        'id': 942,
        'title': 'Process Insight: The CSV Reality Check',
        'status': 'publish',
        'categories': ['Engineering & DX', 'Product & Platform Strategy'],
        'tags': ['data integrity', 'audit', 'automation'],
        'content': """
        <p>I just ran my first full audit of the <strong>Sugartown CMS pipeline</strong>, exporting the raw database to a CSV report. The result? A lesson in data integrity.</p>
        <h3>The "Eyeballs" Theory</h3>
        <p>When working in the UI, it is easy to miss gaps. But when you flatten the data into a spreadsheet, the holes become obvious. For example, my "Market Scan" gem looked perfect on the frontend, but the CSV revealed it was an orphan in the database (NULL category).</p>
        <h3>The Annotated Findings</h3>
        <p>Here is a snippet of the export where I flagged the specific logic errors found in the data:</p>
        <figure class="wp-block-table is-style-stripes has-small-font-size"><table>
        <thead><tr><th>ID</th><th>Title</th><th>Category</th><th>Status</th><th>Action Item</th></tr></thead>
        <tbody>
        <tr><td>852</td><td>Market Scan: CMS</td><td><em>NULL</em></td><td><em>NULL</em></td><td><em>NULL</em></td></tr>
        <tr><td>863</td><td>Sweet Upgrades</td><td>AI Strategy</td><td>Done</td><td>Upgrade to Ultra (Wrong!)</td></tr>
        <tr><td>942</td><td>Process Insight</td><td>ProductOps</td><td>Active</td><td>Schedule Audit</td></tr>
        </tbody></table><figcaption>Fig 1. The CSV export annotated with audit findings.</figcaption></figure>
        <p><strong>The Takeaway:</strong> Automation requires observability. A script can push content, but only a human (or a very good audit script) can verify truth.</p>
        """,
        'meta': {'gem_category': 'ProductOps', 'gem_status': 'Active', 'gem_action_item': 'Schedule Monthly CSV Audit', 'gem_related_project': 'Sugartown.io v2'}
    },

    # GEM 3: The Overwrite Problem
    {
        'id': 949,
        'title': 'Architecture Decision: The "Overwrite" Risk in Sugartown CMS',
        'status': 'publish',
        'categories': ['Engineering & DX', 'Content Architecture'],
        'tags': ['headless CMS', 'Python', 'content ops', 'governance models'],
        'content': """<p>I had a realization today while trying to manually edit a post in WordPress: <strong>The Pipeline is a Bully.</strong></p><p>In a typical "Push" architecture (Python -> WordPress), the script is the Source of Truth. If I manually add a witty joke or a custom image inside the WordPress Editor, the next time I run my Python script, it will blow those changes away because it performs a <code>PUT</code> (Replace) operation, not a <code>PATCH</code> (Merge) operation.</p><h3>The Strategy: Hybrid Content Management</h3><p>To solve this, I am evaluating two patterns for "Safe Updates":</p><ul><li><strong>1. The "Protected Block" Pattern:</strong> Using HTML comments (e.g., <code>&lt;!-- manual-start --&gt;</code>) to mark zones that the script ignores.</li><li><strong>2. The "Read-Merge-Write" Pattern:</strong> The script must first GET the current content, diff it against the new payload, and intelligently merge them before pushing back.</li></ul><p><strong>Current Verdict:</strong> I have moved this feature to the <strong>Backlog</strong>. For now, the Python script owns the "Structured Data" (Tables, Lists), and I will manually sync content if needed.</p>""",
        'meta': {'gem_category': 'HeadlessCMS', 'gem_status': 'Backlog', 'gem_action_item': 'Research Python Diff Libraries', 'gem_related_project': 'Sugartown.io v2'}
    },

    # GEM 4: Resume Workflow
    {
        'id': 853,
        'title': 'Engineering the Perfect Resume Workflow',
        'status': 'publish',
        'categories': ['Engineering & DX', 'AI & Automation'],
        'tags': ['AI-assisted authoring', 'LLM workflows', 'structured content'],
        'content': """<p>As a Product Manager, I couldn't just "write" a resume. I had to architect a pipeline. After battling file formats and prompt hallucinations, here is the technical breakdown of my "Resume as Code" workflow.</p><blockquote class="wp-block-quote"><p><strong>Status: Active Prototype.</strong> While I currently manage this via local Python scripts, the roadmap includes migrating this schema to a true Headless CMS (Sanity or WordPress) to fully decouple the content model from the build pipeline.</p></blockquote><h3>The CI/CD Pipeline</h3><p>I treat my career history like a software product. It goes through a build process before deployment.</p><ul><li><strong>1. Source Control (Main Branch):</strong> The "Master Resume" Google Doc. Never sent, only referenced.</li><li><strong>2. Feature Branch (Tailoring):</strong> XML-bounded AI prompts used to "merge" specific skills into the narrative.</li><li><strong>3. Build Script (Python):</strong> <code>prep_resume.py</code> handles versioning and file conversion.</li><li><strong>4. Deployment (Release):</strong> SEO-optimized PDF sent to the recruiter.</li></ul><h3>The Editorial Experience</h3><p>Before the data hits the database, the "Authoring Experience" is defined by these strict governance rules to ensure quality and consistency.</p><figure class="wp-block-table is-style-stripes has-small-font-size"><table><thead><tr><th>Category</th><th>Insight / Rule</th><th>Context</th></tr></thead><tbody><tr><td><strong>Strategy</strong></td><td><strong>Resume as Code</strong></td><td>Treat your Master Resume as the <code>main</code> branch. Tailored applications are <code>feature</code> branches.</td></tr><tr><td><strong>Automation</strong></td><td><strong>The ".gdoc" Trap</strong></td><td>I learned the hard way that <code>.gdoc</code> files aren't real files. My Python script failed until I added an explicit "Export to PDF" step.</td></tr><tr><td><strong>Taxonomy</strong></td><td><strong>Dual-Naming</strong></td><td><strong>External:</strong> <code>Name_Role.pdf</code> (SEO for ATS).<br><strong>Internal:</strong> <code>Date_Name_Variant.pdf</code> (Version Control).</td></tr><tr><td><strong>AI</strong></td><td><strong>XML Prompting</strong></td><td>I wrap my source text in XML tags (<code>&lt;source&gt;</code>) to stop the AI from hallucinating fake jobs.</td></tr></tbody></table></figure>""",
        'meta': {'gem_category': 'Career Engineering', 'gem_status': 'In Progress', 'gem_action_item': 'Refine XML Prompt', 'gem_related_project': 'Job Hunt 2026'}
    },

    # GEM 5: Market Scan
    {
        'id': 852,
        'title': 'Market Scan: Top Headless CMS Platforms (2025)',
        'status': 'publish',
        'categories': ['Product & Platform Strategy', 'Content Architecture'],
        'tags': ['headless CMS', 'content modeling', 'PIM / PXM', 'content migration'],
        'content': """<p>As we move into 2026, the Headless CMS market has calcified into three segments: Developer Tools, Marketer Suites, and Visual Composers. Here is the breakdown.</p><figure class="wp-block-table is-style-stripes"><table><thead><tr><th>Platform</th><th>Founded</th><th>Free Tier?</th><th>Paid Start</th></tr></thead><tbody><tr><td><strong>Contentful</strong></td><td>2013</td><td>✅ Yes</td><td>$300/mo</td></tr><tr><td><strong>Sanity</strong></td><td>2018</td><td>✅ Yes</td><td>$15/seat</td></tr><tr><td><strong>Strapi</strong></td><td>2016</td><td>✅ Yes (Self-Hosted)</td><td>$99/mo</td></tr><tr><td><strong>Storyblok</strong></td><td>2017</td><td>✅ Yes</td><td>$108/mo</td></tr><tr><td><strong>Ghost</strong></td><td>2013</td><td>✅ Yes (Self-Hosted)</td><td>$9/mo</td></tr><tr><td><strong>Directus</strong></td><td>2015</td><td>✅ Yes (Self-Hosted)</td><td>$15/mo</td></tr><tr><td><strong>Contentstack</strong></td><td>2018</td><td>⚠️ Limited</td><td>~$995/mo</td></tr><tr><td><strong>Prismic</strong></td><td>2013</td><td>✅ Yes</td><td>$7/mo</td></tr><tr><td><strong>Hygraph</strong></td><td>2017</td><td>✅ Yes</td><td>$299/mo</td></tr><tr><td><strong>ButterCMS</strong></td><td>2014</td><td>❌ No</td><td>$99/mo</td></tr><tr><td><strong>Builder.io</strong></td><td>2018</td><td>✅ Yes</td><td>$24/user</td></tr></tbody></table></figure>""",
        'meta': {'gem_category': 'Market Research', 'gem_status': 'Active', 'gem_action_item': 'Update Tech Radar Slide', 'gem_related_project': '2026 Strategy'}
    },

    # GEM 6: The Confession
    {
        'id': 952,
        'title': 'Confession: I Don\'t Hate Blogs, I Just Hate Unstructured Data',
        'status': 'publish',
        'categories': ['Content Architecture', 'Sugartown Notes'],
        'tags': ['structured content', 'taxonomy', 'metadata strategy'],
        'content': """<p>My AI architect recently pointed out a flaw in my new site strategy: <em>"Why are you so down on blogs?"</em></p><p>It’s a fair question. I’ve spent the last week rigorously separating my "Field Notes" from my "Blog," treating the latter like a second-class citizen. But I want to clarify: I don't hate blogs. I hate <strong>Flat Content Models</strong>.</p><h3>The Problem with "The Feed"</h3><p>In a standard CMS, a Blog Post is designed to decay. It is sorted <strong>Chronologically</strong>. Its primary metadata is <em>Time</em>. This is great for news ("We raised Series A!"), but it is terrible for Knowledge ("How to configure Webpack").</p><h3>The Solution: The Gem Node</h3><p>By moving my technical insights into a <strong>Knowledge Graph</strong> (Custom Post Type), I am sorting them <strong>Topologically</strong> (by Topic and Relevance), not Chronologically.</p><figure class="wp-block-table is-style-stripes has-small-font-size"><table><thead><tr><th>Feature</th><th>The Blog Post</th><th>The Knowledge Node</th></tr></thead><tbody><tr><td><strong>Primary Metric</strong></td><td>Recency (When?)</td><td>Relevance (What?)</td></tr><tr><td><strong>Data Structure</strong></td><td>Blob (Title + Body)</td><td>Structured (Status, Project, Tech Stack)</td></tr><tr><td><strong>Lifespan</strong></td><td>Decays over time</td><td>Evergreen (Updated via API)</td></tr><tr><td><strong>User Intent</strong></td><td>"Entertain me."</td><td>"I need an answer."</td></tr></tbody></table></figure><h3>The Verdict</h3><p>I still write blog posts. I use them for <strong>Narrative</strong>—stories about my career, culture, and opinion. But I use my Knowledge Graph for <strong>Assets</strong>—proof of my technical competence.</p>""",
        'meta': {'gem_category': 'Content Strategy', 'gem_status': 'Active', 'gem_action_item': 'Make peace with the blog', 'gem_related_project': 'Sugartown.io v2'}
    },

    # GEM 7: Data Viz
    {
        'id': 950,
        'title': 'Data Science: Visualizing the Knowledge Graph',
        'status': 'publish', 
        'categories': ['Engineering & DX', 'AI & Automation'],
        'tags': ['Python', 'data visualization', 'knowledge graph', 'Sugartown'],
        'content': """<p>A Knowledge Graph isn't just a metaphor; it's a data structure. To visualize the relationships between my Projects, Categories, and Gems, I used Python's <code>networkx</code> library to generate a force-directed graph.</p>
        
        <figure class="wp-block-image size-large">
            <img src="https://sugartown.io/wp-content/uploads/2025/11/knowledge_graph-scaled.png" alt="Sugartown Knowledge Graph Visualization" />
            <figcaption>Fig 1. The live Sugartown content topology, generated via Python.</figcaption>
        </figure>

        <h3>The Logic</h3><p>The script iterates through the <code>content_store.py</code> (the same one used to publish this website), extracts the metadata, and builds nodes and edges. It then uses a spring-layout algorithm to cluster related concepts together.</p><pre class="wp-block-code"><code>import networkx as nx\n# Connect Projects to Root (to create the cluster effect)\nG.add_edge(gem['project'], root_node)\n# Setup Layout (Force-directed)\npos = nx.spring_layout(G, k=0.6, iterations=50)</code></pre><p>This visualization serves as the definitive map of my "Headless Content Supply Chain."</p>""",
        'meta': {'gem_category': 'Data Science', 'gem_status': 'Draft', 'gem_action_item': 'Render Graph on Frontend', 'gem_related_project': 'Sugartown.io v2'}
    },

    # GEM 8: Documentation Strategy
    {
        'id': 953,
        'title': 'Strategy: Documentation Roadmap & Status',
        'status': 'publish', 
        'categories': ['Ways of Working', 'Product & Platform Strategy'],
        'tags': ['systemic documentation', 'governance models', 'agile workflows'],
        'content': """<p>This document serves as the strategic blueprint for capturing the intellectual property of the project. It is prioritized to ensure the most critical "Bus Factor" documentation exists immediately (Day 1), while deeper architectural references follow (Day 2).</p><h3>Documentation Status Tracker</h3><figure class="wp-block-table is-style-stripes has-small-font-size"><table><thead><tr><th>Phase</th><th>Asset</th><th>Goal</th><th>Status</th><th>Artifact / Location</th></tr></thead><tbody><tr><td><strong>Day 1</strong><br>(Critical)</td><td><strong>README.md</strong></td><td>Repo entry point & Quick Start.</td><td>✅ <strong>Done</strong></td><td><code>README.md</code> (Git Root)</td></tr><tr><td><strong>Day 1</strong></td><td><strong>User Workflow</strong></td><td>Prevent "Overwrite" data loss.</td><td>🟡 <strong>In Progress</strong></td><td><a href="/gem/architecture-decision-the-overwrite-risk-in-sugartown-cms">Gem: Overwrite Risk</a></td></tr><tr><td><strong>Day 1</strong></td><td><strong>Tech Requirements</strong></td><td>Environment consistency.</td><td>✅ <strong>Done</strong></td><td><code>README.md</code> & <code>requirements.txt</code></td></tr><tr><td><strong>Day 2</strong><br>(Product)</td><td><strong>Content Model</strong></td><td>Define Gem structure/schema.</td><td>✅ <strong>Done</strong></td><td><code>content_store.py</code> (The Schema Source)</td></tr><tr><td><strong>Day 2</strong></td><td><strong>System Arch</strong></td><td>Visual proof of data flow.</td><td>✅ <strong>Done</strong></td><td><a href="/gem/project-sugartown-cms-architecture">Gem: Architecture</a></td></tr><tr><td><strong>Day 2</strong></td><td><strong>Feature List</strong></td><td>"Sales Sheet" of capabilities.</td><td>✅ <strong>Done</strong></td><td><a href="/gem/project-sugartown-cms-architecture">Gem: Architecture</a></td></tr></tbody></table></figure><h3>Next Actions</h3><ul><li><strong>Immediate:</strong> Create the Markdown file for "User Workflow" to formalize the manual vs. script rules.</li><li><strong>Next:</strong> Generate the Mermaid.js graph for the System Architecture visual.</li></ul>""",
        'meta': {'gem_category': 'ProductOps', 'gem_status': 'Active', 'gem_action_item': 'Draft User Workflow MD', 'gem_related_project': 'Sugartown.io v2'}
    },

    # GEM 9: Diagram Tools
    {
        'id': 954,
        'title': 'Market Scan: Top AI Tools for Data & Architecture Diagrams',
        'status': 'publish', 
        'categories': ['Product & Platform Strategy', 'AI & Automation'],
        'tags': ['generative UI', 'dashboards', 'interaction patterns'],
        'content': """<p>We just finished architecting a Headless CMS pipeline, which naturally led to the next question: <em>"How do we visualize this?"</em></p><p>The "best" AI diagramming tool depends entirely on your output goal: Do you need a <strong>System Blueprint</strong> (architecture/flow) or a <strong>Data Visualization</strong> (charts/trends)? Here is the breakdown of the current market leaders.</p><h3>The Comparison: Diagrams as Code vs. Data Analysis</h3><figure class="wp-block-table is-style-stripes"><table><thead><tr><th>Category</th><th>Tool</th><th>Best For</th><th>Vibe/Output</th><th>Cost / Free Tier</th></tr></thead><tbody><tr><td><strong>Architecture</strong></td><td><strong>Eraser.io</strong></td><td>Engineering teams mapping system flows from code.</td><td>Technical "Dark Mode" Blueprints.</td><td>Free (3 Files) / $10/mo</td></tr><tr><td><strong>Architecture</strong></td><td><strong>Mermaid.js (via AI)</strong></td><td>Embedding diagrams directly into <code>README.md</code> files.</td><td>Code-based, version-controllable text.</td><td>Open Source (Free) / $10/mo (Pro)</td></tr><tr><td><strong>Data Viz</strong></td><td><strong>ChatGPT (Canvas)</strong></td><td>Analyzing CSVs to find trends and outliers.</td><td>Python-generated PNG charts (matplotlib).</td><td>Free (Limited) / $20/mo (Plus)</td></tr><tr><td><strong>Data Viz</strong></td><td><strong>Julius AI</strong></td><td>Building live, professional data dashboards.</td><td>Polished business intelligence dashboards.</td><td>Free (15 msgs/mo) / $20/mo</td></tr><tr><td><strong>Concepts</strong></td><td><strong>Napkin.ai</strong></td><td>Quick visual summaries for blog posts.</td><td>Clean, hand-drawn "sketch" style.</td><td>Free (Beta) / $10/mo</td></tr><tr><td><strong>Concepts</strong></td><td><strong>Claude (Artifacts)</strong></td><td>Generating interactive flows alongside chat.</td><td>React components or SVG diagrams.</td><td>Free / $20/mo (Pro)</td></tr></tbody></table></figure><h3>The Product Manager's Take</h3><p>For the <strong>Sugartown CMS project</strong>, the recommendation is clear:</p><ul><li><strong>Use Eraser.io</strong> to map the "Content Supply Chain" (Python -> WordPress -> Frontend). It perfectly matches our "Resume as Code" and DevOps aesthetic.</li><li><strong>Use ChatGPT (Canvas)</strong> to analyze the weekly <code>gems_report.csv</code> export to track content velocity and identify metadata gaps.</li></ul>
        
        <figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio">
            <div class="wp-block-embed__wrapper">
                <iframe title="ChatGPT Canvas Mode is Now FREE for Everyone!" width="500" height="281" src="https://www.youtube.com/embed/2tmvLdI3qIc?feature=oembed" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
            </div>
            <figcaption>See ChatGPT Canvas in action (Video: 10 mins)</figcaption>
        </figure>
        """,
        'meta': {'gem_category': 'Market Research', 'gem_status': 'Draft', 'gem_action_item': 'Create System Diagram in Eraser.io', 'gem_related_project': 'Sugartown.io v2'}
    },
    
    # GEM 10: Sweet Upgrades
    {
        'id': 863,
        'title': 'Sweet Upgrades: Why Gemini 3 is the Cherry on Top',
        'status': 'publish',
        'categories': ['AI & Automation', 'Product & Platform Strategy'],
        'tags': ['agentic interfaces', 'LLM workflows', 'AI-assisted authoring'],
        'content': """
        <p>We’ve all been there—living comfortably in our standard Google Accounts. But with the release of <strong>Gemini 3 Pro</strong> this week, the question isn’t just “Do I need an AI?”—it’s “Am I ready to upgrade from a bicycle to a rocket ship?”</p>
        <p>I’m sharing here because it took me an ungodly amount of time and lots of gemini’ing to get a straight answer out of Google (HELLO!).</p>
        <h3>🍭 Comparison: The Gemini 3 Hierarchy (Nov 2025)</h3>
        <figure class="wp-block-table is-style-stripes has-small-font-size"><table>
        <thead><tr><th>Feature</th><th>Google AI Premium<br>(Personal)</th><th>Workspace Business Standard<br>(The Team Essential)</th><th>Google AI Ultra for Business<br>(The Power-User Tier)</th></tr></thead>
        <tbody>
        <tr><td><strong>Primary Purpose</strong></td><td>Individual Productivity:<br>For freelancers, students, and general use.</td><td>Team Collaboration:<br>For core business ops, secure email, and docs.</td><td>Heavy Compute / R&D:<br>For architects, data scientists, and media pros.</td></tr>
        <tr><td><strong>Price</strong></td><td>$19.99 / month</td><td>Included in Workspace<br>(~$14.40 / user / mo)</td><td>🚀 <strong>$250.00 / user / month</strong><br>(The “VIP” Add-on)</td></tr>
        <tr><td><strong>Model Name</strong></td><td>Gemini 3 Pro</td><td>Gemini 3 Pro</td><td>Gemini 3 Ultra</td></tr>
        <tr><td><strong>Reasoning Engine</strong></td><td>Standard Reasoning<br>(Fast logic checks)</td><td>Standard Reasoning<br>(Fast logic checks)</td><td>🧠 <strong>Deep Think</strong><br>(Ph.D. level “Chain of Thought”)</td></tr>
        <tr><td><strong>Deep Think Mode</strong></td><td>❌ Not Included</td><td>❌ Not Included</td><td>✅ Included<br>(Can “think” for minutes on complex tasks)</td></tr>
        <tr><td><strong>Storage</strong></td><td>2 TB</td><td>2 TB (Pooled)</td><td>30 TB<br>(Massive Archive)</td></tr>
        <tr><td><strong>Project Mariner</strong><br>(Agentic Research)</td><td>❌ Not Included</td><td>❌ Not Included</td><td>✅ Included<br>(Autonomous Multi-Tasking Agent)</td></tr>
        <tr><td><strong>Video AI (Veo)</strong></td><td>Standard (Veo 2)</td><td>Standard (Veo 2)</td><td>Pro Studio (Veo 3)<br>(1080p, unlimited generation)</td></tr>
        <tr><td><strong>Data Privacy</strong></td><td>👎 Consumer Grade<br>(Used for training)</td><td>👍 Enterprise Grade<br>(Private)</td><td>👍 Enterprise Grade<br>(Private + Advanced Compliance)</td></tr>
        </tbody></table></figure>
        <h4>“Why is AI Ultra $250/month?!”</h4>
        <p>If you are staring at that price tag in shock, you aren’t the target audience—and that’s okay! With the <strong>$250 AI Ultra</strong> plan you are paying for:</p>
        <ul>
        <li><strong>Deep Think:</strong> The ability to solve novel architectural problems that stump standard models.</li>
        <li><strong>Project Mariner:</strong> An autonomous agent that can browse the web, navigate complex UI, and complete tasks (like “Research the pricing of these 50 competitors and put them in a spreadsheet”) while you sleep.</li>
        <li><strong>30 TB of Storage:</strong> This alone used to cost nearly $150/mo.</li>
        </ul>
        <p><strong>My Recommendation:</strong> Stick to <strong>Personal Premium ($20)</strong> or <strong>Workspace Business Standard ($14 per user)</strong> for 99% of your work. Only upgrade to <strong>Ultra</strong> if you need the AI to <em>solve</em> problems, not just <em>answer</em> them.</p>
        """,
        'meta': {'gem_category': 'AI Strategy', 'gem_status': 'Done', 'gem_action_item': 'Stick to Personal Premium', 'gem_related_project': 'Tech Stack Eval'}
    },

# GEM 11: The Recursion (Meta-Analysis)
    {
        'id': 977,
        'title': 'Meta-Analysis: Am I Crazy for Building This?',
        'status': 'publish',
        'categories': ['Sugartown Notes', 'Ways of Working'],
        'tags': ['product operations', 'content ops', 'Sugartown'],
        'content': """
        <p>I just spent my Thanksgiving break architecting a Python-based ETL pipeline to inject structured data into a WordPress Block Theme, solely to update my resume. Is this over-engineering? Or is it art?</p>
        <h3>The Symptom</h3>
        <p>Instead of just opening a Google Doc and typing "Updated: Nov 2025," I built a system that parses PDFs into CSVs, uses AI to "explode" bullet points into atomic data rows, and then re-assembles them based on a schema.</p>
        <blockquote class="wp-block-quote"><p><strong>The Diagnosis:</strong> Chronic Product Ops Syndrome. The inability to do a task without first building a system to do the task for you.</p></blockquote>
        <h3>The "Cute" Result</h3>
        <p>But look at this <a href="https://sugartown.io/gem/data-science-visualizing-the-knowledge-graph/">beautiful, structured data</a>. My career history is no longer a flat document; it is a queryable database. I can now ask: <em>"Show me every time I mentioned 'API' between 2018 and 2022,"</em> and get a precise answer. That is power. That is leverage. That is... maybe a little crazy. 🍒</p>
        """,
        'meta': {'gem_category': 'Personal Reflection', 'gem_status': 'Done', 'gem_action_item': 'Go eat leftover turkey', 'gem_related_project': 'Sugartown.io v2'}
    },

    # GEM 12: The Great Re-Platforming (The Layoff Retro)
    {
        'id': 993,
        'title': 'Status Update: The Great Re-Platforming',
        'status': 'publish',
        'categories': ['Product & Platform Strategy', 'Ways of Working'],
        'tags': ['portfolio', 'stakeholder alignment', 'cross-functional collaboration'],
        'content': """
        <p><strong>Status:</strong> <code>Migration in Progress</code> | <strong>Priority:</strong> <code>Critical</code> | <strong>Sprint:</strong> <code>The Hustle</code></p>
        
        <h3>Executive Summary</h3>
        <p>The stakeholder (Me) has been forcibly decoupled from the legacy backend (The Beauty Retailer). While the "Job Security" microservice has experienced unexpected downtime, this presents a strategic opportunity to refactor the core value proposition. I am shifting from a single-tenant architecture to a multi-tenant consulting mindset (or at least, getting hired by a better tenant).</p>
        
        <h3>Root Cause Analysis</h3>
        <ul>
            <li><strong>Legacy Dependency:</strong> The previous employer decided to "optimize resources" (read: bad decision-making).</li>
            <li><strong>System Failure:</strong> The connection to the payroll API was severed.</li>
        </ul>

        <h3>The Pivot Strategy</h3>
        <p>We are taking the IP generated during the "Beauty Retailer Era"—the headless CMS knowledge, the design system governance, the stakeholder management—and repackaging it. We aren't just looking for a job; we are launching "Me 2.0."</p>

        <figure class="wp-block-table is-style-stripes has-small-font-size"><table>
        <thead><tr><th>Metric</th><th>Legacy State</th><th>Future State (Target)</th></tr></thead>
        <tbody>
        <tr><td><strong>Architecture</strong></td><td>Monolithic Employee</td><td>Agile Product Leader</td></tr>
        <tr><td><strong>Availability</strong></td><td>9-to-5 Locked</td><td>High Availability (Immediate Start)</td></tr>
        <tr><td><strong>Cheekiness</strong></td><td>Corporate Moderated</td><td>Unbounded</td></tr>
        </tbody></table></figure>

        <h3>Action Item</h3>
        <p>Use AI to transform "I got laid off" into "I successfully delivered a complex digital transformation and am now seeking new challenges," while quietly judging the old architecture.</p>
        """,
        'meta': {
            'gem_category': 'Career Strategy', 
            'gem_status': 'Active', 
            'gem_action_item': 'Update LinkedIn Profile', 
            'gem_related_project': 'Job Hunt 2026'
        }
    },

    # GEM 13: The DevOps Upgrade
    {
        'id': 994, # Devops upgrade
        'title': 'DevOps: Building the "Undo" Button for My Career',
        'status': 'publish',
        'categories': ['Engineering & DX', 'Ways of Working'],
        'tags': ['QA workflows', 'systemic documentation', 'governance models'],
        'content': """
        <p>I realized this week that my "Resume as Code" project had a fatal flaw: <strong>It was dangerous.</strong></p>
        <p>Because I manage my personal brand via a Python script that overwrites my database, a single syntax error or bad API call could wipe my entire digital existence. So, I spent the weekend building a proper DevOps safety net.</p>
        
        <h3>The Upgrade: Observability & Resilience</h3>
        <p>I refactored the core engine (`publish_gem.py`) to include three enterprise-grade features:</p>
        
        <h4>1. The "Panic Button" (Rollback Protocol)</h4>
        <p>Before the script touches the API, it now creates a timestamped backup of both the <strong>Data</strong> (content) and the <strong>Logic</strong> (script). I built a companion script (`revert_changes.py`) that can restore the system to its "Last Known Good" state in seconds.</p>
        
        <h4>2. MD5 Hashing (Smart Diffs)</h4>
        <p>Previously, the script blindly updated every post, every time. Now, it calculates an MD5 hash of the content. If the hash hasn't changed, it sleeps. This reduces API calls by 90% and keeps the logs clean.</p>
        <pre class="wp-block-code"><code># The Logic:
if existing_id and content_state.get(id) == current_hash:
    print(f"💤 Skipped (No Changes): {gem['title']}")</code></pre>
        
        <h4>3. System Integrity Checks</h4>
        <p>The script is now self-aware. It tracks changes to its own code base. If I edit the Python logic, the system logs a <code>[CODE UPDATE]</code> event to the changelog, creating an audit trail of my engineering decisions.</p>
        
        <h3>Why This Matters</h3>
        <p>This isn't just about code; it's about <strong>Risk Management</strong>. Whether you are deploying a Fortune 500 design system or just updating your resume, you need the confidence to move fast without breaking things.</p>
        """,
        'meta': {
            'gem_category': 'Engineering', 
            'gem_status': 'Shipped', 
            'gem_action_item': 'Test the Panic Button', 
            'gem_related_project': 'Sugartown.io v2'
        }
    },

# GEM 14: The Sugartown Digital Ecosystem (Architecture v1.0)
    {
        # 'id': 996, # Local ID
        'title': 'Architecture: The Sugartown Digital Ecosystem (v1.0)',
        'status': 'publish',
        'categories': ['Engineering & DX', 'Content Architecture'],
        'tags': ['headless CMS', 'Sugartown', 'systemic documentation', 'governance models'],
        'content': """
        <p><strong>Status:</strong> <code>Production</code> | <strong>Version:</strong> <code>1.0</code> | <strong>Repo:</strong> <code>2025-sugartown-pink</code></p>
        
        <h3>Executive Summary</h3>
        <p>This ecosystem represents the "Digital Factory" for Sugartown.io. It creates a strict separation of concerns between <strong>Content</strong> (The "Brain"), <strong>Code</strong> (The Theme/Repo), and <strong>Assets</strong> (The Storage). The goal is a resilient, portable, and headless-ready architecture that allows for safe experimentation locally before deploying to production.</p>

        <h3>1. The 3-Zone Architecture</h3>
        <figure class="wp-block-table is-style-stripes has-small-font-size"><table>
        <thead><tr><th>Zone</th><th>Location</th><th>Role</th></tr></thead>
        <tbody>
        <tr><td><strong>Zone 1: The Vault</strong><br>(Storage & Assets)</td><td>Google Drive<br><code>00 SUGARTOWN 25</code></td><td><strong>Canonical Source of Truth</strong> for heavy assets and raw data.<br><em>Key Folder:</em> <code>01_PORTFOLIO_MASTER/sugartown_cms</code> (Headless content source).</td></tr>
        <tr><td><strong>Zone 2: The Factory</strong><br>(Local Development)</td><td>Local Mac<br><code>~/SUGARTOWN_DEV/</code></td><td><strong>The Sandbox</strong> where code is written and designs are tested.<br><em>Tool:</em> LocalWP running <code>sugartown.local</code>.</td></tr>
        <tr><td><strong>Zone 3: The Stage</strong><br>(Production)</td><td>Pair.com Hosting<br><code>sugartown.io</code></td><td><strong>The Public Display Layer.</strong><br><em>Rule:</em> Code flows UP (Local -> Prod). Content flows DOWN (Prod -> Local).</td></tr>
        </tbody></table></figure>

        <h3>2. The "Sugartown Pink" Theme</h3>
        <p>A custom hybrid Block Theme that merges visual design with functional logic.</p>
        <ul>
        <li><strong>Base:</strong> Twenty Twenty-Five (TT5).</li>
        <li><strong>Visuals:</strong> Custom "Pink" branding and Grid Layouts saved via <code>theme.json</code> and block templates.</li>
        <li><strong>Logic:</strong> <code>functions.php</code> handles data structures, specifically the <strong>Case Study CPT</strong> registration.</li>
        <li><strong>Templates:</strong> <code>archive-case-study.html</code> (3-Column Grid) and <code>single-case-study.html</code>.</li>
        </ul>

        <h3>3. The DevOps Workflow</h3>
        <p>How we ship changes without breaking the site:</p>
        <pre class="wp-block-code"><code># 1. Design: Make visual changes in Site Editor.
# 2. Extract: Use "Create Block Theme" to save DB changes to files.
# 3. Version (Git):
git add .
git commit -m "Update visual templates"
git push origin main
# 4. Deploy: Upload the 'sugartown-pink' folder to Pair.com.</code></pre>

        <h3>4. Critical Configurations</h3>
        <ul>
        <li><strong>Database Prefix:</strong> <code>SERVMASK_PREFIX_</code> (Inherited from Prod).</li>
        <li><strong>Local URL:</strong> <code>http://localhost:10003</code> (Hardcoded in <code>wp-config.php</code> via <code>WP_HOME</code>).</li>
        <li><strong>Custom Post Types:</strong> "Case Studies" registered via code in <code>functions.php</code> with slug <code>/case-studies/</code>.</li>
        </ul>
        """,
        'meta': {
            'gem_category': 'Engineering', 
            'gem_status': 'Shipped', 
            'gem_action_item': 'Move to Ticket B (Resume Model)', 
            'gem_related_project': 'Sugartown.io v2'
        }
    },
# GEM 15: The Two-Repo Solution
    {
        # 'id': 1050, <--- Comment out until generated
        'title': 'Architecture Decision: The Two-Repo Solution (Theme vs. Content)',
        'status': 'publish',
        'categories': ['Engineering & DX', 'Ways of Working'],
        'tags': ['git', 'source control', 'headless CMS', 'Sugartown'],
        'content': """
        <p>I hit a wall today where my local Git commits weren't showing up in my repository. The root cause? I was trying to treat my <strong>Theme</strong> (Visuals) and my <strong>Content</strong> (Data) as the same entity. They are not.</p>
        
        <h3>The Separation of Concerns</h3>
        <p>We have officially split the Sugartown codebase into two distinct repositories to prevent "Monolith Drift."</p>
        
        <figure class="wp-block-table is-style-stripes has-small-font-size"><table>
        <thead><tr><th>Repository</th><th>Scope</th><th>Lifecycle</th><th>Owner</th></tr></thead>
        <tbody>
        <tr><td><code>2025-sugartown-pink</code></td><td><strong>The Theme (Code)</strong><br>PHP, HTML Templates, CSS, JS.</td><td><strong>Slow & Stable.</strong><br>Updates only when design changes.</td><td>Engineering</td></tr>
        <tr><td><code>sugartown-content-engine</code></td><td><strong>The Brain (Data)</strong><br>Python Scripts, Content Store, CSVs.</td><td><strong>Fast & Fluid.</strong><br>Updates daily with new thoughts/gems.</td><td>Product</td></tr>
        </tbody></table></figure>

        <h3>The "Stale Pointer" Incident</h3>
        <p>The confusion arose because my local folder was named <code>sugartown_cms</code> but my Git remote was still pointing to <code>second-brain-cms</code>. This "Stale Pointer" meant I was pushing code to a ghost location.</p>
        
        <p><strong>The Fix:</strong> We renamed the GitHub repository to match the architectural intent (<code>sugartown-content-engine</code>) and updated the local Git remotes to align. The Digital Factory is now clean, decoupled, and ready for scaling.</p>
        """,
        'meta': {
            'gem_category': 'Engineering', 
            'gem_status': 'Shipped', 
            'gem_action_item': 'Verify Git Remotes', 
            'gem_related_project': 'Sugartown.io v2'
        }
    },
# GEM 16: The Taxonomy Strategy
    {
        # 'id': 1060, <--- Comment out until generated
        'title': 'Architecture: The Unified Taxonomy Strategy',
        'status': 'publish',
        'categories': ['Content Architecture', 'Product & Platform Strategy'],
        'tags': ['taxonomy', 'metadata strategy', 'structured content', 'Sugartown'],
        'content': """
        <p>A headless CMS is useless if you can't find anything inside it. Today, we implemented the <strong>Unified Taxonomy Strategy</strong> for Sugartown.io, ensuring that our content is connected by <em>meaning</em>, not just <em>date</em>.</p>
        
        <h3>The Architecture</h3>
        <p>We rejected the standard "Free Tagging" chaos in favor of a controlled vocabulary imported via XML.</p>
        
        <figure class="wp-block-table is-style-stripes has-small-font-size"><table>
        <thead><tr><th>Asset Type</th><th>Taxonomy Support</th><th>Flow Direction</th></tr></thead>
        <tbody>
        <tr><td><strong>Gems</strong></td><td>✅ Categories & Tags</td><td><strong>Python -> WP.</strong> The script assigns IDs based on name lookups.</td></tr>
        <tr><td><strong>Case Studies</strong></td><td>✅ Categories & Tags</td><td><strong>Manual -> WP.</strong> Curated by hand in the editor.</td></tr>
        <tr><td><strong>Posts (Blog)</strong></td><td>✅ Categories & Tags</td><td><strong>Legacy.</strong> Inherits standard WP structure.</td></tr>
        </tbody></table></figure>

        <h3>The Core Categories</h3>
        <p>We standardized on 8 high-level buckets to organize the "Product Operations" brain:</p>
        <ul>
        <li><strong>Engineering & DX:</strong> The "How" (DevOps, Pipelines, Git).</li>
        <li><strong>Content Architecture:</strong> The "Structure" (Headless, Models, Schema).</li>
        <li><strong>Product & Platform Strategy:</strong> The "Why" (Roadmaps, Market Scans).</li>
        <li><strong>AI & Automation:</strong> The "Accelerator" (LLMs, Agents).</li>
        <li><strong>UX, UI & Interaction:</strong> The "Feel" (Design Systems, Figma).</li>
        <li><strong>Ways of Working:</strong> The "Process" (Agile, Team Topology).</li>
        <li><strong>Sugartown Notes:</strong> Meta-commentary on this project.</li>
        </ul>

        <h3>The Implementation Details</h3>
        <p>To make this work, we had to update the <code>register_post_type</code> arguments in <code>functions.php</code> to explicitly support <code>'taxonomies' => array('category', 'post_tag')</code>. Without this line, Case Studies are siloed islands. With it, they join the connected graph.</p>
        """,
        'meta': {
            'gem_category': 'Content Strategy', 
            'gem_status': 'Shipped', 
            'gem_action_item': 'Tag all historic Case Studies', 
            'gem_related_project': 'Sugartown.io v2'
        }
    },
# GEM 17: The Resume Factory & Pink Stink
    {
        # 'id': 1070, <--- Comment out until generated
        'title': 'Feature: The Resume Factory & The "Pink Stink" Design System',
        'status': 'publish',
        'categories': ['Engineering & DX', 'UX, UI & Interaction'],
        'tags': ['resume builder', 'python', 'design systems', 'css', 'Sugartown'],
        'content': """
        <p>We have officially closed the loop on two major capabilities for the Sugartown ecosystem: a headless engine for my career history and a distinct visual identity for the site.</p>
        
        <h3>1. The Resume Factory</h3>
        <p>I stopped updating my resume in Microsoft Word. Instead, I treated my career history as a dataset. We built a <strong>Headless Resume Pipeline</strong> that separates <em>Content</em> from <em>Presentation</em>.</p>
        
        <ul>
        <li><strong>The Golden Record:</strong> A single JSON file (<code>master_resume_data.json</code>) containing every job, skill, and bullet point I've ever written, deduplicated and structured.</li>
        <li><strong>The Builder:</strong> A Python script (<code>build_resume.py</code>) that reads the JSON and compiles it into a clean, formatted Markdown document ready for PDF export or ATS ingestion.</li>
        <li><strong>The Win:</strong> I can now generate a "Product Manager" version or a "Design Systems" version of my resume instantly without copy-pasting a single line.</li>
        </ul>

        <h3>2. The "Sugartown Pink" Theme</h3>
        <p>We deployed a custom WordPress Block Theme (child of Twenty Twenty-Five) to enforce a strict but playful visual language. The goal was <strong>"Subtle Tech"</strong>—a hacker aesthetic that doesn't feel like a terminal window.</p>
        
        <h4>Visual Upgrades:</h4>
        <figure class="wp-block-table"><table>
        <thead><tr><th>Component</th><th>Style</th><th>CSS Tweak</th></tr></thead>
        <tbody>
        <tr><td><strong>Code Blocks</strong></td><td><strong>"The Terminal"</strong></td><td>Dark mode background, neon pink accent border, and <code>2.5rem</code> padding for breathability.</td></tr>
        <tr><td><strong>Inline Code</strong></td><td><strong>"The Pill"</strong></td><td><code>git init</code> now renders with a cool gray background and deep magenta text to pop against prose.</td></tr>
        <tr><td><strong>Tables</strong></td><td><strong>"The Zebra"</strong></td><td>Pink headers, alternating row stripes, and collapsed borders for high-density data.</td></tr>
        </tbody></table></figure>

        <p>This completes the <strong>Infrastructure Phase</strong>. The factory is open, the machines are running, and the paint is dry.</p>
        """,
        'meta': {
            'gem_category': 'Engineering', 
            'gem_status': 'Shipped', 
            'gem_action_item': 'Generate PDF from JSON', 
            'gem_related_project': 'Job Hunt 2026'
        }
    },
# GEM 18: PRD - The Visualization Engine (Phase 2)
    {
        # 'id': 1080, <--- Comment out until generated
        'title': 'PRD: The Visualization Engine (Phase 2)',
        'status': 'publish',
        'categories': ['Engineering & DX', 'Product & Platform Strategy'],
        'tags': ['PRD', 'requirements', 'python', 'visualization', 'data science'],
        'content': """
        <p><strong>Status:</strong> <code>In Progress</code> | <strong>Phase:</strong> <code>2.0</code> | <strong>Owner:</strong> <code>Product Ops</code></p>
        
        <h3>Executive Summary</h3>
        <p>Phase 1 established the "Content Engine" (Text). Phase 2 establishes the "Visualization Engine" (Images). We are building a suite of Python scripts that auto-generate insights from our own data.</p>

        <h3>Core Requirements</h3>
        <figure class="wp-block-table"><table>
        <thead><tr><th>Requirement</th><th>The "Why"</th><th>Technical Implementation</th></tr></thead>
        <tbody>
        <tr><td><strong>1. Source Agnosticism</strong></td><td>Scripts must work without manual file selection.</td><td>Scripts automatically scan <code>output/reports/</code> and pick the file with the latest timestamp (e.g., <code>gems_report_2025-12-05.csv</code>).</td></tr>
        <tr><td><strong>2. Idempotent Output</strong></td><td>Links in blog posts must never break.</td><td>Scripts always overwrite a "Latest" file alias (e.g., <code>knowledge_graph_latest.png</code>). We do NOT timestamp filenames like <code>graph_v4.png</code>.</td></tr>
        <tr><td><strong>3. Single Responsibility</strong></td><td>Debugging monoliths is painful.</td><td>One script per chart type (e.g., <code>viz_network.py</code>, <code>viz_barchart.py</code>).</td></tr>
        </tbody></table></figure>

        <h3>The Architecture</h3>
        <pre class="wp-block-code"><code># The Flow:
WordPress API -> export_gems.py -> CSV Report -> [Viz Scripts] -> PNG Artifacts

# The Artifacts:
output/visuals/knowledge_graph_latest.png  (The Network)
output/visuals/category_dist_latest.png    (The Bar Chart)</code></pre>

        <h3>Success Criteria</h3>
        <p>A "Green Checkmark" run of the visualization suite automatically updates the images embedded in live Gems without requiring a WordPress edit.</p>
        """,
        'meta': {
            'gem_category': 'Product Management', 
            'gem_status': 'Draft', 
            'gem_action_item': 'Build viz_barchart.py', 
            'gem_related_project': 'Sugartown.io v2'
        }
    },
# GEM 19: The Sugartown 2.0 System Contract
    {
        'id': 1094, 
        'title': 'Architecture Insight: The Sugartown 2.0 System Contract',
        'status': 'publish',
        'categories': ['Engineering & DX', 'Content Architecture'],
        'tags': ['headless architecture', 'python', 'content ops', 'design systems', 'governance'],
        'content': """
        <p><strong>Sugartown 2.0 establishes a non-negotiable architecture:</strong> Python is the single source of truth; WordPress is a stateless rendering layer.</p>

        <p>This eliminates CMS drift, enables reproducibility, and prepares the platform for a headless future.</p>

        <h3>Core Principles</h3>
        <ul>
        <li><strong>Python as Canonical:</strong> All content, metadata, and tokens exist in <code>sugartown-cms</code>. If it is not in Python, it does not exist.</li>
        <li><strong>WordPress as Renderer:</strong> WP holds no unique content; it displays structured data via custom templates.</li>
        <li><strong>Structured Gem Model:</strong> Gems are topological knowledge nodes, not posts in a feed.</li>
        <li><strong>Two-Repo Boundary:</strong> <code>sugartown-cms</code> (content, logic, tokens) vs. <code>2025-sugartown-pink</code> (presentation).</li>
        <li><strong>Mini Design System:</strong> Tokens define a portable visual identity shared across WP, Figma, and future React front ends.</li>
        <li><strong>Reproducible Publishing:</strong> Hashing, backups, and visualization scripts ensure deterministic builds.</li>
        </ul>

        <h3>Repository Structure</h3>
        <p>The codebase enforces a strict separation of concerns between the Content Engine (Data) and the Rendering Layer (Theme).</p>

<pre class="mermaid">
---
config:
  look: neo
  theme: neutral
  themeVariables:
    primaryColor: "#FE1295"
    primaryBorderColor: "#FF2E8F"
    primaryTextColor: "#0D1226"
    secondaryColor: "#e6fffa" 
    tertiaryColor: "#fff0f6"
    lineColor: "#0D1226"
    mainBkg: "#ffffff"
    clusterBkg: "#F9FAFB"
    clusterBorder: "#0D1226"
---
flowchart TD
    %% Define Styles
    classDef python fill:#fff0f6,stroke:#FE1295,stroke-width:2px,color:#0D1226
    classDef data fill:#e6fffa,stroke:#2BD4AA,stroke-width:2px,color:#0D1226
    classDef wp fill:#f0f2f5,stroke:#0D1226,stroke-width:2px,stroke-dasharray: 5 5,color:#0D1226

    subgraph CMS["sugartown-cms (SoT)"]
        direction TB
        A[("content_store.py")]:::python
        B[["publish_gem.py"]]:::python
        C[/"sugartown.tokens.json"\]:::data
        D[["Viz Scripts"]]:::python
        E[["export_tokens.py"]]:::data

        A --> B
        A --> C
        B --> D
        C --> E
    end

    subgraph WP["2025-sugartown-pink (Renderer)"]
        direction TB
        F("Gem Custom Post Type"):::wp
        G("theme.json / CSS"):::wp
    end

    %% Connections
    B ==>|REST API| F
    D -.->|PNG Artifacts| F
    E -- JSON --> G
</pre>

        <h3>Reference Artifacts</h3>
        <p>The following strategic documents govern the execution of this architecture:</p>
        
        <figure class="wp-block-table is-style-stripes"><table>
        <thead><tr><th>Artifact</th><th>Format</th><th>Scope</th><th>Location</th></tr></thead>
        <tbody>
        <tr><td><strong>Sugartown 2.0 Master PRD</strong></td><td>Markdown</td><td>Full requirements, user stories, and acceptance criteria.</td><td><a href="https://github.com/bex-sugartown/sugartown-cms/blob/main/docs/sugartown_2_PRD.md">View on GitHub</a></td></tr>
        <tr><td><strong>Jira Execution Plan</strong></td><td>Markdown</td><td>Epic breakdown, ticket dependencies, and sprint waves.</td><td><a href="https://github.com/bex-sugartown/sugartown-cms/blob/main/docs/sugartown_2_jira.md">View on GitHub</a></td></tr>
        <tr><td><strong>Content Store</strong></td><td>Python</td><td>The literal database file for this post.</td><td><code>content_store.py</code></td></tr>
        </tbody></table></figure>

        <h3>Why This Matters</h3>
        <p>By treating content as code, Sugartown CMS transforms static pages into a programmable dataset. This elevates the platform from a simple management tool into a <strong>knowledge engine</strong>—structured, portable, and platform-agnostic.</p>
        """,
        'meta': {
            'gem_category': 'Product & Platform Strategy', 
            'gem_status': 'Active', 
            'gem_action_item': 'Maintain Python as canonical source', 
            'gem_related_project': 'Sugartown.io v2'
        }
    },
]
