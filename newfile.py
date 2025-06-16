import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="MUPAI - Entrenamiento Digital",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar el diseño
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .section-header {
        color: #2e86ab;
        border-bottom: 3px solid #2e86ab;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
        font-size: 2rem;
    }
    
    .mission-vision-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .policy-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .service-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .contact-info {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .about-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #2e86ab;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Barra lateral de navegación con iconos
st.sidebar.markdown("## 🚀 **NAVEGACIÓN**")
menu = st.sidebar.selectbox(
    "Selecciona una opción:",
    [
        "🏠 Inicio", 
        "👨‍💼 Sobre Mí", 
        "💼 Servicios", 
        "📞 Contacto",
        "⚖️ Cuestionario para determinar balance energético óptimo",
        "🍽️ Cuestionario de patrones y preferencias alimenticias", 
        "🍰 Cuestionario acerca de antojos por comidas"
    ]
)

# Contenido según la selección del menú
if menu == "🏠 Inicio":
    # Logo centrado
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try:
        st.image("LOGO.png", width=400)
    except:
        st.info("📸 Logo no encontrado. Coloca tu archivo LOGO.png en el directorio de la aplicación.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Título principal
    st.markdown('<h1 class="main-header">Bienvenido a MUPAI</h1>', unsafe_allow_html=True)
    
    # Métricas destacadas
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🎯 Clientes Satisfechos",
            value="500+",
            delta="En crecimiento"
        )
    
    with col2:
        st.metric(
            label="📋 Programas Diseñados", 
            value="1000+",
            delta="Basados en ciencia"
        )
    
    with col3:
        st.metric(
            label="🏆 Años de Experiencia",
            value="5+",
            delta="Comprobada"
        )
    
    with col4:
        st.metric(
            label="🔬 Investigaciones",
            value="50+",
            delta="Aplicadas"
        )

    st.markdown("---")

    # Contenido en pestañas
    tab1, tab2 = st.tabs(["🎯 **Misión & Visión**", "📋 **Políticas**"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="mission-vision-card">
                <h2>🎯 Misión</h2>
                <p>Hacer accesible el entrenamiento basado en ciencia, proporcionando planes completamente personalizados a través de herramientas digitales respaldadas por inteligencia artificial, datos precisos y la investigación más actualizada en ciencias del ejercicio. Nos enfocamos en promover el desarrollo integral de nuestros usuarios y su bienestar físico y mental.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="mission-vision-card">
                <h2>🔮 Visión</h2>
                <p>Convertirnos en uno de los máximos referentes a nivel global en entrenamiento digital personalizado, aprovechando las nuevas tecnologías para hacer más accesible el fitness basado en ciencia. Aspiramos a transformar la experiencia del entrenamiento físico, integrando inteligencia artificial, investigación científica y herramientas digitales avanzadas que permitan a cualquier persona alcanzar su máximo potencial.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="policy-card">
            <h2>📜 Política</h2>
            <p>En <strong>MUPAI</strong>, nuestra política está fundamentada en el compromiso con la excelencia, la ética y el servicio centrado en el usuario. Actuamos con responsabilidad y transparencia para ofrecer soluciones tecnológicas que integren ciencia, personalización y accesibilidad, contribuyendo al bienestar integral de quienes confían en nosotros.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="policy-card">
            <h2>🛡️ Política del Servicio</h2>
            <p>En <strong>MUPAI</strong>, guiamos nuestras acciones por los siguientes principios:</p>
            <ul>
                <li>🔬 Diseñamos entrenamientos digitales que combinan personalización, datos confiables y ciencia del ejercicio.</li>
                <li>💻 Aprovechamos la tecnología para ofrecer un servicio accesible y adaptable a las necesidades de cada usuario.</li>
                <li>🔐 Respetamos y protegemos la privacidad de los datos personales, garantizando su uso responsable.</li>
                <li>🚀 Innovamos de forma continua para mejorar la experiencia y los resultados de nuestros usuarios.</li>
                <li>💪 Promovemos valores como el esfuerzo, la constancia y el respeto en cada interacción, fomentando un ambiente de crecimiento y bienestar.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif menu == "👨‍💼 Sobre Mí":
    st.markdown('<h1 class="section-header">👨‍💼 Sobre Mí</h1>', unsafe_allow_html=True)
    
    # Información personal en un contenedor estilizado
    st.markdown("""
    <div class="about-section">
        <h3>🎓 Erick Francisco De Luna Hernández</h3>
        <p><strong>Profesional en Fitness y Ciencias del Ejercicio</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Información dividida en pestañas
    tab1, tab2, tab3 = st.tabs(["📚 **Formación Académica**", "💼 **Experiencia**", "🏆 **Logros**"])
    
    with tab1:
        st.markdown("""
        ### 🎓 Educación Superior
        - **Maestría en Fuerza y Acondicionamiento** - Football Science Institute
        - **Licenciatura en Ciencias del Ejercicio** - Universidad Autónoma de Nuevo León (UANL)
        - **Intercambio Académico Internacional** - Universidad de Sevilla
        - **Miembro del Programa de Talento Universitario** - UANL
        """)
    
    with tab2:
        st.markdown("""
        ### 💼 Experiencia Profesional
        - **Muscle Up Gym** - Diseño y desarrollo de programas de entrenamiento
        - **Laboratorio de Rendimiento Humano UANL** - Evaluaciones de fuerza, biomecánica y acondicionamiento físico
        - **Especialización en metodologías personalizadas** basadas en evidencia científica
        """)
    
    with tab3:
        st.markdown("""
        ### 🏆 Reconocimientos
        - 🥇 **Premio al Mérito Académico** - UANL
        - 🥇 **Primer Lugar de Generación** - Facultad de Organización Deportiva
        - 🌍 **Beca completa para intercambio internacional** - Universidad de Sevilla
        """)

    st.markdown("---")
    
    # Galería de imágenes mejorada
    st.markdown('<h2 class="section-header">📸 Galería de Imágenes</h2>', unsafe_allow_html=True)
    
    images = [
        "FB_IMG_1734820693317.jpg",
        "FB_IMG_1734820729323.jpg", 
        "FB_IMG_1734820709707.jpg",
        "FB_IMG_1734820808186.jpg",
        "FB_IMG_1734820712642.jpg"
    ]
    
    # Crear filas de imágenes con mejor distribución
    for i in range(0, len(images), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(images):
                with col:
                    try:
                        st.image(images[i + j], use_container_width=True, caption=f"Imagen {i + j + 1}")
                    except:
                        st.info(f"📸 Imagen {images[i + j]} no encontrada")

elif menu == "💼 Servicios":
    st.markdown('<h1 class="section-header">💼 Nuestros Servicios</h1>', unsafe_allow_html=True)
    
    # Servicios en tarjetas
    services = [
        {
            "icon": "🎯",
            "title": "Planes de Entrenamiento Individualizados",
            "description": "Programas completamente personalizados basados en tu perfil, objetivos y capacidades físicas."
        },
        {
            "icon": "🧠",
            "title": "Programas de Mejora Física y Mental", 
            "description": "Enfoque integral que combina entrenamiento físico con bienestar mental y emocional."
        },
        {
            "icon": "🥗",
            "title": "Asesoría en Nutrición Deportiva",
            "description": "Planes nutricionales científicamente diseñados para optimizar tu rendimiento y recuperación."
        },
        {
            "icon": "📊",
            "title": "Consultoría en Rendimiento Deportivo",
            "description": "Análisis avanzado y estrategias para maximizar tu potencial atlético y competitivo."
        }
    ]
    
    for i, service in enumerate(services):
        if i % 2 == 0:
            col1, col2 = st.columns(2)
            cols = [col1, col2]
        
        with cols[i % 2]:
            st.markdown(f"""
            <div class="service-card">
                <h3>{service['icon']} {service['title']}</h3>
                <p>{service['description']}</p>
            </div>
            """, unsafe_allow_html=True)

elif menu == "📞 Contacto":
    st.markdown('<h1 class="section-header">📞 Contacto</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Envíanos un mensaje")
        
        # Formulario de contacto
        with st.form("contact_form"):
            name = st.text_input("👤 Nombre completo")
            email = st.text_input("📧 Correo electrónico")
            phone = st.text_input("📱 Teléfono (opcional)")
            service = st.selectbox(
                "🎯 Servicio de interés",
                ["Entrenamiento Personalizado", "Nutrición Deportiva", "Consultoría", "Información General"]
            )
            message = st.text_area("💬 Mensaje", height=150)
            submit = st.form_submit_button("🚀 Enviar Mensaje", use_container_width=True)
            
            if submit:
                if name and email and message:
                    st.success("✅ ¡Mensaje enviado exitosamente! Te contactaremos pronto.")
                else:
                    st.error("❌ Por favor completa todos los campos obligatorios.")
    
    with col2:
        st.markdown("""
        <div class="contact-info">
            <h3>📍 Información de Contacto</h3>
            <p><strong>📧 Email:</strong><br>contacto@mupai.com</p>
            <p><strong>📱 Teléfono:</strong><br>+52 123 456 7890</p>
            <p><strong>🏢 Ubicación:</strong><br>Monterrey, Nuevo León</p>
            <p><strong>🕒 Horarios:</strong><br>Lun-Vie: 8:00-18:00<br>Sáb: 9:00-14:00</p>
        </div>
        """, unsafe_allow_html=True)

# Nuevas secciones de cuestionarios (placeholders)
elif menu == "⚖️ Cuestionario para determinar balance energético óptimo":
    st.markdown('<h1 class="section-header">⚖️ Balance Energético Óptimo</h1>', unsafe_allow_html=True)
    st.info("🚧 Esta sección está en desarrollo. Próximamente podrás acceder al cuestionario personalizado para determinar tu balance energético óptimo.")
    
    # Placeholder content
    st.markdown("""
    ### 🎯 ¿Qué evaluaremos?
    - Metabolismo basal y gasto energético
    - Nivel de actividad física
    - Objetivos de composición corporal
    - Factores individuales que afectan el balance energético
    """)

elif menu == "🍽️ Cuestionario de patrones y preferencias alimenticias":
    st.markdown('<h1 class="section-header">🍽️ Patrones y Preferencias Alimenticias</h1>', unsafe_allow_html=True)
    st.info("🚧 Esta sección está en desarrollo. Próximamente podrás completar el cuestionario sobre tus hábitos alimentarios.")
    
    # Placeholder content
    st.markdown("""
    ### 🍎 ¿Qué analizaremos?
    - Horarios de comida habituales
    - Preferencias alimentarias
    - Restricciones dietéticas
    - Patrones de hidratación
    """)

elif menu == "🍰 Cuestionario acerca de antojos por comidas":
    st.markdown('<h1 class="section-header">🍰 Antojos por Comidas</h1>', unsafe_allow_html=True)
    st.info("🚧 Esta sección está en desarrollo. Próximamente podrás evaluar tus patrones de antojos alimentarios.")
    
    # Placeholder content
    st.markdown("""
    ### 🧠 ¿Qué evaluaremos?
    - Tipos de antojos más frecuentes
    - Momentos del día con mayor intensidad
    - Factores desencadenantes
    - Estrategias de manejo actuales
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>© 2024 MUPAI - Entrenamiento Digital. Todos los derechos reservados.</p>
    <p>🤖 Powered by Science & Technology</p>
</div>
""", unsafe_allow_html=True)
