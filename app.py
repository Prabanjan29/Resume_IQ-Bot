import streamlit as st
from groq import Groq
import json
import re
import os

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResumeIQ · AI Job Match Agent",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
    --bg: #0a0a0f;
    --surface: #13131a;
    --surface2: #1c1c27;
    --accent: #7c6af7;
    --accent2: #f76a8a;
    --accent3: #6af7c8;
    --text: #e8e8f0;
    --muted: #8888aa;
    --border: #2a2a3d;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

.stApp { background-color: var(--bg); }

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 1200px; }

/* Hero */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    background: radial-gradient(ellipse 80% 60% at 50% 0%, rgba(124,106,247,0.18) 0%, transparent 70%);
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
}
.hero-tag {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    background: rgba(124,106,247,0.12);
    border: 1px solid rgba(124,106,247,0.3);
    padding: 0.3rem 0.9rem;
    border-radius: 2rem;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0 0 0.8rem;
    line-height: 1.1;
    background: linear-gradient(135deg, #fff 0%, #b8b0ff 50%, #f76a8a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero p {
    color: var(--muted);
    font-size: 1.05rem;
    font-weight: 300;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.7;
}

/* Panels */
.panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.6rem;
    height: 100%;
}
.panel-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.panel-label span { font-size: 1rem; }

/* Streamlit text areas */
.stTextArea textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    resize: vertical !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(124,106,247,0.15) !important;
}

/* Analyze button */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, var(--accent), #9b8ffa) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    margin-top: 0.5rem;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(124,106,247,0.4) !important;
}

/* Score ring */
.score-ring-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 1.5rem 0;
}
.score-ring {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    margin-bottom: 0.8rem;
    position: relative;
}
.score-ring::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 50%;
    padding: 4px;
    background: conic-gradient(var(--score-color) var(--score-deg), var(--border) 0deg);
    -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 8px), white calc(100% - 8px));
    mask: radial-gradient(farthest-side, transparent calc(100% - 8px), white calc(100% - 8px));
}
.score-num {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    line-height: 1;
}
.score-label {
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
}
.verdict-badge {
    display: inline-block;
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    padding: 0.35rem 1rem;
    border-radius: 2rem;
    text-transform: uppercase;
}

