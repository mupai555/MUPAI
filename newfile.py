import streamlit as st
from fpdf import FPDF

# Logo y Título
st.image("LOGO.png", width=300)
st.title("MUPAI Digital Training Science")
st.write("Bienvenido a tu plataforma de entrenamiento basada en ciencia.")

# Menú lateral para navegación
menu = st.sidebar.selectbox("Selecciona una sección:", ["Inicio", "Cuestionario Potencial Genético", "Cuestionario Estrés Percibido", "Cuestionario Calidad del Sueño (PSQI)"])

# Inicializar variables en session_state
for var in ['ffmi', 'lean_mass', 'genetic_potential', 'stress_score', 'psqi_score']:
    if var not in st.session_state:
        st.session_state[var] = None

# Cuestionario Potencial Genético
if menu == "Cuestionario Potencial Genético":
    st.header("Calculadora de Potencial Genético para Crecimiento Muscular")
    height = st.number_input("Altura (cm):", min_value=100, max_value=250, step=1)
    weight = st.number_input("Peso (kg):", min_value=30.0, max_value=200.0, step=0.1)
    body_fat = st.number_input("Porcentaje de grasa corporal (%):", min_value=5.0, max_value=50.0, step=0.1)

    if st.button("Calcular Potencial Genético"):
        if height > 0 and weight > 0 and body_fat > 0:
            height_m = height / 100
            lean_mass = weight * (1 - body_fat / 100)
            ffmi = lean_mass / (height_m ** 2)
            genetic_potential = (height - 100) * 1.1

            st.session_state.update({'ffmi': ffmi, 'lean_mass': lean_mass, 'genetic_potential': genetic_potential})

            st.subheader("Resultados")
            st.write(f"**FFMI:** {ffmi:.2f}")
            st.write(f"**Masa magra:** {lean_mass:.2f} kg")
            st.write(f"**Potencial genético estimado:** {genetic_potential:.2f} kg")

# Cuestionario Estrés Percibido (PSS)
elif menu == "Cuestionario Estrés Percibido":
    st.header("Escala de Estrés Percibido (PSS)")
    tabs = st.tabs(["Parte 1", "Parte 2"])
    questions = [
        "1. En el último mes, ¿con qué frecuencia te has sentido molesto/a por algo que ocurrió inesperadamente?",
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

    # Dividir preguntas en partes
    with tabs[0]:
        for i in range(5):
            response = st.selectbox(questions[i], options, key=f"pss_{i}")
            score = int(response.split(" - ")[0])
            if i in reversed_indices:
                score = 4 - score
            responses.append(score)

    with tabs[1]:
        for i in range(5, 10):
            response = st.selectbox(questions[i], options, key=f"pss_{i}")
            score = int(response.split(" - ")[0])
            if i in reversed_indices:
                score = 4 - score
            responses.append(score)

    if st.button("Enviar Respuestas PSS"):
        total_score = sum(responses)
        st.session_state['stress_score'] = total_score
        st.subheader("Resultados")
        st.write(f"Tu puntuación total en PSS es: **{total_score}**")
        if total_score <= 13:
            st.success("Estrés bajo.")
        elif total_score <= 26:
            st.warning("Estrés moderado.")
        else:
            st.error("Estrés alto.")

# Cuestionario Calidad del Sueño (PSQI)
elif menu == "Cuestionario Calidad del Sueño (PSQI)":
    st.header("Índice de Calidad del Sueño de Pittsburgh (PSQI)")
    tabs = st.tabs(["Parte 1", "Parte 2", "Parte 3"])
    questions = [
        "1. ¿A qué hora sueles irte a la cama por la noche?",
        "2. ¿Cuánto tiempo (en minutos) tardas en dormirte cada noche?",
        "3. ¿A qué hora sueles levantarte por la mañana?",
        "4. ¿Cuántas horas de sueño real consigues por noche?",
        "5. ¿Con qué frecuencia tienes problemas para dormir porque:\n - No puedes conciliar el sueño en 30 minutos?",
        "6. ¿Con qué frecuencia has tomado medicamentos para dormir?",
        "7. ¿Con qué frecuencia has tenido problemas para mantenerte despierto/a mientras manejas, comes o socializas?",
        "8. ¿Cuánto problema te ha supuesto tener suficiente entusiasmo para realizar cosas?",
        "9. ¿Cómo calificarías tu calidad de sueño en general?",
    ]
    psqi_responses = []

    # Dividir preguntas en partes
    with tabs[0]:
        for i in range(3):
            psqi_responses.append(st.text_input(questions[i], key=f"psqi_{i}"))

    with tabs[1]:
        for i in range(3, 6):
            psqi_responses.append(st.text_input(questions[i], key=f"psqi_{i}"))

    with tabs[2]:
        for i in range(6, 9):
            psqi_responses.append(st.text_input(questions[i], key=f"psqi_{i}"))

    if st.button("Enviar Respuestas PSQI"):
        st.session_state['psqi_score'] = sum(len(resp) for resp in psqi_responses if resp)
        st.subheader("Resultados")
        st.write(f"Tu puntuación en PSQI es: **{st.session_state['psqi_score']}**")

# Página de Inicio y Generación de PDF
if menu == "Inicio":
    st.header("Perfil Completo")
    if all(value is not None for value in [st.session_state.ffmi, st.session_state.stress_score, st.session_state.psqi_score]):
        st.success("Todos los cuestionarios completados.")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Perfil Completo", ln=True, align="C")
        pdf.cell(200, 10, txt=f"FFMI: {st.session_state.ffmi:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Puntuación de Estrés: {st.session_state.stress_score}", ln=True)
        pdf.cell(200, 10, txt=f"Puntuación de PSQI: {st.session_state.psqi_score}", ln=True)
        pdf.output("perfil_completo.pdf")
        with open("perfil_completo.pdf", "rb") as f:
            st.download_button("Descarga tu perfil completo", f, "perfil_completo.pdf")
    else:
        st.warning("Completa todos los cuestionarios para generar tu perfil.")
