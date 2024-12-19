import streamlit as st

# Logo y título
st.image("LOGO.png", width=300)
st.title("MUPAI Digital Training Science")
st.write("Bienvenido a tu plataforma personalizada.")

# Menú lateral
menu = st.sidebar.selectbox("Selecciona una sección:", ["Inicio", "Cuestionario: Potencial Genético", "Cuestionario: Estrés Percibido", "Perfil Completo"])

# Diccionario para almacenar los datos del usuario
user_data = {}

if menu == "Inicio":
    st.header("Funcionalidades")
    st.write("- Calculadora de rendimiento físico")
    st.write("- Entrenamiento personalizado basado en datos científicos")
    st.write("- Análisis de progresos en tiempo real")

elif menu == "Cuestionario: Potencial Genético":
    st.header("Calculadora de Potencial Genético")
    st.write("Ingresa tus datos para calcular tu potencial genético.")
    
    # Entradas
    user_data["height"] = st.number_input("Altura (cm):", min_value=100, max_value=250, step=1)
    user_data["weight"] = st.number_input("Peso (kg):", min_value=30.0, max_value=200.0, step=0.1)
    user_data["body_fat"] = st.number_input("Porcentaje de grasa corporal (%):", min_value=5.0, max_value=50.0, step=0.1)

    if user_data.get("height") and user_data.get("weight") and user_data.get("body_fat"):
        # Cálculos
        height_m = user_data["height"] / 100
        lean_mass = user_data["weight"] * (1 - user_data["body_fat"] / 100)
        ffmi = lean_mass / (height_m ** 2)
        genetic_potential = (user_data["height"] - 100) * 1.1

        # Guardar resultados
        user_data["ffmi"] = ffmi
        user_data["lean_mass"] = lean_mass
        user_data["genetic_potential"] = genetic_potential

        # Mostrar resultados
        st.subheader("Resultados")
        st.write(f"**Tu FFMI:** {ffmi:.2f}")
        st.write(f"**Tu masa magra:** {lean_mass:.2f} kg")
        st.write(f"**Potencial genético estimado:** {genetic_potential:.2f} kg")

elif menu == "Cuestionario: Estrés Percibido":
    st.header("Cuestionario: Estrés Percibido")
    st.write("Completa el cuestionario para medir tu nivel de estrés.")

    # Preguntas del cuestionario
    questions = [
        "1. ¿Con qué frecuencia te has sentido molesto/a por algo inesperado?",
        "2. ¿Con qué frecuencia sentiste que no podías controlar lo importante?",
        # Agregar más preguntas aquí...
    ]
    options = ["0 - Nunca", "1 - Casi nunca", "2 - A veces", "3 - Frecuentemente", "4 - Muy frecuentemente"]
    responses = []

    for i, question in enumerate(questions):
        response = st.selectbox(question, options, key=f"q{i}")
        responses.append(int(response.split(" - ")[0]))

    # Cálculo del puntaje total
    total_score = sum(responses)
    user_data["stress_score"] = total_score

    # Interpretación
    st.subheader("Resultados")
    st.write(f"Tu puntaje total de estrés es: **{total_score}**")
    if total_score <= 13:
        st.success("Bajo nivel de estrés.")
    elif 14 <= total_score <= 26:
        st.warning("Moderado nivel de estrés.")
    else:
        st.error("Alto nivel de estrés.")

elif menu == "Perfil Completo":
    st.header("Perfil Completo")
    st.write("Aquí está tu perfil personalizado basado en las evaluaciones.")

    if user_data:
        # Mostrar datos básicos
        st.subheader("Datos Básicos")
        st.write(f"Altura: {user_data.get('height', 'N/A')} cm")
        st.write(f"Peso: {user_data.get('weight', 'N/A')} kg")
        st.write(f"Porcentaje de grasa corporal: {user_data.get('body_fat', 'N/A')}%")

        # Resultados del potencial genético
        st.subheader("Potencial Genético")
        st.write(f"FFMI: {user_data.get('ffmi', 'N/A'):.2f}")
        st.write(f"Masa magra: {user_data.get('lean_mass', 'N/A'):.2f} kg")
        st.write(f"Potencial genético estimado: {user_data.get('genetic_potential', 'N/A'):.2f} kg")

        # Resultados del estrés percibido
        st.subheader("Estrés Percibido")
        st.write(f"Puntaje total: {user_data.get('stress_score', 'N/A')}")

        # Recomendaciones
        st.subheader("Recomendaciones")
        if user_data.get("stress_score", 0) > 26:
            st.warning("Reduce el volumen de entrenamiento y prioriza la recuperación.")
        else:
            st.success("Puedes seguir con tu plan de entrenamiento actual.")
    else:
        st.write("Por favor, completa los cuestionarios primero.")
