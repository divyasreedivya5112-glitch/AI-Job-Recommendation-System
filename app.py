import streamlit as st
import pandas as pd
import re

# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="AI Job Recommendation",
    page_icon="💼",
    layout="centered"
)

# =====================================================
# SIMPLE STYLISH BACKGROUND
# =====================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 5% 8%,
                rgba(255, 190, 215, 0.25),
                transparent 180px
            ),
            radial-gradient(
                circle at 95% 12%,
                rgba(205, 190, 255, 0.25),
                transparent 190px
            ),
            radial-gradient(
                circle at 90% 90%,
                rgba(255, 220, 180, 0.20),
                transparent 180px
            ),
            linear-gradient(
                135deg,
                #fffafd,
                #fffdf9
            );
        background-attachment: fixed;
    }

    h1 {
        color: #68456f !important;
        text-align: center;
    }

    h2, h3 {
        color: #704d78 !important;
    }

    .stButton > button {
        width: 100%;
        border-radius: 15px;
        border: none;
        background: linear-gradient(
            90deg,
            #ee91b5,
            #b996e5
        );
        color: white;
        font-size: 18px;
        font-weight: 600;
        padding: 12px;
    }

    .job-card {
        background: rgba(255,255,255,0.90);
        border: 1px solid #efc8dc;
        border-radius: 18px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 5px 20px rgba(100,70,110,0.08);
    }

    .score {
        color: #79519a;
        font-size: 27px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# TITLE
# =====================================================

st.title("💼 AI Job Recommendation System")

st.markdown(
    """
    <p style="text-align:center; font-size:18px;">
    Find the best jobs based on your skills, education and experience ✨
    </p>
    """,
    unsafe_allow_html=True
)

# =====================================================
# LOAD JOB DATA
# =====================================================

try:
    jobs = pd.read_csv("jobs.csv")

except FileNotFoundError:
    st.error("❌ jobs.csv file not found!")
    st.stop()

jobs.columns = jobs.columns.str.strip()

# =====================================================
# INPUT SECTION
# =====================================================

st.header("👤 Enter Your Details")

skills_input = st.text_input(
    "🛠️ Enter your skills",
    placeholder="Python, SQL, Flask, Pandas, NumPy, Machine Learning"
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

# =====================================================
# CLEAN TEXT
# =====================================================

def clean_text(text):

    text = str(text).lower().strip()

    text = text.replace(
        "&",
        " and "
    )

    text = re.sub(
        r"[-_/|;]+",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =====================================================
# SKILL ALIASES
# =====================================================

SKILL_ALIASES = {

    "python": [
        "python"
    ],

    "sql": [
        "sql",
        "mysql",
        "postgresql"
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
        "scikit-learn",
        "scikit learn",
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
        "excel"
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
        "aws"
    ],

    "azure": [
        "azure"
    ]
}

# =====================================================
# EXTRACT SKILLS
# =====================================================

def get_skills(text):

    text = clean_text(text)

    result = set()

    for standard_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            if alias in text:

                result.add(
                    standard_skill
                )

                break

    return result


# =====================================================
# EDUCATION MATCH
# =====================================================

def get_education_score(
    user_education,
    job_education
):

    user = clean_text(
        user_education
    )

    job = clean_text(
        job_education
    )

    education_aliases = {

        "b.tech": [
            "b.tech",
            "btech",
            "b tech"
        ],

        "bca": [
            "bca"
        ],

        "mca": [
            "mca"
        ],

        "m.tech": [
            "m.tech",
            "mtech",
            "m tech"
        ],

        "b.sc": [
            "b.sc",
            "bsc",
            "b sc"
        ],

        "mba": [
            "mba"
        ]
    }

    possible_values = education_aliases.get(
        user,
        [user]
    )

    for value in possible_values:

        if value in job:

            return 20

    return 0


# =====================================================
# EXPERIENCE MATCH
# =====================================================

def get_experience_score(
    user_experience,
    job_experience
):

    text = str(
        job_experience
    )

    numbers = re.findall(
        r"\d+(?:\.\d+)?",
        text
    )

    if len(numbers) >= 2:

        minimum = float(
            numbers[0]
        )

        maximum = float(
            numbers[1]
        )

        if minimum <= user_experience <= maximum:

            return 10

        elif user_experience >= minimum:

            return 5

        return 0

    elif len(numbers) == 1:

        required = float(
            numbers[0]
        )

        if user_experience >= required:

            return 10

        return 0

    return 10


# =====================================================
# ROLE BOOST
# =====================================================

def get_role_boost(
    job_name,
    user_skills
):

    job = clean_text(
        job_name
    )

    boost = 0

    # Python Developer
    if "python" in user_skills:

        if (
            "python developer" in job
            or "python programmer" in job
        ):

            boost += 10

    # Backend / Flask
    if (
        "python" in user_skills
        and "flask" in user_skills
    ):

        if (
            "backend" in job
            or "flask" in job
            or "python developer" in job
        ):

            boost += 8

    # Data
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

            boost += 8

    # Machine Learning
    if (
        "python" in user_skills
        and "machine learning" in user_skills
    ):

        if (
            "machine learning" in job
            or "ml engineer" in job
            or "ai engineer" in job
            or "data scientist" in job
        ):

            boost += 8

    # Web development
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

            boost += 8

    return boost


# =====================================================
# RECOMMEND BUTTON
# =====================================================

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
            "⚠️ Please enter recognised skills "
            "such as Python, SQL, Flask, etc."
        )

        st.stop()

    recommendations = []

    # =================================================
    # CHECK EVERY JOB
    # =================================================

    for _, job in jobs.iterrows():

        job_skills = get_skills(
            job["Skills"]
        )

        # Skill matching
        matched_skills = (
            user_skills.intersection(
                job_skills
            )
        )

        missing_skills = (
            job_skills - user_skills
        )

        if len(job_skills) > 0:

            skill_percentage = (
                len(matched_skills)
                / len(job_skills)
            ) * 100

        else:

            skill_percentage = 0

        # Skills = 70%
        skill_score = (
            skill_percentage * 0.70
        )

        # Education = 20%
        edu_score = get_education_score(
            education_input,
            job["Education"]
        )

        # Experience = 10%
        exp_score = get_experience_score(
            experience_input,
            job["Experience"]
        )

        # Role-specific boost
        boost = get_role_boost(
            job["Job"],
            user_skills
        )

        total_score = (
            skill_score
            + edu_score
            + exp_score
            + boost
        )

        total_score = min(
            total_score,
            100
        )

        recommendations.append({

            "job": job["Job"],

            "score": total_score,

            "matched": matched_skills,

            "missing": missing_skills,

            "education": job["Education"],

            "experience": job["Experience"],

            "skill_score": skill_score,

            "education_score": edu_score,

            "experience_score": exp_score

        })

    # =================================================
    # SORT BY BEST MATCH
    # =================================================

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    top_jobs = recommendations[:5]

    # =================================================
    # RESULTS
    # =================================================

    st.success(
        "✅ Best matching jobs generated!"
    )

    st.header(
        "🏆 Top 5 Job Recommendations"
    )

    for i, rec in enumerate(
        top_jobs,
        start=1
    ):

        score = rec["score"]

        # =============================================
        # JOB CARD
        # =============================================

        st.markdown(
            f"""
            <div class="job-card">

            <h2>
            {i}. {rec["job"]}
            </h2>

            <div class="score">
            💜 Match Score: {score:.1f}%
            </div>

            <p>
            🎓 <b>Education Required:</b>
            {rec["education"]}
            </p>

            <p>
            💼 <b>Experience Required:</b>
            {rec["experience"]}
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        # =============================================
        # SCORE BAR
        # =============================================

        st.progress(
            int(score)
        )

        # =============================================
        # MATCHED SKILLS
        # =============================================

        if rec["matched"]:

            st.write(
                "✅ **Matched Skills:** "
                + ", ".join(
                    sorted(
                        rec["matched"]
                    )
                )
            )

        else:

            st.write(
                "✅ **Matched Skills:** None"
            )

        # =============================================
        # MISSING SKILLS
        # =============================================

        if rec["missing"]:

            st.write(
                "⚠️ **Skills to Improve:** "
                + ", ".join(
                    sorted(
                        rec["missing"]
                    )
                )
            )

        else:

            st.success(
                "🎉 All required skills matched!"
            )

        # =============================================
        # SCORE BREAKDOWN
        # =============================================

        with st.expander(
            "📊 Score Breakdown"
        ):

            st.write(
                f"🛠️ Skills: "
                f"{rec['skill_score']:.1f}/70"
            )

            st.write(
                f"🎓 Education: "
                f"{rec['education_score']}/20"
            )

            st.write(
                f"💼 Experience: "
                f"{rec['experience_score']}/10"
            )

            st.write(
                f"🏆 Final Score: "
                f"{score:.1f}/100"
            )

        st.divider()


# =====================================================
# FOOTER
# =====================================================

st.markdown(
    """
    <p style="
        text-align:center;
        color:#806b82;
        margin-top:30px;
    ">
    🤖 AI Job Recommendation System
    <br>
    Python + Pandas + Streamlit
    </p>
    """,
    unsafe_allow_html=True
)
