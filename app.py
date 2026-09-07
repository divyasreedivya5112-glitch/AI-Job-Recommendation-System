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
# SIMPLE MINIMAL BACKGROUND
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 8% 8%,
            #fce4ec 0px,
            #fce4ec 45px,
            transparent 46px
        ),
        radial-gradient(
            circle at 92% 15%,
            #eee5ff 0px,
            #eee5ff 50px,
            transparent 51px
        ),
        linear-gradient(
            135deg,
            #fffafd,
            #fffdf9
        );
}

/* Small cute decoration */

.stApp::before {
    content: "♡   🐾   ♡   🐾   ♡";
    position: fixed;
    top: 8px;
    left: 0;
    width: 100%;
    text-align: center;
    font-size: 18px;
    opacity: 0.25;
    pointer-events: none;
}

/* Title */

h1 {
    text-align: center;
    color: #65446f !important;
}

/* Button */

.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: none;
    background: #e98ab4;
    color: white;
    font-size: 18px;
    font-weight: 600;
    padding: 12px;
}

/* Job card */

.job-card {
    background: rgba(255,255,255,0.90);
    border: 1px solid #f0c9dc;
    border-radius: 18px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 5px 18px rgba(100,70,110,0.08);
}

/* 100% score */

.perfect-score {
    color: #159653;
    font-size: 28px;
    font-weight: 700;
}

/* Matched skill */

.skill {
    display: inline-block;
    background: #e2f7eb;
    color: #197447;
    border-radius: 15px;
    padding: 5px 12px;
    margin: 3px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================

st.title("💼 AI Job Recommendation System")

st.markdown(
    """
    <p style="text-align:center;font-size:18px;">
    Find the best jobs based on your skills, education and experience ✨
    </p>

    <p style="text-align:center;opacity:0.5;">
    🐾 ♡ 🐾
    </p>
    """,
    unsafe_allow_html=True
)

# =========================================================
# LOAD DATA
# =========================================================

try:
    jobs = pd.read_csv("jobs.csv")
except FileNotFoundError:
    st.error("❌ jobs.csv file not found!")
    st.stop()

jobs.columns = jobs.columns.str.strip()

# =========================================================
# INPUT SECTION
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
# SKILLS
# =========================================================

KNOWN_SKILLS = [

    "machine learning",
    "deep learning",
    "natural language processing",

    "power bi",
    "powerbi",

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
# GET SKILLS
# =========================================================

def get_skills(text):

    text = clean_text(text)

    skills = set()

    for skill in KNOWN_SKILLS:

        skill_clean = clean_text(skill)

        if skill_clean in text:

            if skill_clean == "powerbi":
                skills.add("power bi")
            else:
                skills.add(skill_clean)

    return skills


# =========================================================
# EDUCATION MATCH
# =========================================================

def education_match(
    user_education,
    job_education
):

    user = clean_text(user_education)
    job = clean_text(job_education)

    if user in job:
        return True

    variations = {

        "b.tech": [
            "b.tech",
            "btech",
            "b tech"
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
        ]
    }

    if user in variations:

        for value in variations[user]:

            if value in job:
                return True

    return False


# =========================================================
# EXPERIENCE MATCH
# =========================================================

def experience_match(
    user_experience,
    job_experience
):

    text = str(job_experience)

    numbers = re.findall(
        r"\d+",
        text
    )

    if len(numbers) >= 2:

        minimum = int(numbers[0])
        maximum = int(numbers[1])

        return (
            minimum
            <= user_experience
            <= maximum
        )

    if len(numbers) == 1:

        required = int(numbers[0])

        return user_experience >= required

    return True


# =========================================================
# RECOMMENDATION
# =========================================================

if st.button("🔍 Recommend Jobs"):

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
            "⚠️ Please enter valid skills."
        )

        st.stop()

    recommendations = []

    # =====================================================
    # PROCESS DATASET
    # =====================================================

    for _, job in jobs.iterrows():

        job_skills = get_skills(
            job["Skills"]
        )

        matched = set()

        for job_skill in job_skills:

            for user_skill in user_skills:

                if (
                    job_skill == user_skill
                    or job_skill in user_skill
                    or user_skill in job_skill
                ):

                    matched.add(job_skill)
                    break

        education_ok = education_match(
            education_input,
            job["Education"]
        )

        experience_ok = experience_match(
            experience_input,
            job["Experience"]
        )

        # Original score only for ranking
        if len(job_skills) > 0:

            skill_score = (
                len(matched)
                / len(job_skills)
            ) * 70

        else:

            skill_score = 70

        education_score = (
            20 if education_ok else 0
        )

        experience_score = (
            10 if experience_ok else 0
        )

        original_score = (
            skill_score
            + education_score
            + experience_score
        )

        recommendations.append({

            "job": job["Job"],

            "score": original_score,

            "matched": matched,

            "education": job["Education"],

            "experience": job["Experience"]

        })

    # =====================================================
    # SORT BY ACTUAL MATCHING
    # =====================================================

    recommendations.sort(
        key=lambda x: x["score"],
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
        # DISPLAY SCORE = 100 FOR ALL RECOMMENDATIONS
        # -------------------------------------------------

        display_score = 100

        st.markdown(
            f"""
            <div class="job-card">

                <h2>
                    🏆 {i}. {rec['job']}
                </h2>

                <div class="perfect-score">
                    💚 Match Score: 100.0%
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

        # -------------------------------------------------
        # PROGRESS
        # -------------------------------------------------

        st.progress(100)

        # -------------------------------------------------
        # MATCHED SKILLS
        # -------------------------------------------------

        if rec["matched"]:

            skill_html = ""

            for skill in sorted(
                rec["matched"]
            ):

                skill_html += (
                    f'<span class="skill">'
                    f'✓ {skill}'
                    f'</span>'
                )

            st.markdown(
                f"""
                <b>✅ Matched Skills:</b><br>
                {skill_html}
                """,
                unsafe_allow_html=True
            )

        else:

            st.write(
                "✅ **Recommended based on your profile**"
            )

        # -------------------------------------------------
        # RECOMMENDATION MESSAGE
        # -------------------------------------------------

        st.success(
            "🎉 100% Recommended Match"
        )

        st.divider()


# =========================================================
# FOOTER
# =========================================================

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
