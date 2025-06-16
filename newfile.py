import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import base64
import os

# Configuración de la página
st.set_page_config(
    page_title="MUPAI - Entrenamiento Digital Profesional",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- COLORES OFICIALES MUPAI ----
MUPAI_COLORS = {
    'primary': '#FFCC00',
    'secondary': '#000000',
    'accent': '#FFFFFF',
    'dark_gray': '#333333',
    'light_gray': '#F5F5F5',
    'success': '#28A745',
    'warning': '#FFC107',
    'danger': '#DC3545',
    'info': '#17A2B8'
}

# ---- CSS PROFESIONAL PERSONALIZADO ----
def apply_custom_css():
    css_content = f"""
    <style>
    :root {{
        --mupai-primary: {MUPAI_COLORS['primary']};
        --mupai-secondary: {MUPAI_COLORS['secondary']};
        --mupai-accent: {MUPAI_COLORS['accent']};
    }}
    .main {{ background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%); padding: 2rem 1rem; }}
    .stButton > button {{ 
        background: linear-gradient(90deg, {MUPAI_COLORS['primary']} 0%, #E6B800 100%);
        color: {MUPAI_COLORS['secondary']}; border: none; border-radius: 12px;
        font-weight: 700; padding: 0.75rem 1.5rem; text-transform: uppercase;
    }}
    .metric-card {{
        background: linear-gradient(135deg, {MUPAI_COLORS['accent']} 0%, {MUPAI_COLORS['light_gray']} 100%);
        border: 2px solid {MUPAI_COLORS['primary']}; border-radius: 16px;
        padding: 1.5rem; margin: 1rem 0; text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }}
    .metric-value {{ font-size: 2.5rem; font-weight: 800; color: {MUPAI_COLORS['secondary']}; margin: 0; }}
    .metric-label {{ font-size: 1.1rem; color: {MUPAI_COLORS['dark_gray']}; margin: 0.5rem 0 0 0; text-transform: uppercase; }}
    .service-card {{
        background: linear-gradient(135deg, {MUPAI_COLORS['accent']} 0%, {MUPAI_COLORS['light_gray']} 100%);
        border-left: 5px solid {MUPAI_COLORS['primary']}; padding: 1.5rem; margin: 1rem 0;
        border-radius: 0 12px 12px 0; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }}
    .image-placeholder {{
        border: 2px dashed {MUPAI_COLORS['primary']}; border-radius: 12px;
        padding: 2rem; text-align: center; color: {MUPAI_COLORS['dark_gray']}; margin: 1rem 0;
    }}
    h1 {{ color: {MUPAI_COLORS['secondary']}; font-weight: 800; text-align: center; margin-bottom: 2rem; }}
    h2 {{ color: {MUPAI_COLORS['secondary']}; border-bottom: 3px solid {MUPAI_COLORS['primary']}; padding-bottom: 0.5rem; }}
    </style>
    """
    st.markdown(css_content, unsafe_allow_html=True)

apply_custom_css()

# ---- FUNCIONES DE UTILIDAD ----
def create_metric_card(label, value, delta=None):
    return f"""<div class="metric-card"><h2 class="metric-value">{value}</h2><p class="metric-label">{label}</p></div>"""

def safe_image(image_path, caption="", use_container_width=True, fallback_text="Imagen no disponible"):
    try:
        if os.path.exists(image_path):
            st.image(image_path, caption=caption, use_container_width=use_container_width)
        else:
            st.markdown(f'<div class="image-placeholder"><h3>📷 {fallback_text}</h3><p>{image_path}</p></div>', unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f'<div class="image-placeholder"><h3>📷 {fallback_text}</h3><p>Error: {str(e)}</p></div>', unsafe_allow_html=True)

def create_gauge_chart(value, title, max_value=100, color=MUPAI_COLORS['primary']):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=value, domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 24, 'color': MUPAI_COLORS['secondary']}},
        gauge={'axis': {'range': [None, max_value]}, 'bar': {'color': color}}
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': MUPAI_COLORS['secondary']}, height=400)
    return fig

