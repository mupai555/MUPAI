import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="MUPAI - Entrenamiento Digital",
    page_icon="🤖",
    layout="wide",
)

# Función para el cuestionario del PSQI
def cuestionario_calidad_sueno():
    st.title("Evaluación de la Calidad del Sueño - Índice de Pittsburgh")
    st.write("Responde las siguientes preguntas sobre tus hábitos de sueño durante el último mes:")

    # Preguntas principales
    hora_acostarse = st.text_input("1. ¿A qué hora te acuestas normalmente?")
    tiempo_dormirse = st.selectbox(
        "2. ¿Cuánto tiempo tardas normalmente en dormirte?",
        ["Menos de 15 minutos", "16-30 minutos", "31-60 minutos", "Más de 60 minutos"]
    )
    hora_levantarse = st.text_input("3. ¿A qué hora te levantas normalmente?")
    horas_dormidas = st.slider("4. ¿Cuántas horas calculas que duermes habitualmente por noche?", 0, 12, 7)

    # Problemas para dormir
    st.write("5. Durante el último mes, ¿con qué frecuencia has experimentado los siguientes problemas?")
    problemas_dormir = {
        "No poder conciliar el sueño en 30 minutos": st.radio(
            "a. No poder conciliar el sueño en los primeros 30 minutos:",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        ),
        "Despertarte durante la noche o muy temprano": st.radio(
            "b. Despertarte durante la noche o muy temprano:",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        ),
        "Ir al baño durante la noche": st.radio(
            "c. Tener que levantarte para ir al baño:",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        ),
        "No poder respirar bien": st.radio(
            "d. No poder respirar bien mientras duermes:",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        ),
        "Tos o ronquidos fuertes": st.radio(
            "e. Tos o ronquidos fuertes durante la noche:",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        ),
        "Sentir frío": st.radio(
            "f. Sentir demasiado frío mientras duermes:",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        ),
        "Sentir calor": st.radio(
            "g. Sentir demasiado calor mientras duermes:",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        ),
        "Pesadillas": st.radio(
            "h. Tener sueños desagradables o pesadillas:",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        ),
        "Dolor físico": st.radio(
            "i. Tener dolor físico que interfiere con el sueño:",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        ),
    }

    # Calidad del sueño
    calidad_sueno = st.radio(
        "6. ¿Cómo calificarías la calidad de tu sueño?",
        ["Muy buena", "Bastante buena", "Bastante mala", "Muy mala"]
    )

    # Uso de medicación
    uso_medicacion = st.radio(
        "7. ¿Cuántas veces tomaste medicación para dormir?",
        ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
    )

    # Somnolencia diurna
    somnolencia = st.radio(
        "8. ¿Con qué frecuencia has tenido problemas para mantenerte despierto/a durante actividades diurnas?",
        ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
    )
    energia_baja = st.radio(
        "9. ¿Con qué frecuencia has tenido poca energía o entusiasmo para hacer actividades?",
        ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
    )

    # Cálculo de la puntuación
    if st.button("Calcular Puntuación"):
        # Escalas para las respuestas
        puntuacion = {"Ninguna vez": 0, "Menos de una vez a la semana": 1, "Una o dos veces a la semana": 2, "Tres o más veces a la semana": 3}
        calidad_puntuacion = {"Muy buena": 0, "Bastante buena": 1, "Bastante mala": 2, "Muy mala": 3}
        tiempo_puntuacion = {"Menos de 15 minutos": 0, "16-30 minutos": 1, "31-60 minutos": 2, "Más de 60 minutos": 3}

        total_puntuacion = 0
        # Puntuación de calidad del sueño
        total_puntuacion += calidad_puntuacion[calidad_sueno]
        # Problemas de sueño
        for problema, respuesta in problemas_dormir.items():
            total_puntuacion += puntuacion[respuesta]
        # Tiempo para dormirse
        total_puntuacion += tiempo_puntuacion[tiempo_dormirse]
        # Medicación y somnolencia
        total_puntuacion += puntuacion[uso_medicacion]
        total_puntuacion += puntuacion[somnolencia]
        total_puntuacion += puntuacion[energia_baja]

        # Mostrar el resultado
        st.write("### Tu puntuación total del PSQI es:", total_puntuacion)
        if total_puntuacion <= 5:
            st.success("Buena calidad de sueño.")
        elif 6 <= total_puntuacion <= 10:
            st.warning("Calidad de sueño moderada.")
        else:
            st.error("Mala calidad de sueño. Considera consultar a un especialista.")

# Barra lateral de navegación
menu = st.sidebar.selectbox(
    "Menú",
    ["Inicio", "Sobre Mí", "Servicios", "Contacto", "Evaluación del Estilo de Vida"]
)

# Contenido del menú principal
if menu == "Inicio":
    st.image("LOGO.png", use_container_width=True)
    st.title("Bienvenido a MUPAI")
    st.header("Misión")
    st.write("Hacer accesible el entrenamiento basado en ciencia...")
    st.header("Visión")
    st.write("Convertirnos en uno de los máximos referentes...")
    st.header("Política")
    st.write("En MUPAI, nuestra política está fundamentada...")

elif menu == "Sobre Mí":
    st.title("Sobre Mí")
    st.write("Soy Erick Francisco De Luna Hernández...")

elif menu == "Servicios":
    st.title("Servicios")
    st.write("""
    **MUPAI** ofrece una amplia gama de servicios personalizados:
    - Planes de entrenamiento individualizados.
    - Programas de mejora física y mental.
    - Asesoría en nutrición deportiva.
    - Consultoría en rendimiento deportivo.
    """)

elif menu == "Contacto":
    st.title("Contacto")
    st.write("""
    Para más información o consultas, contáctanos:
    - **Correo**: contacto@mupai.com
    - **Teléfono**: +52 123 456 7890
    """)

elif menu == "Evaluación del Estilo de Vida":
    submenu = st.sidebar.radio(
        "Áreas de Evaluación",
        ["Estrés Percibido", "Calidad del Sueño", "Nivel de Actividad Física", "Hábitos Alimenticios", "Potencial Genético Muscular"]
    )
    if submenu == "Calidad del Sueño":
        cuestionario_calidad_sueno()

# Footer
st.markdown("---")
st.write("© 2024 MUPAI - Entrenamiento Digital Basado en Ciencia")
