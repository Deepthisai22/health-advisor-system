import streamlit as st
import requests
from fpdf import FPDF

# ================= PDF FUNCTION =================

def generate_pdf(risk, advice):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=16)

    pdf.cell(
        200,
        10,
        txt="AI Health Advisory Report",
        ln=True,
        align='C'
    )

    pdf.ln(10)

    pdf.set_font("Arial", size=12)

    pdf.multi_cell(
        0,
        10,
        txt=f"Diabetes Risk: {risk}"
    )

    pdf.ln(5)

    pdf.multi_cell(
        0,
        10,
        txt=f"AI Health Advice:\n\n{advice}"
    )

    pdf.output("health_report.pdf")


# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="AI Health Advisory System",
    page_icon="🩺",
    layout="wide"
)

# ================= SIDEBAR =================

st.sidebar.title("🩺 Navigation")

page = st.sidebar.radio(
    "Go To",
    ["Health Prediction", "AI Chatbot"]
)

# =================================================
# PAGE 1 → HEALTH PREDICTION
# =================================================

if page == "Health Prediction":

    st.title("🩺 AI Health Advisory System")

    st.markdown("""
    Predict diabetes risk and receive AI-generated
    health guidance using Machine Learning + Generative AI.
    """)

    st.warning(
        "This system provides AI-generated health guidance and is not a substitute for professional medical advice."
    )

    col1, col2 = st.columns(2)

    # ================= LEFT COLUMN =================

    with col1:

        gender_option = st.selectbox(
            "Gender",
            ["Female", "Male"]
        )

        gender = 0 if gender_option == "Female" else 1

        age = st.slider(
            "Age",
            1,
            100,
            25
        )

        hypertension_option = st.selectbox(
            "Hypertension",
            ["No", "Yes"]
        )

        hypertension = 1 if hypertension_option == "Yes" else 0

        heart_disease_option = st.selectbox(
            "Heart Disease",
            ["No", "Yes"]
        )

        heart_disease = 1 if heart_disease_option == "Yes" else 0

        smoking_option = st.selectbox(
            "Smoking History",
            ["Never", "Former", "Current"]
        )

        smoking_mapping = {
            "Never": 0,
            "Former": 1,
            "Current": 2
        }

        smoking_history = smoking_mapping[smoking_option]

    # ================= RIGHT COLUMN =================

    with col2:

        bmi = st.slider(
            "BMI",
            10.0,
            50.0,
            25.0
        )

        hba1c = st.slider(
            "HbA1c Level",
            3.0,
            15.0,
            5.5
        )

        blood_glucose = st.slider(
            "Blood Glucose Level",
            50,
            300,
            120
        )

        exercise = st.selectbox(
            "Exercise Frequency",
            [
                "Rarely",
                "1-2 times/week",
                "3-5 times/week",
                "Daily"
            ]
        )

        water_intake = st.slider(
            "Daily Water Intake (Liters)",
            1,
            6,
            2
        )

        sleep_hours = st.slider(
            "Sleep Hours",
            3,
            12,
            7
        )

        stress_level = st.selectbox(
            "Stress Level",
            ["Low", "Medium", "High"]
        )

    st.divider()

    # ================= PREDICT BUTTON =================

    if st.button("🔍 Predict Health Risk"):

        data = {
            "gender": gender,
            "age": age,
            "hypertension": hypertension,
            "heart_disease": heart_disease,
            "smoking_history": smoking_history,
            "bmi": bmi,
            "HbA1c_level": hba1c,
            "blood_glucose_level": blood_glucose,
            "exercise": exercise,
            "water_intake": water_intake,
            "sleep_hours": sleep_hours,
            "stress_level": stress_level
        }

        response = requests.post(
            "https://health-advisor-system-q0t3.onrender.com/predict",
            json=data
        )

        result = response.json()

        st.subheader("📊 Prediction Result")

        if result["risk"] == "High Diabetes Risk":
            st.error(result["risk"])
        else:
            st.success(result["risk"])

        st.write("### 🤖 AI Health Advice")
        st.info(result["health_advice"])

        # ================= PDF GENERATION =================

        generate_pdf(
            result["risk"],
            result["health_advice"]
        )

        with open("health_report.pdf", "rb") as file:

            st.download_button(
                label="📥 Download Health Report",
                data=file,
                file_name="health_report.pdf",
                mime="application/pdf"
            )

# =================================================
# PAGE 2 → AI CHATBOT
# =================================================

elif page == "AI Chatbot":

    st.title("💬 AI Health Chatbot")

    st.markdown("""
    Ask health-related questions and receive
    AI-powered healthcare guidance.
    """)

    # Initialize Chat History

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Previous Messages

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input

    user_question = st.chat_input(
        "Ask your health question..."
    )

    if user_question:

        # Store User Message

        st.session_state.messages.append({
            "role": "user",
            "content": user_question
        })

        # Display User Message

        with st.chat_message("user"):
            st.markdown(user_question)

        # Send Question to Backend

        chatbot_data = {
            "question": user_question
        }

        chatbot_response = requests.post(
            "https://health-advisor-system-q0t3.onrender.com/chat",
            json=chatbot_data
        )

        chatbot_result = chatbot_response.json()

        ai_response = chatbot_result["response"]

        # Display AI Response

        with st.chat_message("assistant"):
            st.markdown(ai_response)

        # Store AI Response

        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_response
        })
