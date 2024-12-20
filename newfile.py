import streamlit as st
from fpdf import FPDF

# Logo y título
st.image("LOGO.png", width=300)
st.title("MUPAI Digital Training Science")
st.write("Bienvenido a tu plataforma de entrenamiento basada en ciencia.")

# Menú lateral
menu = st.sidebar.selectbox(
    "Selecciona una sección:",
    ["Inicio", "Cuestionario: Potencial Genético", "Cuestionario: Estrés Percibido", "Cuestionario: Calidad del Sueño (PSQI)"]
)

# Inicializar variables de estado
for var in ['ffmi', 'lean_mass', 'genetic_potential', 'stress_score', 'psqi_score']:
    if var not in st.session_state:
        st.session_state[var] = None

# Función para calcular recomendaciones adaptativas
def obtener_recomendaciones(user_query):
    # Esto es un simulacro, conecta con un modelo o API real para respuestas personalizadas
    return f"Simulando respuesta basada en: {user_query}"

# Cuestionario de Potencial Genético
if menu == "Cuestionario: Potencial Genético":
    st.header("Calculadora de Potencial Genético para Crecimiento Muscular")
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
            st.write(f"**Masa Magra:** {masa_magra:.2f} kg")
            st.write(f"**Potencial Genético:** {potencial_genetico:.2f} kg")

# Cuestionario: Escala de Estrés Percibido
elif menu == "Cuestionario: Estrés Percibido":
    st.header("Escala de Estrés Percibido (PSS)")
    opciones = ["0 - Nunca", "1 - Casi nunca", "2 - A veces", "3 - Frecuentemente", "4 - Muy frecuentemente"]
    preguntas = [
        "1. ¿Con qué frecuencia te has sentido molesto/a por algo inesperado?",
        "2. ¿Con qué frecuencia has sentido que no puedes controlar las cosas importantes?",
        "3. ¿Con qué frecuencia te has sentido nervioso/a y estresado/a?",
        "4. ¿Con qué frecuencia te sentiste confiado/a para manejar tus problemas personales?",
        "5. ¿Con qué frecuencia las cosas iban como querías?",
        "6. ¿Con qué frecuencia te sentiste abrumado/a por lo que debías hacer?",
        "7. ¿Con qué frecuencia controlaste las irritaciones?",
        "8. ¿Con qué frecuencia sentiste que tenías todo bajo control?",
        "9. ¿Con qué frecuencia te enfadaste por cosas fuera de tu control?",
        "10. ¿Con qué frecuencia las dificultades parecían insuperables?"
    ]
    respuestas = [st.selectbox(p, opciones, key=f"q{i}") for i, p in enumerate(preguntas)]
    preguntas_invertidas = [3, 4, 6, 7]
    puntuaciones = [4 - int(r.split(" - ")[0]) if i in preguntas_invertidas else int(r.split(" - ")[0]) for i, r in enumerate(respuestas)]
    puntuacion_total = sum(puntuaciones)

    if st.button("Enviar Respuestas"):
        st.session_state['stress_score'] = puntuacion_total
        st.subheader("Resultados")
        st.write(f"Tu puntuación total es: **{puntuacion_total}**")

# Cuestionario: Calidad del Sueño (PSQI)
elif menu == "Cuestionario: Calidad del Sueño (PSQI)":
    st.header("Índice de Calidad del Sueño de Pittsburgh (PSQI)")
    st.write("Este cuestionario evalúa tu calidad del sueño durante el último mes.")
    
    preguntas_psqi = [
        "1. ¿A qué hora te acostaste generalmente?",
        "2. ¿Cuántos minutos te tomó quedarte dormido?",
        "3. ¿A qué hora te despertaste generalmente?",
        "4. ¿Cuántas horas dormiste por noche?",
        "5a. ¿Con qué frecuencia tuviste dificultad para dormir porque no podías quedarte dormido en 30 minutos?",
        "6. ¿Con qué frecuencia tomaste medicamentos para dormir?",
        "7. ¿Con qué frecuencia tuviste problemas para mantenerte despierto durante el día?",
        "8. ¿Cómo calificarías tu calidad general del sueño?"
    ]
    respuestas_psqi = [st.text_input(p, key=f"psqi_{i}") for i, p in enumerate(preguntas_psqi)]

    if st.button("Enviar Respuestas del PSQI"):
        st.session_state['psqi_score'] = sum([len(r) for r in respuestas_psqi])  # Cambia esto según el método de puntuación
        st.subheader("Resultados")
        st.write(f"Tu puntuación PSQI es: **{st.session_state['psqi_score']}**")

# Página de inicio y generación de PDF
if menu == "Inicio":
    st.header("Perfil Completo")
    if all(value is not None for value in [st.session_state.ffmi, st.session_state.stress_score, st.session_state.psqi_score]):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Perfil Completo del Usuario", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"FFMI: {st.session_state.ffmi:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Puntuación de Estrés: {st.session_state.stress_score}", ln=True)
        pdf.cell(200, 10, txt=f"Puntuación PSQI: {st.session_state.psqi_score}", ln=True)
        pdf.output("perfil.pdf")
        with open("perfil.pdf", "rb") as f:
            st.download_button("Descargar Perfil", f, file_name="perfil.pdf")
    else:
        st.error("Completa todos los cuestionarios para generar tu perfil.")
