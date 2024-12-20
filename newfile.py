import streamlit as st
from fpdf import FPDF

# Logo and Title
st.image("LOGO.png", width=300)
st.title("MUPAI Digital Training Science")
st.write("Welcome to your science-based training platform.")

# Sidebar Menu
menu = st.sidebar.selectbox("Select a section:", ["Home", "Genetic Potential Questionnaire", "Perceived Stress Questionnaire", "Sleep Quality Questionnaire (PSQI)"])

# Initialize session_state variables
for var in ['ffmi', 'lean_mass', 'genetic_potential', 'total_score', 'psqi_score']:
    if var not in st.session_state:
        st.session_state[var] = None

# Function to fetch dynamic recommendations (Simulated for now)
def get_chatgpt_recommendations(user_query):
    response = f"Simulated response based on: {user_query}"  # Replace with actual API call if needed
    return response

# PSQI Component Scoring Function
def calculate_psqi_component_scores(responses):
    components = {}
    components["Component 1"] = int(responses["Q9"])
    q2_score = responses["Q2"]
    q5a_score = responses["Q5a"]
    components["Component 2"] = 0 if q2_score + q5a_score <= 2 else 1 if q2_score + q5a_score <= 4 else 2 if q2_score + q5a_score <= 6 else 3
    q4_hours = responses["Q4"]
    components["Component 3"] = 0 if q4_hours > 7 else 1 if q4_hours > 6 else 2 if q4_hours > 5 else 3
    total_bed_time = responses["Q3"] - responses["Q1"]  # Example calculation
    efficiency = (q4_hours / total_bed_time) * 100 if total_bed_time > 0 else 0
    components["Component 4"] = 0 if efficiency > 85 else 1 if efficiency > 75 else 2 if efficiency > 65 else 3
    q5_disturbances = sum(responses[q] for q in ["Q5b", "Q5c", "Q5d", "Q5e", "Q5f", "Q5g", "Q5h", "Q5i", "Q5j"])
    components["Component 5"] = 0 if q5_disturbances == 0 else 1 if q5_disturbances <= 9 else 2 if q5_disturbances <= 18 else 3
    components["Component 6"] = int(responses["Q6"])
    q7_score = responses["Q7"]
    q8_score = responses["Q8"]
    components["Component 7"] = 0 if q7_score + q8_score <= 2 else 1 if q7_score + q8_score <= 4 else 2 if q7_score + q8_score <= 6 else 3
    global_score = sum(components.values())
    return components, global_score

# Genetic Potential Questionnaire
if menu == "Genetic Potential Questionnaire":
    st.header("Genetic Potential Calculator for Muscle Growth")
    height = st.number_input("Height (cm):", min_value=100, max_value=250, step=1)
    weight = st.number_input("Weight (kg):", min_value=30.0, max_value=200.0, step=0.1)
    body_fat = st.number_input("Body Fat Percentage (%):", min_value=5.0, max_value=50.0, step=0.1)
    if st.button("Calculate Genetic Potential"):
        height_m = height / 100
        lean_mass = weight * (1 - body_fat / 100)
        ffmi = lean_mass / (height_m ** 2)
        genetic_potential = (height - 100) * 1.1
        st.session_state.update({'ffmi': ffmi, 'lean_mass': lean_mass, 'genetic_potential': genetic_potential})
        st.subheader("Results")
        st.write(f"**FFMI:** {ffmi:.2f}")
        st.write(f"**Lean Mass:** {lean_mass:.2f} kg")
        st.write(f"**Genetic Potential:** {genetic_potential:.2f} kg")
        response = get_chatgpt_recommendations(f"My FFMI is {ffmi:.2f}, and my lean mass is {lean_mass:.2f} kg.")
        st.write(f"AI Recommendations: {response}")

# Perceived Stress Questionnaire
elif menu == "Perceived Stress Questionnaire":
    st.header("Perceived Stress Scale (PSS)")
    options = ["0 - Never", "1 - Almost never", "2 - Sometimes", "3 - Fairly often", "4 - Very often"]
    questions = [
        "1. How often have you felt upset because of something unexpected?",
        "2. How often have you felt unable to control the important things in your life?",
        "3. How often have you felt nervous and stressed?",
        "4. How often have you felt confident about your ability to handle personal problems?",
        "5. How often have you felt things were going your way?"
    ]
    responses = [st.selectbox(q, options, key=f"pss_{i}") for i, q in enumerate(questions)]
    reversed_questions = [3, 4]
    scores = [4 - int(r.split(" - ")[0]) if i in reversed_questions else int(r.split(" - ")[0]) for i, r in enumerate(responses)]
    total_score = sum(scores)
    if st.button("Submit Responses"):
        st.session_state['total_score'] = total_score
        st.subheader("Results")
        st.write(f"Your total score is: **{total_score}**")
        response = get_chatgpt_recommendations(f"My stress score is {total_score}.")
        st.write(f"AI Recommendations: {response}")

# Sleep Quality Questionnaire (PSQI)
elif menu == "Sleep Quality Questionnaire (PSQI)":
    st.header("Pittsburgh Sleep Quality Index (PSQI)")
    psqi_questions = {
        "Q1": "1. What time have you usually gone to bed?",
        "Q2": "2. How long (in minutes) does it usually take to fall asleep?",
        "Q3": "3. What time do you usually wake up?",
        "Q4": "4. How many hours of actual sleep do you get?",
        "Q5a": "5a. Trouble sleeping due to taking longer than 30 minutes?",
        "Q5b": "5b. Waking up in the middle of the night?",
        "Q5c": "5c. Waking up to use the bathroom?",
        "Q5d": "5d. Feeling too hot?",
        "Q5e": "5e. Having bad dreams?",
        "Q6": "6. How often have you used medication to sleep?",
        "Q7": "7. Trouble staying awake during activities?",
        "Q8": "8. Trouble keeping enthusiasm?",
        "Q9": "9. Rate your sleep quality overall."
    }
    responses = {key: st.number_input(label, min_value=0, max_value=3, step=1) for key, label in psqi_questions.items()}
    if st.button("Submit PSQI Responses"):
        components, global_score = calculate_psqi_component_scores(responses)
        st.session_state['psqi_score'] = global_score
        st.subheader("Results")
        st.write(f"Your PSQI global score is: **{global_score}**")
        for component, score in components.items():
            st.write(f"{component}: {score}")

# Home and PDF Generation
if menu == "Home":
    st.header("Complete Profile")
    if all(value is not None for value in [st.session_state.ffmi, st.session_state.total_score, st.session_state.psqi_score]):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Complete Profile", ln=True, align="C")
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
