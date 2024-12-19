import streamlit as st

# Logo y título principal
st.image("LOGO.png", width=300)  # Asegúrate de que el archivo LOGO.png esté en el repositorio
st.title("MUPAI Digital Training Science")
st.write("Bienvenido a tu plataforma de entrenamiento basada en ciencia.")

# Menú lateral para navegación
menu = st.sidebar.selectbox(
    "Selecciona una sección:", 
    ["Inicio", "Cuestionario: Potencial Genético", "Cuestionario: Estrés Percibido"]
)

if menu == "Inicio":
    # Contenido de la sección "Inicio"
    st.header("Funcionalidades")
    st.write("- Calculadora de rendimiento físico")
    st.write("- Entrenamiento personalizado basado en datos científicos")
    st.write("- Análisis de progresos en tiempo real")

elif menu == "Cuestionario: Potencial Genético":
    # Calculadora de Potencial Genético
    st.header("Calculadora de Potencial Genético para Crecimiento Muscular")
    st.write("Ingresa tus datos a continuación para calcular tu potencial genético basado en modelos científicos.")

    # Entradas del usuario
    height = st.number_input("Altura (cm):", min_value=100, max_value=250, step=1)
    weight = st.number_input("Peso (kg):", min_value=30.0, max_value=200.0, step=0.1)
    body_fat = st.number_input("Porcentaje de grasa corporal (%):", min_value=5.0, max_value=50.0, step=0.1)

    if height > 0 and weight > 0 and body_fat > 0:
        # Cálculos
        height_m = height / 100  # Convertir altura a metros
        lean_mass = weight * (1 - body_fat / 100)  # Masa magra
        ffmi = lean_mass / (height_m ** 2)  # Índice de masa libre de grasa
        genetic_potential = (height - 100) * 1.1  # Potencial genético estimado

        # Mostrar resultados
        st.subheader("Resultados")
        st.write(f"**Tu FFMI:** {ffmi:.2f}")
        st.write(f"**Tu masa magra:** {lean_mass:.2f} kg")
        st.write(f"**Potencial genético estimado:** {genetic_potential:.2f} kg")

        # Interpretación de los resultados
        if ffmi < 25:
            st.success("Estás dentro del rango natural para el desarrollo muscular.")
        else:
            st.warning("Tu FFMI excede el rango natural, lo que podría indicar el uso de potenciadores.")

elif menu == "Cuestionario: Estrés Percibido":
    # Cuestionario PSS
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
        # Clave única para evitar conflictos
        response = st.selectbox(question, options, key=f"stress_q{i}")
        responses.append(int(response.split(" - ")[0]))

    # Ajuste para preguntas invertidas
    reverse_indices = [3, 4, 6, 7]
    for idx in reverse_indices:
        responses[idx] = 4 - responses[idx]

    # Cálculo del puntaje total
    total_score = sum(responses)

    # Interpretación del puntaje
    st.subheader("Resultados")
    st.write(f"Tu puntaje total es: **{total_score}**")
    if total_score <= 13:
        st.success("Bajo nivel de estrés percibido. ¡Bien hecho!")
    elif 14 <= total_score <= 26:
        st.warning("Moderado nivel de estrés percibido. Considera prácticas de manejo del estrés.")
    else:
        st.error("Alto nivel de estrés percibido. Podrías beneficiarte de ayuda profesional.")

    st.write("Este cuestionario es únicamente informativo y no sustituye un diagnóstico profesional.")
