"""
Multi-Agent Research Assistant — CrewAI + Groq (Free)
python crew.py --topic "Competitive analysis of EV market in India"
"""

import os
import argparse
from datetime import datetime
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY   = os.getenv("GROQ_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set. Get free key at https://console.groq.com")
if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY not set. Get free key at https://serper.dev")

os.environ["GROQ_API_KEY"]   = GROQ_API_KEY
os.environ["SERPER_API_KEY"] = SERPER_API_KEY

llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.3, api_key=GROQ_API_KEY)
search_tool = SerperDevTool()

researcher = Agent(
    role="Senior Research Analyst",
    goal="Conduct thorough web research. Find recent news, statistics, key players, trends. Prioritise last 12 months.",
    backstory="Expert research analyst with 10 years in business intelligence. Methodical, fact-driven, always cites sources.",
    tools=[search_tool], llm=llm, verbose=True, allow_delegation=False, max_iter=5,
)
analyst = Agent(
    role="Critical Analyst",
    goal="Evaluate raw research findings. Structure into: Opportunities, Threats, Key Players, Market Trends.",
    backstory="Sharp strategic analyst who has advised Fortune 500 companies.",
    tools=[search_tool], llm=llm, verbose=True, allow_delegation=False, max_iter=3,
)
writer = Agent(
    role="Business Intelligence Writer",
    goal="Transform analyst findings into a polished Business Intelligence Report for C-suite executives.",
    backstory="Seasoned business writer specialising in executive briefings.",
    llm=llm, verbose=True, allow_delegation=False,
)

def build_tasks(topic):
    research_task = Task(
        description=f"Research '{topic}'. Deliver 8+ findings with URLs, stats, major players, recent developments.",
        expected_output="Structured list of 8+ findings with source URLs, statistics, major players.",
        agent=researcher,
    )
    analysis_task = Task(
        description=f"Analyse findings on '{topic}'. Deliver: Top 5 Insights, Opportunities, Threats, Key Players, Trends, Data Quality Notes.",
        expected_output="Analytical briefing with all 6 sections.",
        agent=analyst,
        context=[research_task],
    )
    writing_task = Task(
        description=(
            f"Write a Business Intelligence Report on '{topic}' with sections: "
            "Executive Summary, Market Overview, Key Findings, Opportunities, Risks, "
            f"Competitive Landscape, Trends, Recommendations, Sources. "
            f"Date: {datetime.now().strftime('%B %d, %Y')}. 600-900 words."
        ),
        expected_output="Complete BI Report in markdown, 600-900 words.",
        agent=writer,
        context=[research_task, analysis_task],
        output_file="report.md",
    )
    return [research_task, analysis_task, writing_task]

def run_crew(topic):
    print(f"\n{'='*60}\n  Topic: {topic}\n  Flow: Researcher → Analyst → Writer\n{'='*60}\n")
    crew = Crew(agents=[researcher, analyst, writer], tasks=build_tasks(topic), process=Process.sequential, verbose=True)
    return str(crew.kickoff())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", type=str, default="Competitive analysis of EV market in India 2025")
    args = parser.parse_args()
    output = run_crew(args.topic)
    print("\n" + "="*60 + "\nFINAL REPORT\n" + "="*60)
    print(output)
    print("\nReport saved to: report.md")