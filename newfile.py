import streamlit as st
import sqlite3

# Configuración inicial de la página
st.set_page_config(
    page_title="Sistema de Entrenamiento y Nutrición Personalizado",
    page_icon="🤖",
    layout="wide",
)

# Configuración inicial de la base de datos
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
    st.title("Inicio")
    st.image("LOGO.png", use_container_width=True)
    st.header("Misión")
    st.write("""
    Hacer accesible el entrenamiento basado en ciencia, proporcionando planes personalizados respaldados por datos precisos y tecnología avanzada.
    """)
    st.header("Visión")
    st.write("""
    Convertirnos en referentes globales en entrenamiento digital personalizado, integrando ciencia e innovación para mejorar el bienestar físico y mental.
    """)
    st.header("Política")
    st.write("""
    En **MUPAI**, nuestra política se basa en excelencia, ética y accesibilidad, promoviendo un enfoque integral de bienestar para todos nuestros usuarios.
    """)

# Sección Sobre Mí
def sobre_mi():
    st.title("Sobre Mí")
    st.write("""
    Soy Erick Francisco De Luna Hernández, un profesional apasionado por el fitness y las ciencias del ejercicio, con experiencia académica y práctica en rendimiento físico.
    """)
    st.subheader("Galería de Imágenes")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("imagen1.jpg", use_container_width=True)
    with col2:
        st.image("imagen2.jpg", use_container_width=True)
    with col3:
        st.image("imagen3.jpg", use_container_width=True)

# Sección Servicios
def servicios():
    st.title("Servicios")
    st.write("""
    - **Planes de entrenamiento personalizados.**
    - **Asesoría en nutrición deportiva.**
    - **Consultoría en rendimiento físico.**
    """)

# Sección Contacto
def contacto():
    st.title("Contacto")
    st.write("""
    **Correo:** contacto@mupai.com  
    **Teléfono:** +52 866 258 05 94  
    **Ubicación:** Monterrey, Nuevo León
    """)

# Sección Perfil MUPAI - Fitness-Performance-Health
def perfil_mupai(user):
    st.title("Perfil MUPAI - Fitness-Performance-Health")
    if user and user[3] == 1:  # Solo usuarios autorizados
        st.write("""
        Bienvenido al cuestionario **Perfil MUPAI - Fitness-Performance-Health**. Este cuestionario recopilará información sobre:
        - Calidad del sueño.
        - Nivel de estrés percibido.
        - Hábitos alimenticios.
        - Nivel de entrenamiento.
        - Composición corporal.
        
        Próximamente, esta información será utilizada para generar automáticamente planes de entrenamiento y nutrición personalizados.
        """)
    else:
        st.warning("No tienes acceso a esta sección. Por favor, espera autorización.")

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
    # Inicializar la base de datos
    init_db()

    # Sidebar para navegación
    st.sidebar.title("Navegación")
    menu = st.sidebar.radio("Ir a:", ["Inicio", "Sobre Mí", "Servicios", "Contacto", "Perfil MUPAI - Fitness-Performance-Health", "Administrar Usuarios"])

    # Registro/Login
    st.sidebar.title("Registro / Login")
    choice = st.sidebar.selectbox("¿Qué quieres hacer?", ["Registro", "Login"])

    user = None
    if choice == "Registro":
        st.sidebar.subheader("Registro de Usuario")
        username = st.sidebar.text_input("Usuario")
        password = st.sidebar.text_input("Contraseña", type="password")
        if st.sidebar.button("Registrar"):
            if register_user(username, password):
                st.sidebar.success("Usuario registrado con éxito. Espera autorización.")
            else:
                st.sidebar.error("El usuario ya existe. Intenta con otro nombre.")
    elif choice == "Login":
        st.sidebar.subheader("Iniciar Sesión")
        username = st.sidebar.text_input("Usuario")
        password = st.sidebar.text_input("Contraseña", type="password")
        if st.sidebar.button("Login"):
            user = login_user(username, password)
            if user:
                if user[3] == 1:
                    st.sidebar.success(f"Bienvenido, {user[1]}.")
                else:
                    st.sidebar.warning("No estás autorizado aún. Por favor, espera aprobación.")
            else:
                st.sidebar.error("Usuario o contraseña incorrectos.")

    # Navegación principal
    if menu == "Inicio":
        inicio()
    elif menu == "Sobre Mí":
        sobre_mi()
    elif menu == "Servicios":
        servicios()
    elif menu == "Contacto":
        contacto()
    elif menu == "Perfil MUPAI - Fitness-Performance-Health":
        perfil_mupai(user)
    elif menu == "Administrar Usuarios":
        administrar_usuarios()

if __name__ == "__main__":
    main()
