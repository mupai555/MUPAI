import streamlit as st
import sqlite3
import bcrypt
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

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

# Función para calcular el FFMI
def calcular_ffmi(peso, altura, porcentaje_grasa):
    masa_magra = peso * (1 - porcentaje_grasa / 100)
    return round(masa_magra / (altura ** 2), 2)

# Función para clasificar el FFMI
def clasificar_ffmi(ffmi):
    if ffmi < 18:
        return "Principiante"
    elif 18 <= ffmi < 20:
        return "Intermedio"
    elif 20 <= ffmi < 23.5:
        return "Avanzado"
    else:
        return "Élite"

# Función para calcular déficit óptimo
def calcular_deficit_optimo(porcentaje_grasa_actual, porcentaje_grasa_objetivo, semanas_restantes, peso):
    if porcentaje_grasa_actual <= porcentaje_grasa_objetivo:
        return 0  # Ya está en el objetivo
    deficit_calorico_semanal = ((porcentaje_grasa_actual - porcentaje_grasa_objetivo) * peso * 7700) / semanas_restantes
    deficit_diario = deficit_calorico_semanal / 7
    return round(deficit_diario, 2)

# Función para determinar balance energético
def calcular_balance_energetico(deficit_diario, calorias_mantenimiento):
    if deficit_diario == 0:
        return "Mantenimiento"
    elif deficit_diario > 0:
        return f"DÉFICIT: {calorias_mantenimiento - deficit_diario} kcal/día"
    else:
        return f"SUPERÁVIT: {calorias_mantenimiento + abs(deficit_diario)} kcal/día"

# Función para calcular volumen ajustado
def ajustar_volumen(base_volumen, balance_energetico, calidad_sueno, estres_percibido):
    ajuste = 1.0
    if balance_energetico == "Déficit":
        ajuste -= 0.15
    elif balance_energetico == "Superávit":
        ajuste += 0.15

    if calidad_sueno in ["Regular", "Mala"]:
        ajuste -= 0.1
    elif calidad_sueno == "Muy buena":
        ajuste += 0.1

    if estres_percibido > 7:
        ajuste -= 0.2
    elif estres_percibido < 4:
        ajuste += 0.1

    volumen_ajustado = {grupo: max(6, int(volumen * ajuste)) for grupo, volumen in base_volumen.items()}
    return volumen_ajustado

# Sección "Perfil MUPAI/Salud y Rendimiento"
def perfil_mupai():
    st.title("Perfil MUPAI/Salud y Rendimiento")
    st.write("""
    Este cuestionario está diseñado para evaluar tu estilo de vida, rendimiento, composición corporal y más. 
    Responde a las preguntas para obtener un feedback inicial sobre tu perfil MUPAI.

    Posteriormente, podrás recibir un plan de entrenamiento personalizado basado en los resultados de este perfil.
    """)

    # Sección para recoger datos del usuario
    peso = st.number_input("¿Cuál es tu peso (kg)?", min_value=1.0, step=0.1)
    altura = st.number_input("¿Cuál es tu altura (cm)?", min_value=1, step=1)
    porcentaje_grasa = st.number_input("¿Cuál es tu porcentaje de grasa corporal (%)?", min_value=0.0, step=0.1)
    
    # Función para calcular FFMI
    ffmi = calcular_ffmi(peso, altura / 100, porcentaje_grasa)  # Convertimos altura de cm a metros
    clasificacion = clasificar_ffmi(ffmi)
    
    # Mostrar resultados del FFMI
    st.subheader("Resultado FFMI")
    st.write(f"Tu FFMI es: {ffmi} - Clasificación: {clasificacion}")

    # Preguntar por más detalles para el ajuste del volumen
    balance_energetico = st.selectbox("¿Cuál es tu balance energético?", ["Mantenimiento", "Déficit", "Superávit"])
    calidad_sueno = st.selectbox("¿Cómo calificarías la calidad de tu sueño?", ["Muy buena", "Buena", "Regular", "Mala"])
    estres_percibido = st.slider("¿Qué tan estresado te sientes (1-10)?", 1, 10, 5)

    base_volumen = {
        'Tren superior': 10,
        'Tren inferior': 12
    }

    # Calcular volumen ajustado
    volumen_ajustado = ajustar_volumen(base_volumen, balance_energetico, calidad_sueno, estres_percibido)

    # Mostrar el volumen ajustado
    st.subheader("Volumen de Entrenamiento Ajustado")
    for grupo, volumen in volumen_ajustado.items():
        st.write(f"{grupo}: {volumen} series por semana")
    
    # Mostrar resultados adicionales como el déficit óptimo
    porcentaje_grasa_objetivo = st.number_input("¿Cuál es tu porcentaje de grasa corporal objetivo?", min_value=0.0, step=0.1)
    semanas_restantes = st.number_input("¿En cuántas semanas te gustaría alcanzar tu objetivo?", min_value=1, step=1)

    deficit_diario = calcular_deficit_optimo(porcentaje_grasa, porcentaje_grasa_objetivo, semanas_restantes, peso)
    calorias_mantenimiento = 2500  # Ejemplo: este valor puede variar según el usuario
    balance = calcular_balance_energetico(deficit_diario, calorias_mantenimiento)
    
    # Mostrar el déficit diario y balance energético
    st.subheader("Déficit Calórico Óptimo y Balance Energético")
    st.write(f"Déficit calórico diario: {deficit_diario} kcal")
    st.write(f"Balance energético: {balance}")
    
    st.write("¡Gracias por completar tu perfil MUPAI! Con esta información, podemos ofrecerte un plan de entrenamiento y nutrición más personalizado.")

