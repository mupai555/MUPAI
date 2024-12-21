git filter-branch --force --index-filter \
"git rm --cached --ignore-unmatch path/to/file/with/token" \
--prune-empty --tag-name-filter cat -- --all
import streamlit as st

# Display all secrets to check if Hugging Face token is available
st.write("Streamlit secrets:")
st.write(st.secrets)  # This will display the secrets to check if the token is loaded
import os
import streamlit as st
from huggingface_hub import login
from transformers import pipeline  # Asegúrate de importar el pipeline

# Verificar si el token de Hugging Face está presente en los secretos
if "HUGGINGFACE_TOKEN" in st.secrets:
    HUGGINGFACE_TOKEN = st.secrets["HUGGINGFACE_TOKEN"]
    
    # Mostrar el contenido de los secretos para verificar si el token está cargado
    st.write(st.secrets)  # Esto mostrará los secretos para comprobar que el token está allí
    
    # Autenticarse con Hugging Face
    login(HUGGINGFACE_TOKEN)
    st.success("Successfully authenticated with Hugging Face.")
else:
    st.error("Hugging Face token not found. Please check your secrets.")

# Inicializar el pipeline de Hugging Face (esto asume que estás cargando un modelo de Hugging Face)
@st.cache_resource
def load_pipeline():
    try:
        # Cargar el modelo de análisis de sentimientos
        classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased")
        return classifier
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

classifier = load_pipeline()

# Barra lateral de Streamlit para navegación
menu = st.sidebar.selectbox(
    "Navigation", ["Home", "Sentiment Analysis", "Stress Questionnaire", "Muscle Genetic Potential"]
)

# Logo (se usa use_container_width para evitar la advertencia deprecada)
st.sidebar.image("LOGO.png", use_container_width=True)  # Asegúrate de que LOGO.png esté en la misma carpeta que la app

# Sección de inicio
if menu == "Home":
    st.title("Welcome to the Digital Training App")
    st.write("This app integrates science-based tools for training, assessment, and analysis.")

# Sección de análisis de sentimientos
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

# Sección del cuestionario de estrés
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

# Sección de cálculo de potencial genético muscular
elif menu == "Muscle Genetic Potential":
    st.title("Muscle Genetic Potential Calculator")
    st.write("Calculate your genetic muscle-building potential based on scientific approaches.")

    # Entradas
    height = st.number_input("Enter your height (in cm):", min_value=100, max_value=250, step=1)
    wrist = st.number_input("Enter your wrist circumference (in cm):", min_value=10, max_value=30, step=1)
    ankle = st.number_input("Enter your ankle circumference (in cm):", min_value=10, max_value=30, step=1)
    body_fat = st.number_input("Enter your current body fat percentage (%):", min_value=0.0, max_value=50.0, step=0.1)
    weight = st.number_input("Enter your current weight (in kg):", min_value=30.0, max_value=200.0, step=0.1)

    # Cálculo
    if st.button("Calculate"):
        if height > 0 and wrist > 0 and ankle > 0 and weight > 0:
            # Fórmula (aproximación de Casey Butt)
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
            import streamlit as st
from transformers import pipeline

# Step 1: Display the logo
st.image("path_to_logo.png", width=200)  # Add the logo image (adjust the path to your logo)

# Step 2: Display secrets to check if Hugging Face token is available
st.write("Streamlit secrets:")
st.write(st.secrets)  # This will display the secrets to check if the token is loaded

# Step 3: Make sure Hugging Face token is correctly loaded from secrets
huggingface_token = st.secrets.get("HUGGINGFACE_TOKEN", "Token not found")

# Check if the token was found and display
if huggingface_token == "Token not found":
    st.warning("Hugging Face token is missing or not correctly set in the secrets.")
else:
    st.success("Hugging Face token loaded successfully.")

# Step 4: Load the sentiment analysis model if the token is available
if huggingface_token != "Token not found":
    classifier = pipeline("sentiment-analysis", use_auth_token=huggingface_token)

    # Step 5: Allow user input to analyze sentiment
    text = st.text_input("Enter text to analyze:", "I am happy with the progress!")
    
    # Step 6: Perform sentiment analysis and display result
    if text:
        st.write("Analyzing sentiment...")
        result = classifier(text)
        st.write(result)

# Step 7: Add Muscle Genetic Potential analysis section
st.header("Muscle Genetic Potential Assessment")
muscle_genetic_score = st.slider("On a scale of 1 to 10, rate your muscle genetic potential:", 1, 10, 5)
st.write(f"Your muscle genetic potential score is: {muscle_genetic_score}")

# Step 8: Add Stress Questionnaire
st.header("Stress Questionnaire")
stress_level = st.radio("How would you rate your current stress level?", ("Low", "Medium", "High"))
sleep_quality = st.radio("How would you rate your sleep quality?", ("Good", "Fair", "Poor"))

st.write(f"Stress level: {stress_level}")
st.write(f"Sleep quality: {sleep_quality}")

# You can add more questions or forms to analyze this data further
