import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np

# Configuración premium de la página
st.set_page_config(
    page_title="MUPAI - Ciencia del Entrenamiento Digital",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://mupai.com/ayuda',
        'Report a bug': "https://mupai.com/reportar",
        'About': "### MUPAI Premium\nPlataforma de entrenamiento científico digital"
    }
)

# Paleta de colores profesional
COLORS = {
    "primary": "#FFD700",  # Oro premium
    "secondary": "#1A1A1A",  # Negro mate
    "background": "#F8F9FA",  # Fondo claro premium
    "text": "#333333",  # Texto oscuro
    "accent": "#FFC72C",  # Amarillo más cálido
    "success": "#4BB543",
    "info": "#0096FF",
    "warning": "#FFA500",
    "danger": "#FF3333",
    "light": "#FFFFFF",
    "dark": "#121212"
}

# Fuentes y tipografía
FONTS = {
    "title": "'Montserrat', sans-serif",
    "text": "'Open Sans', sans-serif",
    "special": "'Playfair Display', serif"
}

# Efectos visuales
SHADOWS = {
    "small": "0 2px 8px rgba(0,0,0,0.1)",
    "medium": "0 4px 12px rgba(0,0,0,0.15)",
    "large": "0 8px 24px rgba(0,0,0,0.2)"
}

