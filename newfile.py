import streamlit as st
from fpdf import FPDF  # Para generar PDFs

# Estructura de datos para almacenar las respuestas de los cuestionarios
user_data = {
    "genetic_potential": {},
    "stress_score": None
}

# Logo y título
st.image("LOGO.png", width=300)
st.title("MUPAI Digital Training Science")
st.write("Bienvenido a tu plataforma de entrenamiento basada en ciencia.")

# Menú lateral para navegación
menu = st.sidebar.selectbox("Selecciona una sección:", ["Inicio", "Cuestionario: Potencial Genético", "Cuestionario: Estrés Percibido", "Perfil Completo"])

if menu == "Inicio":
    st.header("Funcionalidades")
    st.write("- Calculadora de rendimiento físico")
    st.write("- Entrenamiento personalizado basado en datos científicos")
    st.write("- Análisis de progresos en tiempo real")

elif menu == "Cuestionario: Potencial Genético":
    st.header("Calculadora de Potencial Genético para Crecimiento Muscular")
    st.write("Ingresa tus datos a continuación para calcular tu potencial genético basado en modelos científicos.")
    height = st.number_input("Altura (cm):", min_value=100, max_value=250, step=1)
    weight = st.number_input("Peso (kg):", min_value=30.0, max_value=200.0, step=0.1)
    body_fat = st.number_input("Porcentaje de grasa corporal (%):", min_value=5.0, max_value=50.0, step=0.1)

    if st.button("Calcular"):
        if height > 0 and weight > 0 and body_fat > 0:
            # Cálculos
            height_m = height / 100
            lean_mass = weight * (1 - body_fat / 100)
            ffmi = lean_mass / (height_m ** 2)
            genetic_potential = (height - 100) * 1.1

            # Guardar datos
            user_data["genetic_potential"] = {
                "height": height,
                "weight": weight,
                "body_fat": body_fat,
                "ffmi": ffmi,
                "lean_mass": lean_mass,
                "genetic_potential": genetic_potential
            }

            # Mostrar resultados
            st.subheader("Resultados")
            st.write(f"**Tu FFMI:** {ffmi:.2f}")
            st.write(f"**Tu masa magra:** {lean_mass:.2f} kg")
            st.write(f"**Potencial genético estimado:** {genetic_potential:.2f} kg")
            if ffmi < 25:
                st.success("Estás dentro del rango natural para el desarrollo muscular.")
            else:
                st.warning("Tu FFMI excede el rango natural, lo que podría indicar el uso de potenciadores.")

elif menu == "Cuestionario: Estrés Percibido":
    st.header("Cuestionario: Escala de Estrés Percibido (PSS)")
    st.write("Por favor, responde a cada pregunta seleccionando la opción que más represente tu experiencia.")
    
    options = ["0 - Nunca", "1 - Casi nunca", "2 - A veces", "3 - Frecuentemente", "4 - Muy frecuentemente"]
    questions = [
        "1. En el último mes, ¿con qué frecuencia te has sentido molesto/a por algo que ocurrió inesperadamente?",
        "2. En el último mes, ¿con qué frecuencia has sentido que no podías controlar las cosas importantes en tu vida?",
        # ... (resto de preguntas)
    ]

    responses = []
    for i, question in enumerate(questions):
        response = st.selectbox(question, options, key=f"stress_q{i}")
        responses.append(int(response.split(" - ")[0]))

    if st.button("Calcular Estrés"):
        total_score = sum(responses)
        user_data["stress_score"] = total_score

        st.subheader("Resultados")
        st.write(f"Tu puntaje total es: **{total_score}**")
        if total_score <= 13:
            st.success("Bajo nivel de estrés percibido. ¡Bien hecho!")
        elif 14 <= total_score <= 26:
            st.warning("Moderado nivel de estrés percibido. Considera prácticas de manejo del estrés.")
        else:
            st.error("Alto nivel de estrés percibido. Podrías beneficiarte de ayuda profesional.")

elif menu == "Perfil Completo":
    st.header("Perfil Completo del Usuario")

    if user_data["genetic_potential"] and user_data["stress_score"] is not None:
        st.write("### Datos del Potencial Genético")
        st.write(user_data["genetic_potential"])
        
        st.write("### Nivel de Estrés Percibido")
        st.write(f"Puntaje total de estrés: {user_data['stress_score']}")

        # Generar PDF
        if st.button("Descargar Perfil en PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Perfil Completo del Usuario", ln=True, align="C")
            pdf.cell(200, 10, txt="Datos del Potencial Genético", ln=True, align="L")
            for key, value in user_data["genetic_potential"].items():
                pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
            pdf.cell(200, 10, txt=f"Puntaje de Estrés: {user_data['stress_score']}", ln=True)
            
            pdf.output("perfil_usuario.pdf")
            st.success("Perfil generado y listo para descargar.")
    else:
        st.warning("Completa los cuestionarios para generar tu perfil completo.")
