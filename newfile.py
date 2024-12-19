import streamlit as st
from fpdf import FPDF

# Logo y título
st.image("LOGO.png", width=300)  # Asegúrate de que el logo esté en tu repositorio
st.title("MUPAI Digital Training Science")
st.write("Bienvenido a tu plataforma de entrenamiento basada en ciencia.")

# Menú lateral para navegación
menu = st.sidebar.selectbox("Selecciona una sección:", ["Inicio", "Cuestionario: Potencial Genético", "Cuestionario: Estrés Percibido"])

# Inicializar las variables en session_state para evitar que se pierdan los datos
if 'ffmi' not in st.session_state:
    st.session_state.ffmi = None
if 'lean_mass' not in st.session_state:
    st.session_state.lean_mass = None
if 'genetic_potential' not in st.session_state:
    st.session_state.genetic_potential = None
if 'total_score' not in st.session_state:
    st.session_state.total_score = None

# Cuestionario de Potencial Genético
if menu == "Cuestionario: Potencial Genético":
    st.header("Calculadora de Potencial Genético para Crecimiento Muscular")
    st.write("Ingresa tus datos a continuación para calcular tu potencial genético basado en modelos científicos.")
    
    # Datos de entrada
    height = st.number_input("Altura (cm):", min_value=100, max_value=250, step=1)
    weight = st.number_input("Peso (kg):", min_value=30.0, max_value=200.0, step=0.1)
    body_fat = st.number_input("Porcentaje de grasa corporal (%):", min_value=5.0, max_value=50.0, step=0.1)

    # Botón de Submit para guardar las respuestas
    if st.button("Calcular Potencial Genético"):
        if height > 0 and weight > 0 and body_fat > 0:
            # Cálculos
            height_m = height / 100  # Convertir altura a metros
            lean_mass = weight * (1 - body_fat / 100)  # Masa magra
            ffmi = lean_mass / (height_m ** 2)  # Índice de masa libre de grasa
            genetic_potential = (height - 100) * 1.1  # Potencial genético estimado

            # Guardar las respuestas en session_state
            st.session_state.ffmi = ffmi
            st.session_state.lean_mass = lean_mass
            st.session_state.genetic_potential = genetic_potential

            # Resultados
            st.subheader("Resultados")
            st.write(f"**Tu FFMI:** {ffmi:.2f}")
            st.write(f"**Tu masa magra:** {lean_mass:.2f} kg")
            st.write(f"**Potencial genético estimado:** {genetic_potential:.2f} kg")

            # Interpretación
            if ffmi < 20:
                st.write("Tu FFMI indica que estás en el rango promedio para personas no entrenadas.")
            elif 20 <= ffmi < 24:
                st.write("Tu FFMI indica que estás en el rango de un atleta natural bien entrenado.")
            else:
                st.write("Tu FFMI es superior a 24, lo que indica un desarrollo más allá del rango natural.")

# Cuestionario de Estrés Percibido
elif menu == "Cuestionario: Estrés Percibido":
    st.header("Cuestionario: Escala de Estrés Percibido (PSS)")
    st.write("Este cuestionario mide tu percepción de estrés durante el último mes.")
    st.write("Por favor, responde a cada pregunta seleccionando la opción que más represente tu experiencia.")
    
    # Opciones de respuesta
    options = ["0 - Nunca", "1 - Casi nunca", "2 - A veces", "3 - Frecuentemente", "4 - Muy frecuentemente"]

    # Preguntas del cuestionario
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
        "10. En el último mes, ¿con qué frecuencia sentiste que las dificultades se acumulaban tanto que no podías superarlas?"
    ]

    # Variables para las respuestas del usuario
    responses = []
    for i, question in enumerate(questions):
        response = st.selectbox(question, options, key=f"q{i}")
        responses.append(int(response.split(" - ")[0]))

    # Ajuste para preguntas invertidas
    reverse_indices = [3, 4, 6, 7]
    for idx in reverse_indices:
        responses[idx] = 4 - responses[idx]

    # Cálculo del puntaje total
    if st.button("Enviar Respuestas"):
        total_score = sum(responses)
        
        # Guardar el puntaje total en session_state
        st.session_state.total_score = total_score

        # Interpretación del puntaje
        st.subheader("Resultados")
        st.write(f"Tu puntaje total es: **{total_score}**")
        if total_score <= 13:
            st.success("Bajo nivel de estrés percibido. ¡Bien hecho! Mantén prácticas saludables para manejar el estrés.")
        elif 14 <= total_score <= 26:
            st.warning("Moderado nivel de estrés percibido. Considera incorporar actividades como meditación o respiración profunda en tu rutina.")
        else:
            st.error("Alto nivel de estrés percibido. Podrías beneficiarte de buscar apoyo profesional o implementar más estrategias de afrontamiento.")
        
        st.write("Este cuestionario es únicamente informativo y no sustituye un diagnóstico profesional.")

# Generación del Perfil Completo y PDF
if menu == "Inicio":
    # Perfil Completo
    st.header("Perfil Completo")

    if st.session_state.ffmi and st.session_state.total_score:
        # Crea el PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Añadir título
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Perfil Completo del Usuario", ln=True, align="C")

        # Añadir los resultados
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Tu FFMI: {st.session_state.ffmi:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Tu masa magra: {st.session_state.lean_mass:.2f} kg", ln=True)
        pdf.cell(200, 10, txt=f"Potencial genético estimado: {st.session_state.genetic_potential:.2f} kg", ln=True)
        
        pdf.ln(10)
        if st.session_state.total_score <= 13:
            pdf.cell(200, 10, txt="Bajo nivel de estrés percibido. ¡Bien hecho!", ln=True)
        elif 14 <= st.session_state.total_score <= 26:
            pdf.cell(200, 10, txt="Moderado nivel de estrés percibido.", ln=True)
        else:
            pdf.cell(200, 10, txt="Alto nivel de estrés percibido. Podrías beneficiarte de ayuda profesional.", ln=True)

        # Guardar el PDF
        pdf.output("perfil_completo.pdf")

        # Ofrecer la descarga del PDF
        st.download_button("Descargar tu perfil completo", data=open("perfil_completo.pdf", "rb"), file_name="perfil_completo.pdf")
    else:
        st.error("Aún no has completado los cuestionarios. Por favor, asegúrate de llenar ambos cuestionarios para generar tu perfil completo.")
