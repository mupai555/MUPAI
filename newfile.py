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
    'primary': '#FFCC00',      # Amarillo dorado
    'secondary': '#000000',    # Negro
    'accent': '#FFFFFF',       # Blanco
    'dark_gray': '#333333',
    'light_gray': '#F5F5F5',
    'success': '#28A745',
    'warning': '#FFC107',
    'danger': '#DC3545',
    'info': '#17A2B8'
}

# ---- CSS PROFESIONAL PERSONALIZADO ----
def apply_custom_css():
    st.markdown(f"""
    <style>
    /* Variables CSS */
    :root {{
        --mupai-primary: {MUPAI_COLORS['primary']};
        --mupai-secondary: {MUPAI_COLORS['secondary']};
        --mupai-accent: {MUPAI_COLORS['accent']};
        --mupai-dark-gray: {MUPAI_COLORS['dark_gray']};
        --mupai-light-gray: {MUPAI_COLORS['light_gray']};
    }}
    
    /* Fondo principal */
    .main {{
        background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
        padding: 2rem 1rem;
    }}
    
    /* Sidebar personalizado */
    .css-1d391kg {{
        background: linear-gradient(180deg, {MUPAI_COLORS['secondary']} 0%, {MUPAI_COLORS['dark_gray']} 100%);
    }}
    
    .css-1d391kg .css-10trblm {{
        color: {MUPAI_COLORS['accent']};
    }}
    
    /* Botones principales */
    .stButton > button {{
        background: linear-gradient(90deg, {MUPAI_COLORS['primary']} 0%, #E6B800 100%);
        color: {MUPAI_COLORS['secondary']};
        border: none;
        border-radius: 12px;
        font-weight: 700;
        font-size: 16px;
        padding: 0.75rem 1.5rem;
        box-shadow: 0 4px 12px rgba(255, 204, 0, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(90deg, #E6B800 0%, {MUPAI_COLORS['primary']} 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 204, 0, 0.4);
    }}
    
    /* Métricas personalizadas */
    .metric-card {{
        background: linear-gradient(135deg, {MUPAI_COLORS['accent']} 0%, {MUPAI_COLORS['light_gray']} 100%);
        border: 2px solid {MUPAI_COLORS['primary']};
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        text-align: center;
    }}
    
    .metric-value {{
        font-size: 2.5rem;
        font-weight: 800;
        color: {MUPAI_COLORS['secondary']};
        margin: 0;
    }}
    
    .metric-label {{
        font-size: 1.1rem;
        color: {MUPAI_COLORS['dark_gray']};
        margin: 0.5rem 0 0 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    /* Títulos */
    h1 {{
        color: {MUPAI_COLORS['secondary']};
        font-weight: 800;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }}
    
    h2 {{
        color: {MUPAI_COLORS['secondary']};
        border-bottom: 3px solid {MUPAI_COLORS['primary']};
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }}
    
    h3 {{
        color: {MUPAI_COLORS['dark_gray']};
        margin-top: 1.5rem;
    }}
    
    /* Expanders */
    .streamlit-expanderHeader {{
        background: linear-gradient(90deg, {MUPAI_COLORS['primary']} 0%, #FFD633 100%);
        color: {MUPAI_COLORS['secondary']};
        font-weight: 700;
        border-radius: 8px;
        border: none;
    }}
    
    /* Radio buttons */
    .stRadio > div {{
        background: {MUPAI_COLORS['light_gray']};
        padding: 0.5rem;
        border-radius: 8px;
        border: 1px solid {MUPAI_COLORS['primary']};
    }}
    
    /* Progress bars */
    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg, {MUPAI_COLORS['primary']} 0%, #E6B800 100%);
    }}
    
    /* Success/Warning/Error alerts */
    .stSuccess {{
        background: linear-gradient(90deg, {MUPAI_COLORS['success']} 0%, #34CE57 100%);
        color: white;
        border-radius: 8px;
    }}
    
    .stWarning {{
        background: linear-gradient(90deg, {MUPAI_COLORS['warning']} 0%, {MUPAI_COLORS['primary']} 100%);
        color: {MUPAI_COLORS['secondary']};
        border-radius: 8px;
    }}
    
    .stError {{
        background: linear-gradient(90deg, {MUPAI_COLORS['danger']} 0%, #E8495A 100%);
        color: white;
        border-radius: 8px;
    }}
    
    /* Cards especiales */
    .service-card {{
        background: linear-gradient(135deg, {MUPAI_COLORS['accent']} 0%, {MUPAI_COLORS['light_gray']} 100%);
        border-left: 5px solid {MUPAI_COLORS['primary']};
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 0 12px 12px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }}
    
    /* Dividers */
    hr {{
        border: none;
        height: 3px;
        background: linear-gradient(90deg, {MUPAI_COLORS['primary']} 0%, #E6B800 100%);
        margin: 2rem 0;
    }}
    
    /* Footer */
    .footer {{
        background: linear-gradient(90deg, {MUPAI_COLORS['secondary']} 0%, {MUPAI_COLORS['dark_gray']} 100%);
        color: {MUPAI_COLORS['accent']};
        padding: 2rem;
        text-align: center;
        border-radius: 12px;
        margin-top: 3rem;
    }}
    
    /* Imagen placeholder */
    .image-placeholder {{
        background: linear-gradient(45deg, {MUPAI_COLORS['light_gray']} 25%, transparent 25%), 
                    linear-gradient(-45deg, {MUPAI_COLORS['light_gray']} 25%, transparent 25%),
                    linear-gradient(45deg, transparent 75%, {MUPAI_COLORS['light_gray']} 75%), 
                    linear-gradient(-45deg, transparent 75%, {MUPAI_COLORS['light_gray']} 75%);
        background-size: 20px 20px;
        background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
        border: 2px dashed {MUPAI_COLORS['primary']};
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        color: {MUPAI_COLORS['dark_gray']};
        margin: 1rem 0;
    }}
    </style>
    """, unsafe_allow_html=True)

