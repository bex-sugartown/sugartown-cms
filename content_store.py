# --- SUGARTOWN CMS CONTENT STORE ---
# All 7 Gems. 
# Script Logic: New titles = Draft. Existing titles = Publish (Auto-Update).

all_gems = [
    # GEM 1: The Hero Story (Architecture)
    {
        'title': 'Project: Sugartown CMS Architecture',
        'status': 'publish', # <--- LIVE
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
        <p>The result is a system that feels alive. I can refactor my entire portfolio by changing one line of Python. The "Green Checkmark" in the terminal has become my favorite UI:</p>
        <pre class="wp-block-code"><code>beckyalice@Barnabas second-brain-cms % python3 publish_gem.py    
🚀 Processing 7 Gems...
🔄 Updating Existing Gem: Market Scan: Top Headless CMS Platforms (2025) (ID: 852)...
   ✅ Success: https://sugartown.io/?post_type=gem&p=852
✨ Creating New Gem: Visualizing the Knowledge Graph (ID: 994)...
   ✅ Success: https://sugartown.io/?post_type=gem&p=994
✨ Done!</code></pre>
        <h3>Future Roadmap</h3>
        <ul>
        <li><strong>Q1:</strong> Migrate "Master Resume" from Google Docs to Markdown/Git.</li>
        <li><strong>Q2:</strong> Implement "Smart Merge" so manual WP edits aren't overwritten.</li>
        <li><strong>Q3:</strong> Explore a true React frontend (Next.js) consuming this WP API.</li>
        <li><strong>Q4:</strong> Codify the <strong>"Mini Design System"</strong> (Header/Footer Patterns & Tokenized CSS) to ensure brand consistency across templates.</li>
        </ul>
        """,
        'meta': {'gem_category': 'ProductOps', 'gem_status': 'Active', 'gem_action_item': 'Refine Taxonomy Visualization', 'gem_related_project': 'Sugartown.io v2'}
    },

    # GEM 2: The CSV Reality Check
    {
        'title': 'Process Insight: The CSV Reality Check',
        'status': 'publish', # <--- LIVE
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
        'title': 'Architecture Decision: The "Overwrite" Risk in Sugartown CMS',
        'status': 'publish', # <--- LIVE
        'content': """<p>I had a realization today while trying to manually edit a post in WordPress: <strong>The Pipeline is a Bully.</strong></p><p>In a typical "Push" architecture (Python -> WordPress), the script is the Source of Truth. If I manually add a witty joke or a custom image inside the WordPress Editor, the next time I run my Python script, it will blow those changes away because it performs a <code>PUT</code> (Replace) operation, not a <code>PATCH</code> (Merge) operation.</p><h3>The Strategy: Hybrid Content Management</h3><p>To solve this, I am evaluating two patterns for "Safe Updates":</p><ul><li><strong>1. The "Protected Block" Pattern:</strong> Using HTML comments (e.g., <code>&lt;!-- manual-start --&gt;</code>) to mark zones that the script ignores.</li><li><strong>2. The "Read-Merge-Write" Pattern:</strong> The script must first GET the current content, diff it against the new payload, and intelligently merge them before pushing back.</li></ul><p><strong>Current Verdict:</strong> I have moved this feature to the <strong>Backlog</strong>. For now, the Python script owns the "Structured Data" (Tables, Lists), and I will manually sync content if needed.</p>""",
        'meta': {'gem_category': 'HeadlessCMS', 'gem_status': 'Backlog', 'gem_action_item': 'Research Python Diff Libraries', 'gem_related_project': 'Sugartown.io v2'}
    },

    # GEM 4: Resume Workflow
    {
        'title': 'Engineering the Perfect Resume Workflow',
        'status': 'publish', # <--- LIVE
        'content': """<p>As a Product Manager, I couldn't just "write" a resume. I had to architect a pipeline. After battling file formats and prompt hallucinations, here is the technical breakdown of my "Resume as Code" workflow.</p><blockquote class="wp-block-quote"><p><strong>Status: Active Prototype.</strong> While I currently manage this via local Python scripts, the roadmap includes migrating this schema to a true Headless CMS (Sanity or WordPress) to fully decouple the content model from the build pipeline.</p></blockquote><h3>The CI/CD Pipeline</h3><p>I treat my career history like a software product. It goes through a build process before deployment.</p><ul><li><strong>1. Source Control (Main Branch):</strong> The "Master Resume" Google Doc. Never sent, only referenced.</li><li><strong>2. Feature Branch (Tailoring):</strong> XML-bounded AI prompts used to "merge" specific skills into the narrative.</li><li><strong>3. Build Script (Python):</strong> <code>prep_resume.py</code> handles versioning and file conversion.</li><li><strong>4. Deployment (Release):</strong> SEO-optimized PDF sent to the recruiter.</li></ul><h3>The Editorial Experience</h3><p>Before the data hits the database, the "Authoring Experience" is defined by these strict governance rules to ensure quality and consistency.</p><figure class="wp-block-table is-style-stripes has-small-font-size"><table><thead><tr><th>Category</th><th>Insight / Rule</th><th>Context</th></tr></thead><tbody><tr><td><strong>Strategy</strong></td><td><strong>Resume as Code</strong></td><td>Treat your Master Resume as the <code>main</code> branch. Tailored applications are <code>feature</code> branches.</td></tr><tr><td><strong>Automation</strong></td><td><strong>The ".gdoc" Trap</strong></td><td>I learned the hard way that <code>.gdoc</code> files aren't real files. My Python script failed until I added an explicit "Export to PDF" step.</td></tr><tr><td><strong>Taxonomy</strong></td><td><strong>Dual-Naming</strong></td><td><strong>External:</strong> <code>Name_Role.pdf</code> (SEO for ATS).<br><strong>Internal:</strong> <code>Date_Name_Variant.pdf</code> (Version Control).</td></tr><tr><td><strong>AI</strong></td><td><strong>XML Prompting</strong></td><td>I wrap my source text in XML tags (<code>&lt;source&gt;</code>) to stop the AI from hallucinating fake jobs.</td></tr></tbody></table></figure>""",
        'meta': {'gem_category': 'Career Engineering', 'gem_status': 'In Progress', 'gem_action_item': 'Refine XML Prompt', 'gem_related_project': 'Job Hunt 2026'}
    },

    # GEM 5: Market Scan
    {
        'title': 'Market Scan: Top Headless CMS Platforms (2025)',
        'status': 'publish', # <--- LIVE
        'content': """<p>As we move into 2026, the Headless CMS market has calcified into three segments: Developer Tools, Marketer Suites, and Visual Composers. Here is the breakdown.</p><figure class="wp-block-table is-style-stripes"><table><thead><tr><th>Platform</th><th>Founded</th><th>Free Tier?</th><th>Paid Start</th></tr></thead><tbody><tr><td><strong>Contentful</strong></td><td>2013</td><td>✅ Yes</td><td>$300/mo</td></tr><tr><td><strong>Sanity</strong></td><td>2018</td><td>✅ Yes</td><td>$15/seat</td></tr><tr><td><strong>Strapi</strong></td><td>2016</td><td>✅ Yes (Self-Hosted)</td><td>$99/mo</td></tr><tr><td><strong>Storyblok</strong></td><td>2017</td><td>✅ Yes</td><td>$108/mo</td></tr><tr><td><strong>Ghost</strong></td><td>2013</td><td>✅ Yes (Self-Hosted)</td><td>$9/mo</td></tr><tr><td><strong>Directus</strong></td><td>2015</td><td>✅ Yes (Self-Hosted)</td><td>$15/mo</td></tr><tr><td><strong>Contentstack</strong></td><td>2018</td><td>⚠️ Limited</td><td>~$995/mo</td></tr><tr><td><strong>Prismic</strong></td><td>2013</td><td>✅ Yes</td><td>$7/mo</td></tr><tr><td><strong>Hygraph</strong></td><td>2017</td><td>✅ Yes</td><td>$299/mo</td></tr><tr><td><strong>ButterCMS</strong></td><td>2014</td><td>❌ No</td><td>$99/mo</td></tr><tr><td><strong>Builder.io</strong></td><td>2018</td><td>✅ Yes</td><td>$24/user</td></tr></tbody></table></figure>""",
        'meta': {'gem_category': 'Market Research', 'gem_status': 'Active', 'gem_action_item': 'Update Tech Radar Slide', 'gem_related_project': '2026 Strategy'}
    },

    # GEM 6: The Confession
    {
        'title': 'Confession: I Don\'t Hate Blogs, I Just Hate Unstructured Data',
        'status': 'publish', # <--- LIVE
        'content': """
        <p>My AI architect recently pointed out a flaw in my new site strategy: <em>"Why are you so down on blogs?"</em></p>
        <p>It’s a fair question. I’ve spent the last week rigorously separating my "Field Notes" from my "Blog," treating the latter like a second-class citizen. But I want to clarify: I don't hate blogs. I hate <strong>Flat Content Models</strong>.</p>
        <h3>The Problem with "The Feed"</h3><p>In a standard CMS, a Blog Post is designed to decay. It is sorted <strong>Chronologically</strong>. Its primary metadata is <em>Time</em>. This is great for news ("We raised Series A!"), but it is terrible for Knowledge ("How to configure Webpack").</p><h3>The Solution: The Gem Node</h3><p>By moving my technical insights into a <strong>Knowledge Graph</strong> (Custom Post Type), I am sorting them <strong>Topologically</strong> (by Topic and Relevance), not Chronologically.</p><figure class="wp-block-table is-style-stripes has-small-font-size"><table><thead><tr><th>Feature</th><th>The Blog Post</th><th>The Knowledge Node</th></tr></thead><tbody><tr><td><strong>Primary Metric</strong></td><td>Recency (When?)</td><td>Relevance (What?)</td></tr><tr><td><strong>Data Structure</strong></td><td>Blob (Title + Body)</td><td>Structured (Status, Project, Tech Stack)</td></tr><tr><td><strong>Lifespan</strong></td><td>Decays over time</td><td>Evergreen (Updated via API)</td></tr><tr><td><strong>User Intent</strong></td><td>"Entertain me."</td><td>"I need an answer."</td></tr></tbody></table></figure><h3>The Verdict</h3><p>I still write blog posts. I use them for <strong>Narrative</strong>—stories about my career, culture, and opinion. But I use my Knowledge Graph for <strong>Assets</strong>—proof of my technical competence.</p>""",
        'meta': {'gem_category': 'Content Strategy', 'gem_status': 'Active', 'gem_action_item': 'Make peace with the blog', 'gem_related_project': 'Sugartown.io v2'}
    },

    # GEM 7: Data Viz
    {
        'title': 'Data Science: Visualizing the Knowledge Graph',
        'status': 'draft', # <--- Keeping this one DRAFT until you have the image ready
        'content': """
        <p>A Knowledge Graph isn't just a metaphor; it's a data structure. To visualize the relationships between my Projects, Categories, and Gems, I used Python's <code>networkx</code> library to generate a force-directed graph.</p>
        <h3>The Logic</h3><p>The script iterates through the <code>content_store.py</code> (the same one used to publish this website), extracts the metadata, and builds nodes and edges. It then uses a spring-layout algorithm to cluster related concepts together.</p><pre class="wp-block-code"><code>import networkx as nx
# Connect Projects to Root (to create the cluster effect)
G.add_edge(gem['project'], root_node)
# Setup Layout (Force-directed)
pos = nx.spring_layout(G, k=0.6, iterations=50)</code></pre><p>This visualization (coming soon to the homepage) serves as the definitive map of my "Headless Content Supply Chain."</p>""",
        'meta': {'gem_category': 'Data Science', 'gem_status': 'Draft', 'gem_action_item': 'Render Graph on Frontend', 'gem_related_project': 'Sugartown.io v2'}
    }
]
