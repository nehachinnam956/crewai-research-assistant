# 🤖 Multi-Agent Research Assistant

An autonomous business intelligence system built with **CrewAI** that uses three specialised AI agents to research any topic, critically analyse findings, and generate a polished executive report — with zero manual steps in between.

---

## Architecture

```
User Input (topic)
      │
      ▼
┌─────────────────────┐
│  Agent 1: Researcher │  ← Web search (SerperDev), gathers 8+ findings
└─────────┬───────────┘
          │ findings
          ▼
┌─────────────────────┐
│  Agent 2: Analyst   │  ← Structures into Insights / Opportunities / Threats
└─────────┬───────────┘
          │ structured analysis
          ▼
┌─────────────────────┐
│  Agent 3: Writer    │  ← Produces final BI Report (600-900 words)
└─────────────────────┘
          │
          ▼
   report.md / Streamlit UI
```

**Key design decisions:**
- `Process.sequential` — ensures agents run in strict order with context passing
- Each agent has a bounded `max_iter` to prevent infinite loops (self-correcting behaviour)
- Writer receives context from BOTH researcher and analyst tasks
- Tool-calling is isolated to agents that need it (Researcher + Analyst only)

---

## Setup

### 1. Clone and install
```bash
git clone https://github.com/nehachinnam956/crewai-research-assistant
cd crewai-research-assistant
pip install -r requirements.txt
```

### 2. Set API keys
```bash
cp .env.example .env
# Edit .env and add your keys:
# ANTHROPIC_API_KEY — from console.anthropic.com
# SERPER_API_KEY    — from serper.dev (2500 free searches/month)
```

### 3. Run (two options)

**Command line:**
```bash
python crew.py --topic "Competitive analysis of EV market in India 2025"
```

**Streamlit UI:**
```bash
streamlit run app.py
```

---

## Output Example

For topic: *"AI startups in healthcare India 2025"*

The system produces a report with:
- Executive Summary
- Market Overview
- 5+ Key Findings with sources
- Opportunities & Threats
- Competitive Landscape (named companies)
- Strategic Recommendations

---

## Agentic Design Patterns Used

| Pattern | Implementation |
|---|---|
| Multi-agent collaboration | 3 specialised agents with distinct roles |
| Tool-calling | Researcher + Analyst use SerperDev search tool |
| Context passing | Each task receives prior task outputs as context |
| Sequential orchestration | `Process.sequential` enforces agent order |
| Bounded iteration | `max_iter` prevents runaway loops |
| Output persistence | Writer task saves to `report.md` |

---

## Tech Stack

- **CrewAI 1.14+** — agent orchestration framework
- **Claude (Anthropic)** — LLM backbone for all agents
- **SerperDev** — Google Search API for web tool-calling
- **Streamlit** — interactive web UI
- **Python 3.10+**

---

*Built by Bhagavathi Neha Chinnam | SRM University AP | github.com/nehachinnam956*
