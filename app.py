import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain


# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM UI
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg: #08090d;
    --surface: #101219;
    --surface-2: #151821;
    --border: rgba(255,255,255,.08);
    --text: #f5f7fb;
    --muted: #8b93a7;
    --accent: #7c5cff;
    --accent-2: #9b84ff;
    --green: #35d07f;
    --blue: #4da3ff;
}

html, body, [class*="css"] {
    font-family: "DM Sans", sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(124,92,255,.16), transparent 28%),
        radial-gradient(circle at 90% 10%, rgba(77,163,255,.08), transparent 24%),
        var(--bg);
    color: var(--text);
}

.block-container {
    max-width: 1280px;
    padding: 1.5rem 2.2rem 4rem;
}

#MainMenu, footer, header {
    visibility: hidden;
}

/* Header */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: .5rem 0 1.8rem;
    border-bottom: 1px solid var(--border);
}

.brand {
    display: flex;
    align-items: center;
    gap: .75rem;
}

.brand-icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #7c5cff, #4da3ff);
    box-shadow: 0 8px 30px rgba(124,92,255,.25);
    font-size: 1.25rem;
}

.brand-name {
    font-family: "Space Grotesk", sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: -.02em;
}

.brand-sub {
    color: var(--muted);
    font-size: .72rem;
    margin-top: 2px;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: .45rem;
    border: 1px solid rgba(53,208,127,.18);
    background: rgba(53,208,127,.06);
    color: #72e5a5;
    border-radius: 999px;
    padding: .42rem .75rem;
    font-size: .72rem;
}

.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 10px rgba(53,208,127,.8);
}

/* Hero */
.hero {
    padding: 3.5rem 0 2.6rem;
    text-align: center;
}

.hero-kicker {
    color: var(--accent-2);
    font-size: .72rem;
    font-weight: 700;
    letter-spacing: .18em;
    text-transform: uppercase;
    margin-bottom: .9rem;
}

.hero h1 {
    font-family: "Space Grotesk", sans-serif;
    font-size: clamp(2.5rem, 6vw, 4.8rem);
    line-height: 1;
    letter-spacing: -.055em;
    margin: 0;
    color: #fff;
}

.hero h1 span {
    background: linear-gradient(90deg, #a991ff, #62b3ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    max-width: 650px;
    margin: 1.2rem auto 0;
    color: var(--muted);
    font-size: 1rem;
    line-height: 1.7;
}

/* Input */
.search-card {
    background: linear-gradient(180deg, rgba(255,255,255,.045), rgba(255,255,255,.02));
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.4rem;
    box-shadow: 0 20px 70px rgba(0,0,0,.2);
}

.input-label {
    font-size: .74rem;
    font-weight: 700;
    color: #c8ccda;
    text-transform: uppercase;
    letter-spacing: .12em;
    margin-bottom: .7rem;
}

.stTextInput > div > div > input {
    background: #0b0d12 !important;
    border: 1px solid rgba(255,255,255,.1) !important;
    border-radius: 12px !important;
    color: white !important;
    min-height: 48px !important;
    font-size: .98rem !important;
}

.stTextInput > div > div > input:focus {
    border-color: rgba(124,92,255,.7) !important;
    box-shadow: 0 0 0 3px rgba(124,92,255,.12) !important;
}

.stTextInput label {
    display: none !important;
}

.stButton > button {
    border: 0 !important;
    border-radius: 12px !important;
    min-height: 48px !important;
    background: linear-gradient(135deg, #7c5cff, #5b8cff) !important;
    color: white !important;
    font-weight: 700 !important;
    box-shadow: 0 8px 25px rgba(92,91,255,.22) !important;
    transition: all .2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 32px rgba(92,91,255,.32) !important;
}

.examples {
    display: flex;
    gap: .5rem;
    flex-wrap: wrap;
    margin-top: .9rem;
    align-items: center;
}

.example-title {
    color: #656d80;
    font-size: .7rem;
    text-transform: uppercase;
    letter-spacing: .1em;
}

.example-chip {
    color: #aeb5c7;
    background: rgba(255,255,255,.035);
    border: 1px solid var(--border);
    padding: .32rem .65rem;
    border-radius: 999px;
    font-size: .72rem;
}

/* Section */
.section-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    margin: 2rem 0 .9rem;
}

.section-caption {
    color: var(--muted);
    font-size: .78rem;
    margin-top: -.55rem;
    margin-bottom: 1rem;
}

/* Pipeline */
.pipeline {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: .8rem;
    margin: 1.4rem 0 2rem;
}

.agent-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 1rem;
    min-height: 112px;
}

