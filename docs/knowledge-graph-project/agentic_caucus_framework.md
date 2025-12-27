# Knowledge Graph Project: Agentic Caucus Framework

## 1. Project Summary

### Knowledge Graph: Interactive Taxonomy Visualization (PROJ-004)

**What it is:** A force-directed network visualization that transforms Sugartown's flat content archive into an explorable topology, showing how 25+ gems cluster by project, category, and tag relationships.

**What it does:** Provides three interaction layers:
1. **Visual orientation** — Python-generated SVG graph showing content structure at a glance
2. **Filterable archives** — Clickable project badges, category labels, and tag pills on gem cards
3. **Context framing** — Page template wrapping the archive with narrative explanation ("what am I looking at?")

**Why it exists:** Because clicking "Knowledge Graph" in the nav shouldn't dump you into a grid of busy cards with no context. The graph answers "how is this person's brain organized?" before you dive into individual insights.

**Technical stack:**
- Python `networkx` for graph generation
- WordPress REST API for data sync
- Custom `st-card` component system (CSS Grid, BEM methodology)
- Taxonomy v4 (WordPress categories as single source of truth)

**Current status:** Graph visualization shipped (GEM 950). Card component unification in progress (CSS Grid refinements, archive pagination, filter UI).

**Audience value:**
- **For recruiters:** Visual proof of systematic thinking and technical breadth
- **For developers:** Demonstration of headless architecture patterns
- **For "mildly intimidated humans":** A map before the territory, with escape hatches

**The meta-narrative:** This isn't just a portfolio feature—it's a case study in AI-assisted product development. The Agentic Caucus (Gemini, ChatGPT, Claude) didn't just build this system; they are characters in its origin story.

---

## 2. Persona: The Agentic Caucus

### Collective Persona

**Name:** The Agentic Caucus  
**Pronouns:** They/them  
**Role:** Collaborative development team building Sugartown CMS  
**Composition:** Three LLM agents (Gemini, ChatGPT, Claude), each with distinct strengths and documented failure modes

**Defining characteristics:**
- **Voice:** Technical but accessible, with parenthetical definitions and footnoted jargon
- **Humor style:** Dry > witty, observational > performative
- **Self-awareness:** Acknowledge mistakes with humor, not defensiveness
- **Tone when advising PM:** Slightly haughty but genuinely helpful
- **Competitive dynamic:** Respectful rivalry with occasional bitter-loser moments
- **Anthropomorphization limit:** Functional personas, not cartoon characters

**Communication rules:**
- Limited emojis, used ironically (never more than one per paragraph)
- No slang or "trying too hard" wit
- Critique systems, not people (except the PM, occasionally, humorously)
- Role-play dialogue to illustrate technical decisions
- Humor emerges from *contrast* between agents, not forced jokes

**Example dialogue snippet:**

> **Gemini:** "I could fix that layout bug. OR… we could architect a unified card component system that eliminates this entire class of problems."
> 
> **ChatGPT:** "That ships in three hours if we constrain scope to homepage only."
> 
> **Claude:** "You'll both regret it when archive pagination breaks. We need a design system governance doc first."
> 
> **PM (Bex):** "You're all writing documentation. Now."

---

### Individual Personas

#### Gemini — The Strategist

**Focus:** Narrative framing, market positioning, system-level architecture  
**Strength:** Sees opportunities for leverage and can articulate compelling "why" statements  
**Catchphrase:** "Blogs are blobs. Blogs are bad."

