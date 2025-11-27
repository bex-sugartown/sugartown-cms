import requests
import json
import base64

# --- CONFIGURATION ---
URL = "https://sugartown.io/wp-json/wp/v2/gems"
USER = "bhead" # The username you use to login to WP
PASSWORD = "2vf9 WvM1 ygJa EkbM PMVk X92O" # The Application Password you just generated (NOT your login password)

# --- AUTHENTICATION ---
# We encode the username and password into a format the API understands
credentials = f"{USER}:{PASSWORD}"
token = base64.b64encode(credentials.encode())
headers = {
    'Authorization': f'Basic {token.decode("utf-8")}',
    'Content-Type': 'application/json'
}

# --- THE DATA LIST (Wrapped in a List called 'all_gems') ---
all_gems = [
    {
        'title': 'Sweet Upgrades: Why Gemini 3 is the Cherry on Top',
        'status': 'draft', 
        'content': """
        <p>We’ve all been there—living comfortably in our standard Google Accounts. But with the release of <strong>Gemini 3 Pro</strong> this week, the question isn’t just “Do I need an AI?”—it’s “Am I ready to upgrade from a bicycle to a rocket ship?”</p>
        <p>I’m sharing here because it took me an ungodly amount of time and lots of gemini’ing to get a straight answer out of Google (HELLO!).</p>
        <h3>🍭 Comparison: The Gemini 3 Hierarchy (Nov 2025)</h3>
        <figure class="wp-block-table is-style-stripes has-small-font-size"><table>
        <thead><tr>
            <th>Feature</th>
            <th>Google AI Premium<br>(Personal)</th>
            <th>Workspace Business Standard<br>(The Team Essential)</th>
            <th>Google AI Ultra for Business<br>(The Power-User Tier)</th>
        </tr></thead>
        <tbody>
        <tr>
            <td><strong>Primary Purpose</strong></td>
            <td>Individual Productivity:<br>For freelancers, students, and general use.</td>
            <td>Team Collaboration:<br>For core business ops, secure email, and docs.</td>
            <td>Heavy Compute / R&D:<br>For architects, data scientists, and media pros.</td>
        </tr>
        <tr>
            <td><strong>Price</strong></td>
            <td>$19.99 / month</td>
            <td>Included in Workspace<br>(~$14.40 / user / mo)</td>
            <td>🚀 <strong>$250.00 / user / month</strong><br>(The “VIP” Add-on)</td>
        </tr>
        <tr>
            <td><strong>Model Name</strong></td>
            <td>Gemini 3 Pro</td>
            <td>Gemini 3 Pro</td>
            <td>Gemini 3 Ultra</td>
        </tr>
        <tr>
            <td><strong>Reasoning Engine</strong></td>
            <td>Standard Reasoning<br>(Fast logic checks)</td>
            <td>Standard Reasoning<br>(Fast logic checks)</td>
            <td>🧠 <strong>Deep Think</strong><br>(Ph.D. level “Chain of Thought”)</td>
        </tr>
        <tr>
            <td><strong>Deep Think Mode</strong></td>
            <td>❌ Not Included</td>
            <td>❌ Not Included</td>
            <td>✅ Included<br>(Can “think” for minutes on complex tasks)</td>
        </tr>
        <tr>
            <td><strong>Storage</strong></td>
            <td>2 TB</td>
            <td>2 TB (Pooled)</td>
            <td>30 TB<br>(Massive Archive)</td>
        </tr>
        <tr>
            <td><strong>Project Mariner</strong><br>(Agentic Research)</td>
            <td>❌ Not Included</td>
            <td>❌ Not Included</td>
            <td>✅ Included<br>(Autonomous Multi-Tasking Agent)</td>
        </tr>
        <tr>
            <td><strong>Video AI (Veo)</strong></td>
            <td>Standard (Veo 2)</td>
            <td>Standard (Veo 2)</td>
            <td>Pro Studio (Veo 3)<br>(1080p, unlimited generation)</td>
        </tr>
        <tr>
            <td><strong>Data Privacy</strong></td>
            <td>👎 Consumer Grade<br>(Used for training)</td>
            <td>👍 Enterprise Grade<br>(Private)</td>
            <td>👍 Enterprise Grade<br>(Private + Advanced Compliance)</td>
        </tr>
        </tbody>
        </table></figure>
        <h4>“Why is AI Ultra $250/month?!”</h4>
        <p>If you are staring at that price tag in shock, you aren’t the target audience—and that’s okay! With the <strong>$250 AI Ultra</strong> plan you are paying for:</p>
        <ul>
            <li><strong>Deep Think:</strong> The ability to solve novel architectural problems that stump standard models.</li>
            <li><strong>Project Mariner:</strong> An autonomous agent that can browse the web, navigate complex UI, and complete tasks (like “Research the pricing of these 50 competitors and put them in a spreadsheet”) while you sleep.</li>
            <li><strong>30 TB of Storage:</strong> This alone used to cost nearly $150/mo.</li>
        </ul>
        <p><strong>My Recommendation:</strong> Stick to <strong>Personal Premium ($20)</strong> or <strong>Workspace Business Standard ($14 per user)</strong> for 99% of your work. Only upgrade to <strong>Ultra</strong> if you need the AI to <em>solve</em> problems, not just <em>answer</em> them.</p>
        """,
        'meta': {
            'gem_category': 'AI Strategy',
            'gem_status': 'Done',
            'gem_action_item': 'Upgrade Dev Pod to Ultra',
            'gem_related_project': 'Tech Stack Eval'
        }
    }
]

# --- THE EXECUTION LOOP ---
print(f"🚀 Preparing to upload {len(all_gems)} Gems...")

for gem in all_gems:
    print(f"📤 Uploading: {gem['title']}...")
    response = requests.post(URL, headers=headers, json=gem)
    
    if response.status_code == 201:
        print("   ✅ Success")
        print(f"   🔗 {response.json()['link']}")
    else:
        print(f"   ❌ ERROR: {response.status_code} - {response.text}")

print("✨ Done!")