.agent-card.active {
    border-color: rgba(124,92,255,.55);
    background: rgba(124,92,255,.07);
}

.agent-card.done {
    border-color: rgba(53,208,127,.28);
    background: rgba(53,208,127,.035);
}

.agent-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: .85rem;
}

.agent-icon {
    width: 32px;
    height: 32px;
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(124,92,255,.12);
}

.agent-number {
    color: #596175;
    font-size: .68rem;
    font-weight: 700;
}

.agent-name {
    color: #f0f2f7;
    font-size: .82rem;
    font-weight: 700;
}

.agent-desc {
    color: #777f92;
    font-size: .68rem;
    line-height: 1.45;
    margin-top: .25rem;
}

.agent-state {
    margin-top: .55rem;
    font-size: .63rem;
    font-weight: 700;
    letter-spacing: .08em;
    color: #596175;
}

.agent-card.active .agent-state {
    color: var(--accent-2);
}

.agent-card.done .agent-state {
    color: var(--green);
}

/* Results */
.result-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1.25rem 1.4rem;
    margin-bottom: 1rem;
}

.result-header {
    display: flex;
    align-items: center;
    gap: .65rem;
    padding-bottom: .8rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}

.result-icon {
    width: 30px;
    height: 30px;
    border-radius: 8px;
    background: rgba(124,92,255,.12);
    display: flex;
    align-items: center;
    justify-content: center;
}

.result-title {
    font-weight: 700;
    font-size: .86rem;
}

.result-meta {
    margin-left: auto;
    color: #697186;
    font-size: .67rem;
}

.report-card {
    background:
        linear-gradient(180deg, rgba(124,92,255,.07), rgba(255,255,255,.018)),
        var(--surface);
    border: 1px solid rgba(124,92,255,.22);
    border-radius: 20px;
    padding: 1.6rem 1.8rem;
}

.feedback-card {
    background:
        linear-gradient(180deg, rgba(53,208,127,.045), rgba(255,255,255,.018)),
        var(--surface);
    border: 1px solid rgba(53,208,127,.2);
    border-radius: 20px;
    padding: 1.5rem 1.8rem;
}

/* Streamlit markdown inside result areas */
.report-card h1, .report-card h2, .report-card h3 {
    font-family: "Space Grotesk", sans-serif;
    color: #f7f8fc;
}

.report-card p, .report-card li {
    color: #c0c5d2;
    line-height: 1.8;
}

.feedback-card p, .feedback-card li {
    color: #bcc3ce;
    line-height: 1.7;
}

/* Expanders */
div[data-testid="stExpander"] {
    background: rgba(255,255,255,.018);
    border: 1px solid var(--border);
    border-radius: 14px;
}

div[data-testid="stExpander"] summary p {
    font-size: .78rem !important;
    font-weight: 600 !important;
}

/* Download */
.stDownloadButton > button {
    background: rgba(255,255,255,.045) !important;
    border: 1px solid var(--border) !important;
    color: #d7dbe5 !important;
    box-shadow: none !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #50586a;
    font-size: .7rem;
    margin-top: 4rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
}

