import streamlit as st

# Page configuration
st.set_page_config(
    page_title="MUPAI - Entrenamiento Digital",
    page_icon="🤖",
    layout="wide",
)

# Sidebar navigation
menu = st.sidebar.selectbox(
    "Menú",
    ["Inicio", "Sobre Mí", "Servicios", "Contacto"]
)

# Content based on menu selection
if menu == "Inicio":
    st.title("Bienvenido a MUPAI")
    st.write("**MUPAI** es la plataforma de entrenamiento digital basada en ciencia.")

elif menu == "Sobre Mí":
    st.title("Sobre Mí")
    st.write("""
    ¡Hola! Soy Erick Francisco De Luna Hernandez, un profesional apasionado por el fitness y la ciencia del ejercicio.
    """)

    # Add your uploaded images with captions
    st.image("FB_IMG_1734820693317.jpg", caption="Erick Francisco De Luna Hernandez", use_column_width=True)
    st.image("FB_IMG_1734820709707.jpg", caption="Demostración de Entrenamiento Funcional", use_column_width=True)
    st.image("FB_IMG_1734820712642.jpg", caption="Logros en el Gimnasio", use_column_width=True)
    st.image("FB_IMG_1734820729323.jpg", caption="Sesión al Atardecer - Flexión de Brazos", use_column_width=True)
    st.image("FB_IMG_1734820808186.jpg", caption="Entrenamiento de Fuerza y Resistencia", use_column_width=True)

    st.subheader("Formación Académica")
    st.write("""
    - **Maestría** (En curso): Strength and Conditioning, Football Science Institute (2023–Presente).
    - **Licenciatura**: Ciencias del Ejercicio, Universidad Autónoma de Nuevo León (2013–2017).
    - Intercambio Académico: Universidad de Sevilla (2016–2017).
    """)

    st.subheader("Premios y Reconocimientos")
    st.write("""
    - **UANL Academic Merit Award** (2019).
    - **100% Beca para Intercambio Académico**: Universidad de Sevilla (2016–2017).
    """)

elif menu == "Servicios":
    st.title("Servicios")
    st.write("""
    **MUPAI** ofrece una amplia gama de servicios personalizados basados en ciencia del ejercicio:
    - Planes de entrenamiento individualizados.
    - Programas de mejora física y mental.
    - Asesoría en nutrición deportiva.
    """)

elif menu == "Contacto":
    st.title("Contacto")
    st.write("""
    Para más información o consultas, contáctanos:
    - **Correo**: contacto@mupai.com
    - **Teléfono**: +52 123 456 7890
    - **Ubicación**: Monterrey, Nuevo León, México
    """)

# Footer
st.markdown("---")
st.write("© 2024 MUPAI - Entrenamiento Digital Basado en Ciencia")
