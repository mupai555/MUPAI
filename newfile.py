import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st
import sqlite3
from datetime import datetime

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

# Función para calcular déficit calórico diario
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
def ajustar_volumen(base_volumen, balance_energetico, calidad_sueno, estres_percibido, categoria_competitiva, nivel_entrenamiento):
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

    if categoria_competitiva == "Men’s Physique":
        base_volumen['Pectorales'] *= 1.2
        base_volumen['Espalda'] *= 1.2
        base_volumen['Bíceps'] *= 1.1
        base_volumen['Tríceps'] *= 1.1
    elif categoria_competitiva == "Classic Physique":
        base_volumen['Pectorales'] *= 1.15
        base_volumen['Espalda'] *= 1.15
        base_volumen['Cuádriceps'] *= 1.2
        base_volumen['Piernas'] *= 1.2
    elif categoria_competitiva == "Wellness":
        base_volumen['Glúteos'] *= 1.25
        base_volumen['Cuádriceps'] *= 1.2
        base_volumen['Espalda'] *= 1.1

    if nivel_entrenamiento == "Principiante":
        ajuste += 0.1
    elif nivel_entrenamiento == "Intermedio":
        ajuste += 0.05
    elif nivel_entrenamiento == "Avanzado":
        ajuste -= 0.05

    volumen_ajustado = {grupo: max(6, int(volumen * ajuste)) for grupo, volumen in base_volumen.items()}
    return volumen_ajustado

# Función para enviar correo al usuario
def enviar_email_usuario(usuario_email, ffmi, clasificacion_ffmi, porcentaje_grasa, clasificacion_grasa):
    remitente = "tu_email@hotmail.com"
    destinatario = usuario_email
    password = "tu_contraseña"

    subject = "Tu Perfil MUPAI: Resultados"
    body = f"""
    Hola,

    Gracias por completar tu perfil en MUPAI. Aquí están los resultados de tu evaluación:

    1. **Nivel de Entrenamiento**:
    Tu **FFMI** es {ffmi}, lo que te coloca en la categoría: {clasificacion_ffmi}.
    
    2. **Porcentaje de Grasa Corporal**:
    Tu porcentaje de grasa corporal es {porcentaje_grasa}%. Según este porcentaje, tu clasificación es: {clasificacion_grasa}.
    
    --- 
    **Tabla de Clasificación FFMI**:
    - Principiante: FFMI < 18
    - Intermedio: 18 <= FFMI < 20
    - Avanzado: 20 <= FFMI < 23.5
    - Élite: FFMI >= 23.5

    **Tabla de Clasificación de Grasa Corporal**:
    - Hombres:
      - Saludable: 8-20%
      - Atleta: 6-13%
      - Rango elevado (no saludable): >25%
    - Mujeres:
      - Saludable: 21-32%
      - Atleta: 14-20%
      - Rango elevado (no saludable): >35%
    
    ¡Gracias por confiar en MUPAI para tu entrenamiento personalizado!

    Saludos,
    MUPAI Team
    """
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = subject
    mensaje.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(remitente, password)
        text = mensaje.as_string()
        server.sendmail(remitente, destinatario, text)
        server.quit()
        print("Correo enviado exitosamente al usuario.")
    except Exception as e:
        print(f"Error al enviar correo al usuario: {e}")

# Función para enviar correo al administrador
def enviar_email_administrador(usuario_email, usuario_data):
    remitente = "tu_email@hotmail.com"
    destinatario = "tu_email_admin@hotmail.com"
    password = "tu_contraseña"

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
    
    2. **Déficit Calórico Diario**:
    - Déficit diario recomendado: {usuario_data['deficit_calorico_diario']} kcal/día
    - Balance energético: {usuario_data['balance_energetico']}

    3. **Volumen de Entrenamiento Ajustado**:
    - Pectorales: {usuario_data['volumen_pectorales']} series/semana
    - Espalda: {usuario_data['volumen_espalda']} series/semana
    - Bíceps: {usuario_data['volumen_biceps']} series/semana

    --- 
    **Recomendaciones**:
    Basado en la información proporcionada, ajustamos el volumen y el déficit calórico para este usuario.
    
    Saludos,
    MUPAI Team
    """
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = subject
    mensaje.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(remitente, password)
        text = mensaje.as_string()
        server.sendmail(remitente, destinatario, text)
        server.quit()
        print("Correo enviado al administrador exitosamente.")
    except Exception as e:
        print(f"Error al enviar correo al administrador: {e}")

# Función para mostrar el inicio
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

# Función principal
def main():
    init_db()

    logged_user = st.sidebar.text_input("Usuario logueado (simulado para pruebas):")
    user_role = "user"  # Cambiar a "admin" para probar como administrador

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
