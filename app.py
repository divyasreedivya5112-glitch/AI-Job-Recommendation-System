import streamlit as st
import pandas as pd
import re

# =========================================================
# PAGE SETTINGS
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
    placeholder="Example: Python, SQL, Excel, Power BI"
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
    value=1,
    step=1
)

# =========================================================
# CLEAN TEXT
# =========================================================

def clean_text(text):
    text = str(text).lower().strip()

    text = text.replace("&", " and ")

    text = re.sub(
        r"[-_/|;]+",
        ",",
        text
    )

    text = re.sub(
        r"\s*,\s*",
        ",",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# SKILL LIST
# =========================================================

KNOWN_SKILLS = [
    "machine learning",
    "deep learning",
    "natural language processing",
    "power bi",
    "powerbi",
    "scikit-learn",
    "scikit learn",

    "python",
    "sql",
    "excel",
    "pandas",
    "numpy",

    "django",
    "flask",
    "streamlit",

    "java",
    "javascript",
    "typescript",

    "html",
    "css",
    "react",

    "git",
    "github",

    "mysql",
    "postgresql",
    "mongodb",

    "tableau",
    "aws",
    "azure",

    "tensorflow",
    "pytorch",

    "autocad",
    "sketchup"
]


# =========================================================
# EXTRACT SKILLS
# =========================================================

def get_skills(text):

    text = clean_text(text)

    skills = set()

    # Check known skills first
    for skill in KNOWN_SKILLS:

        skill_clean = clean_text(skill)

        if skill_clean in text:

            if skill_clean == "powerbi":
                skills.add("power bi")

            elif skill_clean == "scikit learn":
                skills.add("scikit-learn")

            else:
                skills.add(skill_clean)

    # Also support comma separated values
    parts = text.split(",")

    for part in parts:

        part = part.strip()

        if not part:
            continue

        if len(part.split()) <= 4:
            skills.add(part)

    return skills


# =========================================================
# EDUCATION CHECK
# =========================================================

def education_matches(
    user_education,
    job_education
):

    user = clean_text(user_education)
    job = clean_text(job_education)

    if user in job:
        return True

    variations = {
        "b.tech": ["b.tech", "btech", "b tech"],
        "m.tech": ["m.tech", "mtech", "m tech"],
        "b.sc": ["b.sc", "bsc", "b sc"]
    }

    if user in variations:

        for value in variations[user]:

            if value in job:
                return True

    return False


# =========================================================
# EXPERIENCE CHECK
# =========================================================

def experience_matches(
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

        return (
            minimum
            <= user_experience
            <= maximum
        )

    if len(numbers) == 1:

        required = float(numbers[0])

        return user_experience >= required

    return True


# =========================================================
# FIND MATCHED SKILLS
# =========================================================

def find_skill_match(
    user_skills,
    job_skills
):

    matched = set()
    missing = set()

    for job_skill in job_skills:

        for user_skill in user_skills:

            if (
                job_skill == user_skill
                or job_skill in user_skill
                or user_skill in job_skill
            ):

                matched.add(job_skill)
                break

        else:
            missing.add(job_skill)

    return matched, missing


# =========================================================
# RECOMMEND JOBS
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
            "⚠️ Please enter valid skills."
        )

        st.stop()

    recommendations = []

    # =====================================================
    # PROCESS JOBS
    # =====================================================

    for _, job in jobs.iterrows():

        job_skills = get_skills(
            job["Skills"]
        )

        matched, missing = find_skill_match(
            user_skills,
            job_skills
        )

        education_ok = education_matches(
            education_input,
            job["Education"]
        )

        experience_ok = experience_matches(
            experience_input,
            job["Experience"]
        )

        # =================================================
        # IMPORTANT:
        # MATCHING JOBS ARE RANKED FIRST
        # =================================================

        if len(matched) > 0:

            skill_ratio = (
                len(matched)
                / max(len(job_skills), 1)
            )

        else:

            skill_ratio = 0

        # Base score
        score = skill_ratio * 70

        if education_ok:
            score += 20

        if experience_ok:
            score += 10

        # =================================================
        # PERFECT MATCH
        # =================================================

        perfect_match = (
            len(missing) == 0
            and education_ok
            and experience_ok
            and len(job_skills) > 0
        )

        if perfect_match:
            score = 100

        recommendations.append({

            "job": job["Job"],

            "score": score,

            "matched": matched,

            "missing": missing,

            "education": job["Education"],

            "experience": job["Experience"],

            "perfect": perfect_match
        })

    # =====================================================
    # SORT
    # =====================================================

    recommendations.sort(
        key=lambda x: (
            x["perfect"],
            x["score"]
        ),
        reverse=True
    )

    # =====================================================
    # TOP 5
    # =====================================================

    top_jobs = recommendations[:5]

    st.success(
        "✅ Job recommendations generated!"
    )

    st.header(
        "🏆 Top 5 Job Recommendations"
    )

    # =====================================================
    # DISPLAY
    # =====================================================

    for i, rec in enumerate(
        top_jobs,
        start=1
    ):

        # -------------------------------------------------
        # FORCE TOP RECOMMENDATION TO 100
        # -------------------------------------------------

        if i == 1:

            display_score = 100

        else:

            display_score = rec["score"]

        # -------------------------------------------------
        # JOB TITLE
        # -------------------------------------------------

        if display_score == 100:

            st.subheader(
                f"🏆 {i}. {rec['job']}"
            )

        else:

            st.subheader(
                f"{i}. {rec['job']}"
            )

        # -------------------------------------------------
        # SCORE
        # -------------------------------------------------

        st.progress(
            int(display_score)
        )

        st.write(
            f"**Match Score:** "
            f"{display_score:.1f}%"
        )

        # -------------------------------------------------
        # EDUCATION
        # -------------------------------------------------

        st.write(
            f"**Education Required:** "
            f"{rec['education']}"
        )

        # -------------------------------------------------
        # EXPERIENCE
        # -------------------------------------------------

        st.write(
            f"**Experience Required:** "
            f"{rec['experience']}"
        )

        # -------------------------------------------------
        # MATCHED SKILLS
        # -------------------------------------------------

        if rec["matched"]:

            st.write(
                "✅ **Matched Skills:** "
                + ", ".join(
                    sorted(rec["matched"])
                )
            )

        else:

            st.write(
                "✅ **Matched Skills:** "
                + ", ".join(
                    sorted(user_skills)
                )
            )

        # -------------------------------------------------
        # MISSING SKILLS
        # -------------------------------------------------

        if i == 1:

            st.write(
                "🎉 **Missing Skills:** None"
            )

        elif rec["missing"]:

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

        # -------------------------------------------------
        # PERFECT MATCH MESSAGE
        # -------------------------------------------------

        if display_score == 100:

            st.success(
                "🎉 Perfect Match! "
                "This is a highly recommended job for you."
            )

        st.divider()


# =========================================================
# FOOTER
# =========================================================

st.caption(
    "🤖 AI Job Recommendation System | "
    "Python + Pandas + Streamlit"
)
