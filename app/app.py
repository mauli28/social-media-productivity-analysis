import streamlit as st
import pandas as pd
import joblib
import os

# -------- LOAD MODEL SAFELY --------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

model_path = os.path.join(BASE_DIR, "models", "productivity_model.pkl")
columns_path = os.path.join(BASE_DIR, "models", "columns.pkl")

model = joblib.load(model_path)
columns = joblib.load(columns_path)

# -------- PAGE CONFIG --------
st.set_page_config(page_title="AI Productivity Analyzer", layout="wide")

# -------- CUSTOM CSS --------
st.markdown("""
<style>
.main-title {
    font-size:40px;
    font-weight:bold;
    text-align:center;
    color:#4CAF50;
}
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f0f2f6;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------- HEADER --------
st.markdown('<p class="main-title">🚀 AI Productivity Intelligence System</p>', unsafe_allow_html=True)
st.write("Analyze and improve your daily productivity using AI")

# -------- SIDEBAR --------
st.sidebar.title("ℹ️ About")
st.sidebar.info(
    "This AI system predicts productivity score based on lifestyle habits like "
    "social media usage, sleep, stress, and work patterns."
)

# -------- INPUT SECTION --------
st.subheader("📊 Enter Your Details")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.slider("Age", 18, 60)
    sleep = st.slider("Sleep Hours", 3, 10)
    work = st.slider("Work Hours", 1, 12)

with col2:
    social = st.slider("Social Media Time", 0.0, 10.0)
    stress = st.slider("Stress Level", 1, 10)

with col3:
    gender = st.selectbox("Gender", ["Male", "Other"])
    job = st.selectbox("Job Type", ["IT", "Finance", "Health", "Student", "Unemployed"])
    platform = st.selectbox("Platform", ["Instagram", "Telegram", "TikTok", "Twitter"])

# -------- BUTTON --------
if st.button("🔍 Analyze Productivity"):

    # Create input
    input_data = pd.DataFrame([[0]*len(columns)], columns=columns)
    input_data = input_data.astype(float)

    # -------- USER INPUT --------
    input_data.loc[0, "age"] = int(age)
    input_data.loc[0, "daily_social_media_time"] = float(social)
    input_data.loc[0, "sleep_hours"] = int(sleep)
    input_data.loc[0, "stress_level"] = int(stress)
    input_data.loc[0, "work_hours_per_day"] = int(work)

    # -------- DEFAULT VALUES --------
    input_data.loc[0, "number_of_notifications"] = 50
    input_data.loc[0, "screen_time_before_sleep"] = 2
    input_data.loc[0, "breaks_during_work"] = 3
    input_data.loc[0, "uses_focus_apps"] = 1
    input_data.loc[0, "has_digital_wellbeing_enabled"] = 1
    input_data.loc[0, "coffee_consumption_per_day"] = 2
    input_data.loc[0, "days_feeling_burnout_per_month"] = 10
    input_data.loc[0, "weekly_offline_hours"] = 20
    input_data.loc[0, "job_satisfaction_score"] = 6

    # -------- ENCODING --------
    if f"gender_{gender}" in columns:
        input_data.loc[0, f"gender_{gender}"] = 1

    if f"job_type_{job}" in columns:
        input_data.loc[0, f"job_type_{job}"] = 1

    if f"social_platform_preference_{platform}" in columns:
        input_data.loc[0, f"social_platform_preference_{platform}"] = 1

    # -------- PREDICTION --------
    prediction = model.predict(input_data)[0]

    # -------- LEVEL + COLOR --------
    if prediction < 40:
        level = "Low Productivity"
        color = "red"
    elif prediction < 70:
        level = "Moderate Productivity"
        color = "orange"
    else:
        level = "High Productivity"
        color = "green"

    # -------- RECOMMENDATIONS --------
    rec = []

    if social > 3:
        rec.append("📵 Reduce social media usage")

    if sleep < 6:
        rec.append("😴 Increase sleep hours")

    if stress > 6:
        rec.append("🧘 Manage stress effectively")

    if work > 9:
        rec.append("⚖️ Avoid overworking")

    if len(rec) == 0:
        rec.append("✅ You are doing great! Maintain your routine.")

    # -------- OUTPUT --------
    st.markdown("## 📊 Your Productivity Insights")

    st.markdown(f"""
    <div class="card">
        <h2>Score: {round(prediction,2)}</h2>
        <h3 style='color:{color}'>{level}</h3>
    </div>
    """, unsafe_allow_html=True)

    # Progress bar
    st.progress(min(int(prediction), 100))

    # Recommendations
    st.write("### 💡 Recommendations")
    for r in rec:
        st.write(r)
