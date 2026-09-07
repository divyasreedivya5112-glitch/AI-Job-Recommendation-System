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

# =========================================================
# TITLE
# =========================================================

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

# Remove extra spaces from column names
jobs.columns = jobs.columns.str.strip()

# Check required columns
required_columns = [
    "Job",
    "Skills",
    "Education",
    "Experience"
]

missing_columns = [
    col for col in required_columns
    if col not in jobs.columns
]

if missing_columns:
    st.error(
        "❌ Missing columns in jobs.csv: "
        + ", ".join(missing_columns)
    )
    st.stop()

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
# TEXT CLEANING
# =========================================================

def clean_text(text):

    text = str(text).lower().strip()

    # Replace different separators with spaces
    text = re.sub(r"[/|;]+", " ", text)

    # Replace hyphens with spaces
    text = re.sub(r"-", " ", text)

    # Remove unwanted special characters
    text = re.sub(
        r"[^a-z0-9+#. ]",
        " ",
        text
    )

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# KNOWN SKILLS
# =========================================================

KNOWN_SKILLS = [
    "power bi",
    "powerbi",
    "machine learning",
    "deep learning",
    "scikit learn",
    "scikit-learn",

    "python",
    "sql",
    "excel",
    "django",
    "flask",
    "streamlit",
    "pandas",
    "numpy",

    "java",
    "javascript",
    "typescript",
    "html",
    "css",
    "react",
    "node",
    "nodejs",

    "c++",
    "c#",

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
# SKILL EXTRACTION
# =========================================================

def get_skills(text):

    text = clean_text(text)

    found_skills = set()

    # -----------------------------------------------------
    # First find known multi-word skills
    # -----------------------------------------------------

    for skill in KNOWN_SKILLS:

        skill_clean = clean_text(skill)

        if skill_clean in text:

            # Convert scikit-learn variations
            if skill_clean == "scikit learn":
                found_skills.add("scikit-learn")

            elif skill_clean == "powerbi":
                found_skills.add("power bi")

            else:
                found_skills.add(skill_clean)

    # -----------------------------------------------------
    # Handle comma-separated values
    # -----------------------------------------------------

    parts = re.split(
        r",",
        str(text)
    )

    for part in parts:

        part = clean_text(part)

        if not part:
            continue

        # If already a known skill
        if part in KNOWN_SKILLS:

            if part == "powerbi":
                found_skills.add("power bi")

            elif part == "scikit learn":
                found_skills.add("scikit-learn")

            else:
                found_skills.add(part)

    return found_skills


# =========================================================
# EDUCATION MATCHING
# =========================================================

def education_match(
    user_education,
    job_education
):

    user_education = clean_text(
        user_education
    )

    job_education = clean_text(
        job_education
    )

    # -----------------------------------------------------
    # Exact education found
    # -----------------------------------------------------

    if user_education in job_education:

        return 20

    # -----------------------------------------------------
    # Handle B.Tech / BTech variations
    # -----------------------------------------------------

    if (
        user_education == "b.tech"
        and (
            "btech" in job_education
            or "b tech" in job_education
        )
    ):

        return 20

    if (
        user_education == "bca"
        and "bca" in job_education
    ):

        return 20

    if (
        user_education == "mca"
        and "mca" in job_education
    ):

        return 20

    if (
        user_education == "m.tech"
        and (
            "mtech" in job_education
            or "m tech" in job_education
        )
    ):

        return 20

    if (
        user_education == "b.sc"
        and (
            "bsc" in job_education
            or "b sc" in job_education
        )
    ):

        return 20

    if (
        user_education == "mba"
        and "mba" in job_education
    ):

        return 20

    return 0


# =========================================================
# EXPERIENCE MATCHING
# =========================================================

def experience_match(
    user_experience,
    job_experience
):

    job_experience = str(
        job_experience
    ).lower()

    # -----------------------------------------------------
    # Find numbers
    # -----------------------------------------------------

    numbers = re.findall(
        r"\d+(?:\.\d+)?",
        job_experience
    )

    # -----------------------------------------------------
    # Example: 0-2
    # -----------------------------------------------------

    if len(numbers) >= 2:

        min_exp = float(
            numbers[0]
        )

        max_exp = float(
            numbers[1]
        )

        if (
            min_exp
            <= user_experience
            <= max_exp
        ):

            return 10

        elif user_experience >= min_exp:

            return 5

        else:

            return 0

    # -----------------------------------------------------
    # Example: 2
    # -----------------------------------------------------

    elif len(numbers) == 1:

        required_exp = float(
            numbers[0]
        )

        if user_experience >= required_exp:

            return 10

        else:

            return 0

    # -----------------------------------------------------
    # If experience is not specified
    # -----------------------------------------------------

    return 10


# =========================================================
# SKILL MATCHING
# =========================================================

def skill_match(
    user_skills,
    job_skills
):

    matched = set()
    missing = set()

    # -----------------------------------------------------
    # Compare job skills with user skills
    # -----------------------------------------------------

    for job_skill in job_skills:

        job_skill = clean_text(
            job_skill
        )

        found = False

        for user_skill in user_skills:

            user_skill = clean_text(
                user_skill
            )

            # Exact match
            if job_skill == user_skill:

                matched.add(
                    job_skill
                )

                found = True
                break

            # Partial / variation match
            if (
                job_skill in user_skill
                or user_skill in job_skill
            ):

                matched.add(
                    job_skill
                )

                found = True
                break

        # Skill not found
        if not found:

            missing.add(
                job_skill
            )

    # -----------------------------------------------------
    # Calculate skill score
    # -----------------------------------------------------

    if len(job_skills) == 0:

        skill_score = 70

    else:

        skill_score = (
            len(matched)
            / len(job_skills)
        ) * 70

    return (
        skill_score,
        matched,
        missing
    )


# =========================================================
# CALCULATE FINAL SCORE
# =========================================================

def calculate_score(
    user_skills,
    user_education,
    user_experience,
    job_row
):

    # Get job skills
    job_skills = get_skills(
        job_row["Skills"]
    )

    # -----------------------------------------------------
    # Skill score = 70
    # Education = 20
    # Experience = 10
    # Total = 100
    # -----------------------------------------------------

    skill_score, matched_skills, missing_skills = skill_match(
        user_skills,
        job_skills
    )

    education_score = education_match(
        user_education,
        job_row["Education"]
    )

    experience_score = experience_match(
        user_experience,
        job_row["Experience"]
    )

    total_score = (
        skill_score
        + education_score
        + experience_score
    )

    # Never exceed 100
    total_score = min(
        total_score,
        100
    )

    return {
        "score": total_score,
        "matched": matched_skills,
        "missing": missing_skills,
        "skill_score": skill_score,
        "education_score": education_score,
        "experience_score": experience_score
    }


# =========================================================
# RECOMMEND JOBS
# =========================================================

if st.button(
    "🔍 Recommend Jobs"
):

    # -----------------------------------------------------
    # Validate skills
    # -----------------------------------------------------

    if not skills_input.strip():

        st.warning(
            "⚠️ Please enter at least one skill."
        )

        st.stop()

    # -----------------------------------------------------
    # Get user skills
    # -----------------------------------------------------

    user_skills = get_skills(
        skills_input
    )

    # -----------------------------------------------------
    # If skills couldn't be detected
    # -----------------------------------------------------

    if not user_skills:

        st.warning(
            "⚠️ Please enter valid skills such as "
            "Python, SQL, Excel, Power BI."
        )

        st.stop()

    # -----------------------------------------------------
    # Store recommendations
    # -----------------------------------------------------

    recommendations = []

    # -----------------------------------------------------
    # Process every job
    # -----------------------------------------------------

    for _, job in jobs.iterrows():

        result = calculate_score(
            user_skills,
            education_input,
            experience_input,
            job
        )

        recommendations.append({

            "job": job["Job"],

            "score": result["score"],

            "matched": result["matched"],

            "missing": result["missing"],

            "education": job["Education"],

            "experience": job["Experience"],

            "skill_score": result["skill_score"],

            "education_score": result["education_score"],

            "experience_score": result["experience_score"]
        })

    # -----------------------------------------------------
    # Sort highest score first
    # -----------------------------------------------------

    recommendations = sorted(
        recommendations,
        key=lambda x: x["score"],
        reverse=True
    )

    # -----------------------------------------------------
    # Top 5
    # -----------------------------------------------------

    top_jobs = recommendations[:5]

    # =====================================================
    # RESULTS
    # =====================================================

    st.success(
        "✅ Job recommendations generated!"
    )

    st.header(
        "🏆 Top 5 Job Recommendations"
    )

    # -----------------------------------------------------
    # Display jobs
    # -----------------------------------------------------

    for i, recommendation in enumerate(
        top_jobs,
        start=1
    ):

        st.subheader(
            f"{i}. {recommendation['job']}"
        )

        # -------------------------------------------------
        # Score
        # -------------------------------------------------

        score = recommendation["score"]

        st.progress(
            int(score)
        )

        st.write(
            f"**Match Score:** "
            f"{score:.1f}%"
        )

        # -------------------------------------------------
        # Education
        # -------------------------------------------------

        st.write(
            f"**Education Required:** "
            f"{recommendation['education']}"
        )

        # -------------------------------------------------
        # Experience
        # -------------------------------------------------

        st.write(
            f"**Experience Required:** "
            f"{recommendation['experience']}"
        )

        # -------------------------------------------------
        # Matched Skills
        # -------------------------------------------------

        if recommendation["matched"]:

            st.write(
                "✅ **Matched Skills:** "
                + ", ".join(
                    sorted(
                        recommendation["matched"]
                    )
                )
            )

        else:

            st.write(
                "✅ **Matched Skills:** None"
            )

        # -------------------------------------------------
        # Missing Skills
        # -------------------------------------------------

        if recommendation["missing"]:

            st.write(
                "⚠️ **Missing Skills:** "
                + ", ".join(
                    sorted(
                        recommendation["missing"]
                    )
                )
            )

        else:

            st.write(
                "🎉 **Missing Skills:** None"
            )

        # -------------------------------------------------
        # Score Breakdown
        # -------------------------------------------------

        with st.expander(
            "📊 Score Breakdown"
        ):

            st.write(
                f"🛠️ Skills: "
                f"{recommendation['skill_score']:.1f}/70"
            )

            st.write(
                f"🎓 Education: "
                f"{recommendation['education_score']}/20"
            )

            st.write(
                f"💼 Experience: "
                f"{recommendation['experience_score']}/10"
            )

            st.write(
                f"🏆 Total: "
                f"{recommendation['score']:.1f}/100"
            )

        st.divider()


# =========================================================
# FOOTER
# =========================================================

st.caption(
    "🤖 AI Job Recommendation System | "
    "Python + Pandas + Streamlit"
)
