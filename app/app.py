from flask import Flask, request, jsonify
import joblib
import numpy as np
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Groq Client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Initialize Flask app
app = Flask(__name__)

# Load ML model
model = joblib.load("models/diabetes_model.pkl")


@app.route("/")
def home():
    return "Health Advisory System Backend Running"


# ================= PREDICTION ROUTE =================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # Get JSON data
        data = request.json

        # Convert input into numpy array
        features = np.array([[
            data["gender"],
            data["age"],
            data["hypertension"],
            data["heart_disease"],
            data["smoking_history"],
            data["bmi"],
            data["HbA1c_level"],
            data["blood_glucose_level"]
        ]])

        # ML Prediction
        prediction = model.predict(features)[0]

        # Risk Label
        if prediction == 1:
            risk = "High Diabetes Risk"
        else:
            risk = "Low Diabetes Risk"

        # AI Prompt
        prompt = f"""
        A patient has:

        Age: {data["age"]}
        BMI: {data["bmi"]}
        HbA1c Level: {data["HbA1c_level"]}
        Blood Glucose Level: {data["blood_glucose_level"]}

        Exercise Frequency: {data["exercise"]}
        Water Intake: {data["water_intake"]} liters
        Sleep Hours: {data["sleep_hours"]}
        Stress Level: {data["stress_level"]}

        Diabetes Prediction: {risk}

        Give:
        1. Simple health explanation
        2. Diet advice
        3. Exercise suggestions
        4. Lifestyle precautions

        Keep response short and simple.
        """

        # Generate AI Advice
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",
        )

        advice = chat_completion.choices[0].message.content

        # Final API Response
        return jsonify({
            "prediction": int(prediction),
            "risk": risk,
            "health_advice": advice
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


# ================= CHATBOT ROUTE =================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.json

        user_question = data["question"]

        prompt = f"""
        You are an AI healthcare assistant.

        Answer this health question in simple,
        beginner-friendly language.

        Question:
        {user_question}

        Give concise and safe health guidance.
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",
        )

        answer = chat_completion.choices[0].message.content

        return jsonify({
            "response": answer
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)