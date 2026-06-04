import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from utils import (
    extract_text,
    extract_skills,
    match_skills,
    calculate_ats_score,
    get_grade,
    detect_sections,
    calculate_resume_strength
)

from gemini_utils import (
    setup_gemini,
    get_ai_review,
    generate_resume_summary,
    generate_interview_questions,
    generate_skill_recommendations,
    generate_career_feedback,
    generate_cover_letter,
    generate_linkedin_summary
)

st.set_page_config(
    page_title="AI Resume Analyzer & Career Coach",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>

.stApp{
background:linear-gradient(
135deg,
#020617,
#0f172a,
#1e1b4b
);
}

.hero{
text-align:center;
padding:30px;
margin-bottom:20px;
}

.hero-title{
font-size:70px;
font-weight:800;
background:linear-gradient(
90deg,
#60a5fa,
#a78bfa
);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.hero-sub{
font-size:20px;
color:#cbd5e1;
}

.card{
background:rgba(255,255,255,0.08);
backdrop-filter:blur(20px);
border:1px solid rgba(255,255,255,0.15);
border-radius:25px;
padding:20px;
text-align:center;
box-shadow:
0 8px 32px rgba(0,0,0,0.35);
}

.metric{
font-size:42px;
font-weight:bold;
color:white;
}

.metric-title{
font-size:15px;
color:#cbd5e1;
}

.skill{
background:#2563eb;
padding:8px 14px;
border-radius:20px;
display:inline-block;
margin:4px;
color:white;
}

.missing{
background:#dc2626;
padding:8px 14px;
border-radius:20px;
display:inline-block;
margin:4px;
color:white;
}

</style>
""", unsafe_allow_html=True)

st.sidebar.title(
    "🚀 AI Resume Analyzer"
)

api_key = st.sidebar.text_input(
    "Gemini API Key",
    type="password"
)

st.sidebar.markdown("---")

st.sidebar.success("""
✅ ATS Analysis

✅ Resume Strength

✅ Skill Gap Detection

✅ AI Review

✅ AI Summary

✅ Interview Questions

✅ Career Coach

✅ Cover Letter Generator

✅ LinkedIn Summary Generator

✅ PDF Report
""")

st.markdown("""
<div class='hero'>
<div class='hero-title'>
AI Resume Analyzer
</div>

<div class='hero-sub'>
Optimize Resume • Beat ATS • Prepare For Interviews
</div>

<br>

<div class='hero-sub'>
Powered by Gemini AI
</div>

</div>
""", unsafe_allow_html=True)

left,right = st.columns(2)

with left:

    uploaded_file = st.file_uploader(
        "📄 Upload Resume",
        type=["pdf"]
    )

with right:

    job_description = st.text_area(
        "💼 Paste Job Description",
        height=250
    )

def create_pdf_report(content):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "AI Resume Analysis Report",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1,12)
    )

    story.append(
        Paragraph(
            content,
            styles["BodyText"]
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer

if uploaded_file:

    resume_text = extract_text(
        uploaded_file
    )

    skills = extract_skills(
        resume_text
    )

    ats_score = calculate_ats_score(
        resume_text
    )

    match_score = 0
    matched = []
    missing = []

    if job_description:

        (
            match_score,
            matched,
            missing
        ) = match_skills(
            skills,
            job_description
        )

    grade = get_grade(
        ats_score
    )

    strength = calculate_resume_strength(
        ats_score,
        len(skills),
        match_score
    )

    sections = detect_sections(
        resume_text
    ) 
    c1,c2,c3,c4 = st.columns(4)

    with c1:

        st.markdown(f"""
        <div class='card'>
        <div class='metric-title'>
        ATS SCORE
        </div>

        <div class='metric'>
        {ats_score}%
        </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown(f"""
        <div class='card'>
        <div class='metric-title'>
        MATCH SCORE
        </div>

        <div class='metric'>
        {match_score}%
        </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown(f"""
        <div class='card'>
        <div class='metric-title'>
        GRADE
        </div>

        <div class='metric'>
        {grade}
        </div>
        </div>
        """, unsafe_allow_html=True)

    with c4:

        st.markdown(f"""
        <div class='card'>
        <div class='metric-title'>
        RESUME STRENGTH
        </div>

        <div class='metric'>
        {strength}%
        </div>
        </div>
        """, unsafe_allow_html=True)

    tabs = st.tabs([
        "📊 Dashboard",
        "🛠 Skills",
        "🤖 AI Tools",
        "📈 Career Coach",
        "📄 Resume"
    ])

    with tabs[0]:

        st.subheader(
            "Resume Analytics"
        )

        chart_df = pd.DataFrame({
            "Metric":[
                "ATS Score",
                "Match Score",
                "Strength"
            ],
            "Score":[
                ats_score,
                match_score,
                strength
            ]
        })

        fig = px.bar(
            chart_df,
            x="Metric",
            y="Score",
            title="Resume Performance"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.progress(
            strength / 100
        )

        report_text = f"""
ATS Score: {ats_score}

Match Score: {match_score}

Resume Grade: {grade}

Resume Strength: {strength}

Skills Found:
{", ".join(skills)}

Missing Skills:
{", ".join(missing)}
"""

        pdf_file = create_pdf_report(
            report_text
        )

        st.download_button(
            "📥 Download Analysis Report",
            pdf_file,
            file_name="resume_report.pdf",
            mime="application/pdf"
        )

    with tabs[1]:

        st.subheader(
            "Skills Analysis"
        )

        if skills:

            skill_df = pd.DataFrame({
                "Skill": skills,
                "Count": [1] * len(skills)
            })

            fig = px.pie(
                skill_df,
                names="Skill",
                values="Count",
                title="Detected Skills"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        left,right = st.columns(2)

        with left:

            st.subheader(
                "Skills Found"
            )

            for skill in skills:

                st.markdown(
                    f"<span class='skill'>{skill.upper()}</span>",
                    unsafe_allow_html=True
                )

        with right:

            st.subheader(
                "Missing Skills"
            )

            if missing:

                for skill in missing:

                    st.markdown(
                        f"<span class='missing'>{skill.upper()}</span>",
                        unsafe_allow_html=True
                    )

            else:

                st.success(
                    "No Missing Skills"
                )  
                
    with tabs[2]:

        if api_key:

            model = setup_gemini(
                api_key
            )

            ai_tabs = st.tabs([
                "Review",
                "Summary",
                "Interview",
                "Cover Letter",
                "LinkedIn"
            ])

            with ai_tabs[0]:

                if st.button(
                    "🤖 Generate AI Review"
                ):

                    with st.spinner(
                        "Analyzing Resume..."
                    ):

                        result = get_ai_review(
                            model,
                            resume_text,
                            job_description
                        )

                    st.write(
                        result
                    )

            with ai_tabs[1]:

                if st.button(
                    "📝 Generate Summary"
                ):

                    with st.spinner(
                        "Generating Summary..."
                    ):

                        result = generate_resume_summary(
                            model,
                            resume_text
                        )

                    st.write(
                        result
                    )

            with ai_tabs[2]:

                if st.button(
                    "🎤 Generate Interview Questions"
                ):

                    with st.spinner(
                        "Creating Questions..."
                    ):

                        result = generate_interview_questions(
                            model,
                            resume_text,
                            job_description
                        )

                    st.write(
                        result
                    )

            with ai_tabs[3]:

                if st.button(
                    "📄 Generate Cover Letter"
                ):

                    with st.spinner(
                        "Writing Cover Letter..."
                    ):

                        result = generate_cover_letter(
                            model,
                            resume_text,
                            job_description
                        )

                    st.write(
                        result
                    )

            with ai_tabs[4]:

                if st.button(
                    "💼 Generate LinkedIn Summary"
                ):

                    with st.spinner(
                        "Building LinkedIn Profile..."
                    ):

                        result = generate_linkedin_summary(
                            model,
                            resume_text
                        )

                    st.write(
                        result
                    )

        else:

            st.warning(
                "Please enter Gemini API Key in sidebar."
            )

    with tabs[3]:

        if api_key:

            model = setup_gemini(
                api_key
            )

            st.subheader(
                "Career Coach"
            )

            if st.button(
                "📈 Generate Career Feedback"
            ):

                with st.spinner(
                    "Analyzing Career Path..."
                ):

                    result = generate_career_feedback(
                        model,
                        resume_text
                    )

                st.write(
                    result
                )

            if st.button(
                "🚀 Generate Career Roadmap"
            ):

                with st.spinner(
                    "Creating Learning Roadmap..."
                ):

                    result = generate_skill_recommendations(
                        model,
                        resume_text,
                        job_description
                    )

                st.write(
                    result
                )

        else:

            st.warning(
                "Please enter Gemini API Key in sidebar."
            )

    with tabs[4]:

        st.subheader(
            "Resume Sections"
        )

        for section,status in sections.items():

            if status:

                st.success(
                    f"✅ {section}"
                )

            else:

                st.error(
                    f"❌ {section}"
                )

        st.markdown("---")

        st.subheader(
            "Resume Preview"
        )

        st.text_area(
            "",
            resume_text,
            height=500
        )

        st.markdown("---")

        st.info(
            f"""
ATS Score: {ats_score}

Match Score: {match_score}

Resume Grade: {grade}

Resume Strength: {strength}%
"""
        )