/* Result cards */
.result-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.result-card h4 {
    font-family: 'Syne', sans-serif;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 0 0 0.8rem;
}
.chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.chip {
    font-size: 0.78rem;
    padding: 0.3rem 0.7rem;
    border-radius: 6px;
    font-weight: 500;
}
.chip-green { background: rgba(106,247,200,0.1); color: #6af7c8; border: 1px solid rgba(106,247,200,0.25); }
.chip-red   { background: rgba(247,106,138,0.1); color: #f76a8a; border: 1px solid rgba(247,106,138,0.25); }
.chip-blue  { background: rgba(124,106,247,0.1); color: #a89bff; border: 1px solid rgba(124,106,247,0.25); }

.suggestion-item {
    border-left: 2px solid var(--accent);
    padding: 0.5rem 0 0.5rem 0.9rem;
    margin-bottom: 0.6rem;
    font-size: 0.88rem;
    color: var(--text);
    line-height: 1.6;
}

.section-score-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.88rem;
}
.section-score-row:last-child { border-bottom: none; }

.progress-bar-bg {
    background: var(--border);
    border-radius: 4px;
    height: 6px;
    flex: 1;
    margin: 0 0.8rem;
    overflow: hidden;
}
.progress-bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 1s ease;
}

/* Divider */
hr { border-color: var(--border); }

/* Expander */
.streamlit-expanderHeader {
    background: var(--surface2) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Hero ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-tag">🎯 AI-Powered Agent</div>
  <h1>ResumeIQ</h1>
  <p>Paste your resume and a job description. Our LLM agent will score your match, uncover gaps, and give you a targeted rewrite plan.</p>
</div>
""", unsafe_allow_html=True)


# ─── Input Section ───────────────────────────────────────────────────────────
col_r, col_j = st.columns(2, gap="large")

with col_r:
    st.markdown("""<div class="panel-label"><span>📄</span> Your Resume</div>""", unsafe_allow_html=True)
    resume_text = st.text_area(
        label="resume",
        placeholder="Paste your full resume text here...\n\nInclude: work experience, skills, education, projects, certifications...",
        height=320,
        label_visibility="collapsed",
        key="resume_input"
    )

with col_j:
    st.markdown("""<div class="panel-label"><span>💼</span> Job Description</div>""", unsafe_allow_html=True)
    job_text = st.text_area(
        label="job",
        placeholder="Paste the full job description here...\n\nInclude: responsibilities, required skills, qualifications, nice-to-haves...",
        height=320,
        label_visibility="collapsed",
        key="job_input"
    )

# Center button
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    analyze_btn = st.button("✦ Analyze My Resume", use_container_width=True)


# ─── Analysis Function ────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are ResumeIQ, an expert AI career coach and resume analyst. 
When given a resume and job description, you perform a deep structured analysis.

You MUST respond with ONLY valid JSON (no markdown, no extra text) in this exact format:
{
  "match_score": <integer 0-100>,
  "verdict": "<one of: Excellent Match | Strong Match | Moderate Match | Weak Match | Poor Match>",
  "summary": "<2-3 sentence overall assessment>",
  "matched_skills": ["skill1", "skill2", ...],
  "missing_skills": ["skill1", "skill2", ...],
  "bonus_skills": ["skill1", "skill2", ...],
  "section_scores": {
    "skills": <0-100>,
    "experience": <0-100>,
    "education": <0-100>,
    "keywords": <0-100>
  },
  "strengths": ["strength1", "strength2", "strength3"],
  "gaps": ["gap1", "gap2", "gap3"],
  "suggestions": [
    "Specific rewrite suggestion 1",
    "Specific rewrite suggestion 2",
    "Specific rewrite suggestion 3",
    "Specific rewrite suggestion 4",
    "Specific rewrite suggestion 5"
  ],
  "missing_keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
}

Be specific, actionable, and honest. Base your analysis strictly on what's in the resume vs. the job description."""


def run_analysis(resume: str, job: str) -> dict:
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in secrets or environment.")

    client = Groq(api_key=api_key)

    user_msg = f"""Please analyze this resume against the job description.

=== RESUME ===
{resume}

=== JOB DESCRIPTION ===
{job}

Respond with JSON only."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ],
        temperature=0.3,
        max_tokens=1500,
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


# ─── Results Rendering ────────────────────────────────────────────────────────
def score_color(score):
    if score >= 80: return "#6af7c8"
    if score >= 60: return "#f7c86a"
    if score >= 40: return "#f79d6a"
    return "#f76a8a"

def verdict_style(verdict):
    styles = {
        "Excellent Match": ("background:rgba(106,247,200,0.15);color:#6af7c8;border:1px solid rgba(106,247,200,0.3)", "🏆"),
        "Strong Match":    ("background:rgba(106,247,200,0.1);color:#a0f7d8;border:1px solid rgba(106,247,200,0.2)", "✅"),
        "Moderate Match":  ("background:rgba(247,200,106,0.12);color:#f7d86a;border:1px solid rgba(247,200,106,0.25)", "⚡"),
        "Weak Match":      ("background:rgba(247,157,106,0.12);color:#f7b06a;border:1px solid rgba(247,157,106,0.25)", "⚠️"),
        "Poor Match":      ("background:rgba(247,106,138,0.12);color:#f76a8a;border:1px solid rgba(247,106,138,0.25)", "❌"),
    }
    return styles.get(verdict, styles["Moderate Match"])

def render_results(data: dict):
    score = data.get("match_score", 0)
    verdict = data.get("verdict", "Moderate Match")
    v_style, v_icon = verdict_style(verdict)
    color = score_color(score)
    deg = int(score * 3.6)

    st.markdown("---")
    st.markdown("""<div class="panel-label" style="justify-content:center;font-size:0.85rem;letter-spacing:0.08em;margin-bottom:1.5rem">
        ✦ &nbsp; Analysis Complete
    </div>""", unsafe_allow_html=True)

    # Top row: Score + Summary
    top_l, top_r = st.columns([1, 2], gap="large")

    with top_l:
        st.markdown(f"""
        <div class="score-ring-wrap">
          <div class="score-ring" style="--score-color:{color};--score-deg:{deg}deg;">
            <span class="score-num" style="color:{color}">{score}</span>
            <span class="score-label">/ 100</span>
          </div>
          <span class="verdict-badge" style="{v_style}">{v_icon} {verdict}</span>
        </div>
        """, unsafe_allow_html=True)

    with top_r:
        st.markdown(f"""
        <div class="result-card" style="height:100%;display:flex;flex-direction:column;justify-content:center;">
          <h4 style="color:var(--muted)">📋 Assessment</h4>
          <p style="font-size:0.93rem;line-height:1.75;color:var(--text);margin:0">{data.get("summary", "")}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Section scores
    sec = data.get("section_scores", {})
    sec_items = [
        ("🛠 Skills", sec.get("skills", 0)),
        ("💼 Experience", sec.get("experience", 0)),
        ("🎓 Education", sec.get("education", 0)),
        ("🔑 Keywords", sec.get("keywords", 0)),
    ]
    sc_html = '<div class="result-card"><h4 style="color:var(--muted)">Section Breakdown</h4>'
    for label, val in sec_items:
        c = score_color(val)
        sc_html += f"""
        <div class="section-score-row">
          <span style="min-width:110px">{label}</span>
          <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width:{val}%;background:{c}"></div>
          </div>
          <span style="color:{c};font-weight:600;min-width:38px;text-align:right">{val}</span>
        </div>"""
    sc_html += "</div>"
    st.markdown(sc_html, unsafe_allow_html=True)

    # Skills grid
    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        matched = data.get("matched_skills", [])
        chips = "".join(f'<span class="chip chip-green">✓ {s}</span>' for s in matched)
        st.markdown(f"""
        <div class="result-card">
          <h4 style="color:#6af7c8">✅ Matched Skills ({len(matched)})</h4>
          <div class="chip-row">{chips or '<span style="color:var(--muted);font-size:0.85rem">None found</span>'}</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        missing = data.get("missing_skills", [])
        chips = "".join(f'<span class="chip chip-red">✗ {s}</span>' for s in missing)
        st.markdown(f"""
        <div class="result-card">
          <h4 style="color:#f76a8a">❌ Missing Skills ({len(missing)})</h4>
          <div class="chip-row">{chips or '<span style="color:var(--muted);font-size:0.85rem">None found</span>'}</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        bonus = data.get("bonus_skills", [])
        chips = "".join(f'<span class="chip chip-blue">+ {s}</span>' for s in bonus)
        st.markdown(f"""
        <div class="result-card">
          <h4 style="color:#a89bff">⭐ Bonus Skills ({len(bonus)})</h4>
          <div class="chip-row">{chips or '<span style="color:var(--muted);font-size:0.85rem">None found</span>'}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Strengths & Gaps
    col_s, col_g = st.columns(2, gap="large")

    with col_s:
        strengths = data.get("strengths", [])
        items = "".join(f'<li style="margin-bottom:0.5rem;font-size:0.88rem;line-height:1.6">{s}</li>' for s in strengths)
        st.markdown(f"""
        <div class="result-card">
          <h4 style="color:#6af7c8">💪 Strengths</h4>
          <ul style="padding-left:1.2rem;margin:0;color:var(--text)">{items}</ul>
        </div>""", unsafe_allow_html=True)

    with col_g:
        gaps = data.get("gaps", [])
        items = "".join(f'<li style="margin-bottom:0.5rem;font-size:0.88rem;line-height:1.6">{g}</li>' for g in gaps)
        st.markdown(f"""
        <div class="result-card">
          <h4 style="color:#f76a8a">🔍 Gaps to Address</h4>
          <ul style="padding-left:1.2rem;margin:0;color:var(--text)">{items}</ul>
        </div>""", unsafe_allow_html=True)

    # Suggestions
    suggestions = data.get("suggestions", [])
    sugg_html = '<div class="result-card"><h4 style="color:#a89bff">✏️ Rewrite Suggestions</h4>'
    for s in suggestions:
        sugg_html += f'<div class="suggestion-item">{s}</div>'
    sugg_html += "</div>"
    st.markdown(sugg_html, unsafe_allow_html=True)

    # Missing keywords
    kws = data.get("missing_keywords", [])
    if kws:
        chips = "".join(f'<span class="chip chip-red">#{k}</span>' for k in kws)
        st.markdown(f"""
        <div class="result-card">
          <h4 style="color:#f7c86a">🔑 Missing Keywords to Add</h4>
          <div class="chip-row">{chips}</div>
        </div>""", unsafe_allow_html=True)


# ─── Main Logic ──────────────────────────────────────────────────────────────
if analyze_btn:
    if not resume_text.strip() or not job_text.strip():
        st.error("⚠️ Please provide both your resume and the job description.")
    elif len(resume_text.strip()) < 50:
        st.error("⚠️ Resume seems too short. Please paste your full resume.")
    elif len(job_text.strip()) < 50:
        st.error("⚠️ Job description seems too short. Please paste the full JD.")
    else:
        with st.spinner("🔍 Analyzing your resume against the job description..."):
            try:
                result = run_analysis(resume_text, job_text)
                render_results(result)
            except json.JSONDecodeError as e:
                st.error(f"❌ Failed to parse AI response. Please try again. ({e})")
            except ValueError as e:
                st.error(f"❌ Config error: {e}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")


# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2.5rem 0 1rem;color:var(--muted);font-size:0.8rem;border-top:1px solid var(--border);margin-top:3rem">
  Built with Groq · LLaMA 3.3 70B · <span style="color:var(--accent)">ResumeIQ</span> · AI Job Match Agent
</div>
""", unsafe_allow_html=True)
