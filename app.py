"""
Streamlit UI — Multi-Agent Research Assistant (Groq / Free)
Run: streamlit run app.py
"""

import os
import time
import threading
from datetime import datetime
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

st.set_page_config(page_title="Multi-Agent Research Assistant", page_icon="🤖", layout="wide")

st.title("🤖 Multi-Agent Research Assistant")
st.caption("CrewAI · Groq (Llama 3.3 70B) · 3 autonomous agents: Researcher → Analyst → Writer")

with st.sidebar:
    st.header("⚙️ API Keys")
    groq_key = st.text_input("Groq API Key (free)", type="password", help="Get free key at console.groq.com")
    serper_key = st.text_input("Serper API Key", type="password", help="Free at serper.dev")
    st.markdown("---")
    st.markdown("**Get free keys:**")
    st.markdown("🔑 [console.groq.com](https://console.groq.com)")
    st.markdown("🔍 [serper.dev](https://serper.dev)")
    st.markdown("---")
    st.markdown("**Pipeline:**")
    st.markdown("1. 🔍 **Researcher** — web search, 8+ findings")
    st.markdown("2. 🧠 **Analyst** — structures insights")
    st.markdown("3. ✍️ **Writer** — executive BI report")
    st.markdown("---")
    st.caption("Built by Neha Chinnam | SRM University AP")

col1, col2 = st.columns([3, 1])
with col1:
    topic = st.text_area("Research Topic", placeholder="e.g. Competitive analysis of EV market in India 2025", height=80)
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("🚀 Run Research", use_container_width=True, type="primary")

st.caption("**Try:** `AI startups in healthcare India 2025` · `Fintech trends Southeast Asia` · `EV charging infrastructure globally`")

if run_btn:
    if not topic.strip():
        st.error("Please enter a research topic.")
    elif not groq_key or not serper_key:
        st.error("Please enter both API keys in the sidebar.")
    else:
        os.environ["GROQ_API_KEY"] = groq_key
        os.environ["SERPER_API_KEY"] = serper_key

        llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.3, api_key=groq_key)
        search_tool = SerperDevTool()

        researcher = Agent(
            role="Senior Research Analyst",
            goal="Conduct thorough web research. Find recent news, statistics, key players, and trends. Prioritise last 12 months.",
            backstory="Expert research analyst with 10 years in business intelligence. Methodical and fact-driven.",
            tools=[search_tool], llm=llm, verbose=False, allow_delegation=False, max_iter=5,
        )
        analyst = Agent(
            role="Critical Analyst",
            goal="Evaluate research findings. Structure into Top Insights, Opportunities, Threats, Key Players, and Trends.",
            backstory="Sharp strategic analyst who has advised Fortune 500 companies.",
            tools=[search_tool], llm=llm, verbose=False, allow_delegation=False, max_iter=3,
        )
        writer = Agent(
            role="Business Intelligence Writer",
            goal="Write a polished BI Report with 9 sections for C-suite executives.",
            backstory="Seasoned business writer specialising in executive briefings.",
            llm=llm, verbose=False, allow_delegation=False,
        )

        research_task = Task(
            description=f"Research '{topic}'. Deliver 8+ findings with URLs, stats, major players, recent developments.",
            expected_output="Structured list of 8+ findings with sources, stats, players.",
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
        )

        crew = Crew(
            agents=[researcher, analyst, writer],
            tasks=[research_task, analysis_task, writing_task],
            process=Process.sequential,
            verbose=False,
        )

        progress_box = st.empty()
        result_holder = {}

        def run_bg():
            result_holder["out"] = crew.kickoff()

        thread = threading.Thread(target=run_bg)
        thread.start()

        stages = [
            ("🔍 Researcher Agent is searching the web...", 20),
            ("🔍 Researcher Agent gathering sources and statistics...", 35),
            ("🧠 Analyst Agent is structuring the findings...", 55),
            ("🧠 Analyst Agent identifying opportunities and risks...", 70),
            ("✍️ Writer Agent is generating the report...", 85),
            ("✍️ Writer Agent finalising the report...", 95),
        ]
        i = 0
        while thread.is_alive():
            msg, pct = stages[min(i, len(stages) - 1)]
            with progress_box.container():
                st.info(msg)
                st.progress(pct)
            i += 1
            time.sleep(4)

        thread.join()
        progress_box.empty()

        report = str(result_holder.get("out", "No output generated."))
        st.success("✅ Report ready!")
        st.markdown("---")
        st.markdown("## 📄 Business Intelligence Report")
        st.markdown(report)
        st.markdown("---")
        st.download_button(
            label="⬇️ Download Report (.md)",
            data=report,
            file_name=f"bi_report_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
        )