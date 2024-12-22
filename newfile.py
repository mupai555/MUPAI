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
    st.image("LOGO.png", use_container_width=True)
    st.title("Bienvenido a MUPAI")
    st.header("Misión")
    st.write("Hacer accesible el entrenamiento basado en ciencia...")
    st.header("Visión")
    st.write("Convertirnos en uno de los máximos referentes a nivel global...")
    st.header("Política")
    st.write("En **MUPAI**, nuestra política está fundamentada en el compromiso...")
    st.header("Política del Servicio")
    st.write("- Diseñamos entrenamientos digitales personalizados...\n- Respetamos la privacidad de los datos...")

elif menu == "Sobre Mí":
    st.title("Sobre Mí")
    st.write("Soy Erick Francisco De Luna Hernández...")
    st.subheader("Galería de Imágenes")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("FB_IMG_1734820693317.jpg", use_container_width=True)
    with col2:
        st.image("FB_IMG_1734820709707.jpg", use_container_width=True)
    with col3:
        st.image("FB_IMG_1734820712642.jpg", use_container_width=True)

elif menu == "Servicios":
    st.title("Servicios")
    st.write("**MUPAI** ofrece una amplia gama de servicios personalizados basados en ciencia del ejercicio...")

elif menu == "Contacto":
    st.title("Contacto")
    st.write("Para más información o consultas, contáctanos...\n- **Correo**: contacto@mupai.com\n- **Teléfono**: +52 123 456 7890")

elif menu == "Evaluación del Estilo de Vida":
    submenu = st.sidebar.radio(
        "Áreas de Evaluación",
        ["Estrés Percibido", "Calidad del Sueño", "Nivel de Actividad Física", "Hábitos Alimenticios", "Potencial Genético Muscular"]
    )

    if submenu == "Estrés Percibido":
        st.title("Evaluación del Estrés Percibido")
        st.write("Responde las siguientes preguntas según cómo te has sentido durante el último mes...")
        # Preguntas de Estrés Percibido (código existente)

    elif submenu == "Calidad del Sueño":
        st.title("Evaluación de la Calidad del Sueño")
        st.write("Responde las siguientes preguntas relacionadas con tus hábitos de sueño durante el último mes:")

        # Preguntas principales del cuestionario PSQI
        hora_acostarse = st.text_input("1. ¿A qué hora usualmente te has ido a la cama por la noche?")
        tiempo_para_dormir = st.number_input("2. ¿Cuánto tiempo (en minutos) te ha tomado usualmente quedarte dormido/a cada noche?", min_value=0)
        hora_levantarse = st.text_input("3. ¿A qué hora usualmente te has levantado por la mañana?")
        horas_sueño = st.number_input("4. ¿Cuántas horas de sueño real has tenido por noche?", min_value=0)

        # Frecuencia de problemas para dormir
        st.write("5. ¿Con qué frecuencia has tenido problemas para dormir debido a las siguientes razones?")
        opciones_frecuencia = ["Nunca", "Menos de una vez por semana", "Una o dos veces por semana", "Tres o más veces por semana"]
        p5a = st.radio("a. No puedes dormir en los primeros 30 minutos.", opciones_frecuencia)
        p5b = st.radio("b. Te despiertas en medio de la noche o temprano en la mañana.", opciones_frecuencia)
        p5c = st.radio("c. Necesitas levantarte para ir al baño.", opciones_frecuencia)
        p5d = st.radio("d. No puedes respirar cómodamente.", opciones_frecuencia)
        p5e = st.radio("e. Toses o roncas fuerte.", opciones_frecuencia)
        p5f = st.radio("f. Tienes demasiado frío.", opciones_frecuencia)
        p5g = st.radio("g. Tienes demasiado calor.", opciones_frecuencia)
        p5h = st.radio("h. Tienes sueños malos.", opciones_frecuencia)
        p5i = st.radio("i. Tienes dolor.", opciones_frecuencia)

        # Botón para calcular puntaje
        if st.button("Calcular Puntuación de Calidad de Sueño"):
            # Simplificación para lógica de puntuación
            puntaje_total = 0  # Aquí debes implementar la lógica completa del PSQI si es necesario
            st.write("### Tu puntuación total de calidad de sueño es:", puntaje_total)

# Footer
st.markdown("---")
st.write("© 2024 MUPAI - Entrenamiento Digital Basado en Ciencia")
