import google.generativeai as genai


def setup_gemini(api_key):

    genai.configure(
        api_key=api_key
    )

    return genai.GenerativeModel(
        "gemini-2.5-flash"
    )


def get_ai_review(
    model,
    resume_text,
    job_description
):

    prompt = f"""
You are an expert recruiter and ATS evaluator.

Resume:
{resume_text}

Job Description:
{job_description}

Provide:

# Overall Evaluation

# Strengths

# Weaknesses

# Missing Skills

# ATS Improvements

# Final Recommendation
"""

    response = model.generate_content(
        prompt
    )

    return response.text


def generate_resume_summary(
    model,
    resume_text
):

    prompt = f"""
Create a professional resume summary.

Resume:

{resume_text}

Requirements:

- Professional tone
- ATS friendly
- 80-120 words
- Suitable for internships
"""

    response = model.generate_content(
        prompt
    )

    return response.text


def generate_interview_questions(
    model,
    resume_text,
    job_description
):

    prompt = f"""
Resume:
{resume_text}

Job Description:
{job_description}

Generate:

5 Technical Questions

5 HR Questions

5 Project Based Questions
"""

    response = model.generate_content(
        prompt
    )

    return response.text
def generate_skill_recommendations(
    model,
    resume_text,
    job_description
):

    prompt = f"""
Resume:
{resume_text}

Job Description:
{job_description}

Provide:

1. Missing Technical Skills

2. Important Tools Missing

3. Certifications To Pursue

4. Projects To Build

5. Learning Roadmap
"""

    response = model.generate_content(
        prompt
    )

    return response.text


def generate_career_feedback(
    model,
    resume_text
):

    prompt = f"""
Analyze this resume.

{resume_text}

Provide:

1. Career Level

2. Strongest Areas

3. Weakest Areas

4. Recommended Career Paths

5. Internship Readiness Score out of 100
"""

    response = model.generate_content(
        prompt
    )

    return response.text


def generate_cover_letter(
    model,
    resume_text,
    job_description
):

    prompt = f"""
Create a professional internship cover letter.

Resume:
{resume_text}

Job Description:
{job_description}

Requirements:

- Professional tone
- ATS friendly
- 250-400 words
- Internship focused
- Ready to submit
"""

    response = model.generate_content(
        prompt
    )

    return response.text


def generate_linkedin_summary(
    model,
    resume_text
):

    prompt = f"""
Create a professional LinkedIn About section.

Resume:
{resume_text}

Requirements:

- Professional
- ATS friendly
- Internship focused
- 150-250 words
- Strong opening
"""

    response = model.generate_content(
        prompt
    )

    return response.text