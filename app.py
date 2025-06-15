import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF

# Configuración de la página con colores personalizados
st.set_page_config(
    page_title="MUPAI - Entrenamiento Digital",
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
    }}
    
    /* Barra lateral */
    .css-1d391kg {{
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
    }}
    
    .stButton>button:hover {{
        background-color: {ACCENT_COLOR};
        color: {SECONDARY_COLOR};
        border: 2px solid {SECONDARY_COLOR};
    }}
    
    /* Títulos */
    h1 {{
        color: {SECONDARY_COLOR};
        border-bottom: 3px solid {PRIMARY_COLOR};
        padding-bottom: 10px;
    }}
    
    h2 {{
        color: {SECONDARY_COLOR};
    }}
    
    /* Widgets */
    .stTextInput>div>div>input, 
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {{
        border: 2px solid {SECONDARY_COLOR} !important;
    }}
    
    /* Tarjetas */
    .card {{
        background-color: {BACKGROUND_COLOR};
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-left: 5px solid {PRIMARY_COLOR};
    }}
    
    /* Hero Section */
    .hero {{
        background: linear-gradient(135deg, {SECONDARY_COLOR} 0%, #333333 100%);
        color: white;
        padding: 3rem;
        border-radius: 15px;
        margin-bottom: 2rem;
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
        opacity: 0.2;
        z-index: 0;
    }}
    
    .hero-content {{
        position: relative;
        z-index: 1;
    }}
    
    /* Animaciones */
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
    }}
    
    .pulse {{
        animation: pulse 2s infinite;
    }}
    </style>
    """, unsafe_allow_html=True)

# Logo y cabecera con diseño mejorado
def mostrar_cabecera():
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("LOGO.png", width=150)
    with col2:
        st.markdown(f"""
        <h1 style='color:{SECONDARY_COLOR};'>MUPAI <span style='color:{PRIMARY_COLOR};'>Digital Training Science</span></h1>
        <p style='font-size:18px;color:{TEXT_COLOR};'>Ciencia aplicada al rendimiento humano</p>
        """, unsafe_allow_html=True)

# Menú lateral con diseño moderno
def mostrar_menu():
    with st.sidebar:
        st.image("LOGO.png", width=120)
        st.markdown(f"""
        <div style='background-color:{PRIMARY_COLOR};padding:10px;border-radius:8px;margin-bottom:20px;'>
            <h3 style='color:{SECONDARY_COLOR};text-align:center;'>Menú de Navegación</h3>
        </div>
        """, unsafe_allow_html=True)
        
        menu = st.radio(
            "",
            ["🏠 Inicio", "👤 Sobre Mí", "🔬 Evaluaciones", "📊 Resultados", "💼 Servicios", "📞 Contacto"],
            label_visibility="collapsed"
        )
        return menu

# Página de Inicio con diseño impactante
def pagina_inicio():
    # Hero Section
    st.markdown(f"""
    <div class='hero'>
        <div class='hero-content'>
            <h2 style='color:white;'>Transforma tu rendimiento con ciencia</h2>
            <p style='font-size:18px;color:white;'>La plataforma más avanzada de evaluación y entrenamiento basada en evidencia científica</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tarjetas de características
    st.subheader("🚀 ¿Por qué elegir MUPAI?")
    cols = st.columns(3)
    with cols[0]:
        st.markdown(f"""
        <div class='card'>
            <h3 style='color:{SECONDARY_COLOR};'>🔬 Basado en Ciencia</h3>
            <p>Métodos validados científicamente para garantizar resultados reales.</p>
        </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"""
        <div class='card pulse'>
            <h3 style='color:{SECONDARY_COLOR};'>🎯 Personalizado</h3>
            <p>Planes adaptados a tus necesidades y objetivos específicos.</p>
        </div>
        """, unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f"""
        <div class='card'>
            <h3 style='color:{SECONDARY_COLOR};'>📱 Tecnología Avanzada</h3>
            <p>Plataforma digital con seguimiento en tiempo real.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Misión y Visión
    with st.expander(f"🌟 NUESTRA MISIÓN", expanded=True):
        st.markdown(f"""
        <div style='background-color:{PRIMARY_COLOR}20;padding:15px;border-radius:10px;border-left:4px solid {PRIMARY_COLOR};'>
            <p style='font-size:16px;'>Hacer accesible el entrenamiento basado en ciencia, proporcionando planes completamente personalizados 
            a través de herramientas digitales respaldadas por inteligencia artificial, datos precisos y la 
            investigación más actualizada en ciencias del ejercicio.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Evaluaciones disponibles
    st.subheader("📊 Evaluaciones Disponibles")
    evaluaciones = {
        "💪 Composición Corporal": "Análisis detallado de tu físico y potencial genético",
        "😰 Estrés Percibido": "Evaluación de tus niveles de estrés y su impacto",
        "🌙 Calidad del Sueño": "Análisis de patrones y calidad de descanso",
        "🏃 Nivel de Actividad": "Medición de tu actividad física diaria",
        "🍎 Hábitos Alimenticios": "Evaluación nutricional completa"
    }
    
    for eval, desc in evaluaciones.items():
        st.markdown(f"""
        <div style='background-color:{BACKGROUND_COLOR};border:2px solid {PRIMARY_COLOR};border-radius:10px;
                    padding:15px;margin-bottom:10px;display:flex;align-items:center;'>
            <div style='font-size:24px;margin-right:15px;'>{eval.split()[0]}</div>
            <div>
                <h4 style='color:{SECONDARY_COLOR};margin:0;'>{' '.join(eval.split()[1:])}</h4>
                <p style='margin:0;color:{TEXT_COLOR};'>{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Página "Sobre Mí" con diseño profesional
def pagina_sobre_mi():
    st.header(f"👤 <span style='color:{PRIMARY_COLOR};'>ERICK FRANCISCO DE LUNA HERNÁNDEZ</span>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Perfil con foto
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("tu_foto.jpg", width=200)
    with col2:
        st.markdown(f"""
        <div style='background-color:{PRIMARY_COLOR}10;padding:20px;border-radius:10px;border-left:4px solid {PRIMARY_COLOR};'>
            <h3 style='color:{SECONDARY_COLOR};margin-top:0;'>Formación Académica</h3>
            <p>🎓 <strong>Maestría en Fuerza y Acondicionamiento</strong> - Football Science Institute</p>
            <p>📚 <strong>Licenciatura en Ciencias del Ejercicio</strong> - UANL</p>
            <p>🌍 <strong>Intercambio académico</strong> - Universidad de Sevilla</p>
            
            <h3 style='color:{SECONDARY_COLOR};'>Experiencia Profesional</h3>
            <p>💼 <strong>Diseñador de metodologías de entrenamiento</strong> - Muscle Up Gym</p>
            <p>🔬 <strong>Investigador en Laboratorio de Rendimiento Humano</strong> - UANL</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Logros y reconocimientos
    st.markdown("---")
    st.subheader(f"🏆 <span style='color:{PRIMARY_COLOR};'>Logros y Reconocimientos</span>", unsafe_allow_html=True)
    
    cols = st.columns(2)
    with cols[0]:
        st.markdown(f"""
        <div style='background-color:{PRIMARY_COLOR}10;padding:15px;border-radius:10px;margin-bottom:15px;'>
            <h4 style='color:{SECONDARY_COLOR};margin-top:0;'>Premios Académicos</h4>
            <p>🥇 Premio al Mérito Académico UANL</p>
            <p>🏅 Primer Lugar de Generación</p>
            <p>🎖️ Beca completa para intercambio</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown(f"""
        <div style='background-color:{PRIMARY_COLOR}10;padding:15px;border-radius:10px;margin-bottom:15px;'>
            <h4 style='color:{SECONDARY_COLOR};margin-top:0;'>Publicaciones</h4>
            <p>📄 Métodos innovadores en entrenamiento</p>
            <p>📊 Análisis de rendimiento deportivo</p>
            <p>🔍 Estudios sobre composición corporal</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Galería de imágenes - CORRECCIÓN APLICADA AQUÍ
    st.markdown("---")
    st.subheader(f"📷 <span style='color:{PRIMARY_COLOR};'>Galería</span>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    gallery_images = [
        "FB_IMG_1734820693317.jpg",
        "FB_IMG_1734820729323.jpg",
        "FB_IMG_1734820709707.jpg"
    ]
    
    for idx, col in enumerate(cols):
        with col:
            # USO CORRECTO DE use_container_width
            st.image(gallery_images[idx], use_container_width=True)
            st.caption(f"Imagen {idx+1}: Evento profesional")

# Página de evaluaciones con diseño moderno
def pagina_evaluaciones():
    st.header(f"🔬 <span style='color:{PRIMARY_COLOR};'>Evaluaciones Científicas</span>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Selector de evaluaciones
    evaluacion = st.selectbox(
        "Selecciona una evaluación:",
        [
            "Composición Corporal y Potencial Genético",
            "Escala de Estrés Percibido (PSS)",
            "Índice de Calidad de Sueño (PSQI)",
            "Cuestionario de Actividad Física (IPAQ)",
            "Hábitos Alimenticios"
        ]
    )
    
    st.markdown(f"""
    <div style='background-color:{PRIMARY_COLOR}10;padding:20px;border-radius:10px;border-left:4px solid {PRIMARY_COLOR};margin-top:20px;'>
        <h3 style='color:{SECONDARY_COLOR};margin-top:0;'>{evaluacion}</h3>
    """, unsafe_allow_html=True)
    
    if evaluacion == "Composición Corporal y Potencial Genético":
        # Implementar cuestionario con estilo
        genero = st.radio("Género:", ["Hombre", "Mujer"], horizontal=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            altura = st.number_input("Altura (cm)", min_value=140, max_value=220, value=175)
        with col2:
            peso = st.number_input("Peso (kg)", min_value=40, max_value=150, value=70)
        with col3:
            grasa_corporal = st.slider("Grasa corporal (%)", min_value=5, max_value=50, value=20)
        
        if st.button("Calcular Potencial", key="calc_potencial"):
            with st.spinner("Analizando tus datos..."):
                # Simulación de cálculo
                import time
                time.sleep(2)
                
                st.markdown(f"""
                <div style='background-color:{PRIMARY_COLOR}20;padding:20px;border-radius:10px;margin-top:20px;'>
                    <h4 style='color:{SECONDARY_COLOR};margin-top:0;'>Resultados</h4>
                    <p>📏 <strong>FFMI:</strong> 22.5 (Índice de Masa Libre de Grasa)</p>
                    <p>⚡ <strong>Potencial Genético:</strong> 85% alcanzado</p>
                    <p>🎯 <strong>Recomendación:</strong> Enfoque en hipertrofia con periodización ondulante</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Pie de página consistente
def mostrar_footer():
    st.markdown("---")
    st.markdown(f"""
    <div style='background-color:{SECONDARY_COLOR};color:white;padding:20px;border-radius:10px;text-align:center;'>
        <p style='margin:0;'>© 2023 <strong style='color:{PRIMARY_COLOR};'>MUPAI Digital Training Science</strong> | Todos los derechos reservados</p>
        <p style='margin:0;margin-top:10px;'>
            <a href='#' style='color:{PRIMARY_COLOR};margin:0 10px;'>Términos</a> | 
            <a href='#' style='color:{PRIMARY_COLOR};margin:0 10px;'>Privacidad</a> | 
            <a href='#' style='color:{PRIMARY_COLOR};margin:0 10px;'>Contacto</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Función principal
def main():
    aplicar_estilos()
    mostrar_cabecera()
    menu = mostrar_menu()
    
    if menu == "🏠 Inicio":
        pagina_inicio()
    elif menu == "👤 Sobre Mí":
        pagina_sobre_mi()
    elif menu == "🔬 Evaluaciones":
        pagina_evaluaciones()
    # ... otras páginas
    
    mostrar_footer()

if __name__ == "__main__":
    main()
