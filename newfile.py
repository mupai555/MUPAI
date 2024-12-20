import streamlit as st
from fpdf import FPDF

# Logo y título
st.image("LOGO.png", width=300)
st.title("MUPAI Digital Training Science")
st.write("Bienvenido a tu plataforma de entrenamiento basada en ciencia.")

# Menú lateral
menu = st.sidebar.selectbox("Selecciona una sección:", ["Inicio", "Cuestionario: Potencial Genético", "Cuestionario: Estrés Percibido", "Cuestionario: Índice de Calidad de Sueño (PSQI)"])

# Variables en session_state
for var in ['ffmi', 'lean_mass', 'genetic_potential', 'total_score', 'psqi_score']:
    if var not in st.session_state:
        st.session_state[var] = None

# Función para calcular puntuaciones
def calcular_psqi_respuestas(respuestas):
    puntuaciones = []
    for r in respuestas:
        if r == "0":
            puntuaciones.append(0)
        elif r == "1":
            puntuaciones.append(1)
        elif r == "2":
            puntuaciones.append(2)
        elif r == "3":
            puntuaciones.append(3)
        else:
            puntuaciones.append(0)
    return sum(puntuaciones)

# Cuestionario: Índice de Calidad de Sueño (PSQI)
if menu == "Cuestionario: Índice de Calidad de Sueño (PSQI)":
    st.header("Índice de Calidad de Sueño de Pittsburgh (PSQI)")
    st.write("Este cuestionario mide la calidad de tu sueño durante el último mes.")

    preguntas_psqi = [
        "1. ¿A qué hora te acuestas usualmente por la noche?",
        "2. ¿Cuánto tiempo (en minutos) te toma quedarte dormido?",
        "3. ¿A qué hora te levantas normalmente en la mañana?",
        "4. ¿Cuántas horas reales de sueño tienes cada noche?",
        "5. Durante el último mes, ¿cuántas veces no has podido dormir en menos de 30 minutos?",
        "6. Durante el último mes, ¿cuántas veces te has despertado a medianoche o temprano en la mañana?",
        "7. Durante el último mes, ¿cuántas veces has tenido pesadillas?",
    ]

    respuestas_psqi = [st.text_input(p, key=f"psqi_{i}") for i, p in enumerate(preguntas_psqi)]
    
    if st.button("Enviar respuestas PSQI"):
        psqi_score = calcular_psqi_respuestas(respuestas_psqi)
        st.session_state['psqi_score'] = psqi_score
        st.subheader("Resultados")
        st.write(f"Tu puntuación PSQI es: **{psqi_score}**")
        if psqi_score <= 5:
            st.success("Buena calidad de sueño.")
        elif psqi_score <= 10:
            st.warning("Calidad de sueño moderada.")
        else:
            st.error("Problemas significativos de calidad de sueño.")

# Cuestionario: Escala de Estrés Percibido (PSS)
elif menu == "Cuestionario: Estrés Percibido":
    st.header("Escala de Estrés Percibido (PSS)")
    st.write("Este cuestionario mide tu percepción de estrés durante el último mes.")

    opciones = ["0 - Nunca", "1 - Casi nunca", "2 - A veces", "3 - Frecuentemente", "4 - Muy frecuentemente"]
    preguntas_pss = [
        "1. En el último mes, ¿con qué frecuencia te has sentido molesto por algo inesperado?",
        "2. En el último mes, ¿con qué frecuencia has sentido que no podías controlar lo importante?",
        "3. En el último mes, ¿con qué frecuencia te has sentido nervioso o estresado?",
        "4. En el último mes, ¿con qué frecuencia te sentiste confiado para manejar tus problemas personales?",
        "5. En el último mes, ¿con qué frecuencia sentiste que las cosas iban como querías?",
        "6. En el último mes, ¿con qué frecuencia sentiste que no podías lidiar con todo lo que tenías que hacer?",
    ]

    respuestas_pss = [st.selectbox(q, opciones, key=f"pss_{i}") for i, q in enumerate(preguntas_pss)]
    puntuaciones_pss = [int(r.split(" - ")[0]) for r in respuestas_pss]
    total_pss_score = sum(puntuaciones_pss)

    if st.button("Enviar respuestas PSS"):
        st.session_state['total_score'] = total_pss_score
        st.subheader("Resultados")
        st.write(f"Tu puntuación total PSS es: **{total_pss_score}**")
        if total_pss_score <= 13:
            st.success("Bajo nivel de estrés percibido.")
        elif total_pss_score <= 26:
            st.warning("Moderado nivel de estrés percibido.")
        else:
            st.error("Alto nivel de estrés percibido.")

# Inicio y generación de PDF
if menu == "Inicio":
    st.header("Perfil Completo")
    
    if all(v is not None for v in [st.session_state.ffmi, st.session_state.total_score, st.session_state.psqi_score]):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.cell(200, 10, txt="Perfil Completo del Usuario", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"FFMI: {st.session_state.ffmi:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Masa Magra: {st.session_state.lean_mass:.2f} kg", ln=True)
        pdf.cell(200, 10, txt=f"Potencial Genético: {st.session_state.genetic_potential:.2f} kg", ln=True)
        pdf.cell(200, 10, txt=f"Puntuación de Estrés: {st.session_state.total_score}", ln=True)
        pdf.cell(200, 10, txt=f"Puntuación PSQI: {st.session_state.psqi_score}", ln=True)

        pdf.output("perfil_completo.pdf")
        with open("perfil_completo.pdf", "rb") as f:
            st.download_button("Descargar tu Perfil Completo", f, file_name="perfil_completo.pdf")
    else:
        st.error("Completa todos los cuestionarios para generar tu perfil completo.")
