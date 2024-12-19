import streamlit as st

# Logo y Título
st.image("LOGO.png", width=300)  # Asegúrate de que el logo esté en el repositorio
st.title("MUPAI Digital Training Science")
st.write("Bienvenido a tu plataforma de entrenamiento basada en ciencia.")

# Menú lateral para navegación
menu = st.sidebar.selectbox("Selecciona una sección:", ["Inicio", "Cuestionario: Potencial Genético", "Cuestionario: Estrés Percibido", "Perfil Completo"])

# Variables globales para almacenar resultados
user_data = {
    "genetic_potential": None,
    "stress_score": None,
}

if menu == "Inicio":
    # Página de inicio
    st.header("Funcionalidades")
    st.write("- Calculadora de rendimiento físico")
    st.write("- Entrenamiento personalizado basado en datos científicos")
    st.write("- Análisis de progresos en tiempo real")

elif menu == "Cuestionario: Potencial Genético":
    # Cuestionario de Potencial Genético
    st.header("Calculadora de Potencial Genético para Crecimiento Muscular")
    st.write("Ingresa tus datos a continuación para calcular tu potencial genético basado en modelos científicos.")
    height = st.number_input("Altura (cm):", min_value=100, max_value=250, step=1)
    weight = st.number_input("Peso (kg):", min_value=30.0, max_value=200.0, step=0.1)
    body_fat = st.number_input("Porcentaje de grasa corporal (%):", min_value=5.0, max_value=50.0, step=0.1)

    if st.button("Calcular Potencial Genético"):
        if height > 0 and weight > 0 and body_fat > 0:
            height_m = height / 100  # Convertir altura a metros
            lean_mass = weight * (1 - body_fat / 100)  # Masa magra
            ffmi = lean_mass / (height_m ** 2)  # Índice de masa libre de grasa
            genetic_potential = (height - 100) * 1.1  # Potencial genético estimado

            # Mostrar resultados
            st.subheader("Resultados")
            st.write(f"**Tu FFMI:** {ffmi:.2f}")
            st.write(f"**Tu masa magra:** {lean_mass:.2f} kg")
            st.write(f"**Potencial genético estimado:** {genetic_potential:.2f} kg")

            # Interpretación
            if ffmi < 25:
                st.success("Estás dentro del rango natural para el desarrollo muscular.")
            else:
                st.warning("Tu FFMI excede el rango natural, lo que podría indicar el uso de potenciadores.")

            # Guardar resultado
            user_data["genetic_potential"] = {
                "FFMI": ffmi,
                "Lean Mass": lean_mass,
                "Genetic Potential": genetic_potential,
            }
        else:
            st.error("Por favor, llena todos los campos correctamente.")

elif menu == "Cuestionario: Estrés Percibido":
    # Cuestionario PSS
    st.header("Cuestionario: Escala de Estrés Percibido (PSS)")
    st.write("Este cuestionario mide tu percepción de estrés durante el último mes.")
    st.write("Por favor, responde a cada pregunta seleccionando la opción que más represente tu experiencia.")

    # Opciones de respuesta
    options = ["0 - Nunca", "1 - Casi nunca", "2 - A veces", "3 - Frecuentemente", "4 - Muy frecuentemente"]

    # Preguntas
    questions = [
        "1. En el último mes, ¿con qué frecuencia te has sentido molesto/a por algo que ocurrió inesperadamente?",
        "2. En el último mes, ¿con qué frecuencia has sentido que no podías controlar las cosas importantes en tu vida?",
        "3. En el último mes, ¿con qué frecuencia te has sentido nervioso/a y estresado/a?",
        "4. En el último mes, ¿con qué frecuencia te sentiste confiado/a sobre tu capacidad para manejar tus problemas personales?",
        "5. En el último mes, ¿con qué frecuencia sentiste que las cosas iban como querías?",
    ]

    # Respuestas del usuario
    responses = []
    for i, question in enumerate(questions):
        response = st.selectbox(question, options, key=f"q{i}")
        responses.append(int(response.split(" - ")[0]))

    if st.button("Calcular Nivel de Estrés"):
        # Calcular puntuación total
        total_score = sum(responses)

        # Interpretación
        st.subheader("Resultados")
        st.write(f"Tu puntaje total es: **{total_score}**")
        if total_score <= 13:
            st.success("Bajo nivel de estrés percibido. ¡Bien hecho!")
        elif 14 <= total_score <= 26:
            st.warning("Moderado nivel de estrés percibido. Considera prácticas de manejo del estrés.")
        else:
            st.error("Alto nivel de estrés percibido. Podrías beneficiarte de ayuda profesional.")

        # Guardar resultado
        user_data["stress_score"] = total_score

elif menu == "Perfil Completo":
    # Generar Perfil Completo
    st.header("Perfil Completo del Usuario")
    if user_data["genetic_potential"] and user_data["stress_score"] is not None:
        st.write("### Resultados de Potencial Genético")
        st.write(user_data["genetic_potential"])

        st.write("### Resultados de Estrés Percibido")
        st.write({"Stress Score": user_data["stress_score"]})

        # Descargar Perfil
        profile_text = f"""
        Perfil Completo del Usuario:

        Potencial Genético:
        - FFMI: {user_data["genetic_potential"]["FFMI"]:.2f}
        - Masa Magra: {user_data["genetic_potential"]["Lean Mass"]:.2f} kg
        - Potencial Genético: {user_data["genetic_potential"]["Genetic Potential"]:.2f} kg

        Estrés Percibido:
        - Puntaje Total: {user_data["stress_score"]}
        """
        st.download_button("Descargar Perfil", data=profile_text, file_name="perfil_usuario.txt", mime="text/plain")
    else:
        st.warning("Completa ambos cuestionarios para generar tu perfil.")
