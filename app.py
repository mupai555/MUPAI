import streamlit as st
from fpdf import FPDF

# Logo y Título
st.image("LOGO.png", width=300)
st.title("MUPAI Digital Training Science")
st.write("Welcome to your science-based training platform.")

# Menú Lateral
menu = st.sidebar.selectbox(
    "Select a section:", 
    ["Home", "Genetic Potential Questionnaire", "Perceived Stress Questionnaire"]
)

# Inicialización de variables en session_state
for var in ['ffmi', 'lean_mass', 'genetic_potential', 'stress_score']:
    if var not in st.session_state:
        st.session_state[var] = None

# Cuestionario de Potencial Genético
if menu == "Genetic Potential Questionnaire":
    st.header("Genetic Potential Calculator for Muscle Growth")
    height = st.number_input("Height (cm):", min_value=100, max_value=250, step=1)
    weight = st.number_input("Weight (kg):", min_value=30.0, max_value=200.0, step=0.1)
    body_fat = st.number_input("Body Fat Percentage (%):", min_value=5.0, max_value=50.0, step=0.1)

    if st.button("Calculate Genetic Potential"):
        if height > 0 and weight > 0 and body_fat > 0:
            height_m = height / 100
            lean_mass = weight * (1 - body_fat / 100)
            ffmi = lean_mass / (height_m ** 2)
            genetic_potential = (height - 100) * 1.1

            st.session_state.update({
                'ffmi': ffmi,
                'lean_mass': lean_mass,
                'genetic_potential': genetic_potential
            })

            st.subheader("Results")
            st.write(f"**FFMI:** {ffmi:.2f}")
            st.write(f"**Lean Mass:** {lean_mass:.2f} kg")
            st.write(f"**Genetic Potential:** {genetic_potential:.2f} kg")

# Cuestionario de Estrés Percibido (PSS)
elif menu == "Perceived Stress Questionnaire":
    st.header("Perceived Stress Scale (PSS)")
    st.write("This questionnaire measures your perceived stress over the last month.")

    questions = [
        "1. In the last month, how often have you been upset because of something that happened unexpectedly?",
        "2. In the last month, how often have you felt unable to control the important things in your life?",
        "3. In the last month, how often have you felt nervous and stressed?",
        "4. In the last month, how often have you felt confident about your ability to handle personal problems?",
        "5. In the last month, how often have you felt things were going your way?",
        "6. In the last month, how often have you found that you could not cope with all the things you had to do?",
        "7. In the last month, how often have you been able to control irritations in your life?",
        "8. In the last month, how often have you felt on top of things?",
        "9. In the last month, how often have you been angered by things outside of your control?",
        "10. In the last month, how often have you felt difficulties piling up so high you could not overcome them?",
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
        st.session_state["stress_score"] = total_score

        st.subheader("Results")
        st.write(f"Your total PSS score is: **{total_score}**")
        if total_score <= 13:
            st.success("Low stress.")
        elif total_score <= 26:
            st.warning("Moderate stress.")
        else:
            st.error("High stress.")

# Sección Inicio
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
