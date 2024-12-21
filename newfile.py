import os
import streamlit as st
from huggingface_hub import login
from transformers import pipeline

# Retrieve Hugging Face token securely
HUGGINGFACE_TOKEN = st.secrets["HUGGINGFACE_TOKEN"]

# Authenticate with Hugging Face
login(HUGGINGFACE_TOKEN)

# Initialize Hugging Face pipeline
@st.cache_resource
def load_pipeline():
    try:
        classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased")
        return classifier
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

classifier = load_pipeline()

# Streamlit Sidebar Navigation
menu = st.sidebar.selectbox(
    "Navigation", ["Home", "Sentiment Analysis", "Stress Questionnaire", "Muscle Genetic Potential"]
)

# Logo
st.sidebar.image("LOGO.png", use_column_width=True)  # Ensure LOGO.png is in the same folder as the app

# Home Section
if menu == "Home":
    st.title("Welcome to the Digital Training App")
    st.write("This app integrates science-based tools for training, assessment, and analysis.")

# Sentiment Analysis Section
elif menu == "Sentiment Analysis":
    st.title("Hugging Face Sentiment Analysis")
    st.write("Analyze the sentiment of text using Hugging Face models.")
    user_input = st.text_area("Enter text to analyze:")
    if st.button("Analyze"):
        if classifier and user_input:
            try:
                result = classifier(user_input)
                st.subheader("Sentiment Analysis Result")
                for res in result:
                    st.write(f"Label: {res['label']}, Confidence: {res['score']:.4f}")
            except Exception as e:
                st.error(f"Error during analysis: {e}")
        else:
            st.warning("Please enter text to analyze or ensure the Hugging Face pipeline is loaded.")

# Stress Questionnaire Section
elif menu == "Stress Questionnaire":
    st.title("Perceived Stress Scale (PSS)")
    questions = [
        "In the last month, how often have you been upset because of something unexpected?",
        "In the last month, how often have you felt unable to control the important things in your life?",
        "In the last month, how often have you felt nervous and stressed?",
        "In the last month, how often have you felt confident about your ability to handle your personal problems?",
        "In the last month, how often have you felt that things were going your way?",
        "In the last month, how often have you found that you could not cope with all the things you had to do?",
        "In the last month, how often have you been able to control irritations in your life?",
        "In the last month, how often have you felt that you were on top of things?",
        "In the last month, how often have you been angered because of things outside your control?",
        "In the last month, how often have you felt difficulties piling up so high that you could not overcome them?",
    ]
    options = ["0 - Never", "1 - Almost never", "2 - Sometimes", "3 - Fairly often", "4 - Very often"]
    reversed_indices = [3, 4, 6, 7]
    responses = []

    for i, question in enumerate(questions):
        response = st.selectbox(question, options, key=f"pss_{i}")
        score = int(response.split(" - ")[0])
        if i in reversed_indices:
            score = 4 - score
        responses.append(score)

    if st.button("Submit PSS Responses"):
        total_score = sum(responses)
        st.subheader("Results")
        st.write(f"Your total PSS score is: **{total_score}**")
        if total_score <= 13:
            st.success("Low stress.")
        elif total_score <= 26:
            st.warning("Moderate stress.")
        else:
            st.error("High stress.")

# Muscle Genetic Potential Section
elif menu == "Muscle Genetic Potential":
    st.title("Muscle Genetic Potential Calculator")
    st.write("Calculate your genetic muscle-building potential based on scientific approaches.")

    # Inputs
    height = st.number_input("Enter your height (in cm):", min_value=100, max_value=250, step=1)
    wrist = st.number_input("Enter your wrist circumference (in cm):", min_value=10, max_value=30, step=1)
    ankle = st.number_input("Enter your ankle circumference (in cm):", min_value=10, max_value=30, step=1)
    body_fat = st.number_input("Enter your current body fat percentage (%):", min_value=0.0, max_value=50.0, step=0.1)
    weight = st.number_input("Enter your current weight (in kg):", min_value=30.0, max_value=200.0, step=0.1)

    # Calculation
    if st.button("Calculate"):
        if height > 0 and wrist > 0 and ankle > 0 and weight > 0:
            # Formula (Casey Butt's approximation)
            ffm = (weight * (100 - body_fat) / 100)
            potential_ffm = (
                (height * 0.267) +
                (wrist * 10.5) +
                (ankle * 6.5) - 18
            )
            st.subheader("Results")
            st.write(f"Your current fat-free mass (FFM): **{ffm:.2f} kg**")
            st.write(f"Your genetic potential fat-free mass (FFM): **{potential_ffm:.2f} kg**")
            if ffm >= potential_ffm:
                st.success("You've likely reached your genetic muscle-building potential!")
            else:
                st.info("You still have room to grow towards your genetic potential.")
        else:
            st.error("Please fill in all the fields with valid values.")
