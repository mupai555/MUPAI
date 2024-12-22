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
    st.write("""
        Hacer accesible el entrenamiento basado en ciencia, proporcionando planes completamente personalizados
        a través de herramientas digitales respaldadas por inteligencia artificial, datos precisos y la investigación 
        más actualizada en ciencias del ejercicio.
    """)
    st.header("Visión")
    st.write("""
        Convertirnos en uno de los máximos referentes a nivel global en entrenamiento digital personalizado,
        aprovechando las nuevas tecnologías para hacer más accesible el fitness basado en ciencia.
    """)
elif menu == "Sobre Mí":
    st.title("Sobre Mí")
    st.write("""
        Soy Erick Francisco De Luna Hernández, un profesional apasionado por el fitness y las ciencias del ejercicio.
    """)
elif menu == "Servicios":
    st.title("Servicios")
    st.write("""
        - Planes de entrenamiento individualizados.
        - Programas de mejora física y mental.
        - Asesoría en nutrición deportiva.
    """)
elif menu == "Contacto":
    st.title("Contacto")
    st.write("""
        - Correo: contacto@mupai.com
        - Teléfono: +52 123 456 7890
    """)
elif menu == "Evaluación del Estilo de Vida":
    submenu = st.sidebar.radio(
        "Áreas de Evaluación",
        ["Estrés Percibido", "Calidad del Sueño", "Nivel de Actividad Física"]
    )

    if submenu == "Calidad del Sueño":
        st.title("Evaluación de la Calidad del Sueño")
        st.write("Responde las siguientes preguntas relacionadas con tus hábitos de sueño durante el último mes:")

        hora_acostarse = st.text_input("1. ¿A qué hora usualmente te has ido a la cama por la noche?")
        tiempo_para_dormir = st.number_input("2. ¿Cuánto tiempo (en minutos) te ha tomado usualmente quedarte dormido/a cada noche?", min_value=0)
        hora_levantarse = st.text_input("3. ¿A qué hora usualmente te has levantado por la mañana?")
        horas_sueño = st.number_input("4. ¿Cuántas horas de sueño real has tenido por noche?", min_value=0)

        st.write("5. ¿Con qué frecuencia has tenido problemas para dormir debido a las siguientes razones?")
        opciones_frecuencia = ["Nunca", "Menos de una vez por semana", "Una o dos veces por semana", "Tres o más veces por semana"]
        p5a = st.radio("a. No puedes dormir en los primeros 30 minutos.", opciones_frecuencia)
        p5b = st.radio("b. Te despiertas en medio de la noche o temprano en la mañana.", opciones_frecuencia)
        p5c = st.radio("c. Necesitas levantarte para ir al baño.", opciones_frecuencia)
        p5d = st.radio("d. No puedes respirar cómodamente.", opciones_frecuencia)
        p5e = st.radio("e. Toses o roncas fuerte.", opciones_frecuencia)
        p5f = st.radio("f. Tienes demasiado frío.", opciones_frecuencia)
        p5g = st.radio("g. Tienes demasiado calor.", opciones_frecuencia)
        p5h = st.radio("h. Tuviste sueños desagradables.", opciones_frecuencia)

        # Mostrar puntuación
        if st.button("Calcular Puntuación"):
            st.write("Función de cálculo pendiente")
