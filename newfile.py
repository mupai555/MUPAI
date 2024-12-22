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
        Hacer accesible el entrenamiento basado en ciencia...
    """)
    st.header("Visión")
    st.write("""
        Convertirnos en uno de los máximos referentes a nivel global en entrenamiento digital personalizado...
    """)

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

    if submenu == "Calidad del Sueño":
        st.title("Evaluación de la Calidad del Sueño - Índice de Pittsburgh")
        st.write("""
        Responde las siguientes preguntas sobre tus hábitos de sueño durante el último mes.
        """)

        # Preguntas principales del PSQI
        hora_acostarse = st.text_input("1. ¿A qué hora se ha acostado normalmente?")
        tiempo_dormirse = st.selectbox(
            "2. ¿Cuánto tiempo tarda normalmente en dormirse?",
            ["Menos de 15 minutos", "16-30 minutos", "31-60 minutos", "Más de 60 minutos"]
        )
        hora_levantarse = st.text_input("3. ¿A qué hora se ha levantado normalmente?")
        horas_dormidas = st.number_input(
            "4. ¿Cuántas horas calcula que duerme habitualmente cada noche?",
            min_value=0, max_value=12, step=1
        )

        # Problemas para dormir
        st.write("5. Durante el último mes, ¿con qué frecuencia ha experimentado los siguientes problemas?")
        problemas_dormir = {
            "No poder conciliar el sueño": st.radio(
                "5a. No poder conciliar el sueño en la primera media hora:",
                ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
            ),
            "Despertarse durante la noche": st.radio(
                "5b. Despertarse durante la noche o demasiado temprano:",
                ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
            ),
            "Ir al baño durante la noche": st.radio(
                "5c. Tener que levantarse para ir al baño:",
                ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
            ),
            "Dificultad para respirar": st.radio(
                "5d. No poder respirar bien durante la noche:",
                ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
            ),
            # Continúa con todas las preguntas del apartado 5...
        }

        calidad_sueno = st.radio(
            "6. ¿Cómo calificaría la calidad de su sueño?",
            ["Muy buena", "Bastante buena", "Bastante mala", "Muy mala"]
        )

        uso_medicacion = st.radio(
            "7. ¿Cuántas veces tomó medicación para dormir?",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        )

        somnolencia_diurna = st.radio(
            "8. ¿Con qué frecuencia ha sentido somnolencia durante el día?",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        )

        dificultad_diurna = st.radio(
            "9. ¿Con qué frecuencia ha tenido dificultades para mantener suficiente energía durante el día?",
            ["Ninguna vez", "Leve problema", "Problema", "Grave problema"]
        )

        # Cálculo de puntuaciones
        if st.button("Calcular Puntuación"):
            puntuacion_total = 0

            # Ejemplo de cómo calcular puntuaciones (usar la lógica del PDF):
            puntuacion_total += {"Muy buena": 0, "Bastante buena": 1, "Bastante mala": 2, "Muy mala": 3}[calidad_sueno]
            # Continúa con las demás puntuaciones...

            st.write(f"### Tu puntuación total del PSQI es: {puntuacion_total}")
            if puntuacion_total <= 5:
                st.success("Buena calidad de sueño.")
            elif 6 <= puntuacion_total <= 10:
                st.warning("Calidad de sueño moderada.")
            else:
                st.error("Mala calidad de sueño. Considera consultar a un especialista.")

# Footer
st.markdown("---")
st.write("© 2024 MUPAI - Entrenamiento Digital Basado en Ciencia")
