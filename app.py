import streamlit as st
import pandas as pd
import os
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Student Score Predictor",
    page_icon="🎓",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #2E86C1;
}
.card {
    background-color: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="title">🎓 Student Performance Predictor</div>', unsafe_allow_html=True)

st.write("")

# ---------------- CARD START ----------------
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Enter Student Details")

    # -------- INPUT FIELDS --------
    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Gender", ["male", "female"])
        race_ethnicity = st.selectbox("Race/Ethnicity",
                                     ["group A", "group B", "group C", "group D", "group E"])
        parental_level_of_education = st.selectbox(
            "Parental Education",
            ["some high school", "high school", "some college", "associate's degree", "bachelor's degree", "master's degree"]
        )

    with col2:
        lunch = st.selectbox("Lunch", ["standard", "free/reduced"])
        test_preparation_course = st.selectbox("Test Prep Course", ["none", "completed"])
        reading_score = st.number_input("Reading Score", min_value=0, max_value=100, value=50)
        writing_score = st.number_input("Writing Score", min_value=0, max_value=100, value=50)

    st.write("")

    # -------- BUTTON --------
    if st.button("🔮 Predict Score"):
        try:
            data = CustomData(
                gender=gender,
                race_ethnicity=race_ethnicity,
                parental_level_of_education=parental_level_of_education,
                lunch=lunch,
                test_preparation_course=test_preparation_course,
                reading_score=reading_score,
                writing_score=writing_score
            )

            pred_df = data.get_data_as_data_frame()

            predict_pipeline = PredictPipeline()
            result = predict_pipeline.predict(pred_df)

            st.success(f"🎯 Predicted Math Score: {round(result[0], 2)}")

        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)