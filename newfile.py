from huggingface_hub import login

# Authenticate with Hugging Face
login("your-hugging-face-token-here")  # Replace with your actual token
import streamlit as st
from fpdf import FPDF

# Logo and Title
st.image("LOGO.png", width=300)
st.title("MUPAI Digital Training Science")
st.write("Welcome to your science-based training platform.")

# Sidebar Menu
menu = st.sidebar.selectbox("Select a section:", ["Home", "Genetic Potential Questionnaire", "Perceived Stress Questionnaire"])

# Initialize session_state variables
for var in ['ffmi', 'lean_mass', 'genetic_potential', 'stress_score']:
    if var not in st.session_state:
        st.session_state[var] = None

# Genetic Potential Questionnaire
if menu == "Genetic Potential Questionnaire":
    st.header("Genetic Potential Calculator for Muscle Growth")
    st.write("Enter your details below to calculate your genetic potential based on scientific models.")

    height = st.number_input("Height (cm):", min_value=100, max_value=250, step=1)
    weight = st.number_input("Weight (kg):", min_value=30.0, max_value=200.0, step=0.1)
    body_fat = st.number_input("Body Fat Percentage (%):", min_value=5.0, max_value=50.0, step=0.1)

    if st.button("Calculate Genetic Potential"):
        if height > 0 and weight > 0 and body_fat > 0:
            height_m = height / 100
            lean_mass = weight * (1 - body_fat / 100)
            ffmi = lean_mass / (height_m ** 2)
            genetic_potential = (height - 100) * 1.1

            st.session_state.update({'ffmi': ffmi, 'lean_mass': lean_mass, 'genetic_potential': genetic_potential})

            st.subheader("Results")
            st.write(f"**FFMI:** {ffmi:.2f}")
            st.write(f"**Lean Mass:** {lean_mass:.2f} kg")
            st.write(f"**Genetic Potential:** {genetic_potential:.2f} kg")

# Perceived Stress Questionnaire (PSS)
elif menu == "Perceived Stress Questionnaire":
    st.header("Perceived Stress Scale (PSS)")
    st.write("This questionnaire measures your perceived stress over the last month.")

    questions = [
        "En el último mes, ¿con qué frecuencia te has sentido molesto/a por algo inesperado?",
        "En el último mes, ¿con qué frecuencia has sentido que no podías controlar las cosas importantes en tu vida?",
        "En el último mes, ¿con qué frecuencia te has sentido nervioso/a y estresado/a?",
        "En el último mes, ¿con qué frecuencia te sentiste confiado/a sobre tu capacidad para manejar tus problemas personales?",
        "En el último mes, ¿con qué frecuencia sentiste que las cosas iban como querías?",
        "En el último mes, ¿con qué frecuencia sentiste que no podías lidiar con todo lo que tenías que hacer?",
        "En el último mes, ¿con qué frecuencia fuiste capaz de controlar las irritaciones en tu vida?",
        "En el último mes, ¿con qué frecuencia sentiste que tenías todo bajo control?",
        "En el último mes, ¿con qué frecuencia te has sentido enfadado/a por cosas que estaban fuera de tu control?",
        "En el último mes, ¿con qué frecuencia sentiste que las dificultades se acumulaban tanto que no podías superarlas?",
    ]
    options = ["0 - Nunca", "1 - Casi nunca", "2 - A veces", "3 - Frecuentemente", "4 - Muy frecuentemente"]
    reversed_indices = [3, 4, 6, 7]
    responses = []

    # Loop through the questions with numbering
    for i, question in enumerate(questions, 1):
        response = st.selectbox(f"{i}. {question}", options, key=f"pss_{i}")
        score = int(response.split(" - ")[0])
        if i in reversed_indices:
            score = 4 - score
        responses.append(score)

    if st.button("Submit PSS Responses"):
        total_score = sum(responses)
        st.session_state['stress_score'] = total_score
        st.subheader("Results")
        st.write(f"Your total PSS score is: **{total_score}**")
        if total_score <= 13:
            st.success("Low stress.")
        elif total_score <= 26:
            st.warning("Moderate stress.")
        else:
            st.error("High stress.")

# Home Section
if menu == "Home":
    st.header("Complete Profile")
    if all(value is not None for value in [st.session_state.ffmi, st.session_state.stress_score]):
        st.success("All questionnaires completed.")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Complete Profile", ln=True, align="C")
        pdf.cell(200, 10, txt=f"FFMI: {st.session_state.ffmi:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Stress Score: {st.session_state.stress_score}", ln=True)
        pdf.output("profile.pdf")
        with open("profile.pdf", "rb") as f:
            st.download_button("Download Your Profile", f, "profile.pdf")
    else:
        st.warning("Complete all questionnaires to generate your profile.")
        from transformers import pipeline
import streamlit as st

# Initialize Hugging Face pipeline
@st.cache_resource
def load_pipeline():
    return pipeline("text-generation", model="gpt2")

model = load_pipeline()

# Streamlit interface
st.title("Chatbot App")
user_input = st.text_input("Ask me anything:")
if user_input:
    response = model(user_input, max_length=50, num_return_sequences=1)
    st.write(response[0]['generated_text'])
import os
import streamlit as st
from huggingface_hub import login
from transformers import pipeline

# Set up Hugging Face authentication
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")  # Use your environment variable
if not HUGGINGFACE_TOKEN:
    st.error("Hugging Face token not found. Please add it to your environment variables.")
else:
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

# Streamlit UI
st.title("Hugging Face Sentiment Analysis")
st.write("This app uses Hugging Face's transformers library to analyze the sentiment of text.")

# User input
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

st.sidebar.title("Settings")
st.sidebar.write("Make sure your Hugging Face token is set in the environment variables.")
