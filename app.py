import streamlit as st
import pandas as pd
import re

# -------------------------------
# PAGE SETTINGS
# -------------------------------

st.set_page_config(
    page_title="AI Job Recommendation",
    page_icon="💼",
    layout="centered"
)

# -------------------------------
# TITLE
# -------------------------------

st.title("💼 AI Job Recommendation System")
st.write("Find the best jobs based on your skills, education and experience.")

# -------------------------------
# LOAD DATASET
# -------------------------------

try:
    jobs = pd.read_csv("jobs.csv")
except FileNotFoundError:
    st.error("❌ jobs.csv file not found!")
    st.stop()

# -------------------------------
# CLEAN COLUMN NAMES
# -------------------------------

jobs.columns = jobs.columns.str.strip()

# -------------------------------
# INPUT SECTION
# -------------------------------

st.header("👤 Enter Your Details")

skills_input = st.text_input(
    "🛠️ Enter your skills",
    placeholder="Example: Python, SQL, Excel"
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

# -------------------------------
# RECOMMENDATION FUNCTION
# -------------------------------

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9+#. ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_skills(text):
    text = clean_text(text)
    return set(
        skill.strip()
        for skill in text.split(",")
        if skill.strip()
    )


def calculate_score(user_skills, user_education, user_experience, job_row):

    job_skills = get_skills(job_row["Skills"])

    # Skill matching
    matched_skills = user_skills.intersection(job_skills)

    if len(user_skills) > 0:
        skill_score = (
            len(matched_skills) / len(user_skills)
        ) * 70
    else:
        skill_score = 0

    # Education matching
    user_education = clean_text(user_education)
    job_education = clean_text(job_row["Education"])

    education_score = 0

    if user_education in job_education:
        education_score = 20
    elif any(
        word in job_education
        for word in user_education.split()
    ):
        education_score = 10

    # Experience matching
    experience_score = 0

    job_experience = str(job_row["Experience"])

    # Extract numbers from experience field
    numbers = re.findall(r"\d+", job_experience)

    if len(numbers) >= 2:
        min_exp = int(numbers[0])
        max_exp = int(numbers[1])

        if min_exp <= user_experience <= max_exp:
            experience_score = 10
        elif user_experience >= min_exp:
            experience_score = 5

    elif len(numbers) == 1:
        required_exp = int(numbers[0])

        if user_experience >= required_exp:
            experience_score = 10
        else:
            experience_score = 0

    total_score = skill_score + education_score + experience_score

    missing_skills = job_skills - user_skills

    return {
        "score": total_score,
        "matched": matched_skills,
        "missing": missing_skills
    }


# -------------------------------
# RECOMMEND BUTTON
# -------------------------------

if st.button("🔍 Recommend Jobs"):

    if not skills_input.strip():
        st.warning("⚠️ Please enter at least one skill.")
        st.stop()

    user_skills = get_skills(skills_input)

    recommendations = []

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
            "experience": job["Experience"]
        })

    # Sort by highest score
    recommendations = sorted(
        recommendations,
        key=lambda x: x["score"],
        reverse=True
    )

    # Top 5
    top_jobs = recommendations[:5]

    # -------------------------------
    # RESULTS
    # -------------------------------

    st.success("✅ Job recommendations generated!")

    st.header("🏆 Top 5 Job Recommendations")

    for i, recommendation in enumerate(top_jobs, start=1):

        st.subheader(
            f"{i}. {recommendation['job']}"
        )

        st.progress(
            min(int(recommendation["score"]), 100)
        )

        st.write(
            f"**Match Score:** "
            f"{recommendation['score']:.1f}%"
        )

        st.write(
            f"**Education Required:** "
            f"{recommendation['education']}"
        )

        st.write(
            f"**Experience Required:** "
            f"{recommendation['experience']}"
        )

        # Matched skills
        if recommendation["matched"]:
            st.write(
                "✅ **Matched Skills:** "
                + ", ".join(
                    sorted(recommendation["matched"])
                )
            )
        else:
            st.write("✅ **Matched Skills:** None")

        # Missing skills
        if recommendation["missing"]:
            st.write(
                "⚠️ **Missing Skills:** "
                + ", ".join(
                    sorted(recommendation["missing"])
                )
            )
        else:
            st.write("🎉 **Missing Skills:** None")

        st.divider()


# -------------------------------
# FOOTER
# -------------------------------

st.caption(
    "🤖 AI Job Recommendation System | "
    "Python + Pandas + Streamlit"
)