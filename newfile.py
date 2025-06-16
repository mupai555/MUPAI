import streamlit as st
import base64

# Configuración de la página
st.set_page_config(
    page_title="MUPAI - Entrenamiento Digital",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="auto"
)

# CSS profesional y responsivo
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Variables CSS para colores */
    :root {
        --primary-color: #2E86AB;
        --secondary-color: #A23B72;
        --accent-color: #F18F01;
        --success-color: #3CB371;
        --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --card-shadow: 0 10px 30px rgba(0,0,0,0.1);
        --border-radius: 15px;
    }
    
    /* Header principal */
    .main-header {
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(45deg, #2E86AB, #A23B72);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 2rem 0;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2E86AB 0%, #A23B72 100%);
    }
    
    .css-1d391kg .css-1v0mbdj {
        color: white;
    }
    
    /* Cards modernas */
    .modern-card {
        background: white;
        padding: 2rem;
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
        margin: 1rem 0;
        border: 1px solid rgba(46, 134, 171, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .modern-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .gradient-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .gradient-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        transform: translateX(-100%);
        transition: transform 0.6s;
    }
    
    .gradient-card:hover::before {
        transform: translateX(100%);
    }
    
    /* Service cards */
    .service-card {
        background: white;
        padding: 2rem;
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
        margin: 1rem 0;
        border-left: 5px solid var(--primary-color);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .service-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 50px rgba(46, 134, 171, 0.2);
        border-left-width: 8px;
    }
    
    .service-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        color: var(--primary-color);
    }
    
    /* Metrics styling */
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
        text-align: center;
        margin: 0.5rem;
        border-top: 4px solid var(--accent-color);
        transition: transform 0.3s ease;
    }
    
    .metric-container:hover {
        transform: scale(1.05);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        font-weight: 500;
    }
    
    /* About section */
    .about-hero {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 3rem;
        border-radius: var(--border-radius);
        text-align: center;
        margin: 2rem 0;
        position: relative;
    }
    
    .profile-section {
        background: white;
        padding: 2rem;
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
        margin: 1rem 0;
        border-left: 5px solid var(--success-color);
    }
    
    /* Contact form */
    .contact-container {
        background: white;
        padding: 2rem;
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
        margin: 1rem 0;
    }
    
    .contact-info-card {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
        padding: 2rem;
        border-radius: var(--border-radius);
        text-align: center;
        box-shadow: var(--card-shadow);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .modern-card, .gradient-card, .service-card {
            padding: 1.5rem;
            margin: 0.5rem 0;
        }
        
        .metric-container {
            padding: 1rem;
            margin: 0.25rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
        
        .about-hero {
            padding: 2rem;
        }
    }
    
    /* Navigation improvements */
    .nav-header {
        background: linear-gradient(90deg, #2E86AB, #A23B72);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
        font-weight: 600;
    }
    
    /* Loading animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f0f2f6;
        border-radius: 10px;
        color: #2E86AB;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #2E86AB, #A23B72);
        color: white;
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: var(--border-radius);
        text-align: center;
        margin-top: 3rem;
    }
    
    /* Image gallery */
    .image-container {
        border-radius: var(--border-radius);
        overflow: hidden;
        box-shadow: var(--card-shadow);
        transition: transform 0.3s ease;
        margin: 0.5rem 0;
    }
    
    .image-container:hover {
        transform: scale(1.02);
    }
    
    /* Form styling */
    .stButton > button {
        background: linear-gradient(90deg, #2E86AB, #A23B72);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(46, 134, 171, 0.3);
    }
    
    /* Questionnaire cards */
    .questionnaire-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 3rem;
        border-radius: var(--border-radius);
        text-align: center;
        box-shadow: var(--card-shadow);
        margin: 2rem 0;
    }
    
    .coming-soon {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        color: #2d3436;
        padding: 2rem;
        border-radius: var(--border-radius);
        text-align: center;
        margin: 1rem 0;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Función para crear métricas personalizadas
def create_metric_card(icon, value, label, delta=None):
    delta_html = f'<div style="color: #28a745; font-size: 0.8rem; margin-top: 0.5rem;">📈 {delta}</div>' if delta else ''
    return f"""
    <div class="metric-container animate-fade-in">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {delta_html}
    </div>
    """

# Barra lateral de navegación mejorada
st.sidebar.markdown('<div class="nav-header">🚀 NAVEGACIÓN MUPAI</div>', unsafe_allow_html=True)

menu_options = {
    "🏠 Inicio": "home",
    "👨‍💼 Sobre Mí": "about", 
    "💼 Servicios": "services",
    "📞 Contacto": "contact",
    "⚖️ Balance Energético": "energy",
    "🍽️ Preferencias Alimenticias": "food",
    "🍰 Control de Antojos": "cravings"
}

menu = st.sidebar.selectbox(
    "Selecciona una sección:",
    list(menu_options.keys()),
    format_func=lambda x: x
)

# Contenido según la selección del menú
if menu == "🏠 Inicio":
    # Hero section
    st.markdown('<div class="main-header animate-fade-in">Bienvenido a MUPAI</div>', unsafe_allow_html=True)
    
    # Logo centrado con contenedor
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("LOGO.png", use_container_width=True)
        except:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 3rem; text-align: center; border-radius: 15px; margin: 2rem 0;">
                <h2>🤖 MUPAI</h2>
                <p>Entrenamiento Digital Personalizado</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Métricas en diseño responsive
    st.markdown("### 📊 Nuestros Números")
    col1, col2, col3, col4 = st.columns(4)
    
    metrics_data = [
        ("🎯", "500+", "Clientes Satisfechos", "En crecimiento"),
        ("📋", "1000+", "Programas Diseñados", "Basados en ciencia"),
        ("🏆", "5+", "Años de Experiencia", "Comprobada"),
        ("🔬", "50+", "Investigaciones", "Aplicadas")
    ]
    
    for i, (icon, value, label, delta) in enumerate(metrics_data):
        with [col1, col2, col3, col4][i]:
            st.markdown(create_metric_card(icon, value, label, delta), unsafe_allow_html=True)

    st.markdown("---")

    # Contenido principal en pestañas mejoradas
    tab1, tab2, tab3 = st.tabs(["🎯 **Misión & Visión**", "📋 **Nuestras Políticas**", "🚀 **¿Por qué MUPAI?**"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="gradient-card animate-fade-in">
                <h2>🎯 Nuestra Misión</h2>
                <p style="font-size: 1.1rem; line-height: 1.6;">
                Hacer accesible el entrenamiento basado en ciencia, proporcionando planes completamente personalizados a través de herramientas digitales respaldadas por inteligencia artificial, datos precisos y la investigación más actualizada en ciencias del ejercicio.
                </p>
                <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px;">
                    <strong>🎯 Enfoque:</strong> Desarrollo integral y bienestar físico-mental
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="gradient-card animate-fade-in">
                <h2>🔮 Nuestra Visión</h2>
                <p style="font-size: 1.1rem; line-height: 1.6;">
                Convertirnos en el referente global en entrenamiento digital personalizado, aprovechando las nuevas tecnologías para hacer más accesible el fitness basado en ciencia.
                </p>
                <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px;">
                    <strong>🚀 Meta:</strong> Transformar la experiencia del entrenamiento físico
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="modern-card animate-fade-in">
            <h2 style="color: #2E86AB; margin-bottom: 1.5rem;">📜 Política Empresarial</h2>
            <p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 2rem;">
            En <strong>MUPAI</strong>, nuestra política está fundamentada en el compromiso con la excelencia, 
            la ética y el servicio centrado en el usuario. Actuamos con responsabilidad y transparencia 
            para ofrecer soluciones tecnológicas que integren ciencia, personalización y accesibilidad.
            </p>
            
            <h3 style="color: #A23B72; margin: 2rem 0 1rem 0;">🛡️ Principios del Servicio</h3>
            <div style="display: grid; gap: 1rem; margin-top: 1.5rem;">
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; border-left: 4px solid #2E86AB;">
                    <strong>🔬 Ciencia y Personalización:</strong> Entrenamientos digitales basados en datos confiables y evidencia científica.
                </div>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; border-left: 4px solid #A23B72;">
                    <strong>💻 Tecnología Accesible:</strong> Servicios adaptables a las necesidades de cada usuario.
                </div>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; border-left: 4px solid #F18F01;">
                    <strong>🔐 Privacidad y Seguridad:</strong> Protección responsable de datos personales.
                </div>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; border-left: 4px solid #3CB371;">
                    <strong>🚀 Innovación Continua:</strong> Mejora constante de experiencia y resultados.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div class="modern-card animate-fade-in">
            <h2 style="color: #2E86AB; text-align: center; margin-bottom: 2rem;">🚀 ¿Por qué elegir MUPAI?</h2>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-top: 2rem;">
                <div style="text-align: center; padding: 1.5rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
                    <h4 style="color: #2E86AB;">IA Avanzada</h4>
                    <p>Algoritmos inteligentes que se adaptan a tu progreso</p>
                </div>
                
                <div style="text-align: center; padding: 1.5rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">📱</div>
                    <h4 style="color: #A23B72;">100% Digital</h4>
                    <p>Acceso desde cualquier dispositivo, en cualquier momento</p>
                </div>
                
                <div style="text-align: center; padding: 1.5rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
                    <h4 style="color: #F18F01;">Personalizado</h4>
                    <p>Planes únicos diseñados específicamente para ti</p>
                </div>
                
                <div style="text-align: center; padding: 1.5rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🔬</div>
                    <h4 style="color: #3CB371;">Basado en Ciencia</h4>
                    <p>Respaldado por la investigación más actualizada</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif menu == "👨‍💼 Sobre Mí":
    # Hero section para About
    st.markdown("""
    <div class="about-hero animate-fade-in">
        <h1>👨‍💼 Erick Francisco De Luna Hernández</h1>
        <p style="font-size: 1.3rem; margin-top: 1rem;">Especialista en Ciencias del Ejercicio y Entrenamiento Digital</p>
        <div style="margin-top: 2rem;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.5rem;">🎓 Maestría en Fuerza</span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.5rem;">🏆 Premio al Mérito</span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.5rem;">🌍 Intercambio Internacional</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Información profesional en pestañas
    tab1, tab2, tab3, tab4 = st.tabs(["🎓 **Formación**", "💼 **Experiencia**", "🏆 **Logros**", "📸 **Galería**"])
    
    with tab1:
        st.markdown("""
        <div class="profile-section animate-fade-in">
            <h3 style="color: #2E86AB; margin-bottom: 1.5rem;">🎓 Formación Académica de Excelencia</h3>
            
            <div style="display: grid; gap: 1.5rem;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 10px;">
                    <h4>🏅 Maestría en Fuerza y Acondicionamiento</h4>
                    <p><strong>Football Science Institute</strong></p>
                    <p style="margin-top: 0.5rem; opacity: 0.9;">Especialización avanzada en metodologías de entrenamiento científico</p>
                </div>
                
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 1.5rem; border-radius: 10px;">
                    <h4>🎓 Licenciatura en Ciencias del Ejercicio</h4>
                    <p><strong>Universidad Autónoma de Nuevo León (UANL)</strong></p>
                    <p style="margin-top: 0.5rem; opacity: 0.9;">Fundamentos sólidos en fisiología, biomecánica y metodología del entrenamiento</p>
                </div>
                
                <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 1.5rem; border-radius: 10px;">
                    <h4>🌍 Intercambio Académico Internacional</h4>
                    <p><strong>Universidad de Sevilla, España</strong></p>
                    <p style="margin-top: 0.5rem; opacity: 0.9;">Experiencia internacional en metodologías europeas de entrenamiento</p>
                </div>
                
                <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; padding: 1.5rem; border-radius: 10px;">
                    <h4>⭐ Programa de Talento Universitario</h4>
                    <p><strong>UANL - Estudiante de Excelencia</strong></p>
                    <p style="margin-top: 0.5rem; opacity: 0.9;">Reconocimiento a la excelencia académica y extracurricular</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="profile-section animate-fade-in">
            <h3 style="color: #A23B72; margin-bottom: 1.5rem;">💼 Trayectoria Profesional</h3>
            
            <div style="position: relative; padding-left: 2rem;">
                <div style="position: absolute; left: 0; top: 0; bottom: 0; width: 3px; background: linear-gradient(180deg, #2E86AB, #A23B72);"></div>
                
                <div style="margin-bottom: 2rem; position: relative;">
                    <div style="position: absolute; left: -1.75rem; top: 0.5rem; width: 1rem; height: 1rem; background: #2E86AB; border-radius: 50%;"></div>
                    <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 4px solid #2E86AB;">
                        <h4 style="color: #2E86AB; margin-bottom: 0.5rem;">🏋️ Muscle Up Gym</h4>
                        <p style="color: #666; margin-bottom: 0.5rem;"><strong>Diseñador de Programas de Entrenamiento</strong></p>
                        <p>Desarrollo de metodologías personalizadas basadas en evidencia científica para optimización del rendimiento físico y bienestar integral.</p>
                    </div>
                </div>
                
                <div style="margin-bottom: 2rem; position: relative;">
                    <div style="position: absolute; left: -1.75rem; top: 0.5rem; width: 1rem; height: 1rem; background: #A23B72; border-radius: 50%;"></div>
                    <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 4px solid #A23B72;">
                        <h4 style="color: #A23B72; margin-bottom: 0.5rem;">🔬 Laboratorio de Rendimiento Humano</h4>
                        <p style="color: #666; margin-bottom: 0.5rem;"><strong>Universidad Autónoma de Nuevo León</strong></p>
                        <p>Evaluaciones avanzadas de fuerza, biomecánica y acondicionamiento físico utilizando tecnologías de vanguardia.</p>
                    </div>
                </div>
                
                <div style="position: relative;">
                    <div style="position: absolute; left: -1.75rem; top: 0.5rem; width: 1rem; height: 1rem; background: #F18F01; border-radius: 50%;"></div>
                    <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 4px solid #F18F01;">
                        <h4 style="color: #F18F01; margin-bottom: 0.5rem;">🎯 Especialización en MUPAI</h4>
                        <p style="color: #666; margin-bottom: 0.5rem;"><strong>Fundador y Director Técnico</strong></p>
                        <p>Desarrollo de plataforma digital para entrenamiento personalizado basado en IA y ciencias del ejercicio.</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div class="profile-section animate-fade-in">
            <h3 style="color: #3CB371; margin-bottom: 1.5rem;">🏆 Reconocimientos y Logros</h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
                <div style="background: linear-gradient(135deg, #FFD700, #FFA500); color: white; padding: 2rem; border-radius: 15px; text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🥇</div>
                    <h4>Premio al Mérito Académico</h4>
                    <p style="margin-top: 1rem; opacity: 0.9;">Universidad Autónoma de Nuevo León</p>
                </div>
                
                <div style="background: linear-gradient(135deg, #32CD32, #228B22); color: white; padding: 2rem; border-radius: 15px; text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🎖️</div>
                    <h4>Primer Lugar de Generación</h4>
                    <p style="margin-top: 1rem; opacity: 0.9;">Facultad de Organización Deportiva</p>
                </div>
                
                <div style="background: linear-gradient(135deg, #4169E1, #0000CD); color: white; padding: 2rem; border-radius: 15px; text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🌍</div>
                    <h4>Beca Internacional Completa</h4>
                    <p style="margin-top: 1rem; opacity: 0.9;">Intercambio en Universidad de Sevilla</p>
                </div>
            </div>
            
            <div style="margin-top: 2rem; background: #f8f9fa; padding: 2rem; border-radius: 15px; border-left: 5px solid #3CB371;">
                <h4 style="color: #3CB371; margin-bottom: 1rem;">📊 Impacto Profesional</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; text-align: center;">
                    <div>
                        <div style="font-size: 2rem; color: #2E86AB; font-weight: bold;">500+</div>
                        <div style="color: #666;">Clientes Atendidos</div>
                    </div>
                    <div>
                        <div style="font-size: 2rem; color: #A23B72; font-weight: bold;">1000+</div>
                        <div style="color: #666;">Programas Diseñados</div>
                    </div>
                    <div>
                        <div style="font-size: 2rem; color: #F18F01; font-weight: bold;">50+</div>
                        <div style="color: #666;">Investigaciones</div>
                    </div>
                    <div>
                        <div style="font-size: 2rem; color: #3CB371; font-weight: bold;">5+</div>
                        <div style="color: #666;">Años Experiencia</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<h3 style="color: #2E86AB; text-align: center; margin-bottom: 2rem;">📸 Galería Profesional</h3>', unsafe_allow_html=True)
        
        images = [
            "FB_IMG_1734820693317.jpg",
            "FB_IMG_1734820729323.jpg", 
            "FB_IMG_1734820709707.jpg",
            "FB_IMG_1734820808186.jpg",
            "FB_IMG_1734820712642.jpg"
        ]
        
        # Galería responsive mejorada
        for i in range(0, len(images), 3):
            cols = st.columns(3)
            for j, col in enumerate(cols):
                if i + j < len(images):
                    with col:
                        st.markdown('<div class="image-container">', unsafe_allow_html=True)
                        try:
                            st.image(images[i + j], use_container_width=True, caption=f"Momento profesional {i + j + 1}")
                        except:
                            st.markdown("""
                            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                        color: white; padding: 3rem; text-align: center; border-radius: 15px;">
                                <div style="font-size: 3rem; margin-bottom: 1rem;">📸</div>
                                <p>Imagen no disponible</p>
                            </div>
                            """, unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

elif menu == "💼 Servicios":
    st.markdown("""
    <div class="main-header animate-fade-in" style="font-size: 3rem;">💼 Nuestros Servicios</div>
    <div style="text-align: center; margin-bottom: 3rem;">
        <p style="font-size: 1.2rem; color: #666;">Soluciones integrales de entrenamiento digital basadas en ciencia</p>
    </div>
    """, unsafe_allow_html=True)
    
    services = [
        {
            "icon": "🎯",
            "title": "Planes de Entrenamiento Personalizados",
            "description": "Programas únicos diseñados con IA avanzada, adaptados a tu nivel, objetivos y disponibilidad de tiempo.",
            "features": ["Análisis biomecánico", "Progresión automática", "Seguimiento en tiempo real", "Ajustes dinámicos"],
            "color": "#2E86AB"
        },
        {
            "icon": "🧠",
            "title": "Bienestar Integral Físico-Mental", 
            "description": "Enfoque holístico que combina entrenamiento físico con técnicas de mindfulness y gestión del estrés.",
            "features": ["Meditación guiada", "Técnicas de respiración", "Manejo del estrés", "Equilibrio vida-deporte"],
            "color": "#A23B72"
        },
        {
            "icon": "🥗",
            "title": "Nutrición Deportiva Inteligente",
            "description": "Planes nutricionales personalizados basados en tu metabolismo, actividad física y objetivos específicos.",
            "features": ["Cálculo metabólico", "Macros personalizados", "Recetas adaptadas", "Suplementación opcional"],
            "color": "#F18F01"
        },
        {
            "icon": "📊",
            "title": "Análisis de Rendimiento Avanzado",
            "description": "Evaluaciones completas utilizando tecnología de vanguardia para optimizar tu progreso deportivo.",
            "features": ["Métricas avanzadas", "Reportes detallados", "Comparativas temporales", "Predicciones de progreso"],
            "color": "#3CB371"
        }
    ]
    
    # Mostrar servicios en grid responsivo
    for i in range(0, len(services), 2):
        col1, col2 = st.columns(2)
        cols = [col1, col2]
        
        for j in range(2):
            if i + j < len(services):
                service = services[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div class="service-card animate-fade-in">
                        <div class="service-icon">{service['icon']}</div>
                        <h3 style="color: {service['color']}; margin-bottom: 1rem;">{service['title']}</h3>
                        <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 1.5rem;">{service['description']}</p>
                        
                        <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin-top: 1rem;">
                            <h4 style="color: {service['color']}; margin-bottom: 0.5rem;">✨ Características:</h4>
                            <ul style="margin: 0; padding-left: 1rem;">
                                {"".join(f"<li style='margin: 0.25rem 0;'>{feature}</li>" for feature in service['features'])}
                            </ul>
                        </div>
                        
                        <div style="text-align: center; margin-top: 1.5rem;">
                            <span style="background: {service['color']}; color: white; padding: 0.5rem 1.5rem; border-radius: 20px; font-weight: 600;">
                                Más Información →
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # Sección de proceso
    st.markdown("---")
    st.markdown("""
    <div class="modern-card animate-fade-in">
        <h2 style="color: #2E86AB; text-align: center; margin-bottom: 2rem;">🚀 Nuestro Proceso</h2>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; margin-top: 2rem;">
            <div style="text-align: center;">
                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #2E86AB, #A23B72); 
                           border-radius: 50%; margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem; font-weight: bold;">1</div>
                <h4 style="color: #2E86AB;">Evaluación Inicial</h4>
                <p>Análisis completo de tu condición física actual y objetivos</p>
            </div>
            
            <div style="text-align: center;">
                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #A23B72, #F18F01); 
                           border-radius: 50%; margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem; font-weight: bold;">2</div>
                <h4 style="color: #A23B72;">Diseño Personalizado</h4>
                <p>Creación de tu plan único basado en IA y ciencia</p>
            </div>
            
            <div style="text-align: center;">
                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #F18F01, #3CB371); 
                           border-radius: 50%; margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem; font-weight: bold;">3</div>
                <h4 style="color: #F18F01;">Implementación</h4>
                <p>Seguimiento guiado y ajustes en tiempo real</p>
            </div>
            
            <div style="text-align: center;">
                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #3CB371, #2E86AB); 
                           border-radius: 50%; margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem; font-weight: bold;">4</div>
                <h4 style="color: #3CB371;">Optimización</h4>
                <p>Evolución continua basada en tu progreso</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif menu == "📞 Contacto":
    st.markdown("""
    <div class="main-header animate-fade-in" style="font-size: 3rem;">📞 Contacto</div>
    <div style="text-align: center; margin-bottom: 3rem;">
        <p style="font-size: 1.2rem; color: #666;">¿Listo para transformar tu entrenamiento? Contáctanos</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="contact-container animate-fade-in">
            <h3 style="color: #2E86AB; margin-bottom: 1.5rem;">📝 Envíanos un mensaje</h3>
        """, unsafe_allow_html=True)
        
        # Formulario de contacto mejorado
        with st.form("contact_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                name = st.text_input("👤 Nombre completo", placeholder="Tu nombre completo")
            with col_b:
                email = st.text_input("📧 Correo electrónico", placeholder="tu@email.com")
            
            phone = st.text_input("📱 Teléfono", placeholder="+52 123 456 7890 (opcional)")
            
            service = st.selectbox(
                "🎯 Servicio de interés",
                [
                    "Entrenamiento Personalizado",
                    "Nutrición Deportiva", 
                    "Análisis de Rendimiento",
                    "Bienestar Integral",
                    "Consultoría Completa",
                    "Información General"
                ]
            )
            
            urgency = st.select_slider(
                "⚡ Nivel de urgencia",
                options=["Bajo", "Medio", "Alto", "Urgente"],
                value="Medio"
            )
            
            message = st.text_area(
                "💬 Cuéntanos sobre tus objetivos", 
                height=120,
                placeholder="Describe tus objetivos, experiencia previa y cualquier información relevante..."
            )
            
            col_x, col_y, col_z = st.columns([1, 2, 1])
            with col_y:
                submit = st.form_submit_button(
                    "🚀 Enviar Mensaje", 
                    use_container_width=True
                )
            
            if submit:
                if name and email and message:
                    st.success("✅ ¡Mensaje enviado exitosamente! Te contactaremos en las próximas 24 horas.")
                    st.balloons()
                else:
                    st.error("❌ Por favor completa todos los campos obligatorios (Nombre, Email y Mensaje).")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="contact-info-card animate-fade-in">
            <h3>📍 Información de Contacto</h3>
            
            <div style="margin: 2rem 0;">
                <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <strong>📧 Email Principal</strong><br>
                    contacto@mupai.com
                </div>
                
                <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <strong>📱 WhatsApp</strong><br>
                    +52 123 456 7890
                </div>
                
                <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <strong>🏢 Ubicación</strong><br>
                    Monterrey, Nuevo León<br>
                    México
                </div>
                
                <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <strong>🕒 Horarios de Atención</strong><br>
                    Lunes a Viernes: 8:00 - 18:00<br>
                    Sábados: 9:00 - 14:00<br>
                    Domingos: Solo emergencias
                </div>
            </div>
            
            <div style="margin-top: 2rem;">
                <h4>🌐 Síguenos</h4>
                <div style="margin-top: 1rem;">
                    <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.25rem; display: inline-block;">📘 Facebook</span>
                    <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.25rem; display: inline-block;">📸 Instagram</span>
                    <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.25rem; display: inline-block;">🎥 YouTube</span>
                </div>
            </div>
        </div>
        
        <div style="background: white; padding: 1.5rem; border-radius: 15px; margin-top: 1rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
            <h4 style="color: #2E86AB; text-align: center; margin-bottom: 1rem;">⚡ Respuesta Rápida</h4>
            <p style="text-align: center; color: #666;">
                Tiempo promedio de respuesta:<br>
                <strong style="color: #3CB371;">2-4 horas</strong> en horario laboral
            </p>
        </div>
        """, unsafe_allow_html=True)

# Secciones de cuestionarios con diseño profesional
elif menu == "⚖️ Balance Energético":
    st.markdown("""
    <div class="questionnaire-card animate-fade-in">
        <h1>⚖️ Cuestionario de Balance Energético Óptimo</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">Descubre tu metabolismo y necesidades energéticas personalizadas</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="coming-soon">
        <h3>🚧 Próximamente Disponible</h3>
        <p>Estamos desarrollando un sistema avanzado de evaluación metabólica que incluirá:</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="modern-card">
            <h4 style="color: #2E86AB;">🔬 Evaluaciones Incluidas</h4>
            <ul style="line-height: 2;">
                <li>Tasa metabólica basal (TMB)</li>
                <li>Gasto energético total diario</li>
                <li>Análisis de composición corporal</li>
                <li>Eficiencia metabólica</li>
                <li>Adaptaciones hormonales</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="modern-card">
            <h4 style="color: #A23B72;">🎯 Resultados Personalizados</h4>
            <ul style="line-height: 2;">
                <li>Calorías óptimas para tus objetivos</li>
                <li>Distribución de macronutrientes</li>
                <li>Timing nutricional personalizado</li>
                <li>Estrategias de periodización</li>
                <li>Monitoreo de progreso</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif menu == "🍽️ Preferencias Alimenticias":
    st.markdown("""
    <div class="questionnaire-card animate-fade-in">
        <h1>🍽️ Cuestionario de Patrones Alimenticios</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">Analiza tus hábitos y preferencias para una nutrición personalizada</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="coming-soon">
        <h3>🚧 En Desarrollo Avanzado</h3>
        <p>Sistema integral de análisis nutricional personalizado:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tres columnas para mejor distribución
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="modern-card">
            <h4 style="color: #F18F01;">🕒 Patrones Temporales</h4>
            <ul style="line-height: 1.8;">
                <li>Horarios de comida</li>
                <li>Frecuencia alimentaria</li>
                <li>Ventanas de ayuno</li>
                <li>Cronotipos nutricionales</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="modern-card">
            <h4 style="color: #3CB371;">🥗 Preferencias</h4>
            <ul style="line-height: 1.8;">
                <li>Alimentos favoritos</li>
                <li>Restricciones dietéticas</li>
                <li>Intolerancias</li>
                <li>Estilos culinarios</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="modern-card">
            <h4 style="color: #A23B72;">📊 Análisis</h4>
            <ul style="line-height: 1.8;">
                <li>Calidad nutricional</li>
                <li>Diversidad alimentaria</li>
                <li>Hidratación</li>
                <li>Suplementación</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif menu == "🍰 Control de Antojos":
    st.markdown("""
    <div class="questionnaire-card animate-fade-in">
        <h1>🍰 Cuestionario de Control de Antojos</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">Maneja inteligentemente tus impulsos alimentarios</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="coming-soon">
        <h3>🚧 Sistema Avanzado en Desarrollo</h3>
        <p>Tecnología de vanguardia para el manejo de antojos:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid de características
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin: 2rem 0;">
        <div class="modern-card">
            <h4 style="color: #2E86AB;">🧠 Análisis Psicológico</h4>
            <ul style="line-height: 1.8;">
                <li>Triggers emocionales</li>
                <li>Patrones de comportamiento</li>
                <li>Situaciones de riesgo</li>
                <li>Estados de ánimo</li>
            </ul>
        </div>
        
        <div class="modern-card">
            <h4 style="color: #A23B72;">⏰ Análisis Temporal</h4>
            <ul style="line-height: 1.8;">
                <li>Momentos críticos</li>
                <li>Frecuencia de antojos</li>
                <li>Duración e intensidad</li>
                <li>Patrones cíclicos</li>
            </ul>
        </div>
        
        <div class="modern-card">
            <h4 style="color: #F18F01;">🎯 Estrategias</h4>
            <ul style="line-height: 1.8;">
                <li>Técnicas de control</li>
                <li>Alternativas saludables</li>
                <li>Mindful eating</li>
                <li>Recompensas adaptativas</li>
            </ul>
        </div>
        
        <div class="modern-card">
            <h4 style="color: #3CB371;">📈 Seguimiento</h4>
            <ul style="line-height: 1.8;">
                <li>Progreso semanal</li>
                <li>Alertas preventivas</li>
                <li>Reportes detallados</li>
                <li>Ajustes dinámicos</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer mejorado
st.markdown("""
<div class="footer">
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; margin-bottom: 2rem;">
        <div>
            <h4>🤖 MUPAI</h4>
            <p>Entrenamiento Digital del Futuro</p>
        </div>
        <div>
            <h4>🔗 Enlaces Rápidos</h4>
            <p>Inicio • Servicios • Contacto</p>
        </div>
        <div>
            <h4>📞 Contacto</h4>
            <p>contacto@mupai.com<br>+52 123 456 7890</p>
        </div>
        <div>
            <h4>🌟 Síguenos</h4>
            <p>Facebook • Instagram • YouTube</p>
        </div>
    </div>
    
    <hr style="border: 1px solid rgba(255,255,255,0.2); margin: 2rem 0;">
    
    <div style="text-align: center;">
        <p style="margin: 0.5rem 0;">© 2024 MUPAI - Entrenamiento Digital. Todos los derechos reservados.</p>
        <p style="margin: 0.5rem 0; opacity: 0.8;">🤖 Powered by Science, Technology & AI | Monterrey, México</p>
        <p style="margin: 0.5rem 0; font-size: 0.9rem; opacity: 0.7;">
            Desarrollado por Erick Francisco De Luna Hernández | Última actualización: Junio 2024
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
