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
    Soy Erick Francisco De Luna Hernández, un profesional apasionado por el fitness y las ciencias del ejercicio, con una sólida formación académica y amplia experiencia en el diseño de metodologías de entrenamiento basadas en ciencia. Actualmente, me desempeño en **Muscle Up Gym**, donde estoy encargado del diseño y desarrollo de programas de entrenamiento fundamentados en evidencia científica. Mi labor se centra en crear metodologías personalizadas que optimicen el rendimiento físico y promuevan el bienestar integral de nuestros usuarios.

    Cuento con una Maestría en Fuerza y Acondicionamiento por el **Football Science Institute**, una Licenciatura en Ciencias del Ejercicio por la **Universidad Autónoma de Nuevo León (UANL)** y un intercambio académico internacional en la **Universidad de Sevilla**. Durante mi carrera, fui miembro del **Programa de Talento Universitario de la UANL**, una distinción que reconoce a estudiantes de excelencia académica y extracurricular. Además, adquirí experiencia clave en el **Laboratorio de Rendimiento Humano de la UANL**, colaborando en evaluaciones avanzadas de fuerza, biomecánica y acondicionamiento físico con tecnologías innovadoras.

    Mi trayectoria ha sido reconocida con distinciones como el **Premio al Mérito Académico de la UANL**, el **Primer Lugar de Generación** en la Facultad de Organización Deportiva y una **beca completa para un intercambio internacional** en la Universidad de Sevilla. Estos logros reflejan mi compromiso con la excelencia académica y profesional.

    Con una combinación de preparación académica, experiencia práctica y un enfoque basado en la evidencia, me dedico a diseñar soluciones que transformen el rendimiento físico y promuevan la salud integral, integrando ciencia, innovación y personalización.
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
    **MUPAI** ofrece una amplia gama de servicios personalizados basados en ciencia del ejercicio:
    - Planes de entrenamiento individualizados.
    - Programas de mejora física y mental.
    - Asesoría en nutrición deportiva.
    - Consultoría en rendimiento deportivo.
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
            scores = {"Nunca": 0, "Casi nunca": 1, "A veces": 2, "Bastante seguido": 3, "Muy seguido": 4}

            total_score = (
                scores[q1] + scores[q2] + scores[q3] +
                (4 - scores[q4]) +  # Pregunta inversa
                (4 - scores[q5]) +  # Pregunta inversa
                scores[q6] +
                (4 - scores[q7]) +  # Pregunta inversa
                (4 - scores[q8]) +  # Pregunta inversa
                scores[q9] + scores[q10]
            )

            st.write("### Tu puntuación total es:", total_score)
            if total_score <= 13:
                st.success("Estrés bajo. ¡Excelente trabajo en mantener el equilibrio!")
            elif 14 <= total_score <= 26:
                st.warning("Estrés moderado. Podrías beneficiarte de técnicas de manejo del estrés.")
            else:
                st.error("Estrés alto. Considera buscar apoyo o implementar estrategias de relajación.")

# Footer
st.markdown("---")
st.write("© 2024 MUPAI - Entrenamiento Digital Basado en Ciencia")

# Función para el cuestionario de Calidad del Sueño (Índice de Pittsburgh)
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

    # Cálculo de la puntuación
    if st.button("Calcular Puntuación"):
        puntuacion = {"Ninguna vez": 0, "Menos de una vez a la semana": 1, "Una o dos veces a la semana": 2, "Tres o más veces a la semana": 3}
        calidad_puntuacion = {"Muy buena": 0, "Bastante buena": 1, "Bastante mala": 2, "Muy mala": 3}
        tiempo_puntuacion = {"Menos de 15 minutos": 0, "16-30 minutos": 1, "31-60 minutos": 2, "Más de 60 minutos": 3}

        total_puntuacion = 0
        total_puntuacion += calidad_puntuacion[calidad_sueno]
        total_puntuacion += tiempo_puntuacion[tiempo_dormirse]
        total_puntuacion += puntuacion[uso_medicacion]
        total_puntuacion += puntuacion[somnolencia]

        for problema, respuesta in problemas_dormir.items():
            total_puntuacion += puntuacion[respuesta]

        st.write(f"### Tu puntuación total del PSQI es: {total_puntuacion}")
        if total_puntuacion <= 5:
            st.success("Buena calidad de sueño.")
        elif 6 <= total_puntuacion <= 10:
            st.warning("Calidad de sueño moderada.")
        else:
            st.error("Mala calidad de sueño. Considera consultar a un especialista.")

# Modificar el submenú de "Evaluación del Estilo de Vida"
elif menu == "Evaluación del Estilo de Vida":
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
        # Código existente de Estrés Percibido
        st.title("Evaluación del Estrés Percibido")
        # Mantén la lógica existente aquí...

    elif submenu == "Calidad del Sueño":
        # Llama al cuestionario del PSQI
        cuestionario_calidad_sueno()