# Estilos CSS premium
@st.cache_data
def aplicar_estilos_premium():
    st.markdown(f"""
    <style>
    /* Importar fuentes de Google */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Open+Sans:wght@400;500;600&family=Playfair+Display:wght@700&display=swap');
    
    /* Reset y estilos base */
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    .stApp {{
        background-color: {COLORS['background']};
        color: {COLORS['text']};
        font-family: {FONTS['text']};
        line-height: 1.6;
    }}
    
    /* Mejorar los headers */
    h1 {{
        font-family: {FONTS['title']};
        font-weight: 700;
        color: {COLORS['secondary']};
        margin-bottom: 1.5rem;
        position: relative;
        padding-bottom: 0.5rem;
    }}
    
    h1:after {{
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 80px;
        height: 4px;
        background: linear-gradient(90deg, {COLORS['primary']}, {COLORS['accent']});
        border-radius: 2px;
    }}
    
    h2 {{
        font-family: {FONTS['title']};
        font-weight: 600;
        color: {COLORS['secondary']};
        margin: 2rem 0 1rem;
    }}
    
    h3 {{
        font-family: {FONTS['title']};
        font-weight: 600;
        color: {COLORS['secondary']};
        margin: 1.5rem 0 0.5rem;
    }}
    
    /* Sidebar premium */
    [data-testid="stSidebar"] {{
        background-color: {COLORS['secondary']} !important;
        color: {COLORS['light']};
    }}
    
    [data-testid="stSidebar"] .stRadio div {{
        color: {COLORS['light']} !important;
    }}
    
    /* Botones premium */
    .stButton>button {{
        background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['accent']});
        color: {COLORS['secondary']};
        border: none;
        border-radius: 8px;
        font-family: {FONTS['title']};
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: {SHADOWS['small']};
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: {SHADOWS['medium']};
        background: linear-gradient(135deg, {COLORS['accent']}, {COLORS['primary']});
    }}
    
    /* Tarjetas premium */
    .card-premium {{
        background: {COLORS['light']};
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: {SHADOWS['small']};
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.1);
        border: 1px solid rgba(0,0,0,0.05);
        height: 100%;
        display: flex;
        flex-direction: column;
    }}
    
    .card-premium:hover {{
        transform: translateY(-8px);
        box-shadow: {SHADOWS['large']};
    }}
    
    .card-premium h3 {{
        font-family: {FONTS['special']};
        font-size: 1.5rem;
        margin-top: 0;
        margin-bottom: 1rem;
        color: {COLORS['secondary']};
    }}
    
    .card-premium-icon {{
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: {COLORS['primary']};
    }}
    
    /* Hero section premium */
    .hero-premium {{
        background: linear-gradient(135deg, {COLORS['secondary']}, #2A2A2A);
        color: white;
        padding: 6rem 2rem;
        border-radius: 16px;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        text-align: center;
    }}
    
    .hero-premium::before {{
        content: "";
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,215,0,0.15) 0%, transparent 70%);
        z-index: 0;
    }}
    
    .hero-content {{
        position: relative;
        z-index: 1;
        max-width: 800px;
        margin: 0 auto;
    }}
    
    .hero-premium h1 {{
        font-size: 3.5rem;
        color: white;
        margin-bottom: 1.5rem;
        font-family: {FONTS['special']};
    }}
    
    .hero-premium h1:after {{
        display: none;
    }}
    
    .hero-premium p {{
        font-size: 1.4rem;
        opacity: 0.9;
        margin-bottom: 2.5rem;
    }}
    
    /* Efectos de animación */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .animate-in {{
        animation: fadeInUp 0.6s ease-out forwards;
        opacity: 0;
        animation-fill-mode: forwards;
    }}
    
    /* Timeline de experiencia */
    .timeline {{
        position: relative;
        max-width: 100%;
        margin: 0 auto;
    }}
    
    .timeline::after {{
        content: '';
        position: absolute;
        width: 4px;
        background: linear-gradient(to bottom, {COLORS['primary']}, {COLORS['accent']});
        top: 0;
        bottom: 0;
        left: 50%;
        margin-left: -2px;
        border-radius: 2px;
    }}
    
    .timeline-item {{
        padding: 10px 40px;
        position: relative;
        width: 50%;
        box-sizing: border-box;
    }}
    
    .timeline-item::after {{
        content: '';
        position: absolute;
        width: 20px;
        height: 20px;
        background: {COLORS['primary']};
        border: 4px solid {COLORS['light']};
        border-radius: 50%;
        top: 15px;
        z-index: 1;
    }}
    
    .left {{
        left: 0;
        text-align: right;
    }}
    
    .right {{
        left: 50%;
        text-align: left;
    }}
    
    .left::after {{
        right: -12px;
    }}
    
    .right::after {{
        left: -12px;
    }}
    
    .timeline-content {{
        padding: 20px;
        background: {COLORS['light']};
        border-radius: 12px;
        box-shadow: {SHADOWS['small']};
    }}
    
    /* Footer premium */
    .footer-premium {{
        background: {COLORS['secondary']};
        color: {COLORS['light']};
        padding: 3rem 2rem;
        border-radius: 16px;
        margin-top: 4rem;
        text-align: center;
    }}
    
    .social-icons {{
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin: 1.5rem 0;
    }}
    
    .social-icon {{
        width: 40px;
        height: 40px;
        background: rgba(255,255,255,0.1);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s;
    }}
    
    .social-icon:hover {{
        background: {COLORS['primary']};
        color: {COLORS['secondary']};
        transform: translateY(-3px);
    }}
    
    /* Responsive design */
    @media (max-width: 768px) {{
        .timeline::after {{
            left: 31px;
        }}
        
        .timeline-item {{
            width: 100%;
            padding-left: 70px;
            padding-right: 25px;
        }}
        
        .timeline-item::after {{
            left: 21px;
        }}
        
        .left, .right {{
            left: 0;
            text-align: left;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

# Componente de tarjeta premium
def card_premium(title, content, icon=None, delay=0):
    icon_html = f"<div class='card-premium-icon'>{icon}</div>" if icon else ""
    st.markdown(f"""
    <div class='card-premium animate-in' style='animation-delay: {delay}ms;'>
        {icon_html}
        <h3>{title}</h3>
        {content}
    </div>
    """, unsafe_allow_html=True)

# Hero section premium
def hero_section():
    st.markdown(f"""
    <div class='hero-premium'>
        <div class='hero-content'>
            <h1>Transforma tu Rendimiento con Ciencia</h1>
            <p>Entrenamiento digital personalizado basado en evidencia científica</p>
            <div style='display: flex; gap: 1rem; justify-content: center;'>
                <a href='#servicios' style='
                    background: {COLORS['primary']};
                    color: {COLORS['secondary']};
                    padding: 0.8rem 1.8rem;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: 600;
                    font-family: {FONTS['title']};
                    transition: all 0.3s;
                    box-shadow: {SHADOWS['small']};
                '>Nuestros Servicios</a>
                <a href='#contacto' style='
                    background: transparent;
                    color: white;
                    padding: 0.8rem 1.8rem;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: 600;
                    font-family: {FONTS['title']};
                    transition: all 0.3s;
                    border: 2px solid {COLORS['primary']};
                '>Contacto</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Página de Inicio Premium
def pagina_inicio_premium():
    hero_section()
    
    # Sección de identidad
    st.header("🏆 Nuestra Identidad", anchor="identidad")
    
    cols = st.columns(2)
    with cols[0]:
        card_premium(
            "Misión",
            """
            <p>Hacer accesible el entrenamiento basado en ciencia mediante soluciones digitales 
            personalizadas que integren inteligencia artificial, investigación de vanguardia y 
            metodologías probadas.</p>
            """,
            "🌟",
            100
        )
        
        card_premium(
            "Valores",
            """
            <ul style='margin-left: 1rem;'>
                <li><strong>Excelencia:</strong> En cada detalle de nuestro servicio</li>
                <li><strong>Innovación:</strong> Siempre a la vanguardia tecnológica</li>
                <li><strong>Integridad:</strong> Transparencia en nuestras metodologías</li>
            </ul>
            """,
            "💎",
            300
        )
    
    with cols[1]:
        card_premium(
            "Visión",
            """
            <p>Ser líderes globales en entrenamiento digital científico, transformando la 
            experiencia del fitness mediante tecnología avanzada que democratice el acceso 
            a metodologías de elite.</p>
            """,
            "🌍",
            200
        )
        
        card_premium(
            "Compromiso",
            """
            <p>Garantizar que cada plan de entrenamiento esté respaldado por evidencia 
            científica y adaptado a las necesidades individuales de cada usuario.</p>
            """,
            "🤝",
            400
        )
    
    # Sección de servicios con pestañas
    st.header("💎 Nuestros Servicios Premium", anchor="servicios")
    
    tabs = st.tabs(["🏋️‍♂️ Entrenamiento", "📊 Evaluación", "🧘 Bienestar"])
    
    with tabs[0]:
        cols = st.columns(3)
        with cols[0]:
            card_premium(
                "Planes Personalizados",
                "Programas 100% adaptados a tus objetivos y capacidades",
                "📝",
                100
            )
        with cols[1]:
            card_premium(
                "Periodización Avanzada",
                "Estructuración científica de tu entrenamiento a largo plazo",
                "📅",
                200
            )
        with cols[2]:
            card_premium(
                "Ajuste Automático",
                "Planes que evolucionan con tu progreso",
                "🔄",
                300
            )
    
    with tabs[1]:
        cols = st.columns(3)
        with cols[0]:
            card_premium(
                "Composición Corporal",
                "Análisis avanzado de masa muscular y grasa corporal",
                "📏",
                100
            )
        with cols[1]:
            card_premium(
                "Rendimiento Físico",
                "Evaluación de capacidades y limitaciones",
                "⚡",
                200
            )
        with cols[2]:
            card_premium(
                "Biomecánica",
                "Análisis de movimiento y técnica",
                "👟",
                300
            )
    
    with tabs[2]:
        cols = st.columns(3)
        with cols[0]:
            card_premium(
                "Gestión del Estrés",
                "Técnicas basadas en evidencia científica",
                "😌",
                100
            )
        with cols[1]:
            card_premium(
                "Optimización del Sueño",
                "Mejora tu recuperación con ciencia",
                "🌙",
                200
            )
        with cols[2]:
            card_premium(
                "Nutrición Personalizada",
                "Planes alimenticios para tus objetivos",
                "🍎",
                300
            )

# Página "Sobre Mí" Premium
def pagina_sobre_mi_premium():
    st.header("👨‍🔬 Erick De Luna - Fundador")
    
    # Perfil con columnas
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style='text-align: center;'>
            <img src='https://images.unsplash.com/photo-1583864697784-a0efc8379f70?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=880&q=80' 
                 style='width: 100%; border-radius: 16px; border: 4px solid #FFD700; margin-bottom: 1rem;'>
            <h3 style='font-family: {FONTS["special"]};'>Erick Francisco De Luna</h3>
            <p style='color: {COLORS["primary"]}; font-weight: 600;'>Científico del Ejercicio</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: {COLORS["light"]}; padding: 2rem; border-radius: 16px; box-shadow: {SHADOWS["small"]};'>
            <h2 style='font-family: {FONTS["special"]}; margin-top: 0;'>Biografía Profesional</h2>
            <p>Con más de 10 años de experiencia en ciencias del ejercicio, Erick ha dedicado su carrera 
            a desarrollar metodologías innovadoras que integran la investigación científica con aplicaciones 
            prácticas para atletas y entusiastas del fitness.</p>
            <p>Su enfoque multidisciplinario combina conocimientos avanzados en fisiología, biomecánica 
            y psicología del deporte para crear soluciones de entrenamiento integrales.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Experiencia con timeline interactivo
    st.header("📜 Trayectoria Profesional")
    
    st.markdown("""
    <div class='timeline'>
        <div class='timeline-item left animate-in' style='animation-delay: 100ms;'>
            <div class='timeline-content'>
                <h3>Football Science Institute</h3>
                <p><strong>Maestría en Fuerza y Acondicionamiento</strong></p>
                <p>2020-2022</p>
                <p>Investigación aplicada al alto rendimiento deportivo</p>
            </div>
        </div>
        
        <div class='timeline-item right animate-in' style='animation-delay: 200ms;'>
            <div class='timeline-content'>
                <h3>Muscle Up Gym</h3>
                <p><strong>Diseñador de Metodologías</strong></p>
                <p>2018-2020</p>
                <p>Desarrollo de 15+ protocolos de entrenamiento</p>
            </div>
        </div>
        
        <div class='timeline-item left animate-in' style='animation-delay: 300ms;'>
            <div class='timeline-content'>
                <h3>UANL</h3>
                <p><strong>Investigador en Rendimiento Humano</strong></p>
                <p>2016-2018</p>
                <p>5 publicaciones indexadas en revistas científicas</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Logros con columnas
    st.header("🏆 Logros y Reconocimientos")
    
    cols = st.columns(2)
    with cols[0]:
        card_premium(
            "Premios Académicos",
            """
            <ul>
                <li>Premio al Mérito Académico UANL</li>
                <li>Primer Lugar de Generación</li>
                <li>Beca de Excelencia para intercambio</li>
            </ul>
            """,
            "🎓"
        )
    
    with cols[1]:
        card_premium(
            "Publicaciones",
            """
            <ul>
                <li>Métodos innovadores en entrenamiento</li>
                <li>Análisis de rendimiento físico</li>
                <li>Estudios de composición corporal</li>
            </ul>
            """,
            "📚"
        )
    
    # Filosofía con cita destacada
    st.header("🧠 Filosofía de Entrenamiento")
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, {COLORS["secondary"]}, #2A2A2A);
        color: white;
        padding: 3rem;
        border-radius: 16px;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    '>
        <div style='
            position: absolute;
            top: 20px;
            left: 20px;
            font-size: 5rem;
            opacity: 0.1;
            color: {COLORS["primary"]};
        '>❝</div>
        
        <div style='
            position: relative;
            z-index: 1;
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        '>
            <p style='
                font-size: 1.5rem;
                font-style: italic;
                margin-bottom: 1.5rem;
                line-height: 1.6;
            '>
                "Creo en el poder transformador del entrenamiento científico. Cada individuo 
                tiene necesidades únicas que requieren soluciones personalizadas basadas en 
                evidencia, no en modas pasajeras."
            </p>
            <p style='font-weight: 600;'>— Erick De Luna</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Página de Contacto Premium
def pagina_contacto_premium():
    st.header("📬 Contacto Premium", anchor="contacto")
    
    cols = st.columns(2)
    
    with cols[0]:
        card_premium(
            "Información de Contacto",
            f"""
            <div style='margin-bottom: 1.5rem;'>
                <p style='display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;'>
                    <span style='font-size: 1.2rem;'>📧</span>
                    <span><strong>Email:</strong> contacto@mupai.com</span>
                </p>
                <p style='display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;'>
                    <span style='font-size: 1.2rem;'>📱</span>
                    <span><strong>Teléfono:</strong> +52 866 258 05 94</span>
                </p>
                <p style='display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;'>
                    <span style='font-size: 1.2rem;'>📍</span>
                    <span><strong>Ubicación:</strong> Monterrey, México</span>
                </p>
            </div>
            
            <h4 style='margin-bottom: 0.5rem;'>Horario de Atención</h4>
            <p>Lunes a Viernes: 9:00 - 18:00</p>
            <p>Sábados: 10:00 - 14:00</p>
            """,
            "📌"
        )
        
        # Mapa de ubicación (simulado)
        st.markdown("""
        <div style='
            background: #eee;
            border-radius: 16px;
            height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: 1rem;
            overflow: hidden;
            position: relative;
        '>
            <img src='https://maps.googleapis.com/maps/api/staticmap?center=Monterrey,Mexico&zoom=13&size=600x300&maptype=roadmap&markers=color:red%7CMonterrey,Mexico&key=YOUR_API_KEY' 
                 style='width: 100%; height: 100%; object-fit: cover;'>
            <div style='
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.3);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
                font-size: 1.2rem;
            '>
                Ubicación en Monterrey, México
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        with st.form("contact_form_premium", clear_on_submit=True):
            st.markdown("### ✨ Envíanos un Mensaje")
            
            nombre = st.text_input("Nombre completo*", placeholder="Tu nombre completo")
            email = st.text_input("Correo electrónico*", placeholder="tu@email.com")
            telefono = st.text_input("Teléfono", placeholder="+52 123 456 7890")
            servicio_interes = st.selectbox(
                "Servicio de interés",
                ["Evaluación física", "Plan de entrenamiento", "Asesoría nutricional", "Otro"]
            )
            mensaje = st.text_area("Mensaje*", placeholder="Describe tus necesidades...", height=150)
            
            # Checkbox para newsletter
            newsletter = st.checkbox("Deseo suscribirme al boletín informativo")
            
            submitted = st.form_submit_button("Enviar Mensaje", type="primary")
            
            if submitted:
                if not nombre or not email or not mensaje:
                    st.error("Por favor completa los campos obligatorios (*)")
                elif "@" not in email or "." not in email:
                    st.error("Por favor ingresa un email válido")
                else:
                    # Simular envío
                    with st.spinner("Enviando tu mensaje..."):
                        st.balloons()
                        st.success("¡Mensaje enviado con éxito!")
                        
                        # Mostrar resumen
                        with st.expander("Ver resumen de tu mensaje"):
                            st.json({
                                "nombre": nombre,
                                "email": email,
                                "telefono": telefono if telefono else "No proporcionado",
                                "servicio_interes": servicio_interes,
                                "newsletter": "Sí" if newsletter else "No",
                                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
                            })

# Footer Premium
def footer_premium():
    st.markdown(f"""
    <div class='footer-premium'>
        <div style='max-width: 800px; margin: 0 auto;'>
            <img src='https://via.placeholder.com/200x60/000000/FFFFFF?text=MUPAI+PREMIUM' 
                 style='max-width: 200px; margin-bottom: 1rem;'>
            <p style='margin-bottom: 1.5rem;'>Ciencia aplicada al rendimiento humano</p>
            
            <div class='social-icons'>
                <a href='#' class='social-icon'>📱</a>
                <a href='#' class='social-icon'>📸</a>
                <a href='#' class='social-icon'>🔗</a>
                <a href='#' class='social-icon'>📧</a>
            </div>
            
            <div style='display: flex; justify-content: center; gap: 1.5rem; margin: 1.5rem 0;'>
                <a href='#' style='color: {COLORS["light"]}; text-decoration: none;'>Inicio</a>
                <a href='#' style='color: {COLORS["light"]}; text-decoration: none;'>Servicios</a>
                <a href='#' style='color: {COLORS["light"]}; text-decoration: none;'>Sobre Mí</a>
                <a href='#' style='color: {COLORS["light"]}; text-decoration: none;'>Contacto</a>
            </div>
            
            <p style='font-size: 0.9rem; opacity: 0.8; margin-bottom: 0.5rem;'>
                © {datetime.now().year} MUPAI Premium. Todos los derechos reservados.
            </p>
            <p style='font-size: 0.8rem; opacity: 0.6; margin-bottom: 0;'>
                Ciencia del ejercicio aplicada a tu rendimiento
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar Premium
def sidebar_premium():
    with st.sidebar:
        st.markdown(f"""
        <div style='
            text-align: center; 
            padding: 1rem 0 2rem;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 1.5rem;
        '>
            <img src='https://via.placeholder.com/180x60/FFFFFF/000000?text=MUPAI+PRO' 
                 style='max-width: 180px; margin-bottom: 0.5rem;'>
            <p style='
                color: {COLORS["primary"]}; 
                font-weight: 600; 
                letter-spacing: 1px;
                margin: 0;
            '>DIGITAL TRAINING SCIENCE</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Menú de navegación
        menu_options = {
            "🏠 Inicio": pagina_inicio_premium,
            "👨‍🔬 Sobre Mí": pagina_sobre_mi_premium,
            "📬 Contacto": pagina_contacto_premium
        }
        
        selected = st.radio(
            "Navegación Principal",
            list(menu_options.keys()),
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Widget de suscripción
        with st.expander("💌 Boletín Científico", expanded=False):
            with st.form("sidebar_newsletter"):
                email = st.text_input("Tu email profesional", placeholder="email@ejemplo.com")
                if st.form_submit_button("Suscribirme →"):
                    if email and "@" in email:
                        st.success("¡Gracias por suscribirte!")
                    else:
                        st.warning("Ingresa un email válido")
        
        st.markdown("---")
        
        # Badge de certificación
        st.markdown(f"""
        <div style='
            background: rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            margin: 1rem 0;
        '>
            <div style='
                font-size: 2rem;
                margin-bottom: 0.5rem;
                color: {COLORS["primary"]};
            '>🔬</div>
            <p style='
                font-size: 0.9rem;
                margin-bottom: 0;
                color: white;
            '>Certificado en Ciencias del Ejercicio</p>
        </div>
        """, unsafe_allow_html=True)
        
        return menu_options[selected]

# Función principal
def main():
    aplicar_estilos_premium()
    
    # Sistema de navegación premium
    page_func = sidebar_premium()
    
    # Mostrar página seleccionada
    page_func()
    
    # Mostrar footer premium
    footer_premium()

if __name__ == "__main__":
    main()
