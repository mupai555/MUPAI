import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="MUPAI - Entrenamiento Digital",
    page_icon="🤖",
    layout="wide",
)

# Barra lateral de navegación
menu = st.sidebar.selectbox(
    "Menú",
    ["Inicio", "Sobre Mí", "Servicios", "Contacto", "Evaluación del Estilo de Vida"]
)

# Contenido del menú principal
if menu == "Inicio":
    # Mostrar el logo
    st.image("LOGO.png", use_container_width=True)

    # Título principal
    st.title("Bienvenido a MUPAI")

    # Misión
    st.header("Misión")
    st.write(
        """
        Hacer accesible el entrenamiento basado en ciencia, proporcionando planes completamente personalizados a través de herramientas digitales respaldadas por inteligencia artificial, datos precisos y la investigación más actualizada en ciencias del ejercicio. Nos enfocamos en promover el desarrollo integral de nuestros usuarios y su bienestar físico y mental.
        """
    )

    # Visión
    st.header("Visión")
    st.write(
        """
        Convertirnos en uno de los máximos referentes a nivel global en entrenamiento digital personalizado, aprovechando las nuevas tecnologías para hacer más accesible el fitness basado en ciencia. Aspiramos a transformar la experiencia del entrenamiento físico, integrando inteligencia artificial, investigación científica y herramientas digitales avanzadas que permitan a cualquier persona alcanzar su máximo potencial.
        """
    )

    # Política
    st.header("Política")
    st.write(
        """
        En **MUPAI**, nuestra política está fundamentada en el compromiso con la excelencia, la ética y el servicio centrado en el usuario. Actuamos con responsabilidad y transparencia para ofrecer soluciones tecnológicas que integren ciencia, personalización y accesibilidad, contribuyendo al bienestar integral de quienes confían en nosotros.
        """
    )

    # Política del Servicio
    st.header("Política del Servicio")
    st.write(
        """
        En **MUPAI**, guiamos nuestras acciones por los siguientes principios:
        - Diseñamos entrenamientos digitales que combinan personalización, datos confiables y ciencia del ejercicio.
        - Aprovechamos la tecnología para ofrecer un servicio accesible y adaptable a las necesidades de cada usuario.
        - Respetamos y protegemos la privacidad de los datos personales, garantizando su uso responsable.
        - Innovamos de forma continua para mejorar la experiencia y los resultados de nuestros usuarios.
        - Promovemos valores como el esfuerzo, la constancia y el respeto en cada interacción, fomentando un ambiente de crecimiento y bienestar.
        """
    )

elif menu == "Sobre Mí":
    # Sección "Sobre Mí"
    st.title("Sobre Mí")
    st.write("""
    Soy Erick Francisco De Luna Hernández, un profesional apasionado por el fitness y las ciencias del ejercicio...
    """)

    # Collage de imágenes
    st.subheader("Galería de Imágenes")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("FB_IMG_1734820693317.jpg", use_container_width=True)
        st.image("FB_IMG_1734820729323.jpg", use_container_width=True)

    with col2:
        st.image("FB_IMG_1734820709707.jpg", use_container_width=True)
        st.image("FB_IMG_1734820808186.jpg", use_container_width=True)

    with col3:
        st.image("FB_IMG_1734820712642.jpg", use_container_width=True)

elif menu == "Servicios":
    # Sección "Servicios"
    st.title("Servicios")
    st.write("""
    **MUPAI** ofrece una amplia gama de servicios personalizados basados en ciencia del ejercicio...
    """)

elif menu == "Contacto":
    # Sección "Contacto"
    st.title("Contacto")
    st.write("""
    Para más información o consultas, contáctanos:
    - **Correo**: contacto@mupai.com
    - **Teléfono**: +52 123 456 7890
    - **Ubicación**: Monterrey, Nuevo León
    """)

elif menu == "Evaluación del Estilo de Vida":
    # Submenú para Evaluación del Estilo de Vida
    submenu = st.sidebar.radio(
        "Áreas de Evaluación",
        [
            "Estrés Percibido", 
            "Calidad del Sueño", 
            "Nivel de Actividad Física", 
            "Hábitos Alimenticios", 
            "Potencial Genético Muscular"
        ]
    )

    if submenu == "Estrés Percibido":
        st.title("Evaluación del Estrés Percibido")
        st.write("Responde las siguientes preguntas según cómo te has sentido durante el último mes:")

        # Preguntas del cuestionario
        options = ["Nunca", "Casi nunca", "A veces", "Bastante seguido", "Muy seguido"]
        q1 = st.radio("1. ¿Con qué frecuencia te has sentido molesto/a por algo que ocurrió inesperadamente?", options)
        q2 = st.radio("2. ¿Con qué frecuencia has sentido que no puedes controlar las cosas importantes de tu vida?", options)
        q3 = st.radio("3. ¿Con qué frecuencia has sentido nerviosismo o estrés?", options)
        q4 = st.radio("4. ¿Con qué frecuencia has sentido confianza en tu capacidad para manejar tus problemas personales?", options)
        q5 = st.radio("5. ¿Con qué frecuencia has sentido que las cosas estaban saliendo bien para ti?", options)
        q6 = st.radio("6. ¿Con qué frecuencia has sentido que no podías lidiar con todas las cosas que tenías que hacer?", options)
        q7 = st.radio("7. ¿Con qué frecuencia has sentido que podías controlar las irritaciones en tu vida?", options)
        q8 = st.radio("8. ¿Con qué frecuencia has sentido que tenías el control sobre las cosas?", options)
        q9 = st.radio("9. ¿Con qué frecuencia te has sentido enojado/a por cosas fuera de tu control?", options)
        q10 = st.radio("10. ¿Con qué frecuencia has sentido que las dificultades se acumulaban tanto que no podías superarlas?", options)

        # Botón para calcular el puntaje
        if st.button("Calcular Puntuación"):
            # Asignar valores a las respuestas
            scores = {"Nunca": 0, "Casi nunca": 1, "A veces": 2, "Bastante seguido": 3, "Muy seguido": 4}

            # Calcular el puntaje total
            total_score = (
                scores[q1] + scores[q2] + scores[q3] +
                (4 - scores[q4]) +  # Pregunta inversa
                (4 - scores[q5]) +  # Pregunta inversa
                scores[q6] +
                (4 - scores[q7]) +  # Pregunta inversa
                (4 - scores[q8]) +  # Pregunta inversa
                scores[q9] + scores[q10]
            )

            # Interpretación del puntaje
            st.write("### Tu puntuación total es:", total_score)
            if total_score <= 13:
                st.success("Estrés bajo. ¡Excelente trabajo en mantener el equilibrio!")
            elif 14 <= total_score <= 26:
                st.warning("Estrés moderado. Podrías beneficiarte de técnicas de manejo del estrés.")
            else:
                st.error("Estrés alto. Considera buscar apoyo o implementar estrategias de relajación.")
