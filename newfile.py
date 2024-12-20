import streamlit as st
from fpdf import FPDF

# Logo and Title
st.image("LOGO.png", width=300)
st.title("MUPAI Digital Training Science")
st.write("Welcome to your science-based training platform.")

# Sidebar Menu
menu = st.sidebar.selectbox("Select a section:", ["Home", "Genetic Potential Questionnaire", "Perceived Stress Questionnaire", "Sleep Quality Questionnaire (PSQI)"])

# Initialize session_state variables
for var in ['ffmi', 'lean_mass', 'genetic_potential', 'stress_score', 'psqi_score']:
    if var not in st.session_state:
        st.session_state[var] = None

# Genetic Potential Questionnaire
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

            st.session_state.update({'ffmi': ffmi, 'lean_mass': lean_mass, 'genetic_potential': genetic_potential})

            st.subheader("Results")
            st.write(f"**FFMI:** {ffmi:.2f}")
            st.write(f"**Lean Mass:** {lean_mass:.2f} kg")
            st.write(f"**Genetic Potential:** {genetic_potential:.2f} kg")

# Perceived Stress Questionnaire (PSS)
elif menu == "Perceived Stress Questionnaire":
    st.header("Perceived Stress Scale (PSS)")
    questions = [
        "1. En el último mes, ¿con qué frecuencia te has sentido molesto/a por algo inesperado?",
        "2. En el último mes, ¿con qué frecuencia has sentido que no podías controlar las cosas importantes en tu vida?",
        "3. En el último mes, ¿con qué frecuencia te has sentido nervioso/a y estresado/a?",
        "4. En el último mes, ¿con qué frecuencia te sentiste confiado/a sobre tu capacidad para manejar tus problemas personales?",
        "5. En el último mes, ¿con qué frecuencia sentiste que las cosas iban como querías?",
        "6. En el último mes, ¿con qué frecuencia sentiste que no podías lidiar con todo lo que tenías que hacer?",
        "7. En el último mes, ¿con qué frecuencia fuiste capaz de controlar las irritaciones en tu vida?",
        "8. En el último mes, ¿con qué frecuencia sentiste que tenías todo bajo control?",
        "9. En el último mes, ¿con qué frecuencia te has sentido enfadado/a por cosas que estaban fuera de tu control?",
        "10. En el último mes, ¿con qué frecuencia sentiste que las dificultades se acumulaban tanto que no podías superarlas?",
    ]
    options = ["0 - Nunca", "1 - Casi nunca", "2 - A veces", "3 - Frecuentemente", "4 - Muy frecuentemente"]
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
        st.session_state['stress_score'] = total_score
        st.subheader("Results")
        st.write(f"Your total PSS score is: **{total_score}**")
        if total_score <= 13:
            st.success("Low stress.")
        elif total_score <= 26:
            st.warning("Moderate stress.")
        else:
            st.error("High stress.")

# Sleep Quality Questionnaire (PSQI)
elif menu == "Sleep Quality Questionnaire (PSQI)":
    st.header("Pittsburgh Sleep Quality Index (PSQI)")
    questions = [
        "1. ¿A qué hora usualmente te acuestas por la noche?",
        "2. ¿Cuántos minutos te toma quedarte dormido/a cada noche?",
        "3. ¿A qué hora usualmente te levantas por la mañana?",
        "4. ¿Cuántas horas de sueño efectivo obtienes por noche?",
        "5. ¿Con qué frecuencia tienes problemas para dormir porque no puedes conciliar el sueño en 30 minutos?",
        "6. ¿Con qué frecuencia tomas medicamentos para dormir?",
        "7. ¿Con qué frecuencia has tenido problemas para mantenerte despierto mientras conduces, comes o socializas?",
        "8. ¿Qué tan problemático ha sido mantener suficiente entusiasmo para hacer las cosas?",
        "9. ¿Cómo calificarías tu calidad general del sueño?",
    ]
    responses = [st.text_input(q, key=f"psqi_{i}") for i, q in enumerate(questions)]

    if st.button("Submit PSQI Responses"):
        st.session_state['psqi_score'] = sum(len(resp) for resp in responses if resp)
        st.subheader("Results")
        st.write(f"Your PSQI score is: **{st.session_state['psqi_score']}**")

# Home Section
if menu == "Home":
    st.header("Complete Profile")
    if all(value is not None for value in [st.session_state.ffmi, st.session_state.stress_score, st.session_state.psqi_score]):
        st.success("All questionnaires completed.")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Complete Profile", ln=True, align="C")
        pdf.cell(200, 10, txt=f"FFMI: {st.session_state.ffmi:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Stress Score: {st.session_state.stress_score}", ln=True)
        pdf.cell(200, 10, txt=f"PSQI Score: {st.session_state.psqi_score}", ln=True)
        pdf.output("profile.pdf")
        with open("profile.pdf", "rb") as f:
            st.download_button("Download Your Profile", f, "profile.pdf")
    else:
        st.warning("Complete all questionnaires to generate your profile.")
