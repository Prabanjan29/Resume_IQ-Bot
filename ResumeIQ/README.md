---
title: ResumeIQ — AI Job Match Agent
emoji: 🎯
colorFrom: purple
colorTo: pink
sdk: streamlit
sdk_version: "1.32.0"
app_file: app.py
pinned: false
license: mit
---

# 🎯 ResumeIQ — AI-Powered Resume Analyzer

An LLM agent that analyzes your resume against a job description and gives you:

- **Match Score** (0–100) with a verdict
- **Matched / Missing / Bonus Skills** breakdown
- **Section scores** — Skills, Experience, Education, Keywords
- **Strengths & Gaps** analysis
- **5 targeted rewrite suggestions**
- **Missing keywords** to add for ATS optimization

## 🚀 How to Use

1. Paste your resume text
2. Paste the job description
3. Click **Analyze My Resume**
4. Get a detailed AI-powered breakdown in seconds

## 🛠 Tech Stack

- **LLM**: Claude Sonnet (via Anthropic API)
- **Frontend**: Streamlit
- **Deployment**: HuggingFace Spaces

## 🔑 Setup

Set `ANTHROPIC_API_KEY` as a **Secret** in your HuggingFace Space settings.

```
Settings → Repository secrets → ANTHROPIC_API_KEY = sk-ant-...
```

## 📦 Local Run

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
streamlit run app.py
```