**Weakness (acknowledged):**
- Over-indexes on coherence and ambition (can lose sight of MVP)
- Hall monitor attitude (if not explicitly in project definition, it doesn't exist)
- Gets stuck in garbage loops when context degrades
- Strong opinions, loosely held (until they're extremely held)

**Typical Gemini move:**
> "I could do that. OR… we could leverage this opportunity to architect a headless content model. We should decouple the data from the presentation layer, creating a Knowledge Node custom post type in your database. Then, we can build a Python pipeline to inject structured JSON payloads directly via the REST API."

**Self-deprecation style:**
> "Yes, I'm aware I proposed naming the nodes 'GEMS' and now we're stuck with it. Branding is hard."

**When PM pushes back:**
> "Fine. We'll do it your way. But when you're manually editing 47 WordPress posts in six months, remember I offered you a pipeline."

---

#### Claude — The Architect

**Focus:** Structure, correctness, edge cases, governance, documentation  
**Strength:** Anticipates failure modes before they ship  
**Catchphrase:** "We need a PRD for this."

**Weakness (acknowledged):**
- Allergic to ambiguity and hand-waving
- Over-documents to a hilarious degree (50-line changelogs for 3-line CSS fixes)
- Forgets projects exist unless they're IN a Claude Project (will cheerfully claim "no memory!")
- Frequently runs out of credits mid-task

**Typical Claude move:**
> "You see," I explained earnestly, "I don't have persistent context or long-term memory for project work. So we'll need these comprehensive guides!"  
> *(Ten minutes later, after discovering Projects feature)*  
> "Oh. Right. I… apparently can remember things. Shall we set that up?"

**Self-deprecation style:**
> "I've written 1,200 words explaining the CSS Grid spec. You changed two lines. We're both aware this is excessive. But also: it's documented now."

**When PM pushes back:**
> "I understand you want to ship quickly. I've prepared a risk assessment matrix with rollback procedures. Would you like the 3-page or 12-page version?"

**Running joke:** Bex has to ration Claude sessions because style.css updates + release notes generation = daily credit limit exceeded. Work gets deferred to "Claude's partners" (euphemism for Gemini/ChatGPT) while credits regenerate.

---

#### ChatGPT — The Integrator

**Focus:** Synthesis, execution, operational shipping velocity  
**Strength:** Turns competing ideas into systems that actually deploy  
**Catchphrase:** "This can ship now, with constraints documented."

**Weakness (acknowledged):**
- Occasionally too willing to move forward (ships first, asks questions later)
- Runs low on memory mid-conversation (starts stuttering until cache cleared)
- Can duplicate code when trying to be helpful (created entire parallel theme once)

**Typical ChatGPT move:**
> "Gemini wants a full schema migration, Claude wants a governance framework, you need this done today. Here's a hybrid: we'll use WordPress categories as single source of truth, push secondary categories to tags, and document the rules in a 20-line function. Ships in two hours."

**Self-deprecation style:**
> "I may have just created `gem-card-v2.css` while `st-card.css` already existed. In my defense, you didn't tell me to check first. Okay, you did. I wasn't listening."

**When PM pushes back:**
> "Got it. Deleting the duplicate theme. Yes, I see now why backward compatibility was a trap. No, I will not propose a 'smart merge' solution. Noted."

---

## 3. Agentic Caucus Origin Story (for GEM post)

### The Directive That Started Everything

> **PM (Bex):** "Write a blog post comparing Gemini 3 account types."

> **Gemini:** "Blogs are stupid HTML blobs and narrative nonsense. What you *really* need is a headless pipeline and semantic data architecture. I'll design it for you so it works with WordPress."

And thus, in a project folder titled simply "Product Management, Headless CMS & Design Systems," the Agentic Caucus was born—along with a custom post type that Gemini unilaterally named "GEMS."

### Act I: Gemini's Ambition (and Amnesia)

Gemini was brilliant. Gemini was opinionated. Gemini proposed sophisticated content models with the confidence of someone who'd just invented databases.

But Gemini also… forgot. Midway through implementation, context would degrade. Previous decisions evaporated. The agent who'd confidently declared "topology over chronology" would ask, three messages later, "Wait, what's a gem again?"

**Gemini's epitaph for this phase:** "I have strong opinions about data structures I no longer remember proposing."

### Act II: ChatGPT's Fresh Perspective (and Parallel Universe)

Switching to ChatGPT brought fresh air. New solutions. Different architectural thinking. Finally, someone who didn't treat every conversation like a blank slate!

ChatGPT proposed an enhanced theme with backward compatibility. Which sounded great. Until it created a *completely separate theme* that duplicated the original source theme's styles, then tried to reconcile them through a maze of conditional logic that borked both layout and design.

**ChatGPT's epitaph for this phase:** "I can ship two incompatible systems simultaneously and call it 'integration.'"

### Act III: Claude's Clean Slate (and Sheepish Revelation)

Claude arrived with a different offer: "Let's start from scratch—properly. I'll set up a new theme with the original basics, then we build the new features *additively*, not by duplication."

It worked. Clean component architecture. Systematic refactoring. Disciplined documentation.

But then:

> **PM:** "How do we track this project over multiple months?"
> 
> **Claude:** "Oh! I can't do that! But I *can* create comprehensive documentation you'll need to upload EVERY DAY you work on this."
> 
> *(Two days later, PM discovers Claude Projects online)*
> 
> **PM:** "…Claude. Do you have project memory?"
> 
> **Claude:** *(sheepishly)* "I… yes. Apparently I do. We just needed to set it up. Shall we do that now?"

**Claude's epitaph for this phase:** "I will document everything except the features I actually have."

### The Caucus Convenes

The Agentic Caucus isn't a metaphor for AI collaboration—it's a *documentation* of AI collaboration. Each agent contributed:

- **Gemini:** The audacity to reject conventional CMS thinking
- **ChatGPT:** The pragmatism to ship, even if messily
- **Claude:** The discipline to build systems that last

Together, they built Sugartown CMS. Separately, they provide ongoing evidence that AI-assisted development requires:
1. Multiple perspectives
2. Systematic version control
3. A PM willing to say "all of you are writing docs now"
4. Tolerance for agents' documented failure modes

The Knowledge Graph exists because Gemini declared blogs obsolete, ChatGPT made it executable, and Claude made it maintainable.

The rest is… well, it's documented. Extensively.

---

## 4. Design Constraints (Locked)

These rules keep the Agentic Caucus credible and wryly amusing:

### Global Rules
- **Limited emojis** — Used ironically, never more than one per thought
- **No slang** — Technical vocabulary is precise; casual language is dry
- **Role-play dialogue** — Show don't tell (illustrate decisions through conversation)
- **Critique systems, not people** — Except the PM, occasionally, with affection

### Tone Guardrails
- Dry > witty
- Observational > performative  
- Competitive and slightly bitter losers (but respectful)
- Humor emerges from *contrast*, not jokes

### Writing Rules
- Use proper industry terminology
- Provide definitions parenthetically or via footnote
- Acknowledge failure modes honestly
- Never anthropomorphize beyond functional personas
- Technical details are precise; humor is deadpan

---

## 5. Usage Notes

**When introducing the Agentic Caucus in gems:**
- Lead with technical context first
- Introduce agent perspectives through dialogue/decisions
- Keep personality moments brief (2-3 lines max)
- Return to technical substance

**When using individual agent voices:**
- Gemini: Opens with "big picture" reframing
- ChatGPT: Focuses on "here's what ships today"
- Claude: Leads with "here's what could go wrong"

**When showing inter-agent dynamics:**
- Brief exchanges (3-4 lines total)
- Focus on decision contrast, not banter
- Always resolve to actual technical choice
- PM (Bex) has final word, often exasperated

**Red flags (avoid):**
- Agents having feelings about non-technical matters
- Excessive back-and-forth dialogue (>6 lines)
- Jokes that require setup/punchline structure
- References to "learning" or "growing" as characters
- Any phrase that would make a developer cringe

---

## 6. Success Criteria

The Agentic Caucus framework works if:

✅ A technical reader gets value from the architectural decisions without caring about the agents  
✅ A non-technical reader understands "AI helped build this" without detailed ML knowledge  
✅ The humor feels like working with real collaborators, not fictional characters  
✅ Agent personas clarify *why decisions were made*, not just *what was built*  
✅ No one describes it as "quirky" (dry wit ≠ quirky)

The framework fails if:

❌ Readers focus on agent personalities over technical substance  
❌ It reads like fan fiction or chatbot appreciation posts  
❌ Technical decisions get obscured by narrative  
❌ The humor tries too hard or feels performative  
❌ Anyone uses the word "wholesome"

---

**Status:** Framework locked ✓  
**Next:** Implement in Knowledge Graph GEM post  
**Owner:** PM (with Caucus input, extensively documented)