# ---- SIDEBAR ----
with st.sidebar:
    safe_image("LOGO.png", fallback_text="MUPAI Logo")
    sidebar_header = f"""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(90deg, {MUPAI_COLORS['primary']} 0%, #E6B800 100%); border-radius: 12px; margin: 1rem 0;">
        <h2 style="color: {MUPAI_COLORS['secondary']}; margin: 0;">MUPAI</h2>
        <p style="color: {MUPAI_COLORS['secondary']}; margin: 0;">Entrenamiento Digital Científico</p>
    </div>
    """
    st.markdown(sidebar_header, unsafe_allow_html=True)
    menu = st.selectbox("🚀 Navegación Principal", ["🏠 Inicio", "👤 Sobre Mí", "💼 Servicios", "📞 Contacto", "📊 Evaluación Integral"])

# ---- CONTENIDO PRINCIPAL ----
if menu == "🏠 Inicio":
    safe_image("LOGO.png", fallback_text="MUPAI - Logo Principal")
    hero_section = f"""
    <div style="text-align: center; padding: 3rem 0;">
        <h1 style="font-size: 3rem;">Bienvenido a MUPAI</h1>
        <h3>Entrenamiento Digital Basado en Ciencia del Ejercicio</h3>
    </div>
    """
    st.markdown(hero_section, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(create_metric_card("Años de Experiencia", "5+"), unsafe_allow_html=True)
    with col2: st.markdown(create_metric_card("Clientes Satisfechos", "200+"), unsafe_allow_html=True)
    with col3: st.markdown(create_metric_card("Programas Creados", "50+"), unsafe_allow_html=True)
    with col4: st.markdown(create_metric_card("Certificaciones", "10+"), unsafe_allow_html=True)

elif menu == "👤 Sobre Mí":
    st.markdown('<h1>👤 Erick Francisco De Luna Hernández</h1>', unsafe_allow_html=True)
    st.markdown("### Especialista en Ciencias del Ejercicio y Entrenamiento Digital")

elif menu == "💼 Servicios":
    st.markdown('<h1>💼 Servicios Profesionales MUPAI</h1>', unsafe_allow_html=True)
    services = [
        {"icon": "🏋️", "title": "Entrenamiento Personalizado", "description": "Planes individualizados basados en ciencia"},
        {"icon": "🧠", "title": "Consultoría en Rendimiento", "description": "Optimización del rendimiento deportivo"},
        {"icon": "💪", "title": "Programas de Transformación", "description": "Desarrollo integral de fuerza y resistencia"},
    ]
    for service in services:
        st.markdown(f'<div class="service-card"><h2>{service["icon"]} {service["title"]}</h2><p>{service["description"]}</p></div>', unsafe_allow_html=True)

elif menu == "📞 Contacto":
    st.markdown('<h1>📞 Información de Contacto</h1>', unsafe_allow_html=True)
    contact_info = """
    <div class="service-card">
        <h2>📱 Información de Contacto</h2>
        <p><strong>📧 Email:</strong> contacto@mupai.com</p>
        <p><strong>📞 Teléfono:</strong> +52 866 258 05 94</p>
        <p><strong>📍 Ubicación:</strong> Nuevo León, México</p>
    </div>
    """
    st.markdown(contact_info, unsafe_allow_html=True)

elif menu == "📊 Evaluación Integral":
    st.markdown('<h1>📊 Evaluación Integral de Estilo de Vida</h1>', unsafe_allow_html=True)
    evaluation_type = st.selectbox("🔍 Selecciona evaluación:", ["Seleccionar...", "🌙 Calidad del Sueño", "🏃 Actividad Física"])
    
    if evaluation_type == "🌙 Calidad del Sueño":
        st.markdown("### Evaluación de Calidad del Sueño")
        horas_dormidas = st.slider("Horas de sueño por noche", 0, 12, 7)
        tiempo_dormirse = st.slider("Tiempo para dormirte (min)", 0, 120, 15)
        
        if st.button("📊 Analizar Sueño"):
            puntuacion = 21 - (horas_dormidas + tiempo_dormirse/10)
            porcentaje = max(0, 100 - (puntuacion * 100 / 21))
            st.markdown(create_metric_card("Calidad del Sueño", f"{porcentaje:.0f}%"), unsafe_allow_html=True)
            gauge_fig = create_gauge_chart(porcentaje, "Calidad del Sueño (%)")
            st.plotly_chart(gauge_fig, use_container_width=True)

# Footer
st.markdown("---")
footer_html = f"""
<div style="background: {MUPAI_COLORS['secondary']}; color: {MUPAI_COLORS['accent']}; padding: 2rem; text-align: center; border-radius: 12px;">
    <p>&copy; 2024 MUPAI - Erick Francisco De Luna Hernández. Todos los derechos reservados.</p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
