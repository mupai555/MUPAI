import streamlit as st
from huggingface_hub import login
from transformers import pipeline

# Title for the app
st.title("Fitness and Science App")

# Display Logo (ensure the logo file is in the same folder as the app)
st.sidebar.image("LOGO.png", use_column_width=True)  # Update this if you have a different logo file

# Hugging Face Authentication using token from Streamlit secrets
HUGGINGFACE_TOKEN = st.secrets["HUGGINGFACE_TOKEN"]
try:
    login(HUGGINGFACE_TOKEN)
    st.sidebar.success("Successfully authenticated with Hugging Face.")
except Exception as e:
    st.sidebar.error(f"Failed to authenticate with Hugging Face: {e}")

# Sentiment Analysis Section
st.sidebar.header("Sentiment Analysis")
menu = st.sidebar.selectbox("Select Feature", ["Home", "Sentiment Analysis", "Stress Questionnaire"])

if menu == "Home":
    st.write("Welcome to the Fitness and Science App! Explore various features.")

elif menu == "Sentiment Analysis":
    st.write("### Sentiment Analysis")
    st.write("Analyze the sentiment of any text using Hugging Face models.")
    
    # Load sentiment analysis model
    @st.cache_resource
    def load_model():
        try:
            sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased")
            return sentiment_model
        except Exception as e:
            st.error(f"Error loading model: {e}")
            return None

    model = load_model()
    
    user_input = st.text_area("Enter text for analysis:")
    if st.button("Analyze"):
        if model and user_input:
            try:
                result = model(user_input)
                st.subheader("Sentiment Analysis Result")
                for res in result:
                    st.write(f"Label: {res['label']}, Confidence: {res['score']:.4f}")
            except Exception as e:
                st.error(f"Error during analysis: {e}")
        else:
            st.warning("Please enter some text for analysis.")

elif menu == "Stress Questionnaire":
    st.write("### Perceived Stress Scale (PSS) Questionnaire")
    
    # Questions for the PSS
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
    reversed_indices = [3, 4, 6, 7]  # These indices should be reversed for scoring
    responses = []

    # Loop through questions and collect responses
    for i, question in enumerate(questions):
        response = st.selectbox(question, options, key=f"pss_{i}")
        score = int(response.split(" - ")[0])
        if i in reversed_indices:
            score = 4 - score  # Reverse scoring for certain questions
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
