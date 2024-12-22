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
    [
        "Inicio", 
        "Sobre Mí", 
        "Servicios", 
        "Contacto", 
        "Evaluación del Estilo de Vida"
    ]
)

# Submenú de Evaluación del Estilo de Vida
if menu == "Evaluación del Estilo de Vida":
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
        st.write("""
        En este apartado se evalúa el nivel de estrés percibido mediante preguntas o indicadores clave.
        """)
        # Aquí podrías agregar preguntas o gráficos

    elif submenu == "Calidad del Sueño":
        st.title("Evaluación de la Calidad del Sueño")
        st.write("""
        Evaluación de la calidad del sueño basada en factores como la duración, consistencia y eficiencia.
        """)

    elif submenu == "Nivel de Actividad Física":
        st.title("Nivel de Actividad Física")
        st.write("""
        Análisis del nivel de actividad física diaria y semanal, enfocado en identificar patrones de movimiento.
        """)

    elif submenu == "Hábitos Alimenticios":
        st.title("Hábitos Alimenticios")
        st.write("""
        Evaluación de los hábitos alimenticios, incluyendo el consumo de alimentos procesados, horarios de comidas y balance nutricional.
        """)

    elif submenu == "Potencial Genético Muscular":
        st.title("Potencial Genético Muscular")
        st.write("""
        Evaluación del potencial genético muscular mediante parámetros físicos y genéticos disponibles.
        """)

# Contenido del resto del menú
elif menu == "Inicio":
    st.image("LOGO.png", use_container_width=True)
    st.title("Bienvenido a MUPAI")
    st.header("Misión")
    st.write("Hacer accesible el entrenamiento basado en ciencia...")
    # Aquí va el resto del contenido de Inicio

elif menu == "Sobre Mí":
    st.title("Sobre Mí")
    st.write("""
    Soy Erick Francisco De Luna Hernández...
    """)
    # Aquí va el resto del contenido de Sobre Mí

elif menu == "Servicios":
    st.title("Servicios")
    st.write("""
    **MUPAI** ofrece una amplia gama de servicios personalizados basados en ciencia del ejercicio...
    """)

elif menu == "Contacto":
    st.title("Contacto")
    st.write("""
    Para más información o consultas, contáctanos...
    """)

# Footer
st.markdown("---")
st.write("© 2024 MUPAI - Entrenamiento Digital Basado en Ciencia")