@media (max-width: 900px) {
    .pipeline {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 600px) {
    .block-container {
        padding: 1rem;
    }

    .pipeline {
        grid-template-columns: 1fr;
    }

    .hero {
        padding: 2.5rem 0 2rem;
    }
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def agent_card(number, icon, title, description, state):
    states = {
        "waiting": ("WAITING", ""),
        "running": ("RUNNING", "active"),
        "done": ("COMPLETED", "done"),
    }
    label, css = states[state]

    st.markdown(
        f"""
        <div class="agent-card {css}">
            <div class="agent-top">
                <div class="agent-icon">{icon}</div>
                <div class="agent-number">0{number}</div>
            </div>
            <div class="agent-name">{title}</div>
            <div class="agent-desc">{description}</div>
            <div class="agent-state">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_agent_state(results, running, key, steps):
    if key in results:
        return "done"

    if running:
        for step in steps:
            if step not in results:
                return "running" if step == key else "waiting"

    return "waiting"


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = {}

if "running" not in st.session_state:
    st.session_state.running = False

if "done" not in st.session_state:
    st.session_state.done = False


# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="brand">
        <div class="brand-icon">🧠</div>
        <div>
            <div class="brand-name">ResearchMind</div>
            <div class="brand-sub">Multi-Agent Research System</div>
        </div>
    </div>
    <div class="status-pill">
        <span class="status-dot"></span>
        AI SYSTEM ONLINE
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-kicker">Autonomous Research Workspace</div>
    <h1>Research <span>smarter.</span></h1>
    <p>
        Give ResearchMind a topic and let specialized AI agents search the web,
        extract deeper information, write a structured report, and critically
        review the final result.
    </p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# INPUT
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="search-card">', unsafe_allow_html=True)

st.markdown('<div class="input-label">Research topic</div>', unsafe_allow_html=True)

col_topic, col_button = st.columns([4.8, 1.2], gap="small")

with col_topic:
    topic = st.text_input(
        "topic",
        placeholder="e.g. Impact of AI agents on software development",
        key="topic_input",
        label_visibility="collapsed",
    )

with col_button:
    run_btn = st.button(
        "🚀  Research",
        use_container_width=True,
    )

st.markdown("""
<div class="examples">
    <span class="example-title">Try</span>
    <span class="example-chip">LLM agents in 2026</span>
    <span class="example-chip">CRISPR gene editing</span>
    <span class="example-chip">Fusion energy progress</span>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Research pipeline</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-caption">Four specialized stages work together to produce the final report.</div>',
    unsafe_allow_html=True,
)

results = st.session_state.results
steps = ["search", "reader", "writer", "critic"]

pipeline_cols = st.columns(4, gap="small")

pipeline_data = [
    ("🔎", "Search Agent", "Finds recent and relevant web information"),
    ("📖", "Reader Agent", "Extracts deeper content from selected sources"),
    ("✍️", "Writer Chain", "Turns research into a structured report"),
    ("🧐", "Critic Chain", "Reviews and scores the final report"),
]

for col, (icon, title, desc), key in zip(pipeline_cols, pipeline_data, steps):
    with col:
        agent_card(
            steps.index(key) + 1,
            icon,
            title,
            desc,
            get_agent_state(results, st.session_state.running, key, steps),
        )


# ─────────────────────────────────────────────────────────────────────────────
# START PIPELINE
# ─────────────────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# EXISTING RESEARCH LOGIC
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.running and not st.session_state.done:

    results = {}
    topic_val = st.session_state.topic_input

    # Step 1: Search
    with st.spinner("Search Agent is researching the web..."):
        search_agent = build_search_agent()

        sr = search_agent.invoke({
            "messages": [
                (
                    "user",
                    f"Find recent, reliable and detailed information about: {topic_val}"
                )
            ]
        })

        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    # Step 2: Reader
    with st.spinner("Reader Agent is extracting deeper information..."):
        reader_agent = build_reader_agent()

        rr = reader_agent.invoke({
            "messages": [
                (
                    "user",
                    f"""
                    Based on the following search results about '{topic_val}',
                    pick the most relevant URL and scrape it for deeper content.

                    Search Results:
                    {results['search'][:800]}
                    """
                )
            ]
        })

        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # Step 3: Writer
    with st.spinner("Writer is creating the research report..."):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )

        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined,
        })

        st.session_state.results = dict(results)

    # Step 4: Critic
    with st.spinner("Critic is reviewing the report..."):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })

        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="section-title">Research results</div>', unsafe_allow_html=True)

    if "writer" in r:
        st.markdown('<div class="report-card">', unsafe_allow_html=True)

        st.markdown(
            """
            <div class="result-header">
                <div class="result-icon">📝</div>
                <div class="result-title">Final Research Report</div>
                <div class="result-meta">GENERATED BY WRITER</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="⬇  Download report",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Raw research
    st.markdown('<div class="section-title">Research evidence</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("🔎  Search Agent output", expanded=False):
            st.markdown(r["search"])

    if "reader" in r:
        with st.expander("📖  Reader Agent output", expanded=False):
            st.markdown(r["reader"])

    # Critic
    if "critic" in r:
        st.markdown('<div class="section-title">Quality review</div>', unsafe_allow_html=True)

        st.markdown('<div class="feedback-card">', unsafe_allow_html=True)

        st.markdown(
            """
            <div class="result-header">
                <div class="result-icon">🧐</div>
                <div class="result-title">Critic Feedback</div>
                <div class="result-meta">QUALITY REVIEW</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ResearchMind · LangChain Multi-Agent Research System · Built with Streamlit
</div>
""", unsafe_allow_html=True)