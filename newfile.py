import streamlit as st
import base64

# Configuración de la página
st.set_page_config(
    page_title="MUPAI - Entrenamiento Científico",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta de colores
PRIMARY_COLOR = "#FFD700"  # Amarillo
SECONDARY_COLOR = "#000000"  # Negro
BACKGROUND_COLOR = "#FFFFFF"  # Blanco

# URL de imágenes
LOGO_URL = "https://raw.githubusercontent.com/mupai5/MUPAI/main/LOGO.png"
GYM_IMAGE_URL = "https://raw.githubusercontent.com/mupai5/MUPAI/main/20250116_074233_0000.png"

# Estilos CSS simplificados
def aplicar_estilos():
    st.markdown(f"""
    <style>
    /* Estilos generales */
    body {{
        background-color: {BACKGROUND_COLOR};
        color: #333;
        font-family: Arial, sans-serif;
    }}
    
    .stApp {{
        background-color: {BACKGROUND_COLOR};
    }}
    
    /* Barra lateral */
    [data-testid="stSidebar"] {{
        background-color: {SECONDARY_COLOR} !important;
        color: white;
    }}
    
    /* Títulos */
    h1, h2, h3 {{
        color: {SECONDARY_COLOR};
    }}
    
    h1 {{
        border-bottom: 3px solid {PRIMARY_COLOR};
        padding-bottom: 10px;
    }}
    
    /* Tarjetas */
    .card {{
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 5px solid {PRIMARY_COLOR};
    }}
    
    /* Hero Section */
    .hero {{
        background: linear-gradient(135deg, {SECONDARY_COLOR} 0%, #333333 100%);
        color: white;
        padding: 4rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }}
    
    .hero::before {{
        content: "";
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 200%;
        background: radial-gradient(circle, {PRIMARY_COLOR} 0%, transparent 70%);
        opacity: 0.15;
        z-index: 0;
    }}
    
    .hero-content {{
        position: relative;
        z-index: 1;
    }}
    
    /* Imágenes */
    .hero-logo {{
        max-width: 300px;
        margin: 0 auto 20px;
    }}
    
    .imagen-principal {{
        width: 100%;
        border-radius: 10px;
        margin-bottom: 25px;
        border: 3px solid {PRIMARY_COLOR};
    }}
    
    .profile-img {{
        border-radius: 50%;
        border: 5px solid {PRIMARY_COLOR};
        width: 200px;
        height: 200px;
        object-fit: cover;
        margin: 0 auto;
        display: block;
    }}
    
    .footer-logo {{
        max-width: 200px;
        margin: 20px auto;
    }}
    
    /* Logo en sobre mí */
    .logo-sobre-mi {{
        position: absolute;
        top: 20px;
        right: 20px;
        width: 120px;
        z-index: 10;
    }}
    
    /* Footer */
    .footer {{
        background-color: {SECONDARY_COLOR};
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 3rem;
    }}
    
    /* Responsive */
    @media (max-width: 768px) {{
        .logo-sobre-mi {{
            position: static;
            width: 100px;
            margin: 0 auto 20px;
            text-align: center;
        }}
        
        .hero-logo {{
            max-width: 200px;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

# Página de Inicio
def pagina_inicio():
    # Hero section con logo
    st.markdown(f"""
    <div class='hero'>
        <div class='hero-content'>
            <img src="{LOGO_URL}" alt="MUPAI Logo" class="hero-logo">
            <h1 style='color:white; font-size:2.5rem;'>Digital Training Science</h1>
            <p style='font-size:1.5rem;color:white;'>Ciencia aplicada al rendimiento humano</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Misión, Visión y Valores
    st.header("Nuestra Identidad")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='card'>
            <h3>🌟 Misión</h3>
            <p>Hacer accesible el entrenamiento basado en ciencia, proporcionando planes completamente 
            personalizados a través de herramientas digitales respaldadas por inteligencia artificial, 
            datos precisos y la investigación más actualizada en ciencias del ejercicio.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='card'>
            <h3>💎 Valores</h3>
            <ul>
                <li><strong>Ciencia:</strong> Base en evidencia científica</li>
                <li><strong>Personalización:</strong> Soluciones individualizadas</li>
                <li><strong>Innovación:</strong> Tecnología de vanguardia</li>
                <li><strong>Ética:</strong> Transparencia y responsabilidad</li>
                <li><strong>Excelencia:</strong> Compromiso con la calidad</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='card'>
            <h3>🌍 Visión</h3>
            <p>Convertirnos en referente global en entrenamiento digital personalizado, aprovechando 
            nuevas tecnologías para hacer accesible el fitness basado en ciencia.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='card'>
            <h3>📜 Política</h3>
            <p>En MUPAI, nuestra política está fundamentada en el compromiso con la excelencia, 
            ética y servicio centrado en el usuario.</p>
            
            <h4>📘 Política del Servicio</h4>
            <ul>
                <li>Diseñamos entrenamientos digitales personalizados basados en ciencia</li>
                <li>Ofrecemos servicio accesible y adaptable a necesidades individuales</li>
                <li>Respetamos y protegemos la privacidad de datos personales</li>
                <li>Innovamos continuamente para mejorar experiencia y resultados</li>
                <li>Promovemos valores como esfuerzo, constancia y respeto</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Servicios destacados
    st.header("Nuestros Servicios")
    
    servicios = [
        ("💪 Evaluación Corporal", "Análisis de composición corporal y potencial genético"),
        ("😌 Gestión del Estrés", "Evaluación y manejo científico del estrés"),
        ("🌙 Calidad del Sueño", "Optimización de patrones de descanso"),
        ("🏃 Planes de Entrenamiento", "Programas personalizados basados en ciencia"),
        ("🍎 Asesoría Nutricional", "Planes alimenticios para tus objetivos"),
        ("📊 Seguimiento Continuo", "Monitoreo y ajuste de tu progreso")
    ]
    
    cols = st.columns(3)
    for i, (titulo, desc) in enumerate(servicios):
        with cols[i % 3]:
            st.markdown(f"""
            <div class='card'>
                <h3>{titulo}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

# Página "Sobre Mí"
def pagina_sobre_mi():
    st.markdown(f"""
    <div class="logo-sobre-mi">
        <img src="{LOGO_URL}" alt="Logo MUPAI">
    </div>
    """, unsafe_allow_html=True)
    
    st.header("👤 Sobre Mí - Erick Francisco De Luna Hernández")
    
    # Imagen principal del gimnasio
    st.markdown(f"""
    <div style="text-align:center; margin: 20px 0 30px;">
        <img src="{GYM_IMAGE_URL}" alt="MUSCLE UP GYM" class="imagen-principal">
        <h3>MUSCLE UP GYM</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Descripción
    st.markdown("""
    <div class="card">
        <p>Soy Erick Francisco De Luna Hernández, profesional apasionado por el fitness y ciencias del ejercicio. 
        Actualmente me desempeño en Muscle Up GYM, donde diseño programas de entrenamiento basados en evidencia científica, 
        creando metodologías personalizadas que optimizan el rendimiento físico y promueven el bienestar integral.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Perfil con foto
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style="text-align:center;">
            <img src="https://via.placeholder.com/300x300/000000/FFFFFF?text=FOTO+PERFIL" 
                 alt="Erick De Luna" class="profile-img">
            <h3>Erick Francisco De Luna Hernández</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>Formación Académica</h3>
            <ul>
                <li>🎓 Maestría en Fuerza y Acondicionamiento - Football Science Institute</li>
                <li>📚 Licenciatura en Ciencias del Ejercicio - UANL</li>
                <li>🌍 Intercambio académico - Universidad de Sevilla</li>
            </ul>
        </div>
        
        <div class="card">
            <h3>Experiencia Profesional</h3>
            <ul>
                <li>💼 Diseñador de metodologías de entrenamiento - Muscle Up Gym</li>
                <li>🔬 Investigador en Laboratorio de Rendimiento Humano - UANL</li>
                <li>👨‍🏫 Asesor científico - Atletas de alto rendimiento</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Logros y reconocimientos
    st.header("🏆 Logros y Reconocimientos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>Premios Académicos</h3>
            <ul>
                <li>🥇 Premio al Mérito Académico UANL</li>
                <li>🏅 Primer Lugar de Generación</li>
                <li>🎖️ Beca completa para intercambio internacional</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>Publicaciones y Contribuciones</h3>
            <ul>
                <li>📄 Métodos innovadores en entrenamiento deportivo</li>
                <li>📊 Análisis de rendimiento físico avanzado</li>
                <li>🤖 Desarrollo de herramientas digitales para fitness</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Filosofía profesional
    st.header("🧠 Filosofía Profesional")
    st.markdown("""
    <div class="card">
        <p>"Creo firmemente en el poder transformador del entrenamiento basado en evidencia científica. 
        Mi enfoque combina rigor metodológico con personalización individual, reconociendo que cada 
        persona tiene necesidades y objetivos únicos. A través de MUPAI, busco democratizar 
        el acceso a metodologías de entrenamiento de elite."</p>
    </div>
    """, unsafe_allow_html=True)

# Página de contacto
def pagina_contacto():
    st.header("📞 Contáctanos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>Información de Contacto</h3>
            <p>📧 <strong>Email:</strong> contacto@mupai.com</p>
            <p>📱 <strong>Teléfono:</strong> +52 866 258 05 94</p>
            <p>📍 <strong>Ubicación:</strong> Monterrey, Nuevo León, México</p>
            
            <h3>Horario de Atención</h3>
            <p>Lunes a Viernes: 9:00 - 18:00</p>
            <p>Sábados: 10:00 - 14:00</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        with st.form("form_contacto", clear_on_submit=True):
            st.markdown("### ✉️ Envíanos un mensaje")
            nombre = st.text_input("Nombre completo*", placeholder="Tu nombre completo")
            email = st.text_input("Correo electrónico*", placeholder="tu@email.com")
            telefono = st.text_input("Teléfono", placeholder="+52 123 456 7890")
            asunto = st.selectbox("Asunto*", ["Consulta general", "Servicios", "Colaboraciones", "Soporte técnico", "Otros"])
            mensaje = st.text_area("Mensaje*", placeholder="Escribe tu mensaje aquí...", height=150)
            
            st.markdown("**\* Campos obligatorios**")
            
            if st.form_submit_button("Enviar mensaje", type="primary"):
                if nombre and email and mensaje:
                    st.success("¡Mensaje enviado con éxito! Nos pondremos en contacto contigo pronto.")
                else:
                    st.error("Por favor completa todos los campos obligatorios")

# Pie de página
def mostrar_footer():
    st.markdown(f"""
    <div class="footer">
        <img src="{LOGO_URL}" alt="MUPAI Logo" class="footer-logo">
        <p style="font-size:1.2rem; margin-bottom:10px;">© 2023 <strong style="color:#FFD700;">MUPAI Digital Training Science</strong></p>
        <p style="margin:0;">Todos los derechos reservados | Ciencia aplicada al rendimiento humano</p>
    </div>
    """, unsafe_allow_html=True)

# Menú de navegación
def mostrar_menu():
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center; padding:20px 0;">
            <img src="{LOGO_URL}" alt="MUPAI Logo" style="max-width:200px; margin-bottom:20px;">
        </div>
        """, unsafe_allow_html=True)
        
        menu = st.radio(
            "Menú de Navegación",
            ["🏠 Inicio", "👤 Sobre Mí", "📞 Contacto"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align:center; padding:10px; background-color:#FFD720; border-radius:8px;">
            <p style="color:#000; margin:0; font-weight:bold;">¡Próximamente!</p>
            <p style="color:#000; margin:0;">Evaluaciones científicas</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align:center; color:#fff; font-size:0.9rem;">
            <p>MUPAI Digital Training Science</p>
            <p>Ciencia aplicada al rendimiento humano</p>
        </div>
        """, unsafe_allow_html=True)
        
        return menu

# Función principal
def main():
    aplicar_estilos()
    menu = mostrar_menu()
    
    if menu == "🏠 Inicio":
        pagina_inicio()
    elif menu == "👤 Sobre Mí":
        pagina_sobre_mi()
    elif menu == "📞 Contacto":
        pagina_contacto()
    
    mostrar_footer()

if __name__ == "__main__":
    main()
