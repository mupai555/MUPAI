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

        options = ["Nunca", "Casi nunca", "A veces", "Bastante seguido", "Muy seguido"]
        q1 = st.radio("1. ¿Con qué frecuencia te has sentido molesto/a por algo que ocurrió inesperadamente?", options)
        # Más preguntas relacionadas al estrés...

    elif submenu == "Calidad del Sueño":
        st.title("Evaluación de la Calidad del Sueño")
        st.write("Responde las siguientes preguntas relacionadas con tus hábitos de sueño durante el último mes:")

        hora_acostarse = st.text_input("1. ¿A qué hora usualmente te has ido a la cama por la noche?")
        tiempo_para_dormir = st.number_input("2. ¿Cuánto tiempo (en minutos) te ha tomado usualmente quedarte dormido/a cada noche?", min_value=0)
        hora_levantarse = st.text_input("3. ¿A qué hora usualmente te has levantado por la mañana?")
        horas_sueño = st.number_input("4. ¿Cuántas horas de sueño real has tenido por noche?", min_value=0)

        st.write("5. ¿Con qué frecuencia has tenido problemas para dormir debido a las siguientes razones?")
        opciones_frecuencia = ["Nunca", "Menos de una vez por semana", "Una o dos veces por semana", "Tres o más veces por semana"]
        p5a = st.radio("a. No puedes dormir en los primeros 30 minutos.", opciones_frecuencia)
        # Más preguntas...

        if st.button("Calcular Puntuación"):
            st.write("Función de cálculo pendiente.")

# Footer
st.markdown("---")
st.write("© 2024 MUPAI - Entrenamiento Digital Basado en Ciencia")
elif submenu == "Calidad del Sueño":
    st.title("Evaluación de la Calidad del Sueño (Índice de Pittsburgh)")
    st.write("Responde las siguientes preguntas relacionadas con tus hábitos de sueño durante el último mes.")

    # Preguntas del cuestionario
    p1 = st.text_input("1. ¿A qué hora generalmente te acuestas por la noche?")
    p2 = st.number_input("2. ¿Cuánto tiempo (en minutos) sueles tardar en quedarte dormido cada noche?", min_value=0)
    p3 = st.text_input("3. ¿A qué hora generalmente te levantas por la mañana?")
    p4 = st.number_input("4. ¿Cuántas horas de sueño real obtuviste por noche? (Esto puede ser diferente al tiempo que pasaste en la cama)", min_value=0.0, step=0.1)

    st.write("5. Durante el último mes, ¿con qué frecuencia has tenido problemas para dormir debido a:")
    p5a = st.radio("a. No poder quedarte dormido en 30 minutos:", ["Nunca", "Menos de una vez a la semana", "Una o dos veces por semana", "Tres o más veces por semana"])
    p5b = st.radio("b. Despertarte en medio de la noche o temprano en la mañana:", ["Nunca", "Menos de una vez a la semana", "Una o dos veces por semana", "Tres o más veces por semana"])
    p5c = st.radio("c. Levantarte para ir al baño:", ["Nunca", "Menos de una vez a la semana", "Una o dos veces por semana", "Tres o más veces por semana"])
    p5d = st.radio("d. No poder respirar cómodamente:", ["Nunca", "Menos de una vez a la semana", "Una o dos veces por semana", "Tres o más veces por semana"])
    p5e = st.radio("e. Toser o roncar fuerte:", ["Nunca", "Menos de una vez a la semana", "Una o dos veces por semana", "Tres o más veces por semana"])
    p5f = st.radio("f. Sentirte demasiado frío:", ["Nunca", "Menos de una vez a la semana", "Una o dos veces por semana", "Tres o más veces por semana"])
    p5g = st.radio("g. Sentirte demasiado caliente:", ["Nunca", "Menos de una vez a la semana", "Una o dos veces por semana", "Tres o más veces por semana"])
    p5h = st.radio("h. Tener sueños desagradables:", ["Nunca", "Menos de una vez a la semana", "Una o dos veces por semana", "Tres o más veces por semana"])
    p5i = st.radio("i. Tener dolor:", ["Nunca", "Menos de una vez a la semana", "Una o dos veces por semana", "Tres o más veces por semana"])
    p5j = st.text_input("j. Otro motivo, por favor descríbelo:")

    p6 = st.radio("6. Durante el último mes, ¿con qué frecuencia has tomado medicamentos para ayudarte a dormir (recetados o de venta libre)?", ["Nunca", "Menos de una vez a la semana", "Una o dos veces por semana", "Tres o más veces por semana"])
    p7 = st.radio("7. Durante el último mes, ¿con qué frecuencia has tenido problemas para mantenerte despierto mientras conducías, comías o realizabas actividades sociales?", ["Nunca", "Menos de una vez a la semana", "Una o dos veces por semana", "Tres o más veces por semana"])
    p8 = st.radio("8. Durante el último mes, ¿cuánto problema has tenido para mantener suficiente entusiasmo para hacer las cosas?", ["Ningún problema", "Un problema leve", "Un problema moderado", "Un problema grave"])
    p9 = st.radio("9. Durante el último mes, ¿cómo calificarías la calidad de tu sueño en general?", ["Muy buena", "Bastante buena", "Bastante mala", "Muy mala"])

    # Botón para calcular el puntaje
    if st.button("Calcular Puntuación"):
        # Cálculo de puntajes basado en las reglas de PSQI
        puntuacion = 0

        # Componente 1: Calidad subjetiva del sueño
        puntuacion += {"Muy buena": 0, "Bastante buena": 1, "Bastante mala": 2, "Muy mala": 3}[p9]

        # Componente 2: Latencia del sueño
        latencia = 0 if p2 < 15 else 1 if p2 <= 30 else 2 if p2 <= 60 else 3
        frecuencia_5a = {"Nunca": 0, "Menos de una vez a la semana": 1, "Una o dos veces por semana": 2, "Tres o más veces por semana": 3}[p5a]
        puntuacion += 1 if latencia + frecuencia_5a <= 2 else 2 if latencia + frecuencia_5a <= 4 else 3

        # Mostrar puntaje
        st.write(f"### Tu puntuación total es: {puntuacion}")
        if puntuacion <= 5:
            st.success("Calidad del sueño adecuada.")
        elif puntuacion <= 10:
            st.warning("Calidad del sueño moderada. Considera ajustar tus hábitos de sueño.")
        else:
            st.error("Calidad del sueño pobre. Se recomienda buscar ayuda profesional.")

# Footer
st.markdown("---")
st.write("© 2024 MUPAI - Entrenamiento Digital Basado en Ciencia")
