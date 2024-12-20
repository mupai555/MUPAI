import streamlit as st
from fpdf import FPDF
import fitz  # PyMuPDF
from transformers import pipeline

# Logo and Title
st.image("LOGO.png", width=300)
st.title("MUPAI Digital Training Science")
st.write("Welcome to your science-based training platform.")

# Sidebar Menu
menu = st.sidebar.selectbox("Select a section:", [
    "Home", 
    "Genetic Potential Questionnaire", 
    "Perceived Stress Questionnaire", 
    "Sleep Quality Questionnaire (PSQI)"
])

# Initialize session_state variables
for var in ['ffmi', 'lean_mass', 'genetic_potential', 'total_score', 'psqi_score']:
    if var not in st.session_state:
        st.session_state[var] = None

# Function to fetch dynamic recommendations from ChatGPT
def get_chatgpt_recommendations(user_query, pdf_context=""):
    input_text = f"{user_query}\nContext from document: {pdf_context}" if pdf_context else user_query
    response = f"Simulated response based on: {input_text}"  # Replace with actual API call
    return response

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "".join(page.get_text("text") for page in doc)
    return text

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

            user_query = f"My FFMI is {ffmi:.2f}, and my lean mass is {lean_mass:.2f} kg."
            response = get_chatgpt_recommendations(user_query)
            st.write(f"AI Recommendations: {response}")

# Perceived Stress Questionnaire
elif menu == "Perceived Stress Questionnaire":
    st.header("Perceived Stress Scale (PSS)")
    st.write("This questionnaire measures your perceived stress over the last month.")
    
    options = ["0 - Never", "1 - Almost never", "2 - Sometimes", "3 - Fairly often", "4 - Very often"]
    questions = [
        "1. In the last month, how often have you felt upset because of something unexpected?",
        "2. In the last month, how often have you felt unable to control the important things in your life?",
        "3. In the last month, how often have you felt nervous and stressed?",
        "4. In the last month, how often have you felt confident about your ability to handle your personal problems?",
        "5. In the last month, how often have you felt things were going your way?",
    ]
    
    responses = [st.selectbox(q, options, key=f"q{i}") for i, q in enumerate(questions)]
    reversed_questions = [3, 4]
    scores = [4 - int(r.split(" - ")[0]) if i in reversed_questions else int(r.split(" - ")[0]) for i, r in enumerate(responses)]
    total_score = sum(scores)

    if st.button("Submit Responses"):
        st.session_state['total_score'] = total_score
        st.subheader("Results")
        st.write(f"Your total score is: **{total_score}**")
        
        user_query = f"My stress score is {total_score}. What can I do to reduce stress?"
        response = get_chatgpt_recommendations(user_query)
        st.write(f"AI Recommendations: {response}")

# Sleep Quality Questionnaire (PSQI)
elif menu == "Sleep Quality Questionnaire (PSQI)":
    st.header("Pittsburgh Sleep Quality Index (PSQI)")
    st.write("This questionnaire measures your sleep quality over the past month.")

    psqi_questions = [
        "1. During the past month, what time have you usually gone to bed at night?",
        "2. During the past month, how long (in minutes) has it usually taken you to fall asleep each night?",
        "3. During the past month, what time have you usually gotten up in the morning?",
        "4. During the past month, how many hours of actual sleep did you get at night? (This may be different than the number of hours you spend in bed.)",
        "5. During the past month, how often have you had trouble sleeping because you cannot get to sleep within 30 minutes?",
    ]

    psqi_responses = [st.text_input(q, key=f"psqi_{i}") for i, q in enumerate(psqi_questions)]
    
    if st.button("Submit PSQI Responses"):
        psqi_score = sum([len(r) for r in psqi_responses if r])  # Placeholder scoring logic
        st.session_state['psqi_score'] = psqi_score

        st.subheader("Results")
        st.write(f"Your PSQI score is: **{psqi_score}**")
        
        user_query = f"My PSQI score is {psqi_score}. What does this mean?"
        response = get_chatgpt_recommendations(user_query)
        st.write(f"AI Recommendations: {response}")

# Home and PDF Generation
if menu == "Home":
    st.header("Complete Profile")

    if all(value is not None for value in [st.session_state.ffmi, st.session_state.total_score, st.session_state.psqi_score]):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="User's Complete Profile", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"FFMI: {st.session_state.ffmi:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Lean Mass: {st.session_state.lean_mass:.2f} kg", ln=True)
        pdf.cell(200, 10, txt=f"Genetic Potential: {st.session_state.genetic_potential:.2f} kg", ln=True)
        pdf.cell(200, 10, txt=f"Stress Score: {st.session_state.total_score}", ln=True)
        pdf.cell(200, 10, txt=f"PSQI Score: {st.session_state.psqi_score}", ln=True)

        pdf.output("profile.pdf")
        with open("profile.pdf", "rb") as f:
            st.download_button("Download Your Profile", f, file_name="profile.pdf")
    else:
        st.error("Complete all questionnaires to generate your profile.")
