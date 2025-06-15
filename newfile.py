import streamlit as st
import sqlite3
import bcrypt
import pandas as pd
from datetime import datetime
from PIL import Image
import requests
from io import BytesIO

# Configuración inicial de la página
st.set_page_config(
    page_title="MUPAI - Entrenamiento Digital",
    page_icon="🤖",
    layout="wide",
)

# URLs de las imágenes desde GitHub
LOGO_URL = "https://raw.githubusercontent.com/mupai5/MUPAI/main/LOGO.png"
GYM_IMAGE_URL = "https://raw.githubusercontent.com/mupai5/MUPAI/main/20250116_074233_0000.png"
IMAGE1_URL = "https://raw.githubusercontent.com/mupai5/MUPAI/main/20250116_074806_0000.jpg"
IMAGE2_URL = "https://raw.githubusercontent.com/mupai5/MUPAI/main/FB_IMG_1734820709707.jpg"
IMAGE3_URL = "https://raw.githubusercontent.com/mupai5/MUPAI/main/FB_IMG_1734820712642.jpg"
IMAGE4_URL = "https://raw.githubusercontent.com/mupai5/MUPAI/main/FB_IMG_1734820729323.jpg"
IMAGE5_URL = "https://raw.githubusercontent.com/mupai5/MUPAI/main/FB_IMG_1734820808186.jpg"