# Aplicar CSS
apply_custom_css()

# ---- FUNCIONES DE UTILIDAD ----
def create_metric_card(label, value, delta=None):
    """Crear tarjeta de métrica personalizada"""
    delta_html = ""
    if delta:
        delta_color = MUPAI_COLORS['success'] if delta > 0 else MUPAI_COLORS['danger']
        delta_html = f'<p style="color: {delta_color}; font-size: 0.9rem; margin: 0;">{"↗" if delta > 0 else "↘"} {abs(delta)}</p>'
    
    return f"""
    <div class="metric-card">
        <h2 class="metric-value">{value}</h2>
        <p class="metric-label">{label}</p>
        {delta_html}
    </div>
    """

def create_gauge_chart(value, title, max_value=100, color=MUPAI_COLORS['primary']):
    """Crear gráfico de gauge personalizado"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 24, 'color': MUPAI_COLORS['secondary']}},
        delta = {'reference': max_value/2},
        gauge = {
            'axis': {'range': [None, max_value], 'tickcolor': MUPAI_COLORS['secondary']},
            'bar': {'color': color},
            'steps': [
                {'range': [0, max_value/3], 'color': MUPAI_COLORS['light_gray']},
                {'range': [max_value/3, 2*max_value/3], 'color': '#FFE066'},
                {'range': [2*max_value/3, max_value], 'color': color}
            ],
            'threshold': {
                'line': {'color': MUPAI_COLORS['danger'], 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.9
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': MUPAI_COLORS['secondary']},
        height=400
    )
    return fig

def create_radar_chart(categories, values, title):
    """Crear gráfico radar personalizado"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor=f'rgba(255, 204, 0, 0.3)',
        line=dict(color=MUPAI_COLORS['primary'], width=3),
        marker=dict(color=MUPAI_COLORS['primary'], size=8),
        name='Tu Puntuación'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color=MUPAI_COLORS['secondary']),
                gridcolor=MUPAI_COLORS['light_gray']
            ),
            angularaxis=dict(
                tickfont=dict(color=MUPAI_COLORS['secondary'], size=12)
            )
        ),
        showlegend=False,
        title=dict(
            text=title,
            font=dict(size=20, color=MUPAI_COLORS['secondary']),
            x=0.5
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=500
    )
    return fig

def safe_image(image_path, caption="", use_container_width=True, fallback_text="Imagen no disponible"):
    """Mostrar imagen o placeholder"""
    if os.path.exists(image_path):
        st.image(image_path, caption=caption, use_container_width=use_container_width)
    else:
        st.markdown(f"""
        <div class="image-placeholder">
            <h3>📷 {fallback_text}</h3>
            <p>{image_path}</p>
        </div>
        """, unsafe_allow_html=True)

# ---- FUNCIONES DE CUESTIONARIOS CON GRÁFICOS ----

