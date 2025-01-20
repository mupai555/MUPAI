import streamlit as st
import sqlite3

# Configuración inicial de la página
st.set_page_config(
    page_title="MUPAI - Entrenamiento Digital",
    page_icon="🤖",
    layout="wide",
)

# Configuración de la base de datos
def init_db():
    conn = sqlite3.connect('users.db')
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
    conn.close()

# Guardar un usuario nuevo en la base de datos
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

# Verificar login
def login_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    user = cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
    conn.close()
    return user

# Autorizar usuario manualmente
def authorize_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET authorized=1 WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

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
    Soy Erick Francisco De Luna Hernández, un profesional apasionado por el fitness y las ciencias del ejercicio, con una sólida formación académica y amplia experiencia en el diseño de metodologías de entrenamiento basadas en ciencia.
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
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    pending_users = cursor.execute("SELECT id, username FROM users WHERE authorized=0").fetchall()
    conn.close()

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
    menu = st.sidebar.radio(
        "Ir a:",
        ["Inicio", "Sobre Mí", "Servicios", "Contacto", "Administrar Usuarios"]
    )

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
            elif user:
                st.sidebar.warning("No autorizado.")
            else:
                st.sidebar.error("Usuario o contraseña incorrectos.")

    if menu == "Inicio":
        inicio()
    elif menu == "Sobre Mí":
        sobre_mi()
    elif menu == "Servicios":
        servicios()
    elif menu == "Contacto":
        contacto()
    elif menu == "Administrar Usuarios":
        administrar_usuarios()

if __name__ == "__main__":
    main()
