import streamlit as st
import base64
import os

# Configuración de página optimizada
st.set_page_config(
    page_title="MUPAI - Entrenamiento Digital",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función para mostrar imagen con fallback elegante
def display_image_safe(image_path, caption="", use_container_width=True, width=None):
    """Muestra imagen con fallback elegante si no existe"""
    try:
        if os.path.exists(image_path):
            st.image(image_path, caption=caption, use_container_width=use_container_width, width=width)
        else:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 3rem;
                text-align: center;
                border-radius: 15px;
                margin: 1rem 0;
                border: 2px dashed rgba(255,255,255,0.3);
                box-shadow: 0 8px 30px rgba(0,0,0,0.12);
            ">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📸</div>
                <h4 style="margin-bottom: 1rem;">{caption or 'Imagen'}</h4>
                <p style="opacity: 0.8; margin-top: 1rem; font-size: 0.9rem;">
                    📁 Sube el archivo: <code style="background: rgba(255,255,255,0.2); padding: 0.25rem 0.5rem; border-radius: 4px;">{image_path}</code>
                </p>
                <p style="opacity: 0.6; font-size: 0.8rem; margin-top: 0.5rem;">
                    💡 Formatos soportados: PNG, JPG, JPEG, GIF
                </p>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ Error mostrando imagen {image_path}: {str(e)}")

# CSS profesional completo y optimizado
st.markdown("""
<style>
    /* Importar fuentes modernas */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Variables CSS para consistencia total */
    :root {
        --primary-color: #2E86AB;
        --secondary-color: #A23B72;
        --accent-color: #F18F01;
        --success-color: #3CB371;
        --danger-color: #E74C3C;
        --warning-color: #F39C12;
        --info-color: #3498DB;
        --background-light: #f8f9fa;
        --background-dark: #2c3e50;
        --text-dark: #2d3436;
        --text-light: #636e72;
        --shadow-light: 0 2px 12px rgba(0,0,0,0.08);
        --shadow-medium: 0 8px 30px rgba(0,0,0,0.12);
        --shadow-heavy: 0 20px 60px rgba(0,0,0,0.15);
        --shadow-intense: 0 30px 80px rgba(0,0,0,0.2);
        --border-radius: 15px;
        --border-radius-small: 8px;
        --border-radius-large: 20px;
        --transition-fast: 0.2s ease;
        --transition-medium: 0.4s ease;
        --transition-slow: 0.6s ease;
    }
    
    /* Configuración global mejorada */
    .stApp {
        font-family: 'Poppins', 'Inter', sans-serif;
        background: linear-gradient(135deg, #fafbfc 0%, #f4f6f8 100%);
        color: var(--text-dark);
    }
    
    /* Header principal con efectos avanzados */
    .main-header {
        font-size: 4.5rem;
        font-weight: 800;
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color), var(--accent-color));
        background-size: 300% 300%;
        animation: gradientShift 6s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin: 2rem 0;
        text-shadow: 0 4px 20px rgba(46, 134, 171, 0.3);
        position: relative;
        z-index: 1;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Sidebar profesional mejorado */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
    }
    
    .css-1d391kg .css-1v0mbdj {
        color: white !important;
    }
    
    .sidebar-header {
        background: rgba(255,255,255,0.15);
        color: white;
        padding: 1.5rem;
        border-radius: var(--border-radius-small);
        margin-bottom: 1.5rem;
        text-align: center;
        font-weight: 600;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: var(--shadow-medium);
    }
    
    /* Cards modernas con efectos avanzados */
    .modern-card {
        background: white;
        padding: 2.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-medium);
        margin: 1.5rem 0;
        border: 1px solid rgba(46, 134, 171, 0.1);
        transition: all var(--transition-medium) cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .modern-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(46, 134, 171, 0.04), transparent);
        transition: left var(--transition-slow) ease;
    }
    
    .modern-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: var(--shadow-heavy);
        border-color: var(--primary-color);
    }
    
    .modern-card:hover::before {
        left: 100%;
    }
    
    /* Cards con gradientes espectaculares */
    .gradient-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-medium);
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
        transition: all var(--transition-medium) ease;
    }
    
    .gradient-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        transform: translateX(-100%);
        transition: transform var(--transition-slow) ease;
    }
    
    .gradient-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-intense);
    }
    
    .gradient-card:hover::after {
        transform: translateX(100%);
    }
    
    /* Service cards súper avanzadas */
    .service-card {
        background: white;
        padding: 2.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-light);
        margin: 1.5rem 0;
        border-left: 5px solid var(--primary-color);
        transition: all var(--transition-medium) cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .service-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(46, 134, 171, 0.02), rgba(162, 59, 114, 0.02));
        opacity: 0;
        transition: opacity var(--transition-medium) ease;
    }
    
    .service-card:hover {
        transform: translateY(-12px);
        box-shadow: var(--shadow-heavy);
        border-left-width: 8px;
        border-left-color: var(--accent-color);
    }
    
    .service-card:hover::before {
        opacity: 1;
    }
    
    .service-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        color: var(--primary-color);
        transition: all var(--transition-medium) ease;
        display: inline-block;
    }
    
    .service-card:hover .service-icon {
        transform: scale(1.15) rotate(5deg);
        color: var(--accent-color);
    }
    
    /* Métricas súper avanzadas */
    .metric-container {
        background: white;
        padding: 2rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-medium);
        text-align: center;
        margin: 1rem;
        border-top: 4px solid var(--accent-color);
        transition: all var(--transition-medium) cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color), var(--accent-color));
        background-size: 300% 100%;
        animation: gradientFlow 3s ease infinite;
    }
    
    @keyframes gradientFlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .metric-container:hover {
        transform: scale(1.08) translateY(-5px);
        box-shadow: var(--shadow-heavy);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        color: var(--primary-color);
        margin: 1rem 0;
        transition: all var(--transition-medium) ease;
    }
    
    .metric-container:hover .metric-value {
        color: var(--accent-color);
        transform: scale(1.1);
    }
    
    .metric-label {
        font-size: 1rem;
        color: var(--text-dark);
        font-weight: 500;
        opacity: 0.8;
    }
    
    /* About section espectacular */
    .about-hero {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 4rem;
        border-radius: var(--border-radius);
        text-align: center;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-heavy);
    }
    
    .about-hero::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: floatPattern 20s linear infinite;
    }
    
    @keyframes floatPattern {
        0% { transform: translate(0, 0) rotate(0deg); }
        100% { transform: translate(-50px, -50px) rotate(360deg); }
    }
    
    .profile-section {
        background: white;
        padding: 2.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-medium);
        margin: 1.5rem 0;
        border-left: 5px solid var(--success-color);
        position: relative;
    }
    
    /* Timeline espectacular para experiencia */
    .timeline {
        position: relative;
        padding-left: 2rem;
    }
    
    .timeline::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 3px;
        background: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
        border-radius: 2px;
        box-shadow: 0 0 10px rgba(46, 134, 171, 0.3);
    }
    
    .timeline-item {
        margin-bottom: 2rem;
        position: relative;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -2.25rem;
        top: 0.5rem;
        width: 1.5rem;
        height: 1.5rem;
        background: var(--primary-color);
        border-radius: 50%;
        border: 3px solid white;
        box-shadow: 0 0 0 3px var(--primary-color), 0 0 10px rgba(46, 134, 171, 0.3);
        transition: all var(--transition-medium) ease;
    }
    
    .timeline-item:hover::before {
        background: var(--accent-color);
        box-shadow: 0 0 0 3px var(--accent-color), 0 0 15px rgba(241, 143, 1, 0.4);
        transform: scale(1.2);
    }
    
    .timeline-content {
        background: white;
        padding: 2rem;
        border-radius: var(--border-radius-small);
        box-shadow: var(--shadow-light);
        border-left: 4px solid var(--primary-color);
        transition: all var(--transition-medium) ease;
    }
    
    .timeline-content:hover {
        transform: translateX(10px);
        box-shadow: var(--shadow-medium);
        border-left-color: var(--accent-color);
    }
    
    /* Contact form súper avanzado */
    .contact-container {
        background: white;
        padding: 3rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-medium);
        margin: 1.5rem 0;
        border-top: 5px solid var(--primary-color);
        position: relative;
        overflow: hidden;
    }
    
    .contact-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(46, 134, 171, 0.02), rgba(162, 59, 114, 0.02));
        pointer-events: none;
    }
    
    .contact-info-card {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
        padding: 2.5rem;
        border-radius: var(--border-radius);
        text-align: center;
        box-shadow: var(--shadow-medium);
        position: relative;
        overflow: hidden;
    }
    
    .contact-info-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 2px, transparent 2px);
        background-size: 30px 30px;
        animation: sparkle 15s linear infinite;
    }
    
    @keyframes sparkle {
        0% { transform: translate(0, 0) rotate(0deg); }
        100% { transform: translate(-30px, -30px) rotate(360deg); }
    }
    
    /* Logo container mejorado */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
        padding: 2rem;
        background: white;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-light);
        border: 2px solid rgba(46, 134, 171, 0.1);
        transition: all var(--transition-medium) ease;
    }
    
    .logo-container:hover {
        box-shadow: var(--shadow-medium);
        border-color: var(--primary-color);
        transform: translateY(-3px);
    }
    
    /* Galería de imágenes espectacular */
    .image-gallery-container {
        margin: 2rem 0;
    }
    
    .image-container {
        border-radius: var(--border-radius);
        overflow: hidden;
        box-shadow: var(--shadow-medium);
        transition: all var(--transition-medium) cubic-bezier(0.4, 0, 0.2, 1);
        margin: 1rem 0;
        position: relative;
        background: white;
        border: 3px solid transparent;
    }
    
    .image-container:hover {
        transform: scale(1.05) translateY(-5px);
        box-shadow: var(--shadow-heavy);
        border-color: var(--primary-color);
    }
    
    .image-container img {
        transition: all var(--transition-medium) ease;
        width: 100%;
        height: auto;
    }
    
    .image-container:hover img {
        transform: scale(1.02);
    }
    
    /* Botones súper mejorados */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--border-radius-small) !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all var(--transition-medium) cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
        box-shadow: var(--shadow-light) !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left var(--transition-medium) ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: var(--shadow-heavy) !important;
        background: linear-gradient(135deg, var(--secondary-color), var(--accent-color)) !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Tabs styling espectacular */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        justify-content: center;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 0 2rem;
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: var(--border-radius-small);
        color: var(--primary-color);
        font-weight: 600;
        font-size: 1.1rem;
        border: 2px solid transparent;
        transition: all var(--transition-medium) ease;
        box-shadow: var(--shadow-light);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #e9ecef, #dee2e6);
        border-color: var(--primary-color);
        transform: translateY(-2px);
        box-shadow: var(--shadow-medium);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
        color: white !important;
        border-color: var(--primary-color);
        transform: translateY(-2px);
        box-shadow: var(--shadow-heavy) !important;
    }
    
    /* Footer espectacular */
    .footer {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        padding: 4rem 2rem;
        border-radius: var(--border-radius);
        text-align: center;
        margin-top: 4rem;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-heavy);
    }
    
    .footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/><circle cx="10" cy="90" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
    }
    
    /* Cuestionarios espectaculares */
    .questionnaire-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 4rem;
        border-radius: var(--border-radius);
        text-align: center;
        box-shadow: var(--shadow-heavy);
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .questionnaire-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 40px 40px;
        animation: rotate 30s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .coming-soon {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        color: var(--text-dark);
        padding: 2.5rem;
        border-radius: var(--border-radius);
        text-align: center;
        margin: 1.5rem 0;
        font-weight: 600;
        box-shadow: var(--shadow-medium);
        border: 2px solid rgba(241, 143, 1, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .coming-soon::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 1s ease;
    }
    
    .coming-soon:hover::before {
        left: 100%;
    }
    
    /* Responsive design súper avanzado */
    @media (max-width: 768px) {
        .main-header {
            font-size: 3rem;
        }
        
        .modern-card, .gradient-card, .service-card {
            padding: 2rem;
            margin: 1rem 0;
        }
        
        .metric-container {
            padding: 1.5rem;
            margin: 0.5rem;
        }
        
        .metric-value {
            font-size: 2.5rem;
        }
        
        .about-hero {
            padding: 2.5rem;
        }
        
        .contact-container {
            padding: 2rem;
        }
        
        .timeline {
            padding-left: 1.5rem;
        }
        
        .timeline-content {
            padding: 1.5rem;
        }
        
        .timeline-content:hover {
            transform: translateX(5px);
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding: 0 1rem;
            font-size: 1rem;
        }
        
        .questionnaire-card {
            padding: 2.5rem;
        }
    }
    
    @media (max-width: 480px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .modern-card, .gradient-card, .service-card {
            padding: 1.5rem;
            margin: 0.75rem 0;
        }
        
        .metric-container {
            padding: 1rem;
            margin: 0.25rem;
        }
        
        .about-hero {
            padding: 2rem;
        }
        
        .contact-container {
            padding: 1.5rem;
        }
        
        .questionnaire-card {
            padding: 2rem;
        }
        
        .footer {
            padding: 2rem 1rem;
        }
    }
    
    /* Animaciones de entrada mejoradas */
    .animate-fade-in {
        animation: fadeInUp 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(40px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-fade-in-delay {
        animation: fadeInUp 0.8s cubic-bezier(0.4, 0, 0.2, 1) 0.2s forwards;
        opacity: 0;
    }
    
    /* Efectos de hover para formularios */
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > div:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(46, 134, 171, 0.1) !important;
    }
    
    /* Mejoras en selectbox */
    .stSelectbox > div > div > div {
        border-radius: var(--border-radius-small) !important;
        border: 2px solid #e1e5e9 !important;
        transition: all var(--transition-fast) ease !important;
    }
    
    .stSelectbox > div > div > div:hover {
        border-color: var(--primary-color) !important;
        box-shadow: var(--shadow-light) !important;
    }
    
    /* Mejoras en text input */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: var(--border-radius-small) !important;
        border: 2px solid #e1e5e9 !important;
        transition: all var(--transition-fast) ease !important;
    }
    
    .stTextInput > div > div > input:hover,
    .stTextArea > div > div > textarea:hover {
        border-color: var(--primary-color) !important;
        box-shadow: var(--shadow-light) !important;
    }
    
    /* Loading spinner personalizado */
    .stSpinner > div {
        border-color: var(--primary-color) transparent var(--primary-color) transparent !important;
    }
    
    /* Mensajes de estado mejorados */
    .stSuccess {
        background-color: rgba(60, 179, 113, 0.1) !important;
        border-left: 4px solid var(--success-color) !important;
        border-radius: var(--border-radius-small) !important;
    }
    
    .stError {
        background-color: rgba(231, 76, 60, 0.1) !important;
        border-left: 4px solid var(--danger-color) !important;
        border-radius: var(--border-radius-small) !important;
    }
    
    .stWarning {
        background-color: rgba(243, 156, 18, 0.1) !important;
        border-left: 4px solid var(--warning-color) !important;
        border-radius: var(--border-radius-small) !important;
    }
    
    .stInfo {
        background-color: rgba(52, 152, 219, 0.1) !important;
        border-left: 4px solid var(--info-color) !important;
        border-radius: var(--border-radius-small) !important;
    }
</style>
""", unsafe_allow_html=True)

# Función para crear métricas personalizadas avanzadas
def create_advanced_metric(icon, value, label, delta=None, color="var(--primary-color)"):
    delta_html = f'<div style="color: var(--success-color); font-size: 0.9rem; margin-top: 0.5rem; font-weight: 500;">📈 {delta}</div>' if delta else ''
    return f"""
    <div class="metric-container animate-fade-in">
        <div style="font-size: 2.5rem; margin-bottom: 1rem; color: {color};">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {delta_html}
    </div>
    """

# Navegación en sidebar mejorada
st.sidebar.markdown('<div class="sidebar-header">🚀 NAVEGACIÓN MUPAI</div>', unsafe_allow_html=True)

menu_options = {
    "🏠 Inicio": {"icon": "🏠", "desc": "Página principal"},
    "👨‍💼 Sobre Mí": {"icon": "👨‍💼", "desc": "Perfil profesional"}, 
    "💼 Servicios": {"icon": "💼", "desc": "Nuestras soluciones"},
    "📞 Contacto": {"icon": "📞", "desc": "Contáctanos"},
    "⚖️ Balance Energético": {"icon": "⚖️", "desc": "Evaluación metabólica"},
    "🍽️ Preferencias Alimenticias": {"icon": "🍽️", "desc": "Hábitos nutricionales"},
    "🍰 Control de Antojos": {"icon": "🍰", "desc": "Manejo de impulsos"}
}

menu = st.sidebar.selectbox(
    "Selecciona una sección:",
    list(menu_options.keys()),
    format_func=lambda x: f"{menu_options[x]['icon']} {x.split(' ', 1)[1]}"
)

# Agregar información adicional en sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("""
**🎯 Características Principales:**
- 🤖 IA Personalizada
- 🔬 Ciencia Aplicada  
- 📊 Seguimiento 24/7
- ✅ Resultados Garantizados

**📊 Estado del Sistema:**
🟢 **Operativo** | ⚡ **Alta Velocidad**

**📈 Estadísticas en Tiempo Real:**
- 👥 **500+** Usuarios Activos
- 🏃‍♂️ **95%** Tasa de Adherencia
- 📱 **24/7** Disponibilidad
""")

# CONTENIDO PRINCIPAL
if menu == "🏠 Inicio":
    # Hero section principal espectacular
    st.markdown('<div class="main-header animate-fade-in">Bienvenido a MUPAI</div>', unsafe_allow_html=True)
    
    # Logo con manejo mejorado y efecto hover
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        display_image_safe("LOGO.png", "Logo MUPAI - Entrenamiento Digital", width=400)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Subtítulo profesional con efectos
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;" class="animate-fade-in-delay">
        <p style="font-size: 1.4rem; color: var(--text-dark); font-weight: 500; opacity: 0.8; line-height: 1.6;">
            🤖 <em>Revolucionando el entrenamiento con Inteligencia Artificial y Ciencia del Ejercicio</em>
        </p>
        <div style="margin-top: 1rem;">
            <span style="background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); color: white; padding: 0.5rem 1rem; border-radius: 20px; margin: 0.5rem; font-size: 0.9rem; font-weight: 500;">
                🎯 Personalización Extrema
            </span>
            <span style="background: linear-gradient(135deg, var(--accent-color), var(--success-color)); color: white; padding: 0.5rem 1rem; border-radius: 20px; margin: 0.5rem; font-size: 0.9rem; font-weight: 500;">
                📊 Resultados Comprobados
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Dashboard de métricas súper avanzado
    st.markdown("### 📊 **Nuestro Impacto en Números**")
    st.markdown('<div style="margin: 1rem 0; text-align: center; opacity: 0.7; font-size: 1.1rem;">Resultados respaldados por ciencia y tecnología de vanguardia</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    metrics_data = [
        ("🎯", "500+", "Clientes Transformados", "Crecimiento mensual del 15%", "var(--primary-color)"),
        ("📋", "1000+", "Programas Diseñados", "Basados en IA y ciencia", "var(--secondary-color)"),
        ("🏆", "5+", "Años de Experiencia", "Investigación continua", "var(--accent-color)"),
        ("🔬", "50+", "Estudios Aplicados", "Metodología validada", "var(--success-color)")
    ]
    
    for i, (icon, value, label, delta, color) in enumerate(metrics_data):
        with [col1, col2, col3, col4][i]:
            st.markdown(create_advanced_metric(icon, value, label, delta, color), unsafe_allow_html=True)

    st.markdown("---")

    # Contenido principal en pestañas súper avanzadas
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 **Misión & Visión**", 
        "📋 **Nuestras Políticas**", 
        "🚀 **¿Por qué MUPAI?**",
        "🔬 **Metodología Científica**"
    ])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="gradient-card animate-fade-in">
                <h2 style="margin-bottom: 1.5rem;">🎯 Nuestra Misión</h2>
                <p style="font-size: 1.2rem; line-height: 1.8; margin-bottom: 2rem;">
                Hacer accesible el entrenamiento basado en ciencia, proporcionando planes completamente personalizados a través de herramientas digitales respaldadas por inteligencia artificial, datos precisos y la investigación más actualizada en ciencias del ejercicio.
                </p>
                <div style="margin-top: 2rem; padding: 1.5rem; background: rgba(255,255,255,0.15); border-radius: 12px; backdrop-filter: blur(10px);">
                    <h4 style="margin-bottom: 1rem;">🎯 Nuestro Enfoque:</h4>
                    <ul style="margin: 0; padding-left: 1.5rem; line-height: 1.8;">
                        <li>💪 Desarrollo físico integral</li>
                        <li>🧠 Bienestar mental y emocional</li>
                        <li>🌱 Sostenibilidad a largo plazo</li>
                        <li>📈 Resultados medibles y comprobables</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="gradient-card animate-fade-in">
                <h2 style="margin-bottom: 1.5rem;">🔮 Nuestra Visión</h2>
                <p style="font-size: 1.2rem; line-height: 1.8; margin-bottom: 2rem;">
                Convertirnos en el referente global en entrenamiento digital personalizado, aprovechando las nuevas tecnologías para hacer más accesible el fitness basado en ciencia y transformar millones de vidas.
                </p>
                <div style="margin-top: 2rem; padding: 1.5rem; background: rgba(255,255,255,0.15); border-radius: 12px; backdrop-filter: blur(10px);">
                    <h4 style="margin-bottom: 1rem;">🚀 Metas 2025:</h4>
                    <ul style="margin: 0; padding-left: 1.5rem; line-height: 1.8;">
                        <li>👥 10,000+ usuarios activos globalmente</li>
                        <li>🌍 Expansión a 20 países</li>
                        <li>🏆 Certificaciones científicas internacionales</li>
                        <li>📱 Plataforma móvil nativa completa</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="modern-card animate-fade-in">
            <h2 style="color: var(--primary-color); margin-bottom: 2rem; text-align: center;">📜 Marco de Políticas Empresariales</h2>
            
            <div style="background: linear-gradient(135deg, #f8f9fa, #e9ecef); padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
                <h3 style="color: var(--secondary-color); margin-bottom: 1.5rem;">🏛️ Principios Fundamentales</h3>
                <p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 1.5rem;">
                En <strong>MUPAI</strong>, nuestra política empresarial está fundamentada en el compromiso inquebrantable con la excelencia, la ética profesional y el servicio centrado en el usuario. Actuamos con responsabilidad corporativa, transparencia total y integridad en cada interacción.
                </p>
                <div style="background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid var(--primary-color);">
                    <strong>💎 Valores Core:</strong> Integridad, Innovación, Inclusión, Impacto
                </div>
            </div>
            
            <h3 style="color: var(--accent-color); margin: 2rem 0 1.5rem 0; text-align: center;">🛡️ Pilares del Servicio</h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 2rem;">
                <div style="background: linear-gradient(135deg, var(--primary-color), rgba(46, 134, 171, 0.8)); color: white; padding: 2rem; border-radius: 12px; box-shadow: var(--shadow-medium);">
                    <h4 style="margin-bottom: 1rem;">🔬 Ciencia y Evidencia</h4>
                    <ul style="line-height: 1.6; margin: 0; padding-left: 1rem;">
                        <li>Metodologías basadas en investigación peer-reviewed</li>
                        <li>Datos confiables y verificados científicamente</li>
                        <li>Actualización científica continua</li>
                        <li>Colaboración con universidades</li>
                    </ul>
                </div>
                
                <div style="background: linear-gradient(135deg, var(--secondary-color), rgba(162, 59, 114, 0.8)); color: white; padding: 2rem; border-radius: 12px; box-shadow: var(--shadow-medium);">
                    <h4 style="margin-bottom: 1rem;">💻 Tecnología Responsable</h4>
                    <ul style="line-height: 1.6; margin: 0; padding-left: 1rem;">
                        <li>IA ética y transparente</li>
                        <li>Accesibilidad universal y inclusiva</li>
                        <li>Innovación centrada en el usuario</li>
                        <li>Desarrollo sostenible de software</li>
                    </ul>
                </div>
                
                <div style="background: linear-gradient(135deg, var(--accent-color), rgba(241, 143, 1, 0.8)); color: white; padding: 2rem; border-radius: 12px; box-shadow: var(--shadow-medium);">
                    <h4 style="margin-bottom: 1rem;">🔐 Privacidad y Seguridad</h4>
                    <ul style="line-height: 1.6; margin: 0; padding-left: 1rem;">
                        <li>Protección de datos personales GDPR</li>
                        <li>Cumplimiento normativo estricto</li>
                        <li>Transparencia en el uso de información</li>
                        <li>Encriptación de extremo a extremo</li>
                    </ul>
                </div>
                
                <div style="background: linear-gradient(135deg, var(--success-color), rgba(60, 179, 113, 0.8)); color: white; padding: 2rem; border-radius: 12px; box-shadow: var(--shadow-medium);">
                    <h4 style="margin-bottom: 1rem;">🚀 Mejora Continua</h4>
                    <ul style="line-height: 1.6; margin: 0; padding-left: 1rem;">
                        <li>Feedback constante de usuarios</li>
                        <li>Evolución de metodologías</li>
                        <li>Adaptación a nuevas tendencias</li>
                        <li>Ciclos de mejora Kaizen</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div class="modern-card animate-fade-in">
            <h2 style="color: var(--primary-color); text-align: center; margin-bottom: 3rem;">🚀 Ventajas Competitivas de MUPAI</h2>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-top: 2rem;">
                <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-radius: 15px; transition: transform 0.3s ease; box-shadow: var(--shadow-medium);" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                    <div style="font-size: 4rem; margin-bottom: 1.5rem;">🤖</div>
                    <h4 style="margin-bottom: 1rem;">Inteligencia Artificial Avanzada</h4>
                    <p style="line-height: 1.6; margin-bottom: 1.5rem;">Algoritmos de machine learning que aprenden de tu progreso y se adaptan automáticamente para maximizar tus resultados de forma científica.</p>
                    <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8; background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
                        • <strong>Personalización dinámica</strong><br>
                        • <strong>Predicción de resultados</strong><br>
                        • <strong>Optimización automática</strong><br>
                        • <strong>Aprendizaje continuo</strong>
                    </div>
                </div>
                
                <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f093fb, #f5576c); color: white; border-radius: 15px; transition: transform 0.3s ease; box-shadow: var(--shadow-medium);" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                    <div style="font-size: 4rem; margin-bottom: 1.5rem;">📱</div>
                    <h4 style="margin-bottom: 1rem;">Plataforma 100% Digital</h4>
                    <p style="line-height: 1.6; margin-bottom: 1.5rem;">Acceso completo desde cualquier dispositivo, en cualquier momento y lugar. Sin limitaciones geográficas ni horarias, siempre contigo.</p>
                    <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8; background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
                        • <strong>Disponibilidad 24/7</strong><br>
                        • <strong>Sincronización multi-dispositivo</strong><br>
                        • <strong>Modo offline disponible</strong><br>
                        • <strong>Actualizaciones automáticas</strong>
                    </div>
                </div>
                
                <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #4facfe, #00f2fe); color: white; border-radius: 15px; transition: transform 0.3s ease; box-shadow: var(--shadow-medium);" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                    <div style="font-size: 4rem; margin-bottom: 1.5rem;">🎯</div>
                    <h4 style="margin-bottom: 1rem;">Personalización Extrema</h4>
                    <p style="line-height: 1.6; margin-bottom: 1.5rem;">Cada programa es único, diseñado específicamente para tus objetivos, limitaciones, preferencias y estilo de vida particular.</p>
                    <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8; background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
                        • <strong>Análisis biomecánico</strong><br>
                        • <strong>Evaluación metabólica</strong><br>
                        • <strong>Preferencias individuales</strong><br>
                        • <strong>Adaptación en tiempo real</strong>
                    </div>
                </div>
                
                <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #43e97b, #38f9d7); color: white; border-radius: 15px; transition: transform 0.3s ease; box-shadow: var(--shadow-medium);" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                    <div style="font-size: 4rem; margin-bottom: 1.5rem;">🔬</div>
                    <h4 style="margin-bottom: 1rem;">Respaldo Científico Total</h4>
                    <p style="line-height: 1.6; margin-bottom: 1.5rem;">Metodologías validadas por investigación peer-reviewed y constante actualización con los últimos avances en ciencias del ejercicio.</p>
                    <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8; background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
                        • <strong>50+ estudios aplicados</strong><br>
                        • <strong>Revisión científica mensual</strong><br>
                        • <strong>Colaboración universitaria</strong><br>
                        • <strong>Validación clínica</strong>
                    </div>
                </div>
                
                <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #ffeaa7, #fab1a0); color: #2d3436; border-radius: 15px; transition: transform 0.3s ease; box-shadow: var(--shadow-medium);" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                    <div style="font-size: 4rem; margin-bottom: 1.5rem;">⚡</div>
                    <h4 style="margin-bottom: 1rem;">Resultados Acelerados</h4>
                    <p style="line-height: 1.6; margin-bottom: 1.5rem;">Optimización científica que reduce el tiempo necesario para alcanzar tus objetivos sin comprometer la seguridad ni la sostenibilidad.</p>
                    <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8; background: rgba(0,0,0,0.1); padding: 1rem; border-radius: 8px;">
                        • <strong>Progresión optimizada</strong><br>
                        • <strong>Recuperación inteligente</strong><br>
                        • <strong>Monitoreo continuo</strong><br>
                        • <strong>Prevención de lesiones</strong>
                    </div>
                </div>
                
                <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #a29bfe, #6c5ce7); color: white; border-radius: 15px; transition: transform 0.3s ease; box-shadow: var(--shadow-medium);" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                    <div style="font-size: 4rem; margin-bottom: 1.5rem;">🎓</div>
                    <h4 style="margin-bottom: 1rem;">Expertise Profesional</h4>
                    <p style="line-height: 1.6; margin-bottom: 1.5rem;">Dirigido por especialistas con maestrías y experiencia internacional en ciencias del ejercicio, fisiología y tecnologías deportivas.</p>
                    <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8; background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
                        • <strong>Maestría especializada</strong><br>
                        • <strong>Experiencia internacional</strong><br>
                        • <strong>Educación continua</strong><br>
                        • <strong>Red de expertos</strong>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("""
        <div class="modern-card animate-fade-in">
            <h2 style="color: var(--primary-color); text-align: center; margin-bottom: 2rem;">🔬 Metodología Científica MUPAI</h2>
            
            <div style="background: linear-gradient(135deg, #f8f9fa, #e9ecef); padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
                <h3 style="color: var(--secondary-color); margin-bottom: 1rem;">📊 Nuestro Enfoque Basado en Evidencia</h3>
                <p style="font-size: 1.1rem; line-height: 1.8;">
                MUPAI integra los principios fundamentales de las ciencias del ejercicio con tecnología de vanguardia para crear programas de entrenamiento que no solo son efectivos, sino también seguros y sostenibles a largo plazo.
                </p>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin: 2rem 0;">
                <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 4px solid var(--primary-color); box-shadow: var(--shadow-light);">
                    <h4 style="color: var(--primary-color); margin-bottom: 1rem;">🧬 Fisiología del Ejercicio</h4>
                    <ul style="line-height: 1.6; color: var(--text-dark); margin: 0; padding-left: 1rem;">
                        <li>Análisis de sistemas energéticos</li>
                        <li>Adaptaciones cardiovasculares</li>
                        <li>Respuestas hormonales</li>
                        <li>Recuperación optimizada</li>
                    </ul>
                </div>
                
                <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 4px solid var(--secondary-color); box-shadow: var(--shadow-light);">
                    <h4 style="color: var(--secondary-color); margin-bottom: 1rem;">⚙️ Biomecánica Aplicada</h4>
                    <ul style="line-height: 1.6; color: var(--text-dark); margin: 0; padding-left: 1rem;">
                        <li>Análisis de movimiento</li>
                        <li>Optimización de técnica</li>
                        <li>Prevención de lesiones</li>
                        <li>Eficiencia mecánica</li>
                    </ul>
                </div>
                
                <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 4px solid var(--accent-color); box-shadow: var(--shadow-light);">
                    <h4 style="color: var(--accent-color); margin-bottom: 1rem;">📈 Periodización Científica</h4>
                    <ul style="line-height: 1.6; color: var(--text-dark); margin: 0; padding-left: 1rem;">
                        <li>Macrociclos planificados</li>
                        <li>Microciclos adaptativos</li>
                        <li>Sobrecarga progresiva</li>
                        <li>Deload estratégicos</li>
                    </ul>
                </div>
                
                <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 4px solid var(--success-color); box-shadow: var(--shadow-light);">
                    <h4 style="color: var(--success-color); margin-bottom: 1rem;">🧠 Psicología del Deporte</h4>
                    <ul style="line-height: 1.6; color: var(--text-dark); margin: 0; padding-left: 1rem;">
                        <li>Motivación intrínseca</li>
                        <li>Adherencia a largo plazo</li>
                        <li>Manejo del estrés</li>
                        <li>Confianza y autoeficacia</li>
                    </ul>
                </div>
            </div>
            
            <div style="background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); color: white; padding: 2rem; border-radius: 12px; margin-top: 2rem;">
                <h3 style="text-align: center; margin-bottom: 1.5rem;">🏆 Validación Científica</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; text-align: center;">
                    <div>
                        <div style="font-size: 2.5rem; margin-bottom: 0.5rem; font-weight: 800;">50+</div>
                        <div style="opacity: 0.9; font-weight: 500;">Estudios Revisados</div>
                    </div>
                    <div>
                        <div style="font-size: 2.5rem; margin-bottom: 0.5rem; font-weight: 800;">95%</div>
                        <div style="opacity: 0.9; font-weight: 500;">Adherencia Promedio</div>
                    </div>
                    <div>
                        <div style="font-size: 2.5rem; margin-bottom: 0.5rem; font-weight: 800;">87%</div>
                        <div style="opacity: 
                                                <div style="opacity: 0.9; font-weight: 500;">Objetivos Alcanzados</div>
                    </div>
                    <div>
                        <div style="font-size: 2.5rem; margin-bottom: 0.5rem; font-weight: 800;">12</div>
                        <div style="opacity: 0.9; font-weight: 500;">Semanas Promedio</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif menu == "👨‍💼 Sobre Mí":
    # Hero section para About mejorado
    st.markdown("""
    <div class="about-hero animate-fade-in">
        <h1 style="font-size: 3.5rem; margin-bottom: 1rem;">👨‍💼 Erick Francisco De Luna Hernández</h1>
        <p style="font-size: 1.5rem; margin-bottom: 2rem; opacity: 0.9;">Especialista en Ciencias del Ejercicio y Entrenamiento Digital</p>
        <p style="font-size: 1.1rem; margin-bottom: 2rem; opacity: 0.8; max-width: 800px; margin-left: auto; margin-right: auto;">
            Profesional apasionado por transformar vidas a través del fitness científico, combinando expertise académico con innovación tecnológica de vanguardia
        </p>
        <div style="margin-top: 2rem;">
            <span style="background: rgba(255,255,255,0.25); padding: 0.75rem 1.5rem; border-radius: 25px; margin: 0.5rem; display: inline-block; backdrop-filter: blur(10px);">🎓 Maestría en Fuerza</span>
            <span style="background: rgba(255,255,255,0.25); padding: 0.75rem 1.5rem; border-radius: 25px; margin: 0.5rem; display: inline-block; backdrop-filter: blur(10px);">🏆 Premio al Mérito</span>
            <span style="background: rgba(255,255,255,0.25); padding: 0.75rem 1.5rem; border-radius: 25px; margin: 0.5rem; display: inline-block; backdrop-filter: blur(10px);">🌍 Experiencia Internacional</span>
            <span style="background: rgba(255,255,255,0.25); padding: 0.75rem 1.5rem; border-radius: 25px; margin: 0.5rem; display: inline-block; backdrop-filter: blur(10px);">🥇 Primer Lugar Generación</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Información profesional en pestañas avanzadas
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎓 **Formación Académica**", 
        "💼 **Trayectoria Profesional**", 
        "🏆 **Logros y Reconocimientos**", 
        "📸 **Galería Profesional**"
    ])
    
    with tab1:
        st.markdown("""
        <div class="profile-section animate-fade-in">
            <h3 style="color: var(--primary-color); margin-bottom: 2rem; text-align: center;">🎓 Excelencia Académica y Formación Especializada</h3>
            
            <div style="display: grid; gap: 2rem; margin-top: 2rem;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2.5rem; border-radius: 15px; position: relative; overflow: hidden;">
                    <div style="position: absolute; top: -20px; right: -20px; font-size: 6rem; opacity: 0.1;">🏅</div>
                    <h4 style="font-size: 1.5rem; margin-bottom: 1rem;">🏅 Maestría en Fuerza y Acondicionamiento</h4>
                    <p style="font-size: 1.1rem; margin-bottom: 0.5rem;"><strong>Football Science Institute</strong></p>
                    <p style="margin-bottom: 1.5rem; opacity: 0.9; line-height: 1.6;">Especialización avanzada en metodologías de entrenamiento científico, biomecánica deportiva y periodización del rendimiento atlético de alto nivel.</p>
                    <div style="background: rgba(255,255,255,0.15); padding: 1rem; border-radius: 8px; backdrop-filter: blur(10px);">
                        <strong>Áreas de especialización:</strong> Fisiología del ejercicio avanzada, Metodología del entrenamiento de fuerza, Análisis biomecánico, Periodización para alto rendimiento
                    </div>
                </div>
                
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 2.5rem; border-radius: 15px; position: relative; overflow: hidden;">
                    <div style="position: absolute; top: -20px; right: -20px; font-size: 6rem; opacity: 0.1;">🎓</div>
                    <h4 style="font-size: 1.5rem; margin-bottom: 1rem;">🎓 Licenciatura en Ciencias del Ejercicio</h4>
                    <p style="font-size: 1.1rem; margin-bottom: 0.5rem;"><strong>Universidad Autónoma de Nuevo León (UANL)</strong></p>
                    <p style="margin-bottom: 1.5rem; opacity: 0.9; line-height: 1.6;">Fundamentos sólidos en fisiología humana, biomecánica, metodología del entrenamiento y evaluación del rendimiento físico con enfoque científico.</p>
                    <div style="background: rgba(255,255,255,0.15); padding: 1rem; border-radius: 8px; backdrop-filter: blur(10px);">
                        <strong>Enfoque curricular:</strong> Anatomía funcional, Fisiología del ejercicio, Biomecánica aplicada, Nutrición deportiva, Psicología del deporte
                    </div>
                </div>
                
                <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 2.5rem; border-radius: 15px; position: relative; overflow: hidden;">
                    <div style="position: absolute; top: -20px; right: -20px; font-size: 6rem; opacity: 0.1;">🌍</div>
                    <h4 style="font-size: 1.5rem; margin-bottom: 1rem;">🌍 Intercambio Académico Internacional</h4>
                    <p style="font-size: 1.1rem; margin-bottom: 0.5rem;"><strong>Universidad de Sevilla, España</strong></p>
                    <p style="margin-bottom: 1.5rem; opacity: 0.9; line-height: 1.6;">Inmersión en metodologías europeas de entrenamiento, investigación en ciencias del deporte y colaboración internacional académica.</p>
                    <div style="background: rgba(255,255,255,0.15); padding: 1rem; border-radius: 8px; backdrop-filter: blur(10px);">
                        <strong>Experiencia adquirida:</strong> Metodologías europeas, Investigación colaborativa, Perspectiva internacional, Diversidad cultural en el deporte
                    </div>
                </div>
                
                <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; padding: 2.5rem; border-radius: 15px; position: relative; overflow: hidden;">
                    <div style="position: absolute; top: -20px; right: -20px; font-size: 6rem; opacity: 0.1;">⭐</div>
                    <h4 style="font-size: 1.5rem; margin-bottom: 1rem;">⭐ Programa de Talento Universitario</h4>
                    <p style="font-size: 1.1rem; margin-bottom: 0.5rem;"><strong>UANL - Distinción de Excelencia Académica</strong></p>
                    <p style="margin-bottom: 1.5rem; opacity: 0.9; line-height: 1.6;">Reconocimiento selectivo otorgado a estudiantes que demuestran excelencia académica excepcional y liderazgo extracurricular destacado.</p>
                    <div style="background: rgba(255,255,255,0.15); padding: 1rem; border-radius: 8px; backdrop-filter: blur(10px);">
                        <strong>Criterios de selección:</strong> Promedio superior a 9.5, Liderazgo estudiantil, Proyectos de investigación, Compromiso social
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="profile-section animate-fade-in">
            <h3 style="color: var(--secondary-color); margin-bottom: 2rem; text-align: center;">💼 Trayectoria Profesional y Experiencia</h3>
            
            <div class="timeline">
                <div class="timeline-item">
                    <div class="timeline-content">
                        <h4 style="color: var(--primary-color); margin-bottom: 1rem; font-size: 1.3rem;">🏋️ Muscle Up Gym</h4>
                        <p style="font-size: 1.1rem; font-weight: 600; color: var(--secondary-color); margin-bottom: 1rem;">Diseñador de Programas de Entrenamiento</p>
                        <p style="line-height: 1.6; margin-bottom: 1rem;">Desarrollo de metodologías personalizadas basadas en evidencia científica para optimización del rendimiento físico y bienestar integral de clientes diversos.</p>
                        <div style="background: var(--background-light); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                            <strong>Responsabilidades clave:</strong>
                            <ul style="margin: 0.5rem 0; padding-left: 1rem;">
                                <li>Evaluación biomecánica y fisiológica</li>
                                <li>Diseño de programas individualizados</li>
                                <li>Seguimiento y ajuste de protocolos</li>
                                <li>Educación y asesoramiento nutricional</li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <div class="timeline-item">
                    <div class="timeline-content">
                        <h4 style="color: var(--secondary-color); margin-bottom: 1rem; font-size: 1.3rem;">🔬 Laboratorio de Rendimiento Humano</h4>
                        <p style="font-size: 1.1rem; font-weight: 600; color: var(--accent-color); margin-bottom: 1rem;">Universidad Autónoma de Nuevo León</p>
                        <p style="line-height: 1.6; margin-bottom: 1rem;">Evaluaciones avanzadas de fuerza, biomecánica y acondicionamiento físico utilizando tecnologías de vanguardia y protocolos científicos validados.</p>
                        <div style="background: var(--background-light); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                            <strong>Actividades principales:</strong>
                            <ul style="margin: 0.5rem 0; padding-left: 1rem;">
                                <li>Análisis biomecánico con sensores 3D</li>
                                <li>Evaluaciones metabólicas especializadas</li>
                                <li>Investigación aplicada en rendimiento</li>
                                <li>Colaboración en proyectos científicos</li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <div class="timeline-item">
                    <div class="timeline-content">
                        <h4 style="color: var(--accent-color); margin-bottom: 1rem; font-size: 1.3rem;">🎯 Fundador y Director Técnico - MUPAI</h4>
                        <p style="font-size: 1.1rem; font-weight: 600; color: var(--success-color); margin-bottom: 1rem;">Entrenamiento Digital Personalizado</p>
                        <p style="line-height: 1.6; margin-bottom: 1rem;">Desarrollo y dirección de plataforma digital innovadora para entrenamiento personalizado basado en inteligencia artificial y ciencias del ejercicio.</p>
                        <div style="background: var(--background-light); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                            <strong>Logros destacados:</strong>
                            <ul style="margin: 0.5rem 0; padding-left: 1rem;">
                                <li>500+ clientes transformados exitosamente</li>
                                <li>1000+ programas personalizados diseñados</li>
                                <li>Integración de IA en metodologías de entrenamiento</li>
                                <li>Expansión digital y escalabilidad global</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div class="profile-section animate-fade-in">
            <h3 style="color: var(--success-color); margin-bottom: 2rem; text-align: center;">🏆 Reconocimientos y Logros Destacados</h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin: 2rem 0;">
                <div style="background: linear-gradient(135deg, #FFD700, #FFA500); color: white; padding: 2rem; border-radius: 15px; text-align: center; box-shadow: var(--shadow-heavy);">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">🥇</div>
                    <h4 style="margin-bottom: 1rem;">Premio al Mérito Académico</h4>
                    <p style="margin-bottom: 1rem; opacity: 0.9; font-weight: 500;">Universidad Autónoma de Nuevo León</p>
                    <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px; backdrop-filter: blur(10px);">
                        <small>Reconocimiento por excelencia académica excepcional y contribución destacada al área de ciencias del ejercicio</small>
                    </div>
                </div>
                
                <div style="background: linear-gradient(135deg, #32CD32, #228B22); color: white; padding: 2rem; border-radius: 15px; text-align: center; box-shadow: var(--shadow-heavy);">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">🎖️</div>
                    <h4 style="margin-bottom: 1rem;">Primer Lugar de Generación</h4>
                    <p style="margin-bottom: 1rem; opacity: 0.9; font-weight: 500;">Facultad de Organización Deportiva</p>
                    <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px; backdrop-filter: blur(10px);">
                        <small>Máximo promedio académico de la generación con calificación sobresaliente en todas las materias especializadas</small>
                    </div>
                </div>
                
                <div style="background: linear-gradient(135deg, #4169E1, #0000CD); color: white; padding: 2rem; border-radius: 15px; text-align: center; box-shadow: var(--shadow-heavy);">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">🌍</div>
                    <h4 style="margin-bottom: 1rem;">Beca Internacional Completa</h4>
                    <p style="margin-bottom: 1rem; opacity: 0.9; font-weight: 500;">Intercambio en Universidad de Sevilla</p>
                    <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px; backdrop-filter: blur(10px);">
                        <small>Beca de excelencia académica para estudios de especialización en metodologías europeas de entrenamiento deportivo</small>
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 3rem; background: var(--background-light); padding: 2rem; border-radius: 15px; border-left: 5px solid var(--success-color);">
                <h4 style="color: var(--success-color); margin-bottom: 2rem; text-align: center;">📊 Impacto Profesional Cuantificado</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 2rem; text-align: center;">
                    <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: var(--shadow-light);">
                        <div style="font-size: 2.5rem; color: var(--primary-color); font-weight: 800; margin-bottom: 0.5rem;">500+</div>
                        <div style="color: var(--text-dark); font-weight: 500;">Clientes Atendidos</div>
                        <div style="font-size: 0.8rem; color: var(--text-light); margin-top: 0.5rem;">Transformaciones exitosas</div>
                    </div>
                    <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: var(--shadow-light);">
                        <div style="font-size: 2.5rem; color: var(--secondary-color); font-weight: 800; margin-bottom: 0.5rem;">1000+</div>
                        <div style="color: var(--text-dark); font-weight: 500;">Programas Diseñados</div>
                        <div style="font-size: 0.8rem; color: var(--text-light); margin-top: 0.5rem;">Metodologías personalizadas</div>
                    </div>
                    <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: var(--shadow-light);">
                        <div style="font-size: 2.5rem; color: var(--accent-color); font-weight: 800; margin-bottom: 0.5rem;">50+</div>
                        <div style="color: var(--text-dark); font-weight: 500;">Investigaciones</div>
                        <div style="font-size: 0.8rem; color: var(--text-light); margin-top: 0.5rem;">Estudios aplicados</div>
                    </div>
                    <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: var(--shadow-light);">
                        <div style="font-size: 2.5rem; color: var(--success-color); font-weight: 800; margin-bottom: 0.5rem;">5+</div>
                        <div style="color: var(--text-dark); font-weight: 500;">Años Experiencia</div>
                        <div style="font-size: 0.8rem; color: var(--text-light); margin-top: 0.5rem;">Trayectoria comprobada</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<h3 style="color: var(--primary-color); text-align: center; margin-bottom: 2rem;">📸 Galería Profesional</h3>', unsafe_allow_html=True)
        
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
                        display_image_safe(images[i + j], f"Momento profesional {i + j + 1}")
                        st.markdown('</div>', unsafe_allow_html=True)

elif menu == "💼 Servicios":
    st.markdown("""
    <div class="main-header animate-fade-in" style="font-size: 3rem;">💼 Nuestros Servicios</div>
    <div style="text-align: center; margin-bottom: 3rem;">
        <p style="font-size: 1.2rem; color: var(--text-light);">Soluciones integrales de entrenamiento digital basadas en ciencia de vanguardia</p>
    </div>
    """, unsafe_allow_html=True)
    
    services = [
        {
            "icon": "🎯",
            "title": "Planes de Entrenamiento Personalizados",
            "description": "Programas únicos diseñados con IA avanzada, adaptados a tu nivel, objetivos y disponibilidad de tiempo específica.",
            "features": ["Análisis biomecánico completo", "Progresión automática inteligente", "Seguimiento en tiempo real", "Ajustes dinámicos continuos"],
            "color": "var(--primary-color)"
        },
        {
            "icon": "🧠",
            "title": "Bienestar Integral Físico-Mental", 
            "description": "Enfoque holístico que combina entrenamiento físico con técnicas avanzadas de mindfulness y gestión del estrés.",
            "features": ["Meditación guiada personalizada", "Técnicas de respiración avanzadas", "Manejo científico del estrés", "Equilibrio óptimo vida-deporte"],
            "color": "var(--secondary-color)"
        },
        {
            "icon": "🥗",
            "title": "Nutrición Deportiva Inteligente",
            "description": "Planes nutricionales personalizados basados en tu metabolismo individual, actividad física y objetivos específicos.",
            "features": ["Cálculo metabólico preciso", "Macros personalizados dinámicos", "Recetas adaptadas gustos", "Suplementación científica opcional"],
            "color": "var(--accent-color)"
        },
        {
            "icon": "📊",
            "title": "Análisis de Rendimiento Avanzado",
            "description": "Evaluaciones completas utilizando tecnología de vanguardia para optimizar tu progreso deportivo de forma científica.",
            "features": ["Métricas avanzadas detalladas", "Reportes científicos completos", "Comparativas temporales precisas", "Predicciones de progreso IA"],
            "color": "var(--success-color)"
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
                        
                        <div style="background: var(--background-light); padding: 1rem; border-radius: 10px; margin-top: 1rem;">
                            <h4 style="color: {service['color']}; margin-bottom: 0.5rem;">✨ Características Principales:</h4>
                            <ul style="margin: 0; padding-left: 1rem;">
                                {"".join(f"<li style='margin: 0.25rem 0; line-height: 1.4;'>{feature}</li>" for feature in service['features'])}
                            </ul>
                        </div>
                        
                        <div style="text-align: center; margin-top: 1.5rem;">
                            <span style="background: {service['color']}; color: white; padding: 0.5rem 1.5rem; border-radius: 20px; font-weight: 600; cursor: pointer; transition: all 0.3s ease;">
                                Más Información →
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # Sección de proceso mejorada
    st.markdown("---")
    st.markdown("""
    <div class="modern-card animate-fade-in">
        <h2 style="color: var(--primary-color); text-align: center; margin-bottom: 2rem;">🚀 Nuestro Proceso Científico</h2>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; margin-top: 2rem;">
            <div style="text-align: center;">
                <div style="width: 80px; height: 80px; background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); 
                           border-radius: 50%; margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center; color: white; font-size: 2rem; font-weight: bold; box-shadow: var(--shadow-medium);">1</div>
                <h4 style="color: var(--primary-color); margin-bottom: 1rem;">Evaluación Inicial Completa</h4>
                <p style="line-height: 1.6;">Análisis exhaustivo de tu condición física actual, objetivos específicos y limitaciones individuales</p>
            </div>
            
            <div style="text-align: center;">
                <div style="width: 80px; height: 80px; background: linear-gradient(135deg, var(--secondary-color), var(--accent-color)); 
                           border-radius: 50%; margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center; color: white; font-size: 2rem; font-weight: bold; box-shadow: var(--shadow-medium);">2</div>
                <h4 style="color: var(--secondary-color); margin-bottom: 1rem;">Diseño Personalizado IA</h4>
                <p style="line-height: 1.6;">Creación de tu plan único utilizando algoritmos de inteligencia artificial y metodología científica validada</p>
            </div>
            
            <div style="text-align: center;">
                <div style="width: 80px; height: 80px; background: linear-gradient(135deg, var(--accent-color), var(--success-color)); 
                           border-radius: 50%; margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center; color: white; font-size: 2rem; font-weight: bold; box-shadow: var(--shadow-medium);">3</div>
                <h4 style="color: var(--accent-color); margin-bottom: 1rem;">Implementación Guiada</h4>
                <p style="line-height: 1.6;">Seguimiento profesional continuo con ajustes en tiempo real basados en tu progreso y respuesta</p>
            </div>
            
            <div style="text-align: center;">
                <div style="width: 80px; height: 80px; background: linear-gradient(135deg, var(--success-color), var(--primary-color)); 
                           border-radius: 50%; margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center; color: white; font-size: 2rem; font-weight: bold; box-shadow: var(--shadow-medium);">4</div>
                <h4 style="color: var(--success-color); margin-bottom: 1rem;">Optimización Continua</h4>
                <p style="line-height: 1.6;">Evolución constante del programa basada en datos de progreso y adaptación fisiológica individual</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif menu == "📞 Contacto":
    st.markdown("""
    <div class="main-header animate-fade-in" style="font-size: 3rem;">📞 Contacto</div>
    <div style="text-align: center; margin-bottom: 3rem;">
        <p style="font-size: 1.2rem; color: var(--text-light);">¿Listo para transformar tu entrenamiento? Contáctanos ahora</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="contact-container animate-fade-in">
            <h3 style="color: var(--primary-color); margin-bottom: 1.5rem;">📝 Envíanos un mensaje</h3>
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
                placeholder="Describe tus objetivos, experiencia previa, disponibilidad de tiempo y cualquier información relevante que nos ayude a personalizar mejor tu programa..."
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
                <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin: 1rem 0; backdrop-filter: blur(10px);">
                    <strong>📧 Email Principal</strong><br>
                    contacto@mupai.com
                </div>
                
                <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin: 1rem 0; backdrop-filter: blur(10px);">
                    <strong>📱 WhatsApp Directo</strong><br>
                    +52 123 456 7890
                </div>
                
                <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin: 1rem 0; backdrop-filter: blur(10px);">
                    <strong>🏢 Ubicación</strong><br>
                    Monterrey, Nuevo León<br>
                    México
                </div>
                
                <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin: 1rem 0; backdrop-filter: blur(10px);">
                    <strong>🕒 Horarios de Atención</strong><br>
                    Lunes a Viernes: 8:00 - 18:00<br>
                    Sábados: 9:00 - 14:00<br>
                    Domingos: Solo emergencias
                </div>
            </div>
            
            <div style="margin-top: 2rem;">
                <h4>🌐 Síguenos en Redes</h4>
                <div style="margin-top: 1rem;">
                    <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.25rem; display: inline-block; backdrop-filter: blur(10px);">📘 Facebook</span>
                    <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.25rem; display: inline-block; backdrop-filter: blur(10px);">📸 Instagram</span>
                    <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.25rem; display: inline-block; backdrop-filter: blur(10px);">🎥 YouTube</span>
                </div>
            </div>
        </div>
        
        <div style="background: white; padding: 1.5rem; border-radius: 15px; margin-top: 1rem; box-shadow: var(--shadow-medium);">
            <h4 style="color: var(--primary-color); text-align: center; margin-bottom: 1rem;">⚡ Respuesta Rápida Garantizada</h4>
            <p style="text-align: center; color: var(--text-dark);">
                Tiempo promedio de respuesta:<br>
                <strong style="color: var(--success-color); font-size: 1.2rem;">2-4 horas</strong> en horario laboral<br>
                <strong style="color: var(--accent-color); font-size: 1.1rem;">24 horas máximo</strong> fines de semana
            </p>
        </div>
        """, unsafe_allow_html=True)

# Secciones de cuestionarios con diseño profesional avanzado
elif menu == "⚖️ Balance Energético":
    st.markdown("""
    <div class="questionnaire-card animate-fade-in">
        <h1>⚖️ Cuestionario de Balance Energético Óptimo</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">Descubre tu metabolismo y necesidades energéticas personalizadas con precisión científica</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="coming-soon">
        <h3>🚧 Próximamente Disponible - Sistema Avanzado</h3>
        <p>Estamos desarrollando un sistema revolucionario de evaluación metabólica que incluirá tecnología de vanguardia</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="modern-card">
            <h4 style="color: var(--primary-color);">🔬 Evaluaciones Científicas Incluidas</h4>
            <ul style="line-height: 2;">
                <li><strong>Tasa metabólica basal (TMB)</strong> - Cálculo preciso de gasto energético en reposo</li>
                <li><strong>Gasto energético total diario</strong> - Evaluación completa de necesidades calóricas</li>
                <li><strong>Análisis de composición corporal</strong> - Medición detallada de masa muscular y grasa</li>
                <li><strong>Eficiencia metabólica</strong> - Evaluación de adaptaciones metabólicas</li>
                <li><strong>Adaptaciones hormonales</strong> - Análisis de respuestas endocrinas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="modern-card">
            <h4 style="color: var(--secondary-color);">🎯 Resultados Personalizados</h4>
            <ul style="line-height: 2;">
                <li><strong>Calorías óptimas</strong> para tus objetivos específicos de composición corporal</li>
                <li><strong>Distribución de macronutrientes</strong> personalizada según tu metabolismo</li>
                <li><strong>Timing nutricional personalizado</strong> optimizado para tu cronobiología</li>
                <li><strong>Estrategias de periodización</strong> nutricional para máximos resultados</li>
                <li><strong>Monitoreo de progreso</strong> con métricas avanzadas y ajustes dinámicos</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif menu == "🍽️ Preferencias Alimenticias":
    st.markdown("""
    <div class="questionnaire-card animate-fade-in">
        <h1>🍽️ Cuestionario de Patrones Alimenticios</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">Analiza tus hábitos y preferencias para una nutrición personalizada y sostenible</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="coming-soon">
        <h3>🚧 En Desarrollo Avanzado</h3>
        <p>Sistema integral de análisis nutricional personalizado con IA para recomendaciones precisas:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tres columnas para mejor distribución
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="modern-card">
            <h4 style="color: var(--accent-color);">🕒 Patrones Temporales</h4>
            <ul style="line-height: 1.8;">
                <li><strong>Horarios de comida</strong> preferidos y habituales</li>
                <li><strong>Frecuencia alimentaria</strong> óptima para tu estilo de vida</li>
                <li><strong>Ventanas de ayuno</strong> naturales y estratégicas</li>
                <li><strong>Cronotipos nutricionales</strong> según tu reloj biológico</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="modern-card">
            <h4 style="color: var(--success-color);">🥗 Preferencias Personales</h4>
            <ul style="line-height: 1.8;">
                <li><strong>Alimentos favoritos</strong> y grupos alimentarios preferidos</li>
                <li><strong>Restricciones dietéticas</strong> médicas o personales</li>
                <li><strong>Intolerancias alimentarias</strong> conocidas o sospechadas</li>
                <li><strong>Estilos culinarios</strong> y tradiciones culturales</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="modern-card">
            <h4 style="color: var(--secondary-color);">📊 Análisis Nutricional</h4>
            <ul style="line-height: 1.8;">
                <li><strong>Calidad nutricional</strong> de patrones actuales</li>
                <li><strong>Diversidad alimentaria</strong> y variedad de nutrientes</li>
                <li><strong>Hidratación</strong> y hábitos de consumo de líquidos</li>
                <li><strong>Suplementación</strong> necesaria según deficiencias</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif menu == "🍰 Control de Antojos":
    st.markdown("""
    <div class="questionnaire-card animate-fade-in">
        <h1>🍰 Cuestionario de Control de Antojos</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">Maneja inteligentemente tus impulsos alimentarios con estrategias científicamente validadas</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="coming-soon">
        <h3>🚧 Sistema Avanzado en Desarrollo</h3>
        <p>Tecnología de vanguardia para el manejo inteligente de antojos basada en neurociencia nutricional:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid de características mejorado
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin: 2rem 0;">
        <div class="modern-card">
            <h4 style="color: var(--primary-color);">🧠 Análisis Psicológico Profundo</h4>
            <ul style="line-height: 1.8;">
                <li><strong>Triggers emocionales</strong> identificación y mapeo</li>
                <li><strong>Patrones de comportamiento</strong> análisis temporal</li>
                <li><strong>Situaciones de riesgo</strong> predicción y prevención</li>
                <li><strong>Estados de ánimo</strong> correlación con impulsos</li>
            </ul>
        </div>
        
        <div class="modern-card">
            <h4 style="color: var(--secondary-color);">⏰ Análisis Temporal Inteligente</h4>
            <ul style="line-height: 1.8;">
                <li><strong>Momentos críticos</strong> del día más vulnerables</li>
                <li><strong>Frecuencia de antojos</strong> patrones semanales/mensuales</li>
                <li><strong>Duración e intensidad</strong> medición científica</li>
                <li><strong>Patrones cíclicos</strong> hormonales y estacionales</li>
            </ul>
        </div>
        
        <div class="modern-card">
            <h4 style="color: var(--accent-color);">🎯 Estrategias Científicas</h4>
            <ul style="line-height: 1.8;">
                <li><strong>Técnicas de control</strong> basadas en neurociencia</li>
                <li><strong>Alternativas saludables</strong> personalizadas por perfil</li>
                <li><strong>Mindful eating</strong> prácticas de alimentación consciente</li>
                <li><strong>Recompensas adaptativas</strong> sistema de refuerzo positivo</li>
            </ul>
        </div>
        
        <div class="modern-card">
            <h4 style="color: var(--success-color);">📈 Seguimiento Avanzado</h4>
            <ul style="line-height: 1.8;">
                <li><strong>Progreso semanal</strong> medición objetiva de mejoras</li>
                <li><strong>Alertas preventivas</strong> notificaciones inteligentes</li>
                <li><strong>Reportes detallados</strong> análisis de tendencias</li>
                <li><strong>Ajustes dinámicos</strong> estrategias evolutivas</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer espectacular y completo
st.markdown("""
<div class="footer">
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; margin-bottom: 2rem;">
        <div>
            <h4>🤖 MUPAI</h4>
            <p>Entrenamiento Digital del Futuro</p>
            <p style="font-size: 0.9rem; opacity: 0.8;">Revolucionando el fitness con IA y ciencia</p>
        </div>
        <div>
            <h4>🔗 Enlaces Rápidos</h4>
            <p>Inicio • Servicios • Contacto</p>
            <p style="font-size: 0.9rem; opacity: 0.8;">Navegación intuitiva</p>
        </div>
        <div>
            <h4>📞 Contacto Directo</h4>
            <p>contacto@mupai.com<br>+52 123 456 7890</p>
            <p style="font-size: 0.9rem; opacity: 0.8;">Respuesta en 24h máximo</p>
        </div>
        <div>
            <h4>🌟 Síguenos</h4>
            <p>Facebook • Instagram • YouTube</p>
            <p style="font-size: 0.9rem; opacity: 0.8;">Contenido exclusivo diario</p>
        </div>
    </div>
    
    <hr style="border: 1px solid rgba(255,255,255,0.2); margin: 2rem 0;">
    
    <div style="text-align: center;">
        <p style="margin: 0.5rem 0; font-size: 1rem;">© 2024 MUPAI - Entrenamiento Digital. Todos los derechos reservados.</p>
        <p style="margin: 0.5rem 0; opacity: 0.8; font-size: 0.95rem;">🤖 Powered by Science, Technology & AI | Monterrey, México</p>
        <p style="margin: 0.5rem 0; font-size: 0.9rem; opacity: 0.7;">
            Desarrollado con ❤️ por Erick Francisco De Luna Hernández | Última actualización: Junio 2024
        </p>
        <p style="margin: 1rem 0; font-size: 0.8rem; opacity: 0.6;">
            🔬 Respaldado por 50+ estudios científicos | 🏆 500+ transformaciones exitosas | 📱 Disponible 24/7
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
