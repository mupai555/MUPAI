import streamlit as st
from fpdf import FPDF

# Guardar información en session_state
if "genetic_data" not in st.session_state:
    st.session_state["genetic_data"] = {}
if "stress_data" not in st.session_state:
    st.session_state["stress_data"] = {}

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

    # Entrada de datos
    height = st.number_input("Altura (cm):", min_value=100, max_value=250, step=1)
    weight = st.number_input("Peso (kg):", min_value=30.0, max_value=200.0, step=0.1)
    body_fat = st.number_input("Porcentaje de grasa corporal (%):", min_value=5.0, max_value=50.0, step=0.1)

    if height > 0 and weight > 0 and body_fat > 0:
        # Cálculos
        height_m = height / 100
        lean_mass = weight * (1 - body_fat / 100)
        ffmi = lean_mass / (height_m ** 2)
        genetic_potential = (height - 100) * 1.1

        # Guardar resultados en session_state
        st.session_state["genetic_data"] = {
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

elif menu == "Cuestionario: Estrés Percibido":
    st.header("Cuestionario: Escala de Estrés Percibido (PSS)")
    st.write("Este cuestionario mide tu percepción de estrés durante el último mes.")

    # Opciones de respuesta
    options = ["0 - Nunca", "1 - Casi nunca", "2 - A veces", "3 - Frecuentemente", "4 - Muy frecuentemente"]
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

    # Respuestas del usuario
    responses = []
    for i, question in enumerate(questions):
        response = st.selectbox(question, options, key=f"stress_q{i}")
        responses.append(int(response.split(" - ")[0]))

    # Calcular puntaje total
    reverse_indices = [3, 4, 6, 7]
    for idx in reverse_indices:
        responses[idx] = 4 - responses[idx]
    total_score = sum(responses)

    # Guardar resultados en session_state
    st.session_state["stress_data"] = {
        "responses": responses,
        "total_score": total_score
    }

    # Interpretación
    st.subheader("Resultados")
    st.write(f"Tu puntaje total es: **{total_score}**")
    if total_score <= 13:
        st.success("Bajo nivel de estrés percibido.")
    elif 14 <= total_score <= 26:
        st.warning("Moderado nivel de estrés percibido.")
    else:
        st.error("Alto nivel de estrés percibido.")

elif menu == "Perfil Completo":
    st.header("Perfil Completo")
    st.write("Resumen de los cuestionarios completados:")

    # Mostrar resultados de ambos cuestionarios
    if st.session_state["genetic_data"]:
        st.write("### Potencial Genético:")
        st.write(st.session_state["genetic_data"])
    if st.session_state["stress_data"]:
        st.write("### Estrés Percibido:")
        st.write(st.session_state["stress_data"])

    # Generar PDF
    if st.button("Descargar PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Perfil Completo", ln=True, align="C")
        
        # Añadir datos de Potencial Genético
        pdf.cell(200, 10, txt="Potencial Genético:", ln=True)
        for key, value in st.session_state["genetic_data"].items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
        
        # Añadir datos de Estrés Percibido
        pdf.cell(200, 10, txt="Estrés Percibido:", ln=True)
        for key, value in st.session_state["stress_data"].items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

        # Guardar PDF
        pdf_file = "perfil_completo.pdf"
        pdf.output(pdf_file)
        with open(pdf_file, "rb") as f:
            st.download_button("Descargar Perfil Completo", f, file_name=pdf_file)
