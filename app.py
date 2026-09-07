# =========================================================
# STYLISH MINIMAL BACKGROUND
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 8% 12%,
            rgba(255, 182, 210, 0.28) 0px,
            rgba(255, 182, 210, 0.12) 90px,
            transparent 180px
        ),
        radial-gradient(
            circle at 92% 18%,
            rgba(194, 174, 255, 0.25) 0px,
            rgba(194, 174, 255, 0.10) 100px,
            transparent 190px
        ),
        radial-gradient(
            circle at 90% 88%,
            rgba(255, 220, 170, 0.22) 0px,
            rgba(255, 220, 170, 0.08) 100px,
            transparent 180px
        ),
        linear-gradient(
            135deg,
            #fff9fc 0%,
            #fffdf9 50%,
            #faf8ff 100%
        );

    background-attachment: fixed;
}


/* Very small cute decorations */

.stApp::before {
    content: "♡   🐾        ✦        🐾   ♡";
    position: fixed;
    top: 12px;
    left: 0;
    width: 100%;
    text-align: center;
    font-size: 18px;
    letter-spacing: 6px;
    opacity: 0.25;
    pointer-events: none;
    z-index: 0;
}


/* Main content */

.block-container {
    position: relative;
    z-index: 1;
}


/* Title */

h1 {
    color: #68456f !important;
    text-align: center;
    font-weight: 700 !important;
}


/* Section headings */

h2, h3 {
    color: #704d78 !important;
}


/* Input areas */

div[data-testid="stTextInput"] > div,
div[data-testid="stSelectbox"] > div,
div[data-testid="stNumberInput"] > div {

    border-radius: 14px;
}


/* Recommend button */

.stButton > button {

    width: 100%;
    border-radius: 16px;
    border: 1px solid #e8b9d1;

    background:
        linear-gradient(
            90deg,
            #f19abc,
            #bd9be5
        );

    color: white;
    font-size: 18px;
    font-weight: 600;

    padding: 12px;

    box-shadow:
        0 5px 15px
        rgba(180, 120, 170, 0.15);

    transition: 0.2s;
}


.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 8px 20px
        rgba(180, 120, 170, 0.22);
}


/* Job recommendation card */

.job-card {

    background: rgba(255, 255, 255, 0.82);

    border: 1px solid
        rgba(226, 187, 211, 0.65);

    border-radius: 20px;

    padding: 22px;

    margin: 16px 0;

    box-shadow:
        0 8px 25px
        rgba(100, 70, 110, 0.07);

    backdrop-filter: blur(5px);
}


/* Score */

.score {

    color: #80509a;

    font-size: 27px;

    font-weight: 700;
}


/* Matched skills */

.skill {

    display: inline-block;

    background: #e4f8ec;

    color: #197447;

    border-radius: 18px;

    padding: 5px 13px;

    margin: 4px;

    font-size: 14px;
}


/* Footer */

.footer {

    text-align: center;

    color: #806b82;

    padding-top: 20px;

    opacity: 0.8;
}

</style>
""", unsafe_allow_html=True)
