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
    # Continúa con los demás textos de Inicio...

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
        Responda las siguientes preguntas sobre sus hábitos de sueño durante el último mes.
        """)

        # Preguntas
        hora_acostarse = st.text_input("1. ¿A qué hora se ha acostado normalmente?")
        tiempo_dormirse = st.selectbox(
            "2. ¿Cuánto tiempo tarda en dormirse?",
            ["Menos de 15 minutos", "16-30 minutos", "31-60 minutos", "Más de 60 minutos"]
        )
        hora_levantarse = st.text_input("3. ¿A qué hora se levanta habitualmente?")
        horas_dormidas = st.slider("4. ¿Cuántas horas calcula que duerme por noche?", 0, 12, 7)

        problemas_dormir = {
            "No poder conciliar el sueño": st.radio(
                "5a. No poder conciliar el sueño en la primera media hora:",
                ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
            ),
            "Despertarse durante la noche": st.radio(
                "5b. Despertarse durante la noche o de madrugada:",
                ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
            ),
            # Continúa con las demás preguntas del apartado 5...
        }

        calidad_sueno = st.radio(
            "6. ¿Cómo valoraría la calidad de su sueño?",
            ["Muy buena", "Bastante buena", "Bastante mala", "Muy mala"]
        )

        medicamentos_dormir = st.radio(
            "7. ¿Cuántas veces tomó medicamentos para dormir?",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        )

        somnolencia = st.radio(
            "8. ¿Cuántas veces ha sentido somnolencia durante el día?",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        )

        dificultad_diurna = st.radio(
            "9. ¿Ha tenido problemas para realizar actividades diurnas?",
            ["Ningún problema", "Leve problema", "Problema", "Grave problema"]
        )

        # Procesamiento de puntuaciones
        if st.button("Calcular Puntuación"):
            puntuaciones = {
                "calidad_sueno": {"Muy buena": 0, "Bastante buena": 1, "Bastante mala": 2, "Muy mala": 3},
                "tiempo_dormirse": {"Menos de 15 minutos": 0, "16-30 minutos": 1, "31-60 minutos": 2, "Más de 60 minutos": 3},
                # Añade las demás puntuaciones aquí...
            }

            total_puntuacion = 0
            total_puntuacion += puntuaciones["calidad_sueno"][calidad_sueno]
            total_puntuacion += puntuaciones["tiempo_dormirse"][tiempo_dormirse]
            # Continúa con el cálculo de puntuaciones...

            st.write("### Tu puntuación total del PSQI es:", total_puntuacion)
            if total_puntuacion <= 5:
                st.success("Buena calidad de sueño.")
            elif 6 <= total_puntuacion <= 10:
                st.warning("Calidad de sueño moderada.")
            else:
                st.error("Mala calidad de sueño. Considera consultar a un especialista.")

# Footer
st.markdown("---")
st.write("© 2024 MUPAI - Entrenamiento Digital Basado en Ciencia")
