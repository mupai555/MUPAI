import streamlit as st
import sqlite3
import bcrypt

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
                username TEXT UNIQUE,
                password TEXT,
                authorized INTEGER DEFAULT 0
            )
        ''')
        conn.commit()

# Guardar un usuario nuevo en la base de datos
def register_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

# Verificar login
def login_user(username, password):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        user = cursor.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            return user
        return None

# Autorizar usuario manualmente
def authorize_user(user_id):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET authorized=1 WHERE id=?", (user_id,))
        conn.commit()

# Ver usuarios activos
def gestionar_usuarios_activos():
    st.subheader("Usuarios Activos y Autorizados")
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        active_users = cursor.execute("SELECT id, username FROM users WHERE authorized=1").fetchall()

    if active_users:
        st.write("Usuarios activos:")
        for user in active_users:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**Usuario**: {user[1]}")
            with col2:
                if st.button("Revocar", key=f"revoke_{user[0]}"):
                    with sqlite3.connect('users.db') as conn:
                        cursor = conn.cursor()
                        cursor.execute("UPDATE users SET authorized=0 WHERE id=?", (user[0],))
                        conn.commit()
                    st.success(f"Acceso revocado para {user[1]}.")
    else:
        st.write("No hay usuarios activos autorizados.")

# Función exclusiva para usuarios autorizados
def funcionalidad_exclusiva():
    st.subheader("Área Exclusiva para Usuarios Autorizados")
    st.write("Bienvenido a la sección exclusiva de MUPAI. Aquí puedes acceder a contenido y herramientas especiales.")

# Sección Perfil MUPAI/Salud y Rendimiento
def perfil_mupai():
    st.title("Perfil MUPAI/Salud y Rendimiento")
    st.write("""
    Este es un cuestionario diseñado para evaluar tu estilo de vida, rendimiento, composición corporal y más. Contesta las preguntas para obtener un feedback inicial sobre tu perfil MUPAI.

    Próximamente, podrás recibir un plan de entrenamiento personalizado basado en los resultados de este perfil.
    """)
    st.write("Aquí se mostrará el cuestionario cuando esté listo.")

# Sección Inicio
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

    Cuento con una Maestría en Fuerza y Acondicionamiento por el *Football Science Institute, una Licenciatura en Ciencias del Ejercicio por la **Universidad Autónoma de Nuevo León (UANL)* y un intercambio académico internacional en la *Universidad de Sevilla. Durante mi carrera, fui miembro del **Programa de Talento Universitario de la UANL, una distinción que reconoce a estudiantes de excelencia académica y extracurricular. Además, adquirí experiencia clave en el **Laboratorio de Rendimiento Humano de la UANL*, colaborando en evaluaciones avanzadas de fuerza, biomecánica y acondicionamiento físico con tecnologías innovadoras.

    Mi trayectoria ha sido reconocida con distinciones como el *Premio al Mérito Académico de la UANL, el **Primer Lugar de Generación* en la Facultad de Organización Deportiva y una *beca completa para un intercambio internacional* en la Universidad de Sevilla. Estos logros reflejan mi compromiso con la excelencia académica y profesional.

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

# Sección Servicios
def servicios():
    st.title("Servicios")
    st.write("""
    **MUPAI** ofrece una amplia gama de servicios personalizados basados en ciencia del ejercicio:
    - Planes de entrenamiento individualizados.
    - Programas de mejora física y mental.
    - Asesoría en nutrición deportiva.
    - Consultoría en rendimiento deportivo.
    """)

# Sección Contacto
def contacto():
    st.title("Contacto")
    st.write("""
    Para más información o consultas, contáctanos:
    - **Correo**: contacto@mupai.com  
    - **Teléfono**: +52 866 258 05 94  
    - **Ubicación**: Monterrey, Nuevo León  
    """)

# Panel de administración
def administrar_usuarios():
    st.subheader("Administrar Usuarios Pendientes")
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        pending_users = cursor.execute("SELECT id, username FROM users WHERE authorized=0").fetchall()

    if pending_users:
        st.write("Usuarios pendientes de autorización:")
        for user in pending_users:
            if st.button(f"Autorizar a {user[1]}", key=user[0]):
                authorize_user(user[0])
                st.success(f"Usuario {user[1]} autorizado.")
    else:
        st.write("No hay usuarios pendientes de autorización.")

# Main function
def main():
    init_db()

    st.sidebar.title("Navegación")
    menu = ["Inicio", "Sobre Mí", "Servicios", "Contacto", "Perfil MUPAI/Salud y Rendimiento", "Administrar Usuarios"]

    user = None
    st.sidebar.title("Registro / Login")
    choice = st.sidebar.selectbox("¿Qué quieres hacer?", ["Registro", "Login"])
    if choice == "Registro":
        username = st.sidebar.text_input("Usuario")
        password = st.sidebar.text_input("Contraseña", type="password")
        if st.sidebar.button("Registrar"):
            if register_user(username, password):
                st.sidebar.success("Usuario registrado con éxito. Espera autorización.")
            else:
                st.sidebar.error("El usuario ya existe.")
    elif choice == "Login":
        username = st.sidebar.text_input("Usuario")
        password = st.sidebar.text_input("Contraseña", type="password")
        if st.sidebar.button("Login"):
            user = login_user(username, password)
            if user and user[3] == 1:
                st.sidebar.success(f"Bienvenido, {user[1]}.")
                menu.append("Exclusivo")
            elif user:
                st.sidebar.warning("No autorizado.")
            else:
                st.sidebar.error("Usuario o contraseña incorrectos.")

    selected_menu = st.sidebar.radio("Ir a:", menu)

    if selected_menu == "Inicio":
        inicio()
    elif selected_menu == "Sobre Mí":
        sobre_mi()
    elif selected_menu == "Servicios":
        servicios()
    elif selected_menu == "Contacto":
        contacto()
    elif selected_menu == "Perfil MUPAI/Salud y Rendimiento":
        perfil_mupai()
    elif selected_menu == "Administrar Usuarios":
        administrar_usuarios()
    elif selected_menu == "Exclusivo" and user and user[3] == 1:
        funcionalidad_exclusiva()

if __name__ == "__main__":
    main()
