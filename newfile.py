import streamlit as st
from fpdf import FPDF

# Logo y título
st.image("LOGO.png", width=300)
st.title("MUPAI Ciencia del Entrenamiento Digital")
st.write("Bienvenido a tu plataforma de entrenamiento basada en ciencia.")

# Menú lateral
menu = st.sidebar.selectbox("Selecciona una sección:", ["Inicio", "Cuestionario: Potencial Genético", "Cuestionario: Estrés Percibido", "Cuestionario: Calidad de Sueño (PSQI)"])

# Inicializar variables en session_state
for var in ['ffmi', 'lean_mass', 'genetic_potential', 'stress_score', 'psqi_score']:
    if var not in st.session_state:
        st.session_state[var] = None

# Cuestionario de Potencial Genético
if menu == "Cuestionario: Potencial Genético":
    st.header("Calculadora de Potencial Genético para el Crecimiento Muscular")
    altura = st.number_input("Altura (cm):", min_value=100, max_value=250, step=1)
    peso = st.number_input("Peso (kg):", min_value=30.0, max_value=200.0, step=0.1)
    grasa_corporal = st.number_input("Porcentaje de grasa corporal (%):", min_value=5.0, max_value=50.0, step=0.1)

    if st.button("Calcular Potencial Genético"):
        if altura > 0 and peso > 0 and grasa_corporal > 0:
            altura_m = altura / 100
            masa_magra = peso * (1 - grasa_corporal / 100)
            ffmi = masa_magra / (altura_m ** 2)
            potencial_genetico = (altura - 100) * 1.1

            st.session_state.update({'ffmi': ffmi, 'lean_mass': masa_magra, 'genetic_potential': potencial_genetico})

            st.subheader("Resultados")
            st.write(f"**FFMI:** {ffmi:.2f}")
            st.write(f"**Masa magra:** {masa_magra:.2f} kg")
            st.write(f"**Potencial genético estimado:** {potencial_genetico:.2f} kg")

# Cuestionario de Estrés Percibido (PSS)
elif menu == "Cuestionario: Estrés Percibido":
    st.header("Escala de Estrés Percibido (PSS)")
    preguntas = [
        "1. En el último mes, ¿con qué frecuencia te has sentido molesto/a por algo que ocurrió inesperadamente?",
        "2. En el último mes, ¿con qué frecuencia has sentido que no podías controlar las cosas importantes en tu vida?",
        "3. En el último mes, ¿con qué frecuencia te has sentido nervioso/a y estresado/a?",
        "4. En el último mes, ¿con qué frecuencia te sentiste confiado/a sobre tu capacidad para manejar problemas personales?",
        "5. En el último mes, ¿con qué frecuencia sentiste que las cosas iban como querías?",
        "6. En el último mes, ¿con qué frecuencia sentiste que no podías lidiar con todo lo que tenías que hacer?",
        "7. En el último mes, ¿con qué frecuencia fuiste capaz de controlar las irritaciones en tu vida?",
        "8. En el último mes, ¿con qué frecuencia sentiste que tenías todo bajo control?",
        "9. En el último mes, ¿con qué frecuencia te has sentido enfadado/a por cosas fuera de tu control?",
        "10. En el último mes, ¿con qué frecuencia sentiste que las dificultades se acumulaban tanto que no podías superarlas?",
    ]
    opciones = ["0 - Nunca", "1 - Casi nunca", "2 - A veces", "3 - Con bastante frecuencia", "4 - Muy a menudo"]
    indices_invertidos = [3, 4, 6, 7]
    respuestas = []

    for i, pregunta in enumerate(preguntas):
        respuesta = st.selectbox(pregunta, opciones, key=f"pss_{i}")
        puntaje = int(respuesta.split(" - ")[0])
        if i in indices_invertidos:
            puntaje = 4 - puntaje
        respuestas.append(puntaje)

    if st.button("Enviar Respuestas del PSS"):
        puntaje_total = sum(respuestas)
        st.session_state['stress_score'] = puntaje_total
        st.subheader("Resultados")
        st.write(f"Tu puntaje total en el PSS es: **{puntaje_total}**")
        if puntaje_total <= 13:
            st.success("Estrés bajo.")
        elif puntaje_total <= 26:
            st.warning("Estrés moderado.")
        else:
            st.error("Estrés alto.")

# Cuestionario de Calidad de Sueño (PSQI)
elif menu == "Cuestionario: Calidad de Sueño (PSQI)":
    st.header("Índice de Calidad de Sueño de Pittsburgh (PSQI)")
    preguntas = [
        "1. ¿A qué hora te has ido a la cama normalmente durante el último mes?",
        "2. ¿Cuánto tiempo (en minutos) te toma normalmente quedarte dormido/a cada noche?",
        "3. ¿A qué hora te has levantado normalmente por la mañana durante el último mes?",
        "4. ¿Cuántas horas de sueño real has tenido por noche durante el último mes?",
        "5. ¿Con qué frecuencia has tenido problemas para dormir por estas razones:\n - No poder dormir en 30 minutos?",
        "6. ¿Con qué frecuencia has tomado medicinas para dormir?",
        "7. ¿Con qué frecuencia has tenido problemas para mantenerte despierto/a mientras conducías, comías o interactuabas socialmente?",
        "8. ¿Qué tan problemático ha sido mantener suficiente entusiasmo para realizar tus actividades?",
        "9. ¿Cómo calificarías tu calidad de sueño en general?",
    ]
    respuestas_psqi = [st.text_input(q, key=f"psqi_{i}") for i, q in enumerate(preguntas)]

    if st.button("Enviar Respuestas del PSQI"):
        # Lógica de puntaje simulada
        st.session_state['psqi_score'] = sum(len(resp) for resp in respuestas_psqi if resp)
        st.subheader("Resultados")
        st.write(f"Tu puntaje en el PSQI es: **{st.session_state['psqi_score']}**")

# Sección de Inicio
if menu == "Inicio":
    st.header("Perfil Completo")
    if all(value is not None for value in [st.session_state.ffmi, st.session_state.stress_score, st.session_state.psqi_score]):
        st.success("Todos los cuestionarios han sido completados.")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Perfil Completo", ln=True, align="C")
        pdf.cell(200, 10, txt=f"FFMI: {st.session_state.ffmi:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Puntaje de Estrés Percibido: {st.session_state.stress_score}", ln=True)
        pdf.cell(200, 10, txt=f"Puntaje de Calidad de Sueño: {st.session_state.psqi_score}", ln=True)
        pdf.output("perfil_completo.pdf")
        with open("perfil_completo.pdf", "rb") as f:
            st.download_button("Descargar tu perfil completo", f, "perfil_completo.pdf")
    else:
        st.warning("Completa todos los cuestionarios para generar tu perfil.")
