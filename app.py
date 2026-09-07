import streamlit as st
import pandas as pd
import re

st.set_page_config(
    page_title="AI Job Recommendation",
    page_icon="💼",
    layout="centered"
)

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 8% 12%,
            rgba(255, 182, 210, 0.25),
            transparent 180px
        ),
        radial-gradient(
            circle at 92% 18%,
            rgba(194, 174, 255, 0.22),
            transparent 190px
        ),
        linear-gradient(
            135deg,
            #fffafd,
            #fffdf9
        );
}

.stApp::before {
    content: "♡   🐾   ✦   🐾   ♡";
    position: fixed;
    top: 10px;
    left: 0;
    width: 100%;
    text-align: center;
    font-size: 18px;
    opacity: 0.25;
    pointer-events: none;
}

h1 {
    text-align: center;
    color: #68456f !important;
}

.stButton > button {
    width: 100%;
    border-radius: 15px;
    border: none;
    background: linear-gradient(90deg, #f19abc, #bd9be5);
    color: white;
    font-size: 18px;
    font-weight: 600;
    padding: 12px;
}

</style>
""", unsafe_allow_html=True)
