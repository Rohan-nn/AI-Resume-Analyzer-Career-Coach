import pdfplumber

SKILLS_DB = [
    "python",
    "java",
    "c",
    "c++",
    "html",
    "css",
    "javascript",
    "react",
    "nodejs",
    "express",
    "flask",
    "django",
    "sql",
    "mysql",
    "mongodb",
    "git",
    "github",
    "opencv",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "ai",
    "data structures",
    "dsa",
    "aws",
    "docker",
    "kubernetes",
    "tensorflow",
    "pytorch",
    "numpy",
    "pandas",
    "streamlit"
]


def extract_text(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS_DB:

        if skill in text:
            found_skills.append(skill)

    return found_skills


def match_skills(resume_skills, jd_text):

    jd_text = jd_text.lower()

    jd_skills = []

    for skill in SKILLS_DB:

        if skill in jd_text:
            jd_skills.append(skill)

    matched = list(
        set(resume_skills) &
        set(jd_skills)
    )

    missing = list(
        set(jd_skills) -
        set(resume_skills)
    )

    score = 0

    if len(jd_skills) > 0:

        score = round(
            (len(matched) /
             len(jd_skills))
            * 100
        )

    return score, matched, missing


def calculate_ats_score(text):

    text = text.lower()

    score = 0

    if "education" in text:
        score += 15

    if "skills" in text:
        score += 15

    if "project" in text:
        score += 15

    if "experience" in text:
        score += 15

    if "achievement" in text:
        score += 10

    if "certification" in text:
        score += 10

    if len(text) > 1000:
        score += 20

    return min(score, 100)


def get_grade(score):

    if score >= 90:
        return "A+"

    elif score >= 80:
        return "A"

    elif score >= 70:
        return "B"

    elif score >= 60:
        return "C"

    return "D"


def detect_sections(text):

    text = text.lower()

    sections = {

        "Education":
        "education" in text,

        "Skills":
        "skills" in text,

        "Projects":
        "project" in text,

        "Experience":
        "experience" in text,

        "Certifications":
        (
            "certification" in text
            or
            "certifications" in text
        ),

        "Achievements":
        (
            "achievement" in text
            or
            "achievements" in text
        )
    }

    return sections


def calculate_resume_strength(
    ats_score,
    skills_count,
    match_score
):

    strength = (
        ats_score * 0.4
        +
        min(skills_count * 5, 30)
        +
        match_score * 0.3
    )

    return min(
        round(strength),
        100
    )