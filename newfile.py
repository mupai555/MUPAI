import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')

# Configuración inicial de la página
st.set_page_config(
    page_title="MUPAI - Entrenamiento Digital",
    page_icon="🤖",
    layout="wide",
)

# Configuración de la base de datos
def init_db():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                full_name TEXT,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                phone TEXT,
                birth_date TEXT,
                password TEXT,
                authorized INTEGER DEFAULT 0,
                role TEXT DEFAULT 'user',
                terms_accepted INTEGER DEFAULT 0,
                date_added TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_activity (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                action TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        conn.commit()

# Función para enviar correo al usuario
def enviar_email_usuario(usuario_email, ffmi, clasificacion_ffmi, porcentaje_grasa, clasificacion_grasa):
    subject = "Tu Perfil MUPAI: Resultados"
    body = f"""
    Hola,

    Gracias por completar tu perfil en MUPAI. Aquí están los resultados de tu evaluación:

    1. **Nivel de Entrenamiento**:
    Tu **FFMI** es {ffmi}, lo que te coloca en la categoría: {clasificacion_ffmi}.
    
    2. **Porcentaje de Grasa Corporal**:
    Tu porcentaje de grasa corporal es {porcentaje_grasa}%. Según este porcentaje, tu clasificación es: {clasificacion_grasa}.
    
    ¡Gracias por confiar en MUPAI para tu entrenamiento personalizado!

    Saludos,
    MUPAI Team
    """

    mensaje = MIMEMultipart()
    mensaje['From'] = EMAIL_ADDRESS
    mensaje['To'] = usuario_email
    mensaje['Subject'] = subject
    mensaje.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, usuario_email, mensaje.as_string())
        server.quit()
        print("Correo enviado exitosamente al usuario.")
    except Exception as e:
        print(f"Error al enviar correo al usuario: {e}")

# Función para enviar correo al administrador
def enviar_email_administrador(usuario_email, usuario_data):
    subject = f"Información Completa del Usuario {usuario_data['username']}"
    body = f"""
    Hola,

    Aquí está la información detallada de un nuevo usuario registrado en MUPAI:

    1. **Datos del Usuario**:
    - Nombre: {usuario_data['full_name']}
    - Usuario: {usuario_data['username']}
    - Email: {usuario_data['email']}
    - Fecha de Registro: {usuario_data['date_added']}
    - Porcentaje de Grasa Corporal: {usuario_data['porcentaje_grasa']}%
    - FFMI: {usuario_data['ffmi']}
    - Clasificación FFMI: {usuario_data['clasificacion_ffmi']}
    
    Saludos,
    MUPAI Team
    """

    mensaje = MIMEMultipart()
    mensaje['From'] = EMAIL_ADDRESS
    mensaje['To'] = ADMIN_EMAIL
    mensaje['Subject'] = subject
    mensaje.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, ADMIN_EMAIL, mensaje.as_string())
        server.quit()
        print("Correo enviado al administrador exitosamente.")
    except Exception as e:
        print(f"Error al enviar correo al administrador: {e}")

# Funciones para cada sección
def inicio():
    st.image("LOGO.png", use_container_width=True)
    st.title("Bienvenido a MUPAI")

    # Misión
    st.header("Misión")
    st.write("""
    Hacer accesible el entrenamiento basado en ciencia, proporcionando planes completamente personalizados a través de herramientas digitales respaldadas por inteligencia artificial, datos precisos y la investigación más actualizada en ciencias del ejercicio. Nos enfocamos en promover el desarrollo integral de nuestros usuarios y su bienestar físico y mental.
    """)

    # Visión
    st.header("Visión")
    st.write("""
    Convertirnos en uno de los máximos referentes a nivel global en entrenamiento digital personalizado, aprovechando las nuevas tecnologías para hacer más accesible el fitness basado en ciencia. Aspiramos a transformar la experiencia del entrenamiento físico, integrando inteligencia artificial, investigación científica y herramientas digitales avanzadas que permitan a cualquier persona alcanzar su máximo potencial.
    """)

    # Política
    st.header("Política")
    st.write("""
    En **MUPAI**, nuestra política está fundamentada en el compromiso con la excelencia, la ética y el servicio centrado en el usuario. Actuamos con responsabilidad y transparencia para ofrecer soluciones tecnológicas que integren ciencia, personalización y accesibilidad, contribuyendo al bienestar integral de quienes confían en nosotros.
    """)

    # Política del Servicio
    st.header("Política del Servicio")
    st.write("""
    En **MUPAI**, guiamos nuestras acciones por los siguientes principios:
    - Diseñamos entrenamientos digitales que combinan personalización, datos confiables y ciencia del ejercicio.
    - Aprovechamos la tecnología para ofrecer un servicio accesible y adaptable a las necesidades de cada usuario.
    - Respetamos y protegemos la privacidad de los datos personales, garantizando su uso responsable.
    - Innovamos de forma continua para mejorar la experiencia y los resultados de nuestros usuarios.
    - Promovemos valores como el esfuerzo, la constancia y el respeto en cada interacción, fomentando un ambiente de crecimiento y bienestar.
    """)

def sobre_mi():
    st.title("Sobre Mí")
    st.write("""
    Soy Erick Francisco De Luna Hernández, un profesional apasionado por el fitness y las ciencias del ejercicio, con una sólida formación académica y amplia experiencia en el diseño de metodologías de entrenamiento basadas en ciencia. Actualmente, me desempeño en *Muscle Up GYM*, donde estoy encargado del diseño y desarrollo de programas de entrenamiento fundamentados en evidencia científica.
    """)

    st.subheader("Galería de Imágenes")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("20250116_074806_0000.jpg", use_container_width=True)
        st.image("FB_IMG_1734820729323.jpg", use_container_width=True)
    with col2:
        st.image("FB_IMG_1734820709707.jpg", use_container_width=True)
        st.image("FB_IMG_1734820808186.jpg", use_container_width=True)
    with col3:
        st.image("FB_IMG_1734820712642.jpg", use_container_width=True)

def contacto():
    st.title("Contacto")
    st.write("""
    Para más información o consultas, contáctanos:
    - **Correo**: contacto@mupai.com  
    - **Teléfono**: +52 866 258 05 94  
    - **Ubicación**: Monterrey, Nuevo León  
    """)

# Función principal
def main():
    init_db()

    st.sidebar.title("Navegación")
    menu = ["Inicio", "Sobre Mí", "Contacto"]
    choice = st.sidebar.radio("Selecciona una opción:", menu)

    if choice == "Inicio":
        inicio()
    elif choice == "Sobre Mí":
        sobre_mi()
    elif choice == "Contacto":
        contacto()

if __name__ == "__main__":
    main()
