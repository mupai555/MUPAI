import streamlit as st
import base64

# Configuración de la página
st.set_page_config(
    page_title="MUPAI - Entrenamiento Científico",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta de colores basada en el logo (amarillo tráfico, negro, blanco)
PRIMARY_COLOR = "#FFD700"  # Amarillo tráfico
SECONDARY_COLOR = "#000000"  # Negro
BACKGROUND_COLOR = "#FFFFFF"  # Blanco
TEXT_COLOR = "#333333"  # Gris oscuro para texto
ACCENT_COLOR = "#FFED00"  # Amarillo más claro para acentos

# Aplicar estilos CSS personalizados
def aplicar_estilos():
    st.markdown(f"""
    <style>
    /* Estilos generales */
    .stApp {{
        background-color: {BACKGROUND_COLOR};
        color: {TEXT_COLOR};
        font-family: 'Arial', sans-serif;
    }}
    
    /* Barra lateral */
    [data-testid="stSidebar"] {{
        background-color: {SECONDARY_COLOR} !important;
        color: white;
    }}
    
    /* Botones */
    .stButton>button {{
        background-color: {PRIMARY_COLOR};
        color: {SECONDARY_COLOR};
        border: 2px solid {SECONDARY_COLOR};
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s;
    }}
    
    .stButton>button:hover {{
        background-color: {ACCENT_COLOR};
        transform: scale(1.05);
    }}
    
    /* Títulos */
    h1 {{
        color: {SECONDARY_COLOR};
        border-bottom: 3px solid {PRIMARY_COLOR};
        padding-bottom: 10px;
        margin-bottom: 20px;
    }}
    
    h2 {{
        color: {SECONDARY_COLOR};
        margin-top: 30px;
    }}
    
    h3 {{
        color: {SECONDARY_COLOR};
    }}
    
    /* Widgets */
    .stTextInput>div>div>input, 
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select,
    .stTextArea>div>div>textarea {{
        border: 2px solid {SECONDARY_COLOR} !important;
        border-radius: 8px;
    }}
    
    /* Tarjetas */
    .card {{
        background-color: {BACKGROUND_COLOR};
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 5px solid {PRIMARY_COLOR};
        transition: transform 0.3s, box-shadow 0.3s;
    }}
    
    .card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }}
    
    /* Hero Section */
    .hero {{
        background: linear-gradient(135deg, {SECONDARY_COLOR} 0%, #333333 100%);
        color: white;
        padding: 4rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        text-align: center;
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
    
    /* Animaciones */
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.03); }}
        100% {{ transform: scale(1); }}
    }}
    
    .pulse {{
        animation: pulse 3s infinite;
    }}
    
    /* Secciones */
    .section {{
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        background-color: {BACKGROUND_COLOR};
        border: 1px solid #eee;
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
    
    /* Imágenes */
    .profile-img {{
        border-radius: 50%;
        border: 5px solid {PRIMARY_COLOR};
        width: 200px;
        height: 200px;
        object-fit: cover;
        margin: 0 auto;
        display: block;
    }}
    
    .logo {{
        max-width: 200px;
        margin: 0 auto;
        display: block;
    }}
    </style>
    """, unsafe_allow_html=True)

# Función para mostrar el logo
def mostrar_logo():
    st.markdown(f"""
    <div class="logo-container" style="text-align:center; margin:20px 0;">
        <img src="https://via.placeholder.com/300x100/000000/FFFFFF?text=MUPAI+LOGO" 
             alt="MUPAI Logo" class="logo">
    </div>
    """, unsafe_allow_html=True)

# Página de Inicio
def pagina_inicio():
    st.markdown(f"""
    <div class='hero'>
        <div class='hero-content'>
            <h1 style='color:white; font-size:3rem;'>MUPAI Digital Training Science</h1>
            <p style='font-size:1.5rem;color:white;'>Ciencia aplicada al rendimiento humano</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Misión, Visión y Valores
    st.header("Nuestra Identidad")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown("""
            <div class='card'>
                <h3>🌟 Misión</h3>
                <p>Hacer accesible el entrenamiento basado en ciencia, proporcionando planes completamente 
                personalizados a través de herramientas digitales respaldadas por inteligencia artificial, 
                datos precisos y la investigación más actualizada en ciencias del ejercicio. Nos enfocamos 
                en promover el desarrollo integral de nuestros usuarios y su bienestar físico y mental.</p>
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
        with st.container():
            st.markdown("""
            <div class='card'>
                <h3>🌍 Visión</h3>
                <p>Convertirnos en uno de los máximos referentes a nivel global en entrenamiento digital 
                personalizado, aprovechando las nuevas tecnologías para hacer más accesible el fitness basado 
                en ciencia. Aspiramos a transformar la experiencia del entrenamiento físico, integrando 
                inteligencia artificial, investigación científica y herramientas digitales avanzadas que 
                permitan a cualquier persona alcanzar su máximo potencial.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='card'>
                <h3>📜 Política</h3>
                <p>En <strong>MUPAI</strong>, nuestra política está fundamentada en el compromiso con la 
                excelencia, la ética y el servicio centrado en el usuario. Actuamos con responsabilidad y 
                transparencia para ofrecer soluciones tecnológicas que integren ciencia, personalización y 
                accesibilidad, contribuyendo al bienestar integral de quienes confían en nosotros.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Servicios destacados
    st.header("Nuestros Servicios")
    
    cols = st.columns(3)
    servicios = [
        ("💪 Evaluación Corporal", "Análisis de composición corporal y potencial genético"),
        ("😌 Gestión del Estrés", "Evaluación y manejo científico del estrés"),
        ("🌙 Calidad del Sueño", "Optimización de patrones de descanso"),
        ("🏃 Planes de Entrenamiento", "Programas personalizados basados en ciencia"),
        ("🍎 Asesoría Nutricional", "Planes alimenticios para tus objetivos"),
        ("📊 Seguimiento Continuo", "Monitoreo y ajuste de tu progreso")
    ]
    
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
    st.header("👤 Sobre Mí - Erick Francisco De Luna Hernández")
    
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
                <li>🎓 <strong>Maestría en Fuerza y Acondicionamiento</strong> - Football Science Institute</li>
                <li>📚 <strong>Licenciatura en Ciencias del Ejercicio</strong> - UANL</li>
                <li>🌍 <strong>Intercambio académico</strong> - Universidad de Sevilla</li>
            </ul>
        </div>
        
        <div class="card">
            <h3>Experiencia Profesional</h3>
            <ul>
                <li>💼 <strong>Diseñador de metodologías de entrenamiento</strong> - Muscle Up Gym</li>
                <li>🔬 <strong>Investigador en Laboratorio de Rendimiento Humano</strong> - UANL</li>
                <li>👨‍🏫 <strong>Asesor científico</strong> - Atletas de alto rendimiento</li>
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
                <li>⭐ Miembro del Programa de Talento Universitario UANL</li>
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
                <li>🔍 Estudios sobre composición corporal</li>
                <li>🤖 Desarrollo de herramientas digitales para fitness</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Filosofía profesional
    st.header("🧠 Filosofía Profesional")
    st.markdown("""
    <div class="card">
        <p>"Creo firmemente en el poder transformador del entrenamiento basado en evidencia científica. 
        Mi enfoque combina el rigor metodológico con la personalización individual, reconociendo que cada 
        persona tiene necesidades, capacidades y objetivos únicos. A través de MUPAI, busco democratizar 
        el acceso a metodologías de entrenamiento de elite, haciendo que la ciencia del ejercicio sea 
        accesible para todos."</p>
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
            
            <h3>Redes Sociales</h3>
            <p>📱 Facebook: @MUPAI</p>
            <p>📸 Instagram: @MUPAI</p>
            <p>💼 LinkedIn: MUPAI</p>
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
            
            # Campos obligatorios
            required = st.markdown("**\* Campos obligatorios**")
            
            # Botón de envío
            enviado = st.form_submit_button("Enviar mensaje", type="primary")
            if enviado:
                if nombre and email and mensaje:
                    st.success("¡Mensaje enviado con éxito! Nos pondremos en contacto contigo pronto.")
                else:
                    st.error("Por favor completa todos los campos obligatorios (*)")

# Pie de página
def mostrar_footer():
    st.markdown("""
    <div class="footer">
        <p style="font-size:1.2rem; margin-bottom:10px;">© 2023 <strong style="color:#FFD700;">MUPAI Digital Training Science</strong></p>
        <p style="margin:0;">Todos los derechos reservados | Ciencia aplicada al rendimiento humano</p>
        <div style="margin-top:15px;">
            <a href="#" style="color:#FFD700; margin:0 10px;">Términos de Uso</a> | 
            <a href="#" style="color:#FFD700; margin:0 10px;">Política de Privacidad</a> | 
            <a href="#" style="color:#FFD700; margin:0 10px;">Contacto</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Menú de navegación
def mostrar_menu():
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center; padding:20px 0;">
            <img src="https://via.placeholder.com/150x50/000000/FFFFFF?text=MUPAI" 
                 alt="MUPAI Logo" style="max-width:150px; margin-bottom:20px;">
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
