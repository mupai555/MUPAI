import streamlit as st
from fpdf import FPDF

# Logo y título
st.image("LOGO.png", width=300)
st.title("MUPAI Digital Training Science")
st.write("Bienvenido a tu plataforma de entrenamiento basada en ciencia.")

# Menú lateral
menu = st.sidebar.selectbox("Selecciona una sección:", ["Inicio", "Cuestionario: Potencial Genético", "Cuestionario: Estrés Percibido", "Cuestionario: Calidad del Sueño (PSQI)"])

# Inicializar variables de sesión
for var in ['ffmi', 'lean_mass', 'genetic_potential', 'stress_score', 'psqi_score']:
    if var not in st.session_state:
        st.session_state[var] = None

# Cuestionario: Potencial Genético
if menu == "Cuestionario: Potencial Genético":
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
            st.write(f"**Masa Magra:** {lean_mass:.2f} kg")
            st.write(f"**Potencial Genético:** {genetic_potential:.2f} kg")

# Cuestionario: Escala de Estrés Percibido (PSS)
elif menu == "Cuestionario: Estrés Percibido":
    st.header("Escala de Estrés Percibido (PSS)")
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
        with st.expander(question):  # Usamos expansores para mantener las preguntas organizadas
            response = st.radio("Selecciona una opción:", options, key=f"pss_{i}")
            score = int(response.split(" - ")[0])
            if i in reversed_indices:
                score = 4 - score
            responses.append(score)

    if st.button("Enviar Respuestas PSS"):
        total_score = sum(responses)
        st.session_state['stress_score'] = total_score
        st.subheader("Resultados")
        st.write(f"Tu puntuación total en la PSS es: **{total_score}**")
        if total_score <= 13:
            st.success("Estrés bajo.")
        elif total_score <= 26:
            st.warning("Estrés moderado.")
        else:
            st.error("Estrés alto.")

# Cuestionario: Calidad del Sueño (PSQI)
elif menu == "Cuestionario: Calidad del Sueño (PSQI)":
    st.header("Índice de Calidad de Sueño de Pittsburgh (PSQI)")
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

    if st.button("Enviar Respuestas PSQI"):
        st.session_state['psqi_score'] = sum(len(resp) for resp in responses if resp)
        st.subheader("Resultados")
        st.write(f"Tu puntuación PSQI es: **{st.session_state['psqi_score']}**")

# Inicio
if menu == "Inicio":
    st.header("Perfil Completo")
    if all(value is not None for value in [st.session_state.ffmi, st.session_state.stress_score, st.session_state.psqi_score]):
        st.success("Todos los cuestionarios completados.")