def cuestionario_calidad_sueno():
    """Cuestionario de calidad del sueño con visualizaciones"""
    st.markdown('<h1>🌙 Evaluación de la Calidad del Sueño</h1>', unsafe_allow_html=True)
    st.markdown("### Índice de Pittsburgh - PSQI")
    
    # Crear columnas para mejor layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.expander("📅 Horarios de sueño", expanded=True):
            subcol1, subcol2 = st.columns(2)
            with subcol1:
                hora_acostarse = st.text_input("¿A qué hora te acuestas?", key="hora_acostarse", placeholder="ej: 23:00")
            with subcol2:
                hora_levantarse = st.text_input("¿A qué hora te levantas?", key="hora_levantarse", placeholder="ej: 07:00")
            
            subcol3, subcol4 = st.columns(2)
            with subcol3:
                tiempo_dormirse = st.slider("Tiempo para dormirte (min)", 0, 120, 15, key="tiempo_dormirse")
            with subcol4:
                horas_dormidas = st.slider("Horas de sueño por noche", 0, 12, 7, key="horas_dormidas")

        with st.expander("⚠️ Problemas para dormir", expanded=True):
            opciones_frecuencia = ["Ninguna vez", "Menos de una vez/semana", "1-2 veces/semana", "3+ veces/semana"]
            
            problemas_dormir = {}
            problemas_lista = [
                ("No poder conciliar el sueño en 30 min", "problema_conciliar"),
                ("Despertarte durante la noche", "problema_despertar"),
                ("Ir al baño durante la noche", "problema_baño"),
                ("No poder respirar bien", "problema_respirar"),
                ("Toser o roncar fuerte", "problema_roncar"),
                ("Sentir frío", "problema_frio"),
                ("Sentir calor", "problema_calor"),
                ("Tener pesadillas", "problema_pesadillas"),
                ("Sentir dolor", "problema_dolor")
            ]
            
            for problema, key in problemas_lista:
                problemas_dormir[problema] = st.select_slider(
                    problema, opciones_frecuencia, key=key
                )

        with st.expander("💊 Medicación y otros factores"):
            uso_medicacion = st.select_slider(
                "Uso de medicamentos para dormir",
                opciones_frecuencia,
                key="uso_medicacion"
            )
            
            disfuncion_diurna_1 = st.select_slider(
                "Problemas para mantenerte despierto/a",
                opciones_frecuencia,
                key="disfuncion_1"
            )
            
            disfuncion_diurna_2 = st.select_slider(
                "Dificultad para mantener el entusiasmo",
                opciones_frecuencia,
                key="disfuncion_2"
            )
            
            calidad_sueno = st.select_slider(
                "Calidad general del sueño",
                ["Muy buena", "Bastante buena", "Bastante mala", "Muy mala"],
                key="calidad_sueno"
            )

    with col2:
        st.markdown("### 💡 Consejos para mejor sueño")
        st.info("""
        **Higiene del sueño:**
        • Horarios regulares
        • Ambiente fresco y oscuro
        • Evitar pantallas 1h antes
        • Actividad física regular
        • Evitar cafeína tarde
        """)

    if st.button("📊 Analizar Calidad del Sueño", use_container_width=True, type="primary", key="calc_psqi"):
        try:
            # Cálculos PSQI
            puntuacion = {"Ninguna vez": 0, "Menos de una vez/semana": 1, "1-2 veces/semana": 2, "3+ veces/semana": 3}
            calidad_puntuacion = {"Muy buena": 0, "Bastante buena": 1, "Bastante mala": 2, "Muy mala": 3}

            componente_1 = calidad_puntuacion[calidad_sueno]
            componente_2 = min(3, tiempo_dormirse // 15)
            componente_3 = 0 if horas_dormidas >= 7 else (1 if horas_dormidas >= 6 else (2 if horas_dormidas >= 5 else 3))
            componente_4 = min(3, sum(puntuacion.get(v, 0) for v in problemas_dormir.values()) // 3)
            componente_5 = puntuacion.get(uso_medicacion, 0)
            componente_6 = min(3, (puntuacion.get(disfuncion_diurna_1, 0) + puntuacion.get(disfuncion_diurna_2, 0)) // 2)

            total_puntuacion = componente_1 + componente_2 + componente_3 + componente_4 + componente_5 + componente_6
            porcentaje_calidad = max(0, 100 - (total_puntuacion * 100 / 21))

            st.markdown("---")
            st.markdown("## 📊 Resultados del Análisis")
            
            # Métricas principales
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(create_metric_card("Puntuación PSQI", f"{total_puntuacion}/21"), unsafe_allow_html=True)
            with col2:
                st.markdown(create_metric_card("Calidad (%)", f"{porcentaje_calidad:.0f}%"), unsafe_allow_html=True)
            with col3:
                st.markdown(create_metric_card("Horas de Sueño", f"{horas_dormidas}h"), unsafe_allow_html=True)
            with col4:
                st.markdown(create_metric_card("Tiempo p/Dormir", f"{tiempo_dormirse}min"), unsafe_allow_html=True)

            # Gráfico de gauge
            col1, col2 = st.columns(2)
            with col1:
                gauge_fig = create_gauge_chart(
                    porcentaje_calidad, 
                    "Calidad del Sueño (%)", 
                    100, 
                    MUPAI_COLORS['primary']
                )
                st.plotly_chart(gauge_fig, use_container_width=True)

            with col2:
                # Gráfico de componentes
                componentes = ['Calidad Subjetiva', 'Latencia', 'Duración', 'Eficiencia', 'Perturbaciones', 'Medicación', 'Disfunción Diurna']
                valores_comp = [componente_1, componente_2, componente_3, 0, componente_4, componente_5, componente_6]
                
                fig_comp = px.bar(
                    x=componentes,
                    y=valores_comp,
                    title="Componentes PSQI",
                    color=valores_comp,
                    color_continuous_scale=['#FFCC00', '#FF8C00', '#FF6B00']
                )
                fig_comp.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color=MUPAI_COLORS['secondary'],
                    showlegend=False
                )
                st.plotly_chart(fig_comp, use_container_width=True)

            # Interpretación con colores
            if total_puntuacion <= 5:
                st.success("✅ **EXCELENTE CALIDAD DE SUEÑO**")
                st.markdown("Tu sueño es reparador y de alta calidad. ¡Mantén estos hábitos!")
            elif total_puntuacion <= 10:
                st.warning("⚠️ **CALIDAD DE SUEÑO MODERADA**")
                st.markdown("Hay áreas de mejora. Considera optimizar tu rutina nocturna.")
            else:
                st.error("❌ **CALIDAD DE SUEÑO DEFICIENTE**")
                st.markdown("Tu sueño necesita atención inmediata. Considera consultar un especialista.")

        except Exception as e:
            st.error(f"Error en el análisis: {e}")

def cuestionario_ipaq():
    """Cuestionario IPAQ con visualizaciones avanzadas"""
    st.markdown('<h1>🏃 Análisis de Actividad Física - IPAQ</h1>', unsafe_allow_html=True)
    
    # Layout en columnas
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.markdown("### 🎯 Objetivos Recomendados")
        st.info("""
        **OMS recomienda:**
        • 150-300 min/semana moderada
        • 75-150 min/semana vigorosa
        • 2+ días de fortalecimiento
        • Reducir sedentarismo
        """)

    with col1:
        # Actividades vigorosas
        with st.expander("💪 Actividades Vigorosas", expanded=True):
            dias_vigorosa = st.slider("Días por semana de actividad vigorosa", 0, 7, 0, key="dias_vigorosa")
            if dias_vigorosa > 0:
                subcol1, subcol2 = st.columns(2)
                with subcol1:
                    tiempo_vigorosa_horas = st.number_input("Horas por día", 0, 10, 0, key="horas_vigorosa")
                with subcol2:
                    tiempo_vigorosa_minutos = st.number_input("Minutos adicionales", 0, 59, 0, key="minutos_vigorosa")
            else:
                tiempo_vigorosa_horas = tiempo_vigorosa_minutos = 0

        # Actividades moderadas
        with st.expander("🚴 Actividades Moderadas", expanded=True):
            dias_moderada = st.slider("Días por semana de actividad moderada", 0, 7, 0, key="dias_moderada")
            if dias_moderada > 0:
                subcol1, subcol2 = st.columns(2)
                with subcol1:
                    tiempo_moderada_horas = st.number_input("Horas por día", 0, 10, 0, key="horas_moderada")
                with subcol2:
                    tiempo_moderada_minutos = st.number_input("Minutos adicionales", 0, 59, 0, key="minutos_moderada")
            else:
                tiempo_moderada_horas = tiempo_moderada_minutos = 0

        # Caminata
        with st.expander("🚶 Caminata", expanded=True):
            dias_caminata = st.slider("Días por semana de caminata", 0, 7, 0, key="dias_caminata")
            if dias_caminata > 0:
                subcol1, subcol2 = st.columns(2)
                with subcol1:
                    tiempo_caminata_horas = st.number_input("Horas por día", 0, 10, 0, key="horas_caminata")
                with subcol2:
                    tiempo_caminata_minutos = st.number_input("Minutos adicionales", 0, 59, 0, key="minutos_caminata")
            else:
                tiempo_caminata_horas = tiempo_caminata_minutos = 0

        # Sedentarismo
        with st.expander("🪑 Tiempo Sedentario"):
            subcol1, subcol2 = st.columns(2)
            with subcol1:
                tiempo_sedentario_horas = st.slider("Horas sentado/día", 0, 24, 8, key="horas_sedentario")
            with subcol2:
                tiempo_sedentario_minutos = st.slider("Minutos adicionales", 0, 59, 0, key="minutos_sedentario")

    if st.button("📊 Analizar Actividad Física", use_container_width=True, type="primary", key="calc_ipaq"):
        try:
            # Cálculos
            total_vigorosa = dias_vigorosa * (tiempo_vigorosa_horas * 60 + tiempo_vigorosa_minutos)
            total_moderada = dias_moderada * (tiempo_moderada_horas * 60 + tiempo_moderada_minutos)
            total_caminata = dias_caminata * (tiempo_caminata_horas * 60 + tiempo_caminata_minutos)

            met_vigorosa = total_vigorosa * 8.0
            met_moderada = total_moderada * 4.0
            met_caminata = total_caminata * 3.3

            total_met = met_vigorosa + met_moderada + met_caminata
            tiempo_sedentario_total = tiempo_sedentario_horas * 60 + tiempo_sedentario_minutos

            st.markdown("---")
            st.markdown("## 📊 Análisis Completo de Actividad Física")

            # Métricas principales
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(create_metric_card("MET-min/semana", f"{total_met:.0f}"), unsafe_allow_html=True)
            with col2:
                st.markdown(create_metric_card("Min Vigorosa/sem", f"{total_vigorosa:.0f}"), unsafe_allow_html=True)
            with col3:
                st.markdown(create_metric_card("Min Moderada/sem", f"{total_moderada:.0f}"), unsafe_allow_html=True)
            with col4:
                st.markdown(create_metric_card("Sedentario/día", f"{tiempo_sedentario_total:.0f}min"), unsafe_allow_html=True)

            # Gráficos
            col1, col2 = st.columns(2)
            
            with col1:
                # Gauge de nivel de actividad
                if total_met >= 3000:
                    nivel_actividad = 100
                    color_gauge = MUPAI_COLORS['success']
                elif total_met >= 600:
                    nivel_actividad = 50 + (total_met - 600) * 50 / 2400
                    color_gauge = MUPAI_COLORS['warning']
                else:
                    nivel_actividad = total_met * 50 / 600
                    color_gauge = MUPAI_COLORS['danger']

                gauge_fig = create_gauge_chart(
                    nivel_actividad,
                    "Nivel de Actividad Física",
                    100,
                    color_gauge
                )
                st.plotly_chart(gauge_fig, use_container_width=True)

            with col2:
                # Gráfico de distribución de actividades
                actividades = ['Vigorosa', 'Moderada', 'Caminata']
                minutos = [total_vigorosa, total_moderada, total_caminata]
                
                fig_pie = px.pie(
                    values=minutos,
                    names=actividades,
                    title="Distribución de Actividades (min/semana)",
                    color_discrete_sequence=[MUPAI_COLORS['primary'], '#FFD633', '#FFE066']
                )
                fig_pie.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color=MUPAI_COLORS['secondary']
                )
                st.plotly_chart(fig_pie, use_container_width=True)

            # Gráfico de barras comparativo
            fig_bar = go.Figure()
            
            # Valores actuales
            fig_bar.add_trace(go.Bar(
                name='Tu Actividad',
                x=['Vigorosa', 'Moderada', 'Caminata'],
                y=[total_vigorosa, total_moderada, total_caminata],
                marker_color=MUPAI_COLORS['primary']
            ))
            
            # Recomendaciones OMS
            fig_bar.add_trace(go.Bar(
                name='Recomendado (OMS)',
                x=['Vigorosa', 'Moderada', 'Caminata'],
                y=[75, 150, 150],  # Mínimos recomendados
                marker_color=MUPAI_COLORS['success'],
                opacity=0.7
            ))
            
            fig_bar.update_layout(
                title="Comparación con Recomendaciones OMS (min/semana)",
                xaxis_title="Tipo de Actividad",
                yaxis_title="Minutos por Semana",
                barmode='group',
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color=MUPAI_COLORS['secondary']
            )
            st.plotly_chart(fig_bar, use_container_width=True)

            # Clasificación y recomendaciones
            if total_met >= 3000:
                st.success("🏆 **NIVEL DE ACTIVIDAD: ALTO**")
                st.markdown("¡Excelente! Superas ampliamente las recomendaciones. Mantén este nivel.")
                recomendaciones = [
                    "Continúa con tu rutina actual",
                    "Varía los tipos de ejercicio",
                    "Incluye ejercicios de flexibilidad",
                    "Mantén el equilibrio trabajo-descanso"
                ]
            elif total_met >= 600:
                st.info("📈 **NIVEL DE ACTIVIDAD: MODERADO**")
                st.markdown("Buen nivel base. Puedes optimizar para obtener mayores beneficios.")
                recomendaciones = [
                    "Aumenta gradualmente la intensidad",
                    "Añade 1-2 días más de actividad vigorosa",
                    "Combina ejercicios de fuerza con cardio",
                    "Reduce el tiempo sedentario"
                ]
            else:
                st.warning("📉 **NIVEL DE ACTIVIDAD: BAJO**")
                st.markdown("Es importante incrementar tu actividad física para mejorar tu salud.")
                recomendaciones = [
                    "Comienza con caminatas de 10-15 min diarios",
                    "Usa escaleras en lugar de ascensor",
                    "Realiza pausas activas cada hora",
                    "Busca actividades que disfrutes"
                ]

            # Panel de recomendaciones
            st.markdown("### 💡 Recomendaciones Personalizadas")
            for i, rec in enumerate(recomendaciones, 1):
                st.markdown(f"**{i}.** {rec}")

            # Alerta de sedentarismo
            if tiempo_sedentario_total > 480:  # >8 horas
                st.error("⚠️ **ALTO NIVEL DE SEDENTARISMO DETECTADO**")
                st.markdown("Más de 8 horas diarias sentado aumenta riesgos de salud. Implementa pausas activas.")

        except Exception as e:
            st.error(f"Error en el análisis: {e}")

def cuestionario_habitos_alimenticios():
    """Cuestionario de hábitos alimenticios con análisis nutricional"""
    st.markdown('<h1>🍎 Análisis de Hábitos Alimenticios</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.markdown("### 🥗 Guía Nutricional")
        st.success("""
        **Alimentación Saludable:**
        • 5 porciones frutas/verduras
        • Granos integrales
        • Proteínas magras
        • Grasas saludables
        • 1.5-2L agua/día
        """)

    with col1:
        # Sección 1: Alimentos Frescos
        with st.expander("🥦 Consumo de Alimentos Frescos", expanded=True):
            opciones = ["Nunca", "Algunas veces", "Casi siempre", "Siempre"]
            
            agua = st.select_slider("Agua natural (1.5L+ diario)", opciones, key="agua")
            verduras = st.select_slider("Verduras frescas (200g+ diario)", opciones, key="verduras")
            frutas = st.select_slider("Frutas (200g+ diario)", opciones, key="frutas")
            leguminosas = st.select_slider("Leguminosas (300g+ semanal)", opciones, key="leguminosas")
            frutos_secos = st.select_slider("Frutos secos/aguacate (30g+ diario)", opciones, key="frutos_secos")

        # Sección 2: Proteínas
        with st.expander("🍗 Fuentes de Proteína"):
            carne_fresca = st.selectbox(
                "Tipo de carne más frecuente",
                ["Pescado fresco", "Pollo fresco", "Carne roja fresca", "No consumo carne fresca"],
                key="carne_fresca"
            )
            carnes_procesadas = st.select_slider(
                "Carnes procesadas (embutidos, enlatadas)",
                opciones,
                key="carnes_procesadas"
            )

        # Sección 3: Hábitos Generales
        with st.expander("🍽️ Patrones Alimentarios"):
            alimentos_fuera = st.select_slider("Comida no preparada en casa (3+ veces/semana)", opciones, key="alimentos_fuera")
            bebidas_azucaradas = st.select_slider("Bebidas azucaradas", ["Nunca", "1–3 veces/semana", "4–6 veces/semana", "Diario"], key="bebidas_azucaradas")
            postres_dulces = st.select_slider("Postres/dulces (2+ veces/semana)", opciones, key="postres_dulces")
            alimentos_procesados = st.select_slider("Alimentos ultraprocesados (2+ veces/semana)", opciones, key="alimentos_procesados")
            
            cereales = st.selectbox(
                "Tipo de cereales más frecuente",
                ["Granos integrales", "Granos mínimamente procesados", "Granos procesados/ultraprocesados"],
                key="cereales"
            )

        # Sección 4: Alcohol
        with st.expander("🍷 Consumo de Alcohol"):
            alcohol = st.select_slider(
                "Alcohol (>2 bebidas/día hombres, >1 bebida/día mujeres)",
                opciones,
                key="alcohol"
            )

    if st.button("📊 Analizar Hábitos Alimenticios", use_container_width=True, type="primary", key="calc_alimentacion"):
        try:
            # Sistema de puntuación
            puntuaciones = {"Nunca": 1, "Algunas veces": 2, "Casi siempre": 3, "Siempre": 4}
            bebidas_puntuacion = {"Nunca": 4, "1–3 veces/semana": 3, "4–6 veces/semana": 2, "Diario": 1}
            carne_fresca_valores = {"Pescado fresco": 4, "Pollo fresco": 3, "Carne roja fresca": 2, "No consumo carne fresca": 1}
            carnes_procesadas_valores = {"Nunca": 4, "Algunas veces": 3, "Casi siempre": 2, "Siempre": 1}
            cereales_valores = {"Granos integrales": 4, "Granos mínimamente procesados": 3, "Granos procesados/ultraprocesados": 1}

            # Cálculos por categorías
            alimentos_frescos = (
                puntuaciones[agua] + puntuaciones[verduras] + puntuaciones[frutas] + 
                puntuaciones[leguminosas] + puntuaciones[frutos_secos]
            ) / 5 * 25  # Convertir a porcentaje

            proteinas = (carne_fresca_valores[carne_fresca] + carnes_procesadas_valores[carnes_procesadas]) / 8 * 100

            habitos_generales = (
                (5 - puntuaciones[alimentos_fuera]) + bebidas_puntuacion[bebidas_azucaradas] + 
                (5 - puntuaciones[postres_dulces]) + (5 - puntuaciones[alimentos_procesados]) + 
                cereales_valores[cereales]
            ) / 20 * 100

            consumo_alcohol = (5 - puntuaciones[alcohol]) / 4 * 100

            puntuacion_total = (alimentos_frescos + proteinas + habitos_generales + consumo_alcohol) / 4

            st.markdown("---")
            st.markdown("## 📊 Análisis Nutricional Completo")

            # Métricas principales
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(create_metric_card("Puntuación Total", f"{puntuacion_total:.0f}%"), unsafe_allow_html=True)
            with col2:
                st.markdown(create_metric_card("Alimentos Frescos", f"{alimentos_frescos:.0f}%"), unsafe_allow_html=True)
            with col3:
                st.markdown(create_metric_card("Calidad Proteínas", f"{proteinas:.0f}%"), unsafe_allow_html=True)
            with col4:
                st.markdown(create_metric_card("Hábitos Generales", f"{habitos_generales:.0f}%"), unsafe_allow_html=True)

            # Gráficos
            col1, col2 = st.columns(2)

            with col1:
                # Gráfico radar
                categorias = ['Alimentos Frescos', 'Proteínas', 'Hábitos Generales', 'Alcohol']
                valores = [alimentos_frescos, proteinas, habitos_generales, consumo_alcohol]
                
                radar_fig = create_radar_chart(categorias, valores, "Perfil Nutricional")
                st.plotly_chart(radar_fig, use_container_width=True)

            with col2:
                # Gauge principal
                if puntuacion_total >= 80:
                    color_gauge = MUPAI_COLORS['success']
                elif puntuacion_total >= 60:
                    color_gauge = MUPAI_COLORS['warning']
                else:
                    color_gauge = MUPAI_COLORS['danger']

                gauge_fig = create_gauge_chart(
                    puntuacion_total,
                    "Calidad Nutricional (%)",
                    100,
                    color_gauge
                )
                st.plotly_chart(gauge_fig, use_container_width=True)

            # Gráfico de barras detallado
            alimentos_detalle = {
                'Agua': puntuaciones[agua] * 25,
                'Verduras': puntuaciones[verduras] * 25,
                'Frutas': puntuaciones[frutas] * 25,
                'Leguminosas': puntuaciones[leguminosas] * 25,
                'Frutos Secos': puntuaciones[frutos_secos] * 25,
                'Carnes Procesadas': carnes_procesadas_valores[carnes_procesadas] * 25,
                'Comida Fuera': (5 - puntuaciones[alimentos_fuera]) * 25,
                'Bebidas Azucaradas': bebidas_puntuacion[bebidas_azucaradas] * 25
            }

            fig_detail = px.bar(
                x=list(alimentos_detalle.keys()),
                y=list(alimentos_detalle.values()),
                title="Análisis Detallado por Alimento (%)",
                color=list(alimentos_detalle.values()),
                color_continuous_scale=['#FF6B6B', '#FFE066', '#4ECDC4', '#45B7D1']
            )
            fig_detail.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color=MUPAI_COLORS['secondary'],
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_detail, use_container_width=True)

            # Interpretación y recomendaciones
            if puntuacion_total >= 80:
                st.success("✅ **HÁBITOS ALIMENTICIOS EXCELENTES**")
                st.markdown("¡Felicidades! Tu alimentación es muy saludable. Mantén estos hábitos.")
                icono_recomendacion = "🏆"
            elif puntuacion_total >= 60:
                st.warning("⚠️ **HÁBITOS ALIMENTICIOS MODERADOS**")
                st.markdown("Tienes una base sólida, pero hay áreas importantes que mejorar.")
                icono_recomendacion = "📈"
            else:
                st.error("❌ **HÁBITOS ALIMENTICIOS NECESITAN MEJORA**")
                st.markdown("Es crucial hacer cambios significativos en tu alimentación.")
                icono_recomendacion = "🚨"

            # Recomendaciones específicas
            st.markdown(f"### {icono_recomendacion} Recomendaciones Personalizadas")
            
            recomendaciones = []
            
            if alimentos_frescos < 70:
                recomendaciones.append("🥬 **Aumenta frutas y verduras**: Objetivo 5 porciones/día")
            if proteinas < 70:
                recomendaciones.append("🐟 **Mejora fuentes de proteína**: Prioriza pescado y reduce procesados")
            if habitos_generales < 70:
                recomendaciones.append("🍽️ **Optimiza patrones alimentarios**: Cocina más en casa")
            if consumo_alcohol < 70:
                recomendaciones.append("🚫 **Modera el alcohol**: Respeta los límites recomendados")

            if puntuaciones[agua] < 3:
                recomendaciones.append("💧 **Hidratación**: Lleva botella de agua y programa recordatorios")
            if bebidas_puntuacion[bebidas_azucaradas] < 3:
                recomendaciones.append("🥤 **Reduce azúcares**: Sustituye bebidas azucaradas por agua/té")

            if not recomendaciones:
                st.markdown("🎉 **¡Excelente trabajo! Continúa con tus hábitos saludables.**")
            else:
                for i, rec in enumerate(recomendaciones, 1):
                    st.markdown(f"**{i}.** {rec}")

        except Exception as e:
            st.error(f"Error en el análisis: {e}")

def cuestionario_estres():
    """Cuestionario de estrés percibido con análisis psicológico"""
    st.markdown('<h1>😰 Evaluación del Estrés Percibido</h1>', unsafe_allow_html=True)
    st.markdown("### Escala de Estrés Percibido (PSS-10)")
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.markdown("### 🧘 Manejo del Estrés")
        st.info("""
        **Técnicas efectivas:**
        • Respiración profunda
        • Ejercicio regular
        • Meditación/Mindfulness
        • Tiempo en naturaleza
        • Sueño adecuado
        • Apoyo social
        """)

    with col1:
        opciones = ["Nunca", "Casi nunca", "A veces", "Bastante seguido", "Muy seguido"]
        
        with st.expander("🧠 Cuestionario de Estrés (Último Mes)", expanded=True):
            preguntas_estres = [
                ("Molesto por algo inesperado", "stress_q1"),
                ("No puedes controlar cosas importantes", "stress_q2"),
                ("Nerviosismo o estrés", "stress_q3"),
                ("Confianza para manejar problemas", "stress_q4"),  # Inversa
                ("Las cosas van bien", "stress_q5"),  # Inversa
                ("No puedes lidiar con todo", "stress_q6"),
                ("Controlas las irritaciones", "stress_q7"),  # Inversa
                ("Tienes el control", "stress_q8"),  # Inversa
                ("Enojado por cosas fuera de control", "stress_q9"),
                ("Dificultades se acumulan", "stress_q10")
            ]
            
            respuestas = {}
            for i, (pregunta, key) in enumerate(preguntas_estres, 1):
                respuestas[key] = st.select_slider(
                    f"{i}. {pregunta}",
                    opciones,
                    key=key
                )

    if st.button("📊 Analizar Nivel de Estrés", use_container_width=True, type="primary", key="calc_stress"):
        try:
            scores = {"Nunca": 0, "Casi nunca": 1, "A veces": 2, "Bastante seguido": 3, "Muy seguido": 4}
            
            # Preguntas inversas (4, 5, 7, 8)
            preguntas_inversas = ["stress_q4", "stress_q5", "stress_q7", "stress_q8"]
            
            total_score = 0
            scores_detalle = {}
            
            for key, respuesta in respuestas.items():
                if key in preguntas_inversas:
                    score = 4 - scores[respuesta]  # Invertir puntuación
                else:
                    score = scores[respuesta]
                scores_detalle[key] = score
                total_score += score

            porcentaje_estres = (total_score / 40) * 100

            st.markdown("---")
            st.markdown("## 📊 Análisis de Estrés Percibido")

            # Métricas principales
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(create_metric_card("Puntuación PSS", f"{total_score}/40"), unsafe_allow_html=True)
            with col2:
                st.markdown(create_metric_card("Nivel de Estrés", f"{porcentaje_estres:.0f}%"), unsafe_allow_html=True)
            with col3:
                if total_score <= 13:
                    categoria = "BAJO"
                    color_cat = MUPAI_COLORS['success']
                elif total_score <= 26:
                    categoria = "MODERADO"
                    color_cat = MUPAI_COLORS['warning']
                else:
                    categoria = "ALTO"
                    color_cat = MUPAI_COLORS['danger']
                st.markdown(create_metric_card("Categoría", categoria), unsafe_allow_html=True)
            with col4:
                riesgo = "Bajo" if total_score <= 13 else ("Medio" if total_score <= 26 else "Alto")
                st.markdown(create_metric_card("Riesgo", riesgo), unsafe_allow_html=True)

            # Gráficos
            col1, col2 = st.columns(2)

            with col1:
                # Gauge de estrés
                gauge_fig = create_gauge_chart(
                    porcentaje_estres,
                    "Nivel de Estrés (%)",
                    100,
                    color_cat
                )
                st.plotly_chart(gauge_fig, use_container_width=True)

            with col2:
                # Gráfico de distribución de respuestas
                distribucion = {opcion: list(respuestas.values()).count(opcion) for opcion in opciones}
                
                fig_dist = px.pie(
                    values=list(distribucion.values()),
                    names=list(distribucion.keys()),
                    title="Distribución de Respuestas",
                    color_discrete_sequence=['#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#FDCB6E']
                )
                fig_dist.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color=MUPAI_COLORS['secondary']
                )
                st.plotly_chart(fig_dist, use_container_width=True)

            # Análisis temporal (simulado)
            fechas = pd.date_range(end=datetime.now(), periods=7)
            estres_semanal = np.random.normal(total_score, 3, 7)
            estres_semanal = np.clip(estres_semanal, 0, 40)

            fig_temporal = px.line(
                x=fechas,
                y=estres_semanal,
                title="Evolución del Estrés (Última Semana - Simulado)",
                markers=True
            )
            fig_temporal.update_traces(line_color=MUPAI_COLORS['primary'], marker_color=MUPAI_COLORS['primary'])
            fig_temporal.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color=MUPAI_COLORS['secondary'],
                xaxis_title="Fecha",
                yaxis_title="Puntuación de Estrés"
            )
            st.plotly_chart(fig_temporal, use_container_width=True)

            # Interpretación
            if total_score <= 13:
                st.success("✅ **ESTRÉS BAJO - EXCELENTE MANEJO**")
                st.markdown("Tienes un buen control del estrés. Mantén tus estrategias actuales.")
                recomendaciones = [
                    "Continúa con tus técnicas de afrontamiento",
                    "Practica mindfulness preventivo",
                    "Mantén rutinas saludables",
                    "Comparte tus estrategias con otros"
                ]
            elif total_score <= 26:
                st.warning("⚠️ **ESTRÉS MODERADO - REQUIERE ATENCIÓN**")
                st.markdown("Nivel de estrés manejable pero con margen de mejora.")
                recomendaciones = [
                    "Implementa técnicas de respiración profunda",
                    "Establece límites claros trabajo-vida personal",
                    "Incluye ejercicio regular en tu rutina",
                    "Considera hablar con un profesional",
                    "Dedica tiempo a actividades placenteras"
                ]
            else:
                st.error("❌ **ESTRÉS ALTO - INTERVENCIÓN NECESARIA**")
                st.markdown("Nivel de estrés que requiere atención profesional inmediata.")
                recomendaciones = [
                    "🚨 Busca ayuda profesional (psicólogo/psiquiatra)",
                    "Implementa técnicas de relajación inmediatamente",
                    "Evalúa cambios significativos en tu estilo de vida",
                    "Considera técnicas de meditación guiada",
                    "Establece una red de apoyo social",
                    "Evalúa tu carga de trabajo y responsabilidades"
                ]

            # Panel de recomendaciones
            st.markdown("### 💡 Plan de Acción Personalizado")
            for i, rec in enumerate(recomendaciones, 1):
                st.markdown(f"**{i}.** {rec}")

            # Recursos adicionales
            st.markdown("### 📚 Recursos Adicionales")
            st.info("""
            **Apps recomendadas**: Headspace, Calm, Insight Timer
            
            **Técnicas rápidas**:
            • Respiración 4-7-8 (inhala 4, mantén 7, exhala 8)
            • Relajación muscular progresiva
            • Caminata de 10 minutos en la naturaleza
            
            **Cuándo buscar ayuda**: Si el estrés interfiere con tu trabajo, relaciones o sueño.
            """)

        except Exception as e:
            st.error(f"Error en el análisis: {e}")