# Otras secciones (Misión, Visión, Política, etc.)

def inicio():
    st.image("LOGO.png", use_container_width=True)
    st.title("Bienvenido a MUPAI")

    st.header("Misión")
    st.write("""
    Hacer accesible el entrenamiento basado en ciencia, proporcionando planes completamente personalizados a través de herramientas digitales respaldadas por inteligencia artificial, datos precisos y la investigación más actualizada en ciencias del ejercicio. Nos enfocamos en promover el desarrollo integral de nuestros usuarios y su bienestar físico y mental.
    """)

    st.header("Visión")
    st.write("""
    Convertirnos en uno de los máximos referentes a nivel global en entrenamiento digital personalizado, aprovechando las nuevas tecnologías para hacer más accesible el fitness basado en ciencia. Aspiramos a transformar la experiencia del entrenamiento físico, integrando inteligencia artificial, investigación científica y herramientas digitales avanzadas que permitan a cualquier persona alcanzar su máximo potencial.
    """)

    st.header("Política")
    st.write("""
    En **MUPAI**, nuestra política está fundamentada en el compromiso con la excelencia, la ética y el servicio centrado en el usuario. Actuamos con responsabilidad y transparencia para ofrecer soluciones tecnológicas que integren ciencia, personalización y accesibilidad, contribuyendo al bienestar integral de quienes confían en nosotros.
    """)

    st.header("Política del Servicio")
    st.write("""
    En **MUPAI**, guiamos nuestras acciones por los siguientes principios:
    - Diseñamos entrenamientos digitales que combinan personalización, datos confiables y ciencia del ejercicio.
    - Aprovechamos la tecnología para ofrecer un servicio accesible y adaptable a las necesidades de cada usuario.
    - Respetamos y protegemos la privacidad de los datos personales, garantizando su uso responsable.
    - Innovamos de forma continua para mejorar la experiencia y los resultados de nuestros usuarios.
    - Promovemos valores como el esfuerzo, la constancia y el respeto en cada interacción, fomentando un ambiente de crecimiento y bienestar.
    """)

# Sección Sobre Mí
def sobre_mi():
    st.title("Sobre Mí")
    st.write("""
    Soy Erick Francisco De Luna Hernández, un profesional apasionado por el fitness y las ciencias del ejercicio, con una sólida formación académica y amplia experiencia en el diseño de metodologías de entrenamiento basadas en ciencia. Actualmente, me desempeño en *Muscle Up GYM*, donde estoy encargado del diseño y desarrollo de programas de entrenamiento fundamentados en evidencia científica. Mi labor se centra en crear metodologías personalizadas que optimicen el rendimiento físico y promuevan el bienestar integral de nuestros usuarios.

    Cuento con una Maestría en Fuerza y Acondicionamiento por el *Football Science Institute*, una Licenciatura en Ciencias del Ejercicio por la **Universidad Autónoma de Nuevo León (UANL)** y un intercambio académico internacional en la *Universidad de Sevilla*. Durante mi carrera, fui miembro del **Programa de Talento Universitario de la UANL**, una distinción que reconoce a estudiantes de excelencia académica y extracurricular. Además, adquirí experiencia clave en el **Laboratorio de Rendimiento Humano de la UANL**, colaborando en evaluaciones avanzadas de fuerza, biomecánica y acondicionamiento físico con tecnologías innovadoras.

    Mi trayectoria ha sido reconocida con distinciones como el *Premio al Mérito Académico de la UANL*, el **Primer Lugar de Generación** en la Facultad de Organización Deportiva y una *beca completa para un intercambio internacional* en la Universidad de Sevilla. Estos logros reflejan mi compromiso con la excelencia académica y profesional.

    Con una combinación de preparación académica, experiencia práctica y un enfoque basado en la evidencia, me dedico a diseñar soluciones que transformen el rendimiento físico y promuevan la salud integral, integrando ciencia, innovación y personalización.
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

# Otras secciones como Servicios, Contacto, etc.

# Función principal
def main():
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
