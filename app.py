import streamlit as st
import pandas as pd
import re

# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="AI Job Recommendation",
    page_icon="💼",
    layout="centered"
)

st.title("💼 AI Job Recommendation System")
st.write(
    "Find the best jobs based on your skills, education and experience."
)

# =========================================================
# LOAD DATASET
# =========================================================

try:
    jobs = pd.read_csv("jobs.csv")
except FileNotFoundError:
    st.error("❌ jobs.csv file not found!")
    st.stop()

jobs.columns = jobs.columns.str.strip()

# =========================================================
# USER INPUT
# =========================================================

st.header("👤 Enter Your Details")

skills_input = st.text_input(
    "🛠️ Enter your skills",
    placeholder="Example: Python, SQL, Flask, Pandas, NumPy"
)

education_input = st.selectbox(
    "🎓 Select your education",
    [
        "B.Tech",
        "BCA",
        "MCA",
        "M.Tech",
        "B.Sc",
        "MBA",
        "M.Tech, MBA"
    ]
)

experience_input = st.number_input(
    "💼 Enter your experience in years",
    min_value=0,
    max_value=30,
    value=0,
    step=1
)

# =========================================================
# CLEAN TEXT
# =========================================================

def clean_text(text):
    text = str(text).lower().strip()

    text = text.replace("&", " and ")

    text = re.sub(r"[-_/|;]+", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# SKILL ALIASES
# =========================================================

SKILL_ALIASES = {

    "python": [
        "python"
    ],

    "sql": [
        "sql",
        "mysql",
        "postgresql",
        "database"
    ],

    "flask": [
        "flask"
    ],

    "django": [
        "django"
    ],

    "pandas": [
        "pandas"
    ],

    "numpy": [
        "numpy"
    ],

    "scikit-learn": [
        "scikit learn",
        "scikit-learn",
        "sklearn"
    ],

    "machine learning": [
        "machine learning",
        "ml"
    ],

    "deep learning": [
        "deep learning",
        "dl"
    ],

    "html": [
        "html"
    ],

    "css": [
        "css"
    ],

    "javascript": [
        "javascript",
        "js"
    ],

    "react": [
        "react",
        "reactjs"
    ],

    "java": [
        "java"
    ],

    "git": [
        "git",
        "github"
    ],

    "excel": [
        "excel",
        "ms excel"
    ],

    "power bi": [
        "power bi",
        "powerbi"
    ],

    "tableau": [
        "tableau"
    ],

    "streamlit": [
        "streamlit"
    ],

    "tensorflow": [
        "tensorflow"
    ],

    "pytorch": [
        "pytorch"
    ],

    "aws": [
        "aws",
        "amazon web services"
    ],

    "azure": [
        "azure"
    ]
}

# =========================================================
# GET USER SKILLS
# =========================================================

def get_skills(text):

    text = clean_text(text)

    result = set()

    for standard_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            if alias in text:

                result.add(standard_skill)
                break

    return result


# =========================================================
# GET JOB SKILLS
# =========================================================

def get_job_skills(text):

    text = clean_text(text)

    result = set()

    for standard_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            if alias in text:

                result.add(standard_skill)
                break

    return result


# =========================================================
# EDUCATION MATCH
# =========================================================

def education_score(user_education, job_education):

    user = clean_text(user_education)
    job = clean_text(job_education)

    aliases = {
        "b.tech": ["b.tech", "btech", "b tech"],
        "bca": ["bca"],
        "mca": ["mca"],
        "m.tech": ["m.tech", "mtech", "m tech"],
        "b.sc": ["b.sc", "bsc", "b sc"],
        "mba": ["mba"]
    }

    user_values = aliases.get(
        user,
        [user]
    )

    for value in user_values:

        if value in job:
            return 20

    return 0


# =========================================================
# EXPERIENCE MATCH
# =========================================================

def experience_score(
    user_experience,
    job_experience
):

    text = str(job_experience).lower()

    numbers = re.findall(
        r"\d+(?:\.\d+)?",
        text
    )

    if len(numbers) >= 2:

        minimum = float(numbers[0])
        maximum = float(numbers[1])

        if minimum <= user_experience <= maximum:
            return 10

        if user_experience >= minimum:
            return 5

        return 0

    if len(numbers) == 1:

        required = float(numbers[0])

        if user_experience >= required:
            return 10

        return 0

    return 10


# =========================================================
# JOB TYPE BOOST
# =========================================================

def role_boost(job_name, user_skills):

    job = clean_text(job_name)

    boost = 0

    # Python related jobs
    if "python" in user_skills:

        if (
            "python developer" in job
            or "python developer" in job
            or "backend developer" in job
            or "flask developer" in job
        ):
            boost += 8

    # Data related jobs
    if (
        "python" in user_skills
        and "pandas" in user_skills
        and "numpy" in user_skills
    ):

        if (
            "data analyst" in job
            or "data scientist" in job
            or "data science" in job
        ):
            boost += 7

    # AI / ML
    if (
        "python" in user_skills
        and "machine learning" in user_skills
    ):

        if (
            "ai engineer" in job
            or "machine learning" in job
            or "ml engineer" in job
            or "data scientist" in job
        ):
            boost += 7

    # Web
    if (
        "html" in user_skills
        and "css" in user_skills
        and "javascript" in user_skills
    ):

        if (
            "web developer" in job
            or "frontend" in job
            or "full stack" in job
        ):
            boost += 7

    return boost


# =========================================================
# RECOMMEND BUTTON
# =========================================================

if st.button("🔍 Recommend Jobs"):

    if not skills_input.strip():

        st.warning(
            "⚠️ Please enter your skills."
        )

        st.stop()

    user_skills = get_skills(
        skills_input
    )

    if not user_skills:

        st.warning(
            "⚠️ No recognised skills found. "
            "Please enter skills such as Python, SQL, Flask, etc."
        )

        st.stop()

    recommendations = []

    # =====================================================
    # CALCULATE EACH JOB
    # =====================================================

    for _, job in jobs.iterrows():

        job_skills = get_job_skills(
            job["Skills"]
        )

        # -----------------------------------------------
        # SKILL MATCH
        # -----------------------------------------------

        matched = (
            user_skills.intersection(
                job_skills
            )
        )

        missing = (
            job_skills - user_skills
        )

        if len(job_skills) > 0:

            skill_percentage = (
                len(matched)
                / len(job_skills)
            ) * 100

        else:

            skill_percentage = 0

        # -----------------------------------------------
        # EDUCATION
        # -----------------------------------------------

        edu_score = education_score(
            education_input,
            job["Education"]
        )

        # -----------------------------------------------
        # EXPERIENCE
        # -----------------------------------------------

        exp_score = experience_score(
            experience_input,
            job["Experience"]
        )

        # -----------------------------------------------
        # MAIN SCORE
        # -----------------------------------------------

        skill_score = (
            skill_percentage * 0.70
        )

        total_score = (
            skill_score
            + edu_score
            + exp_score
        )

        # -----------------------------------------------
        # ROLE BOOST
        # -----------------------------------------------

        boost = role_boost(
            job["Job"],
            user_skills
        )

        total_score += boost

        total_score = min(
            total_score,
            100
        )

        recommendations.append({

            "job": job["Job"],

            "score": total_score,

            "matched": matched,

            "missing": missing,

            "education": job["Education"],

            "experience": job["Experience"]

        })

    # =====================================================
    # SORT BEST MATCH FIRST
    # =====================================================

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # =====================================================
    # TOP 5
    # =====================================================

    top_jobs = recommendations[:5]

    # =====================================================
    # RESULTS
    # =====================================================

    st.success(
        "✅ Best matching jobs found!"
    )

    st.header(
        "🏆 Top 5 Job Recommendations"
    )

    for i, rec in enumerate(
        top_jobs,
        start=1
    ):

        score = rec["score"]

        st.subheader(
            f"{i}. {rec['job']}"
        )

        st.progress(
            int(score)
        )

        st.write(
            f"**Match Score:** "
            f"{score:.1f}%"
        )

        st.write(
            f"**Education Required:** "
            f"{rec['education']}"
        )

        st.write(
            f"**Experience Required:** "
            f"{rec['experience']}"
        )

        # -----------------------------------------------
        # MATCHED SKILLS
        # -----------------------------------------------

        if rec["matched"]:

            st.write(
                "✅ **Matched Skills:** "
                + ", ".join(
                    sorted(rec["matched"])
                )
            )

        else:

            st.write(
                "✅ **Matched Skills:** None"
            )

        # -----------------------------------------------
        # MISSING SKILLS
        # -----------------------------------------------

        if rec["missing"]:

            st.write(
                "⚠️ **Missing Skills:** "
                + ", ".join(
                    sorted(rec["missing"])
                )
            )

        else:

            st.write(
                "🎉 **Missing Skills:** None"
            )

        # -----------------------------------------------
        # RECOMMENDATION LEVEL
        # -----------------------------------------------

        if score >= 80:

            st.success(
                "🌟 Excellent Match"
            )

        elif score >= 60:

            st.info(
                "👍 Good Match"
            )

        elif score >= 40:

            st.warning(
                "🙂 Moderate Match"
            )

        else:

            st.error(
                "⚠️ Low Match"
            )

        st.divider()


# =========================================================
# FOOTER
# =========================================================

st.caption(
    "🤖 AI Job Recommendation System | "
    "Python + Pandas + Streamlit"
)
