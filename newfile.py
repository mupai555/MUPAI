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
    ["Inicio", "Sobre Mí", "Servicios", "Contacto"]
)

# Contenido según la selección del menú
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
    ¡Hola! Soy Erick Francisco De Luna Hernandez, un profesional apasionado por el fitness y la ciencia del ejercicio.
    """)

    # Mostrar imágenes con captions
    st.image("FB_IMG_1734820693317.jpg", caption="Erick Francisco De Luna Hernandez", use_container_width=True)
    st.image("FB_IMG_1734820709707.jpg", caption="Demostración de Entrenamiento Funcional", use_container_width=True)
    st.image("FB_IMG_1734820712642.jpg", caption="Logros en el Gimnasio", use_container_width=True)
    st.image("FB_IMG_1734820729323.jpg", caption="Sesión al Atardecer - Flexión de Brazos", use_container_width=True)
    st.image("FB_IMG_1734820808186.jpg", caption="Entrenamiento de Fuerza y Resistencia", use_container_width=True)

    # Formación académica
    st.subheader("Formación Académica")
    st.write("""
    - **Maestría** (En curso): Strength and Conditioning, Football Science Institute (2023–Presente).
    - **Licenciatura**: Ciencias del Ejercicio, Universidad Autónoma de Nuevo León (2013–2017).
    - Intercambio Académico: Universidad de Sevilla (2016–2017).
    """)

    # Premios y reconocimientos
    st.subheader("Premios y Reconocimientos")
    st.write("""
    - **UANL Academic Merit Award** (2019).
    - **100% Beca para Intercambio Académico**: Universidad de Sevilla (2016–2017).
    """)

elif menu == "Servicios":
    # Sección "Servicios"
    st.title("Servicios")
    st.write("""
    **MUPAI** ofrece una amplia gama de servicios personalizados basados en ciencia del ejercicio:
    - Planes de entrenamiento individualizados.
    - Programas de mejora física y mental.
    - Asesoría en nutrición deportiva.
    """)

elif menu == "Contacto":
    # Sección "Contacto"
    st.title("Contacto")
    st.write("""
    Para más información o consultas, contáctanos:
    - **Correo**: contacto@mupai.com
    - **Teléfono**: +52 123 456 7890
    - **Ubicación**: Monterrey, Nuevo León, México
    """)

# Pie de página
st.markdown("---")
st.write("© 2024 MUPAI - Entrenamiento Digital Basado en Ciencia")
