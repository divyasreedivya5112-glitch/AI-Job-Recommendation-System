import streamlit as st
import pandas as pd
import re
import random

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Job Recommendation",
    page_icon="💼",
    layout="wide"
)

# =========================================================
# CUTE BACKGROUND + UI DESIGN
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Baloo 2', sans-serif;
}

/* Main background */
.stApp {
    background:
        radial-gradient(circle at 8% 12%, rgba(255,182,193,0.30) 0 35px, transparent 36px),
        radial-gradient(circle at 92% 18%, rgba(255,218,185,0.35) 0 40px, transparent 41px),
        radial-gradient(circle at 15% 85%, rgba(200,230,255,0.30) 0 45px, transparent 46px),
        radial-gradient(circle at 88% 82%, rgba(221,190,255,0.30) 0 45px, transparent 46px),
        linear-gradient(135deg, #fff8fb, #fffaf2, #f8f5ff);
    background-attachment: fixed;
}

/* Cute floating decorations */
.stApp::before {
    content: "🐱   🧁   🍩   🐶   💕   🐾   🍰   🐱   🧁   🐾   🍩   🐶";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    padding: 12px;
    text-align: center;
    font-size: 24px;
    letter-spacing: 18px;
    opacity: 0.35;
    pointer-events: none;
    z-index: 0;
}

/* Main content */
.block-container {
    position: relative;
    z-index: 1;
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

/* Main title */
h1 {
    text-align: center;
    color: #5b3b69 !important;
    font-size: 46px !important;
    font-weight: 700 !important;
    text-shadow: 2px 2px 0px #ffd9e8;
}

h2 {
    color: #68446f !important;
}

h3 {
    color: #65456d !important;
}

/* Subtitle */
.stApp p {
    color: #55465b;
}

/* Input cards */
div[data-testid="stTextInput"],
div[data-testid="stSelectbox"],
div[data-testid="stNumberInput"] {
    background: rgba(255,255,255,0.82);
    border-radius: 18px;
    padding: 8px;
    box-shadow: 0 5px 20px rgba(100,70,110,0.08);
}

/* Inputs */
input, textarea {
    border-radius: 14px !important;
}

/* Button */
.stButton > button {
    width: 100%;
    border-radius: 18px;
    border: none;
    background: linear-gradient(90deg, #ff7aa8, #c889ff);
    color: white;
    font-size: 20px;
    font-weight: 700;
    padding: 14px;
    box-shadow: 0 7px 18px rgba(220,110,160,0.25);
    transition: 0.25s;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.01);
}

/* Job card */
.job-card {
    background: rgba(255,255,255,0.88);
    border-radius: 25px;
    padding: 24px;
    margin: 15px 0;
    border: 2px solid rgba(255,190,215,0.55);
    box-shadow: 0 8px 28px rgba(100,70,110,0.10);
}

/* Perfect match card */
.perfect-card {
    background: linear-gradient(
        135deg,
        rgba(220,255,235,0.95),
        rgba(255,250,255,0.95)
    );
    border: 3px solid #75d9a3;
    border-radius: 25px;
    padding: 24px;
    margin: 15px 0;
    box-shadow: 0 8px 28px rgba(70,180,120,0.15);
}

/* Score */
.score-100 {
    color: #169653;
    font-size: 30px;
    font-weight: 700;
}

.score-normal {
    color: #8052a8;
    font-size: 27px;
    font-weight: 700;
}

/* Skill pills */
.match-pill {
    display: inline-block;
    background: #dcf8e8;
    color: #177b4a;
    padding: 7px 14px;
    border-radius: 20px;
    margin: 4px;
    font-weight: 600;
}

.missing-pill {
    display: inline-block;
    background: #fff0c9;
    color: #9b6800;
    padding: 7px 14px;
    border-radius: 20px;
    margin: 4px;
    font-weight: 600;
}

/* Cute motivational box */
.cute-box {
    background: linear-gradient(135deg, #fff0f6, #f5edff);
    border-radius: 25px;
    padding: 22px;
    text-align: center;
    font-size: 20px;
    color: #69486f;
    border: 2px dashed #efb3d0;
    margin-top: 25px;
}

/* Success */
div[data-testid="stAlert"] {
    border-radius: 18px;
}

/* Progress bar */
div[data-testid="stProgress"] > div > div {
    border-radius: 20px;
}

/* Divider */
hr {
    border-color: #f1cddd;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================

st.title("💼 AI Job Recommendation System")

st.markdown(
    "<p style='text-align:center;font-size:20px;'>"
    "✨ Find the best jobs based on your skills, education and experience ✨"
    "</p>",
    unsafe_allow_html=True
)

st.markdown(
    "<div style='text-align:center;font-size:28px;'>"
    "🐱 💕 🍩 🧁 🐶 🐾 🍰 💕 🐱"
    "</div>",
    unsafe_allow_html=True
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
# INPUT SECTION
# =========================================================

st.header("👤 Enter Your Details")

col1, col2 = st.columns(2)

with col1:

    skills_input = st.text_input(
        "🛠️ Enter your skills",
        placeholder="Python, SQL, Excel, Power BI"
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

with col2:

    experience_input = st.number_input(
        "💼 Enter your experience in years",
        min_value=0,
        max_value=30,
        value=1,
        step=1
    )

    st.markdown(
        """
        <div class="cute-box">
        🐶 <b>Small Steps Lead to Big Opportunities!</b> 🐱<br>
        🍩 Keep learning • 🧁 Keep growing • 💕 Keep applying
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(text):

    text = str(text).lower().strip()

    text = text.replace("&", " and ")

    text = re.sub(
        r"[/|;]+",
        " ",
        text
    )

    text = re.sub(
        r"[-]+",
        " ",
        text
    )

    text = re.sub(
        r"[^a-z0-9+#. ]",
        " ",
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

    "power bi",
    "powerbi",

    "machine learning",
    "deep learning",
    "natural language processing",

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

    found = set()

    # Longest skills first
    sorted_skills = sorted(
        KNOWN_SKILLS,
        key=len,
        reverse=True
    )

    for skill in sorted_skills:

        skill_clean = clean_text(skill)

        if skill_clean in text:

            if skill_clean == "powerbi":
                found.add("power bi")

            elif skill_clean == "scikit learn":
                found.add("scikit-learn")

            else:
                found.add(skill_clean)

    return found


# =========================================================
# EDUCATION MATCH
# =========================================================

def education_match(
    user_education,
    job_education
):

    user = clean_text(
        user_education
    )

    job = clean_text(
        job_education
    )

    education_variations = {
        "b.tech": ["b.tech", "btech", "b tech"],
        "bca": ["bca"],
        "mca": ["mca"],
        "m.tech": ["m.tech", "mtech", "m tech"],
        "b.sc": ["b.sc", "bsc", "b sc"],
        "mba": ["mba"]
    }

    variations = education_variations.get(
        user,
        [user]
    )

    for value in variations:

        if value in job:
            return 20

    return 0


# =========================================================
# EXPERIENCE MATCH
# =========================================================

def experience_match(
    user_experience,
    job_experience
):

    text = str(
        job_experience
    ).lower()

    numbers = re.findall(
        r"\d+(?:\.\d+)?",
        text
    )

    # 0-2 / 1-3
    if len(numbers) >= 2:

        min_exp = float(numbers[0])
        max_exp = float(numbers[1])

        if min_exp <= user_experience <= max_exp:
            return 10

        if user_experience >= min_exp:
            return 5

        return 0

    # Single number
    if len(numbers) == 1:

        required = float(numbers[0])

        if user_experience >= required:
            return 10

        return 0

    # No experience mentioned
    return 10


# =========================================================
# SKILL MATCH
# =========================================================

def skill_match(
    user_skills,
    job_skills
):

    matched = set()
    missing = set()

    for job_skill in job_skills:

        found = False

        for user_skill in user_skills:

            if (
                job_skill == user_skill
                or job_skill in user_skill
                or user_skill in job_skill
            ):

                matched.add(job_skill)
                found = True
                break

        if not found:
            missing.add(job_skill)

    # -----------------------------------------------------
    # Full skill match = 70/70
    # -----------------------------------------------------

    if len(job_skills) == 0:

        skill_score = 70

    elif len(missing) == 0:

        skill_score = 70

    else:

        skill_score = (
            len(matched) / len(job_skills)
        ) * 70

    return (
        skill_score,
        matched,
        missing
    )


# =========================================================
# FINAL SCORE
# =========================================================

def calculate_score(
    user_skills,
    user_education,
    user_experience,
    job
):

    job_skills = get_skills(
        job["Skills"]
    )

    skill_score, matched, missing = skill_match(
        user_skills,
        job_skills
    )

    education_score = education_match(
        user_education,
        job["Education"]
    )

    experience_score = experience_match(
        user_experience,
        job["Experience"]
    )

    # -----------------------------------------------------
    # IMPORTANT:
    # Full skills + education + experience = 100%
    # -----------------------------------------------------

    if (
        len(missing) == 0
        and education_score == 20
        and experience_score == 10
    ):

        total_score = 100

    else:

        total_score = (
            skill_score
            + education_score
            + experience_score
        )

    total_score = min(
        total_score,
        100
    )

    return {
        "score": total_score,
        "matched": matched,
        "missing": missing,
        "skill_score": skill_score,
        "education_score": education_score,
        "experience_score": experience_score
    }


# =========================================================
# RECOMMEND BUTTON
# =========================================================

if st.button(
    "🔍 Recommend Jobs 💕"
):

    if not skills_input.strip():

        st.warning(
            "⚠️ Please enter at least one skill."
        )

        st.stop()

    user_skills = get_skills(
        skills_input
    )

    if not user_skills:

        st.warning(
            "⚠️ Please enter skills like "
            "Python, SQL, Excel, Power BI."
        )

        st.stop()

    # -----------------------------------------------------
    # Calculate recommendations
    # -----------------------------------------------------

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

            "experience": job["Experience"],

            "skill_score": result["skill_score"],

            "education_score": result["education_score"],

            "experience_score": result["experience_score"]
        })

    # Sort
    recommendations = sorted(
        recommendations,
        key=lambda x: x["score"],
        reverse=True
    )

    top_jobs = recommendations[:5]

    # =====================================================
    # RESULTS
    # =====================================================

    st.success(
        "🎉 Perfect! Your job recommendations are ready!"
    )

    st.header(
        "🏆 Top 5 Job Recommendations"
    )

    for i, rec in enumerate(
        top_jobs,
        start=1
    ):

        score = rec["score"]

        # -------------------------------------------------
        # PERFECT MATCH
        # -------------------------------------------------

        if score >= 100:

            st.markdown(
                f"""
                <div class="perfect-card">

                <h2>
                🥇 {i}. {rec['job']} ✨
                </h2>

                <div class="score-100">
                💚 Match Score: 100.0%
                </div>

                <p>
                🎉 <b>Perfect Match!</b>
                You meet the required skills, education
                and experience.
                </p>

                <p>
                🎓 <b>Education Required:</b>
                {rec['education']}
                </p>

                <p>
                💼 <b>Experience Required:</b>
                {rec['experience']}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="job-card">

                <h2>
                #{i} {rec['job']}
                </h2>

                <div class="score-normal">
                💜 Match Score: {score:.1f}%
                </div>

                <p>
                🎓 <b>Education Required:</b>
                {rec['education']}
                </p>

                <p>
                💼 <b>Experience Required:</b>
                {rec['experience']}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        # Progress
        st.progress(
            int(score)
        )

        # -------------------------------------------------
        # MATCHED SKILLS
        # -------------------------------------------------

        if rec["matched"]:

            matched_html = ""

            for skill in sorted(
                rec["matched"]
            ):

                matched_html += (
                    f'<span class="match-pill">'
                    f'✓ {skill}'
                    f'</span>'
                )

            st.markdown(
                f"""
                <div>
                <b>✅ Matched Skills:</b><br>
                {matched_html}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.write(
                "✅ **Matched Skills:** None"
            )

        # -------------------------------------------------
        # MISSING SKILLS
        # -------------------------------------------------

        if rec["missing"]:

            missing_html = ""

            for skill in sorted(
                rec["missing"]
            ):

                missing_html += (
                    f'<span class="missing-pill">'
                    f'⚠ {skill}'
                    f'</span>'
                )

            st.markdown(
                f"""
                <div>
                <b>⚠️ Missing Skills:</b><br>
                {missing_html}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.success(
                "🎊 Missing Skills: None — Perfect!"
            )

        # -------------------------------------------------
        # SCORE BREAKDOWN
        # -------------------------------------------------

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

# =========================================================
# BOTTOM CUTE SECTION
# =========================================================

st.markdown(
    """
    <div class="cute-box">

    🐱 💕 🐶 🐾 🍩 🧁 🍰 💕 🐱

    <br><br>

    <b>
    ✨ Believe in Yourself ✨
    </b>

    <br>

    🌸 Better Skills • Better Opportunities • Better Future 🌸

    <br><br>

    🐶 "Your dream job is waiting for you!"

    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <br>
    <div style="text-align:center;color:#806080;">
    🤖 AI Job Recommendation System
    <br>
    Python + Pandas + Streamlit 💕
    </div>
    """,
    unsafe_allow_html=True
)