# ---- BARRA LATERAL PROFESIONAL ----
with st.sidebar:
    # Logo
    safe_image("LOGO.png", fallback_text="MUPAI Logo")
    
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(90deg, {MUPAI_COLORS['primary']} 0%, #E6B800 100%); border-radius: 12px; margin: 1rem 0;">
        <h2 style="color: {MUPAI_COLORS['secondary']}; margin: 0;">MUPAI</h2>
        <p style="color: {MUPAI_COLORS['secondary']}; margin: 0; font-weight: 600;">Entrenamiento Digital Científico</p>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.selectbox(
        "🚀 Navegación Principal",
        ["🏠 Inicio", "👤 Sobre Mí", "💼 Servicios", "📞 Contacto", "📊 Evaluación Integral"],
        index=0,
        key="menu_principal"
    )
    
    st.markdown("---")
    
    # Información de contacto en sidebar
    st.markdown("### 📱 Contacto Rápido")
    st.markdown("📧 contacto@mupai.com")
    st.markdown("📞 +52 866 258 05 94")
    
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: {MUPAI_COLORS['dark_gray']}; font-size: 0.8rem;">
        © 2024 MUPAI<br>
        Todos los derechos reservados
    </div>
    """, unsafe_allow_html=True)

# ---- CONTENIDO PRINCIPAL ----
if menu == "🏠 Inicio":
    # Hero Section
    safe_image("LOGO.png", fallback_text="MUPAI - Logo Principal")
    
    st.markdown(f"""
    <div style="text-align: center; padding: 3rem 0;">
        <h1 style="font-size: 3rem; color: {MUPAI_COLORS['secondary']}; margin-bottom: 1rem;">
            Bienvenido a MUPAI
        </h1>
        <h3 style="color: {MUPAI_COLORS['dark_gray']}; font-weight: 400;">
            Entrenamiento Digital Basado en Ciencia del Ejercicio
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas destacadas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(create_metric_card("Años de Experiencia", "5+"), unsafe_allow_html=True)
    with col2:
        st.markdown(create_metric_card("Clientes Satisfechos", "200+"), unsafe_allow_html=True)
    with col3:
        st.markdown(create_metric_card("Programas Creados", "50+"), unsafe_allow_html=True)
    with col4:
        st.markdown(create_metric_card("Certificaciones", "10+"), unsafe_allow_html=True)

    st.markdown("---")

    # Secciones informativas
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="service-card">
            <h2>🎯 Nuestra Misión</h2>
            <p>Hacer accesible el entrenamiento basado en ciencia, proporcionando planes completamente personalizados 
            a través de herramientas digitales respaldadas por inteligencia artificial, datos precisos y metodologías 
            validadas científicamente.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="service-card">
            <h2>📋 Nuestra Política</h2>
            <p>En <strong>MUPAI</strong>, nuestra política está fundamentada en el compromiso con la excelencia, 
            la ética y el servicio centrado en el usuario. Actuamos con responsabilidad y transparencia para 
            ofrecer soluciones de entrenamiento que transformen positivamente la vida de nuestros usuarios.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="service-card">
            <h2>🔮 Nuestra Visión</h2>
            <p>Convertirnos en uno de los máximos referentes a nivel global en entrenamiento digital personalizado, 
            aprovechando las nuevas tecnologías para hacer más accesible el fitness basado en ciencia para todas 
            las personas, sin importar su ubicación o nivel de experiencia.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="service-card">
            <h2>🤝 Valores Fundamentales</h2>
            <ul>
                <li><strong>Personalización Científica</strong>: Datos confiables y ciencia del ejercicio</li>
                <li><strong>Tecnología Accesible</strong>: Servicio adaptable a cada usuario</li>
                <li><strong>Privacidad y Seguridad</strong>: Protección de datos personales</li>
                <li><strong>Innovación Continua</strong>: Mejora constante