# Función para cargar imágenes desde URL
def load_image(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        st.error(f"Error cargando imagen: {e}")
        return None

# Aplicar estilos CSS personalizados
def aplicar_estilos():
    st.markdown("""
    <style>
    /* Estilos generales */
    body {
        font-family: 'Arial', sans-serif;
        color: #333;
        line-height: 1.6;
    }
    
    h1, h2, h3, h4 {
        color: #000000;
    }
    
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* Mejorar contraste de texto */
    p, li, div {
        color: #333333 !important;
    }
    
    /* Barra lateral */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
    }
    
    /* Imágenes */
    .logo-img {
        max-width: 400px;
        margin: 0 auto;
        display: block;
    }
    
    .gallery-img {
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Secciones */
    .section {
        margin-bottom: 30px;
    }
    
    /* Tarjetas */
    .card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 5px solid #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)

# Sección Inicio (actualizada)
def inicio():
    logo_img = load_image(LOGO_URL)
    if logo_img:
        st.image(logo_img, use_column_width=True, output_format="PNG")
    
    st.title("Bienvenido a MUPAI")

    st.markdown("""
    <div class="section">
        <h2>Misión</h2>
        <div class="card">
            Hacer accesible el entrenamiento basado en ciencia, proporcionando planes completamente personalizados 
            a través de herramientas digitales respaldadas por inteligencia artificial, datos precisos y la 
            investigación más actualizada en ciencias del ejercicio. Nos enfocamos en promover el desarrollo 
            integral de nuestros usuarios y su bienestar físico y mental.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section">
        <h2>Visión</h2>
        <div class="card">
            Convertirnos en uno de los máximos referentes a nivel global en entrenamiento digital personalizado, 
            aprovechando las nuevas tecnologías para hacer más accesible el fitness basado en ciencia. Aspiramos 
            a transformar la experiencia del entrenamiento físico, integrando inteligencia artificial, investigación 
            científica y herramientas digitales avanzadas que permitan a cualquier persona alcanzar su máximo potencial.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section">
        <h2>Política</h2>
        <div class="card">
            En <strong>MUPAI</strong>, nuestra política está fundamentada en el compromiso con la excelencia, 
            la ética y el servicio centrado en el usuario. Actuamos con responsabilidad y transparencia para 
            ofrecer soluciones tecnológicas que integren ciencia, personalización y accesibilidad, contribuyendo 
            al bienestar integral de quienes confían en nosotros.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section">
        <h2>Política del Servicio</h2>
        <div class="card">
            En <strong>MUPAI</strong>, guiamos nuestras acciones por los siguientes principios:
            <ul>
                <li>Diseñamos entrenamientos digitales que combinan personalización, datos confiables y ciencia del ejercicio.</li>
                <li>Aprovechamos la tecnología para ofrecer un servicio accesible y adaptable a las necesidades de cada usuario.</li>
                <li>Respetamos y protegemos la privacidad de los datos personales, garantizando su uso responsable.</li>
                <li>Innovamos de forma continua para mejorar la experiencia y los resultados de nuestros usuarios.</li>
                <li>Promovemos valores como el esfuerzo, la constancia y el respeto en cada interacción, fomentando un ambiente de crecimiento y bienestar.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Sección Sobre Mí (actualizada)
def sobre_mi():
    st.title("Sobre Mí")
    
    # Imagen principal del gimnasio
    gym_img = load_image(GYM_IMAGE_URL)
    if gym_img:
        st.image(gym_img, use_column_width=True, caption="MUSCLE UP GYM")
    
    st.markdown("""
    <div class="section">
        <div class="card">
            Soy Erick Francisco De Luna Hernández, un profesional apasionado por el fitness y las ciencias del ejercicio, 
            con una sólida formación académica y amplia experiencia en el diseño de metodologías de entrenamiento basadas 
            en ciencia. Actualmente, me desempeño en <em>Muscle Up GYM</em>, donde estoy encargado del diseño y desarrollo 
            de programas de entrenamiento fundamentados en evidencia científica. Mi labor se centra en crear metodologías 
            personalizadas que optimicen el rendimiento físico y promuevan el bienestar integral de nuestros usuarios.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section">
        <h3>Formación Académica</h3>
        <div class="card">
            <ul>
                <li>🎓 <strong>Maestría en Fuerza y Acondicionamiento</strong> - Football Science Institute</li>
                <li>📚 <strong>Licenciatura en Ciencias del Ejercicio</strong> - Universidad Autónoma de Nuevo León (UANL)</li>
                <li>🌍 <strong>Intercambio académico internacional</strong> - Universidad de Sevilla</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section">
        <h3>Logros y Reconocimientos</h3>
        <div class="card">
            <ul>
                <li>🥇 Premio al Mérito Académico UANL</li>
                <li>🏅 Primer Lugar de Generación en la Facultad de Organización Deportiva</li>
                <li>🎖️ Beca completa para intercambio internacional</li>
                <li>⭐ Miembro del Programa de Talento Universitario de la UANL</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Galería de Imágenes")
    
    # Cargar imágenes para la galería
    img1 = load_image(IMAGE1_URL)
    img2 = load_image(IMAGE2_URL)
    img3 = load_image(IMAGE3_URL)
    img4 = load_image(IMAGE4_URL)
    img5 = load_image(IMAGE5_URL)
    
    # Mostrar galería en columnas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if img1:
            st.image(img1, use_column_width=True, caption="", output_format="JPEG")
        if img4:
            st.image(img4, use_column_width=True, caption="", output_format="JPEG")
    
    with col2:
        if img2:
            st.image(img2, use_column_width=True, caption="", output_format="JPEG")
        if img5:
            st.image(img5, use_column_width=True, caption="", output_format="JPEG")
    
    with col3:
        if img3:
            st.image(img3, use_column_width=True, caption="", output_format="JPEG")

# (Mantén las demás funciones como registro, contacto, servicios, etc. sin cambios)

def main():
    aplicar_estilos()
    init_db()

    # Simulación de usuario logueado (reemplazar con lógica de sesión en producción)
    logged_user = st.sidebar.text_input("Usuario logueado (simulado para pruebas):")
    user_role = "user"  # Cambia a "admin" para probar como administrador

    st.sidebar.title("Navegación")
    menu = ["Inicio", "Sobre Mí", "Servicios", "Contacto", "Perfil MUPAI/Salud y Rendimiento", "Registro"]

    if logged_user and user_role == "admin":
        menu.append("Administrar Usuarios")
        menu.append("Historial de Actividades")

    choice = st.sidebar.radio("Selecciona una opción:", menu)

    if choice == "Inicio":
        inicio()
    elif choice == "Sobre Mí":
        sobre_mi()
    elif choice == "Servicios":
        servicios()
    elif choice == "Contacto":
        contacto()
    elif choice == "Perfil MUPAI/Salud y Rendimiento":
        perfil_mupai()
    elif choice == "Registro":
        registro()
    elif choice == "Administrar Usuarios" and user_role == "admin":
        gestionar_usuarios_pendientes()
        gestionar_usuarios_activos()
        exportar_usuarios_activos()
    elif choice == "Historial de Actividades" and user_role == "admin":
        ver_historial_actividades()

if __name__ == "__main__":
    main()
