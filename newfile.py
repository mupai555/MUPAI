import streamlit as st
import pandas as pd
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import datetime
import base64
from collections import Counter
# Temporarily comment out if the module doesn't exist yet
# from cuestionario_fbeo import mostrar_cuestionario_fbeo

# Configuración de la página
st.set_page_config(
    page_title="MUPAI - Entrenamiento Digital Basado en Ciencia",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado mejorado
st.markdown("""
<style>  
    .main-header {  
        background: linear-gradient(135deg, #FFCC00 0%, #FFD700 50%, #FFA500 100%);  
        padding: 2rem;  
        border-radius: 15px;  
        text-align: center;  
        margin-bottom: 2rem;  
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);  
    }  
      
    .main-header h1 {  
        color: #000;  
        font-size: 3rem;  
        font-weight: bold;  
        margin: 0;  
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);  
    }  
      
    .main-header p {  
        color: #000;  
        font-size: 1.3rem;  
        margin: 0.5rem 0 0 0;  
        font-weight: 500;  
    }  
      
    .section-header {  
        background: linear-gradient(90deg, #000 0%, #333 100%);  
        color: #FFCC00;  
        padding: 1rem;  
        border-radius: 10px;  
        margin: 1.5rem 0;  
        text-align: center;  
        font-weight: bold;  
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);  
    }  
      
    .questionnaire-container {  
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);  
        padding: 1.5rem;  
        border-radius: 12px;  
        border-left: 5px solid #FFCC00;  
        margin: 1rem 0;  
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);  
    }  
      
    .results-container {  
        background: linear-gradient(135deg, #FFCC00 0%, #FFE066 50%, #FFF2A6 100%);  
        padding: 2rem;  
        border-radius: 15px;  
        color: #000;  
        margin: 1rem 0;  
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);  
    }  
      
    .metric-card {  
        background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);  
        padding: 1.5rem;  
        border-radius: 12px;  
        box-shadow: 0 3px 12px rgba(0,0,0,0.1);  
        border-left: 6px solid #FFCC00;  
        margin: 1rem 0;  
        transition: transform 0.2s ease;  
    }  
      
    .metric-card:hover {  
        transform: translateY(-2px);  
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);  
    }  
      
    .corporate-section {  
        background: linear-gradient(135deg, #f1f3f4 0%, #ffffff 100%);  
        padding: 2rem;  
        border-radius: 15px;  
        margin: 1.5rem 0;  
        border: 2px solid #FFCC00;  
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);  
    }  
      
    .corporate-section h3 {  
        color: #000;  
        border-bottom: 3px solid #FFCC00;  
        padding-bottom: 0.5rem;  
        margin-bottom: 1rem;  
    }  
      
    .logo-container {  
        text-align: center;  
        padding: 2rem;  
        background: linear-gradient(135deg, #FFCC00 0%, #FFD700 100%);  
        border-radius: 15px;  
        margin-bottom: 2rem;  
    }  
      
    .professional-profile {  
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);  
        padding: 2rem;  
        border-radius: 15px;  
        border-left: 6px solid #FFCC00;  
        margin: 1rem 0;  
    }  
      
    .achievement-badge {  
        background: linear-gradient(135deg, #FFCC00 0%, #FFD700 100%);  
        color: #000;  
        padding: 0.5rem 1rem;  
        border-radius: 20px;  
        display: inline-block;  
        margin: 0.2rem;  
        font-weight: bold;  
        font-size: 0.9rem;  
    }  
</style>  
""", unsafe_allow_html=True)

# Funciones de cálculo
def calcular_tmb_katch_mcardle(peso, grasa_corporal):
    """Calcula TMB usando fórmula Katch-McArdle"""
    masa_magra = peso * (1 - grasa_corporal / 100)
    tmb = 370 + (21.6 * masa_magra)
    return tmb

def calcular_geaf(sexo, nivel_actividad):
    """Calcula GEAF según nivel de actividad y sexo"""
    geaf_valores = {
        "Sedentario": 1.00,
        "Ligera": 1.11 if sexo == "Hombre" else 1.12,
        "Activo": 1.25 if sexo == "Hombre" else 1.27,
        "Muy activo": 1.48 if sexo == "Hombre" else 1.45
    }
    return geaf_valores.get(nivel_actividad, 1.00)

def calcular_gee(peso, dias_entrenamiento):
    """Calcula Gasto Energético por Ejercicio"""
    return 0.1 * peso * 60 * dias_entrenamiento

def evaluar_calidad_sueno(horas, tiempo_dormir, despertares, descansado):
    """Evalúa calidad del sueño y retorna penalización"""
    puntos = 0
    
    # Extract numeric value from sleep hours string
    if "<5h" in horas:
        puntos += 1
    elif "5-6h" in horas:
        puntos += 0.5
    elif ">9h" in horas:
        puntos += 1
    
    # Extract numeric value from sleep time string
    if "Más de 60 min" in tiempo_dormir:
        puntos += 1
    elif "45-60 min" in tiempo_dormir:
        puntos += 0.5
    
    # Extract numeric value from awakenings string
    if "Más de 3 veces" in despertares:
        puntos += 1
    elif "3 veces" in despertares:
        puntos += 0.5
    
    # Extract numeric value from quality string
    if "Muy mala" in descansado or "Mala" in descansado:
        puntos += 1
    elif "Regular" in descansado:
        puntos += 0.5
    
    if puntos <= 1:
        return 0
    elif puntos <= 2:
        return 0.05
    else:
        return 0.10

def evaluar_estres(respuestas_estres):
    """Evalúa nivel de estrés y retorna penalización"""
    total = sum(respuestas_estres)
    
    if total <= 5:
        return 0
    elif total <= 10:
        return 0.05
    else:
        return 0.10

def enviar_email_resultados(destinatario, asunto, contenido):
    """Nueva función - Sin emails, solo acceso de coach"""
    import json
    from datetime import datetime
    
    # Tu contraseña de coach
    CONTRASEÑA_COACH = "MuPai2025"
    
    try:
        # Mensaje para el cliente
        st.success("✅ Gracias! Tu cuestionario ha sido procesado correctamente.")
        st.info("🎯 Tu coach revisará los resultados y te contactará pronto.")
        
        # Área del coach
        st.markdown("---")
        st.header("🔐 Área Exclusiva del Coach")
        
        contraseña = st.text_input("🔑 Contraseña de Coach:", type="password")
        
        if contraseña == CONTRASEÑA_COACH:
            st.success("✅ Coach mupai555 verificado")
            
            # Mostrar resultados completos
            st.header("📊 Análisis Completo del Cliente")
            st.text_area("Resultados:", contenido, height=400)
            
            # Datos para descarga
            datos_completos = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "coach": "mupai555",
                "destinatario": destinatario,
                "asunto": asunto,
                "contenido": contenido
            }
            
            # Botón de descarga
            st.download_button(
                label="📥 Descargar Análisis Completo",
                data=json.dumps(datos_completos, ensure_ascii=False, indent=2),
                file_name=f"analisis_cliente_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            
        elif contraseña:
            st.error("❌ Acceso denegado. Solo el coach autorizado puede ver los resultados.")
        
        return True
        
    except Exception as e:
        st.error(f"Error al procesar: {str(e)}")
        return False
        
# Inicializar session state
if 'page' not in st.session_state:
    st.session_state.page = "inicio"

# Sidebar con navegación mejorada
with st.sidebar:
    st.markdown("""
    <div class="logo-container">
        <h1 style='color: #000; margin: 0; font-size: 2.5rem;'>💪 MUPAI</h1>
        <p style='color: #000; font-size: 1rem; margin: 0.5rem 0 0 0;'>Entrenamiento Digital</p>
        <p style='color: #000; font-size: 0.9rem; margin: 0;'>Basado en Ciencia</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navegación principal
    if st.button("🏠 Inicio", use_container_width=True):
        st.session_state.page = "inicio"
    
    st.markdown("### 📋 Cuestionarios Especializados")
    
    if st.button("⚡ Balance Energético Óptimo", use_container_width=True):
        st.session_state.page = "balance_energetico"
    
    if st.button("🍽️ Patrones y Preferencias Alimenticias", use_container_width=True):
        st.session_state.page = "preferencias_alimentarias"
    
    if st.button("🧁 Antojos Alimentarios", use_container_width=True):
        st.session_state.page = "antojos_alimentarios"
    
    st.markdown("---")
    
    if st.button("👨‍🎓 Acerca del Profesional", use_container_width=True):
        st.session_state.page = "about"
    
    if st.button("📞 Contacto", use_container_width=True):
        st.session_state.page = "contacto"

# ==================== PÁGINA DE INICIO ====================
if st.session_state.page == "inicio":
    # Página de inicio con misión, visión y políticas
    st.markdown("""
    <div class="main-header">
        <h1>💪 MUPAI</h1>
        <p>Plataforma Digital Profesional para Entrenamiento Basado en Ciencia</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sección de Misión, Visión y Políticas
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Misión", "🔮 Visión", "📋 Política", "📘 Política del Servicio"])
    
    with tab1:
        st.markdown("""
        <div class="corporate-section">
            <h3>🎯 Nuestra Misión</h3>
            <p style="font-size: 1.1rem; line-height: 1.6;">
                Hacer accesible el <strong>entrenamiento basado en ciencia</strong>, proporcionando planes completamente personalizados 
                a través de herramientas digitales respaldadas por <strong>inteligencia artificial</strong>, datos precisos y la 
                investigación más actualizada en ciencias del ejercicio.
            </p>
            <p style="font-size: 1.1rem; line-height: 1.6;">
                Nos enfocamos en promover el <strong>desarrollo integral</strong> de nuestros usuarios y su bienestar físico y mental.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="corporate-section">
            <h3>🔮 Nuestra Visión</h3>
            <p style="font-size: 1.1rem; line-height: 1.6;">
                Convertirnos en uno de los <strong>máximos referentes a nivel global</strong> en entrenamiento digital personalizado, 
                aprovechando las nuevas tecnologías para hacer más accesible el fitness basado en ciencia.
            </p>
            <p style="font-size: 1.1rem; line-height: 1.6;">
                Aspiramos a <strong>transformar la experiencia del entrenamiento físico</strong>, integrando inteligencia artificial, 
                investigación científica y herramientas digitales avanzadas que permitan a cualquier persona alcanzar su máximo potencial.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div class="corporate-section">
            <h3>📋 Nuestra Política</h3>
            <p style="font-size: 1.1rem; line-height: 1.6;">
                En MUPAI, nuestra política está fundamentada en el <strong>compromiso con la excelencia</strong>, la ética y 
                el servicio centrado en el usuario.
            </p>
            <p style="font-size: 1.1rem; line-height: 1.6;">
                Actuamos con <strong>responsabilidad y transparencia</strong> para ofrecer soluciones tecnológicas que integren 
                ciencia, personalización y accesibilidad, contribuyendo al bienestar integral de quienes confían en nosotros.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("""
        <div class="corporate-section">
            <h3>📘 Política del Servicio</h3>
            <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 1rem;">
                En MUPAI, guiamos nuestras acciones por los siguientes principios:
            </p>
            <ul style="font-size: 1rem; line-height: 1.8;">
                <li><strong>🔬 Diseñamos entrenamientos digitales</strong> que combinan personalización, datos confiables y ciencia del ejercicio.</li>
                <li><strong>💻 Aprovechamos la tecnología</strong> para ofrecer un servicio accesible y adaptable a las necesidades de cada usuario.</li>
                <li><strong>🔒 Respetamos y protegemos la privacidad</strong> de los datos personales, garantizando su uso responsable.</li>
                <li><strong>🚀 Innovamos de forma continua</strong> para mejorar la experiencia y los resultados de nuestros usuarios.</li>
                <li><strong>🤝 Promovemos valores</strong> como el esfuerzo, la constancia y el respeto en cada interacción, fomentando un ambiente de crecimiento y bienestar.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Resto de la página de inicio con servicios, etc.
    st.markdown("""
    <div class="section-header">
        <h2>🚀 Nuestros Servicios Especializados</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>⚡ Balance Energético Óptimo</h3>
            <p>Cálculo personalizado de tu ingesta calórica ideal usando fórmulas científicas avanzadas como Katch-McArdle, evaluando tu composición corporal, nivel de actividad, calidad del sueño y estrés.</p>
            <ul style="font-size: 0.9rem;">
                <li>📊 TMB personalizada</li>
                <li>🏃 Gasto energético por ejercicio</li>
                <li>😴 Evaluación del sueño</li>
                <li>🧠 Análisis de estrés</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🍽️ Preferencias Alimentarias</h3>
            <p>Análisis detallado de tus gustos alimentarios con más de 150 opciones organizadas en 8 categorías nutricionales para crear tu perfil alimentario personalizado.</p>
            <ul style="font-size: 0.9rem;">
                <li>🥩 Proteínas especializadas</li>
                <li>🍌 Frutas y vegetales</li>
                <li>🧀 Lácteos variados</li>
                <li>🕒 Patrones alimentarios</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🧁 Antojos Alimentarios</h3>
            <p>Evaluación especializada para población mexicana que analiza 10 categorías de antojos con contexto cultural, identificando patrones emocionales y estrategias de control.</p>
            <ul style="font-size: 0.9rem;">
                <li>🇲🇽 Adaptado a México</li>
                <li>🎭 Análisis emocional</li>
                <li>📊 Patrones de comportamiento</li>
                <li>💡 Estrategias personalizadas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==================== CUESTIONARIO BALANCE ENERGÉTICO ====================
elif st.session_state.page == "balance_energetico":
    st.markdown("""
    <div class="section-header">
        <h2>🧮 Cálculo del Factor de Balance Energético Óptimo (FBEO)</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="questionnaire-container">
        <h3>🎯 Objetivo</h3>
        <p>Esta sección permite estimar la <strong>ingesta calórica personalizada</strong> según tu composición corporal, 
        actividad física, frecuencia de entrenamiento, calidad de la dieta, y estado de recuperación fisiológica 
        (estrés y sueño). Se define automáticamente si debes estar en déficit, mantenimiento o superávit calórico.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("balance_energetico_form"):
        st.subheader("📋 Datos Antropométricos")
        col1, col2 = st.columns(2)
        
        with col1:
            sexo = st.selectbox("Sexo", ["Hombre", "Mujer"])
            peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1)
            estatura = st.number_input("Estatura (m)", min_value=1.0, max_value=2.5, value=1.70, step=0.01)
        
        with col2:
            grasa_corporal = st.number_input("Porcentaje de grasa corporal (%)", min_value=5.0, max_value=50.0, value=20.0, step=0.1)
            masa_magra = peso * (1 - grasa_corporal/100)
            st.info(f"Masa magra calculada: {masa_magra:.1f} kg")
        
        st.subheader("🏃 Actividad Física")
        col1, col2 = st.columns(2)
        
        with col1:
            nivel_actividad = st.selectbox("Nivel de actividad diaria", [
                "Sedentario (trabajo de escritorio, poco/nada de ejercicio)",
                "Ligeramente activo (ejercicio ligero/deportes 1-3 días/semana)",
                "Moderadamente activo (ejercicio moderado/deportes 3-5 días/semana)",
                "Muy activo (ejercicio intenso/deportes 6-7 días/semana)",
                "Extremadamente activo (ejercicio muy intenso, trabajo físico)"
            ])
        
        with col2:
            dias_entrenamiento = st.number_input("Días de entrenamiento de fuerza por semana", min_value=0, max_value=7, value=3)
        
        st.subheader("😴 Evaluación del Sueño")
        col1, col2 = st.columns(2)
        
        with col1:
            horas_sueno = st.selectbox("¿Cuántas horas duermes por noche?", [
                "Menos de 5h (1)", "5-6h (2)", "6-7h (3)", "7-8h (5)", "8-9h (4)", "Más de 9h (2)"
            ])
            tiempo_dormir = st.selectbox("¿Cuánto tardas en quedarte dormido?", [
                "Menos de 15 min (5)", "15-30 min (4)", "30-45 min (3)", "45-60 min (2)", "Más de 60 min (1)"
            ])
        
        with col2:
            despertares_nocturnos = st.selectbox("¿Cuántas veces te despiertas por noche?", [
                "Nunca (5)", "1 vez (4)", "2 veces (3)", "3 veces (2)", "Más de 3 veces (1)"
            ])
            calidad_percibida = st.selectbox("¿Cómo percibes la calidad de tu sueño?", [
                "Excelente (5)", "Buena (4)", "Regular (3)", "Mala (2)", "Muy mala (1)"
            ])
        
        st.subheader("🧠 Evaluación del Estrés (PSS-4)")
        st.markdown("**En el último mes, ¿con qué frecuencia...**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            pss1 = st.selectbox("¿Has sentido que no podías controlar las cosas importantes de tu vida?", [
                "Nunca (0)", "Casi nunca (1)", "A veces (2)", "Frecuentemente (3)", "Muy frecuentemente (4)"
            ])
            pss2 = st.selectbox("¿Te has sentido confiado/a sobre tu capacidad para manejar tus problemas personales?", [
                "Nunca (4)", "Casi nunca (3)", "A veces (2)", "Frecuentemente (1)", "Muy frecuentemente (0)"
            ])
        
        with col2:
            pss3 = st.selectbox("¿Has sentido que las cosas van como tú quieres?", [
                "Nunca (4)", "Casi nunca (3)", "A veces (2)", "Frecuentemente (1)", "Muy frecuentemente (0)"
            ])
            pss4 = st.selectbox("¿Has sentido que las dificultades se acumulan tanto que no puedes superarlas?", [
                "Nunca (0)", "Casi nunca (1)", "A veces (2)", "Frecuentemente (3)", "Muy frecuentemente (4)"
            ])
        
        st.subheader("📧 Información de Contacto")
        email_destinatario = st.text_input("Email para seguimiento", placeholder="tu@email.com")
        
        submitted = st.form_submit_button("🚀 Calcular FBEO", type="primary")
        
        if submitted:
            # PASO 1: Calcular TMB usando Katch-McArdle
            tmb = 370 + (21.6 * masa_magra)
            
            # PASO 2: Calcular GER
            ger = tmb * 1.1
            
            # PASO 3: Determinar GEAF según nivel de actividad
            actividad_factores = {
                "Sedentario (trabajo de escritorio, poco/nada de ejercicio)": {
                    "geaf": 1.40, "descripcion": "Trabajo de escritorio, sin ejercicio regular", "pasos": "< 5,000"
                },
                "Ligeramente activo (ejercicio ligero/deportes 1-3 días/semana)": {
                    "geaf": 1.55, "descripcion": "Trabajo sedentario + ejercicio ligero", "pasos": "5,000-7,500"
                },
                "Moderadamente activo (ejercicio moderado/deportes 3-5 días/semana)": {
                    "geaf": 1.70, "descripcion": "Trabajo activo o ejercicio regular", "pasos": "7,500-10,000"
                },
                "Muy activo (ejercicio intenso/deportes 6-7 días/semana)": {
                    "geaf": 1.85, "descripcion": "Ejercicio intenso diario", "pasos": "10,000-12,500"
                },
                "Extremadamente activo (ejercicio muy intenso, trabajo físico)": {
                    "geaf": 2.00, "descripcion": "Ejercicio muy intenso + trabajo físico", "pasos": "> 12,500"
                }
            }
            
            datos_actividad = actividad_factores[nivel_actividad]
            geaf = datos_actividad["geaf"]
            
            # PASO 4: Calcular GEE por sesión de entrenamiento
            gee_por_sesion = masa_magra * 5
            gee_semanal = gee_por_sesion * dias_entrenamiento
            
            # PASO 5: Calcular GET con y sin entrenamiento
            get_con_entrenamiento = ger * geaf + gee_semanal / 7  # Fixed: use daily average
            get_sin_entrenamiento = ger * geaf
            
            # PASO 6: Calcular GET promedio semanal
            get_promedio = ((get_con_entrenamiento * dias_entrenamiento) + 
                           (get_sin_entrenamiento * (7 - dias_entrenamiento))) / 7
            
            # PASO 7: Determinar FBEO base según % grasa corporal
            if sexo == "Hombre":
                if grasa_corporal > 25:
                    fbeo_base = 0.875  # Déficit para perder grasa
                elif 18 <= grasa_corporal <= 24:
                    fbeo_base = 0.975  # Déficit leve
                elif 12 <= grasa_corporal < 18:
                    fbeo_base = 1.05   # Superávit leve
                else:  # < 12%
                    fbeo_base = 1.125  # Superávit para ganar músculo
            else:  # Mujer
                if grasa_corporal > 32:
                    fbeo_base = 0.875
                elif 25 <= grasa_corporal <= 31:
                    fbeo_base = 0.975
                elif 20 <= grasa_corporal < 25:
                    fbeo_base = 1.05
                else:  # < 20%
                    fbeo_base = 1.125
            
            # PASO 8: Calcular puntuaciones de estrés y sueño
            # PSS-4
            pss_valores = {
                "Nunca (0)": 0, "Casi nunca (1)": 1, "A veces (2)": 2, 
                "Frecuentemente (3)": 3, "Muy frecuentemente (4)": 4,
                "Nunca (4)": 4, "Casi nunca (3)": 3, "Frecuentemente (1)": 1, 
                "Muy frecuentemente (0)": 0
            }
            
            pss_total = (pss_valores[pss1] + pss_valores[pss2] + 
                        pss_valores[pss3] + pss_valores[pss4])
            estres_alto = pss_total > 13
            
            # Calidad del sueño
            sueno_valores = {
                "Menos de 5h (1)": 1, "5-6h (2)": 2, "6-7h (3)": 3, 
                "7-8h (5)": 5, "8-9h (4)": 4, "Más de 9h (2)": 2,
                "Menos de 15 min (5)": 5, "15-30 min (4)": 4, "30-45 min (3)": 3, 
                "45-60 min (2)": 2, "Más de 60 min (1)": 1,
                "Nunca (5)": 5, "1 vez (4)": 4, "2 veces (3)": 3, 
                "3 veces (2)": 2, "Más de 3 veces (1)": 1,
                "Excelente (5)": 5, "Buena (4)": 4, "Regular (3)": 3, 
                "Mala (2)": 2, "Muy mala (1)": 1
            }
            
            sueno_promedio = (sueno_valores[horas_sueno] + sueno_valores[tiempo_dormir] + 
                             sueno_valores[despertares_nocturnos] + sueno_valores[calidad_percibida]) / 4
            sueno_malo = sueno_promedio < 3.5
            
            # PASO 9: Ajustar FBEO según estrés y sueño (LÓGICA CORREGIDA)
            ajuste_fbeo = 0
            
            if estres_alto and sueno_malo:
                # Estrés alto + sueño malo = MÁS CONSERVADOR
                if fbeo_base < 1.0:  # Si está en déficit
                    ajuste_fbeo = 0.10  # REDUCE el déficit (sube hacia 1.0)
                else:  # Si está en superávit
                    ajuste_fbeo = -0.10  # REDUCE el superávit (baja hacia 1.0)
                    
            elif estres_alto or sueno_malo:
                # Solo uno de los dos = MODERADAMENTE CONSERVADOR
                if fbeo_base < 1.0:  # Si está en déficit
                    ajuste_fbeo = 0.05  # REDUCE el déficit
                else:  # Si está en superávit
                    ajuste_fbeo = -0.05  # REDUCE el superávit
            
            # Si ambos están bien (estres_alto = False AND sueno_malo = False):
            # ajuste_fbeo = 0  --> NO HAY AJUSTE, se mantiene el FBEO original
            
            fbeo_ajustado = fbeo_base + ajuste_fbeo
            
            # Límites de seguridad para evitar extremos
            fbeo_ajustado = max(0.80, min(fbeo_ajustado, 1.20))
            
            # PASO 10: Ingesta calórica final
            calorias_totales = get_promedio * fbeo_ajustado
            
            # PASO 11: Generar tips personalizados
            tips_sueno = []
            tips_estres = []
            
            # Tips para mejorar el sueño según puntuación
            if sueno_malo:
                if sueno_valores[horas_sueno] <= 3:
                    tips_sueno.append("🕐 **Prioriza 7-8 horas de sueño:** Tu cuerpo necesita este tiempo para la síntesis proteica y recuperación muscular óptima.")
                
                if sueno_valores[tiempo_dormir] <= 2:
                    tips_sueno.extend([
                        "🚿 **Ducha caliente pre-sueño:** Toma una ducha caliente 90 minutos antes de dormir para relajar los músculos.",
                        "🧘 **Meditación nocturna:** Dedica 10 minutos a meditación guiada antes de acostarte.",
                        "💊 **Considera suplementos:** Melatonina (3-5mg) o L-teanina (200mg) 30 min antes de dormir."
                    ])
                
                if sueno_valores[despertares_nocturnos] <= 2:
                    tips_sueno.extend([
                        "💧 **Limita líquidos:** Reduce consumo de líquidos 2 horas antes de dormir.",
                        "🌡️ **Temperatura óptima:** Mantén tu habitación a 19°C para un sueño profundo.",
                        "🔇 **Insonorización:** Usa tapones para oídos o ruido blanco para minimizar interrupciones."
                    ])
                
                if sueno_valores[calidad_percibida] <= 2:
                    tips_sueno.extend([
                        "📱 **Desconexión digital:** Evita pantallas 1 hora antes de dormir para mantener la melatonina.",
                        "🛏️ **Revisa tu colchón:** Un colchón inadecuado puede afectar significativamente la calidad del sueño.",
                        "☕ **Límite de cafeína:** No consumas cafeína después de las 14:00 hrs."
                    ])
                
                tips_sueno.extend([
                    "⏰ **Horario consistente:** Acuéstate y levántate a la misma hora todos los días.",
                    "🌞 **Luz matutina:** Exponte a luz brillante en las primeras 2 horas del día.",
                    "🥗 **Cena balanceada:** Incluye carbohidratos complejos y proteína magra 2-3 horas antes de dormir."
                ])
            
            # Tips para manejar el estrés según puntuación PSS-4
            if estres_alto:
                if pss_valores[pss1] >= 3:
                    tips_estres.extend([
                        "🎯 **Afrontamiento activo:** Identifica y aborda directamente las causas del estrés en lugar de evitarlas.",
                        "📝 **Lista de prioridades:** Organiza tareas por importancia para recuperar sensación de control."
                    ])
                
                if pss_valores[pss2] >= 3:
                    tips_estres.extend([
                        "💪 **Entrenamiento de fuerza:** El ejercicio regular mejora la confianza y reduce el cortisol.",
                        "🧘 **Mindfulness diario:** 10 minutos de atención plena fortalecen la resiliencia mental."
                    ])
                
                if pss_valores[pss4] >= 3:
                    tips_estres.extend([
                        "👥 **Apoyo social:** Dedica tiempo a conexiones significativas que liberan oxitocina.",
                        "😄 **Terapia de risa:** Ver comedias o actividades humorísticas reduce fisiológicamente el estrés.",
                        "🏥 **Considera apoyo profesional:** Un psicólogo puede ofrecer herramientas personalizadas."
                    ])
                
                tips_estres.extend([
                    "🌿 **Conexión con naturaleza:** Caminatas de 20 min en parques reducen el cortisol.",
                    "🎵 **Música relajante:** Crea playlists calmantes para momentos de tensión.",
                    "❄️ **Duchas frías:** Termina tu ducha con 30 segundos de agua fría para fortalecer resiliencia.",
                    "📓 **Diario de gratitud:** Escribe 3 cosas positivas cada noche antes de dormir.",
                    "💊 **Suplementos anti-estrés:** Considera Ashwagandha (600mg), Omega-3 (2g) o Magnesio (400mg)."
                ])
            
            # PASO 12: Calcular macronutrientes
            # Proteínas ajustadas según grasa corporal
            if sexo == "Hombre":
                if grasa_corporal > 25:
                    factor_proteina = 1.8
                elif 18 <= grasa_corporal <= 24:
                    factor_proteina = 2.0
                elif 12 <= grasa_corporal < 18:
                    factor_proteina = 2.2
                else:
                    factor_proteina = 2.4
            else:
                if grasa_corporal > 32:
                    factor_proteina = 1.8
                elif 25 <= grasa_corporal <= 31:
                    factor_proteina = 2.0
                elif 20 <= grasa_corporal < 25:
                    factor_proteina = 2.2
                else:
                    factor_proteina = 2.4
            
            proteinas_g_ajustadas = peso * factor_proteina
            proteinas_g_ajustadas = max(peso * 1.8, min(proteinas_g_ajustadas, peso * 2.4))
            proteinas_kcal_ajustadas = proteinas_g_ajustadas * 4
            
            grasas_kcal_ajustadas = calorias_totales * 0.275
            grasas_g_ajustadas = grasas_kcal_ajustadas / 9
            carbs_kcal_ajustadas = calorias_totales - proteinas_kcal_ajustadas - grasas_kcal_ajustadas
            carbs_g_ajustadas = carbs_kcal_ajustadas / 4
            
            # MOSTRAR INFORMACIÓN MÍNIMA AL USUARIO
            st.success("✅ **¡Evaluación completada con éxito!**")
            
            st.info("""
            📧 **Tu evaluación ha sido enviada a tu entrenador personal.**
            
            **¿Qué sigue?**
            - Tu entrenador revisará tus resultados
            - Recibirás tu plan nutricional personalizado
            - Te contactaremos para coordinar tu programa
            
            ⏰ **Tiempo estimado de respuesta: 24-48 horas**
            
            💡 **Importante:** Mantén tu teléfono disponible para coordinar detalles.
            """)
            
            # Resumen MÍNIMO para el usuario
            st.markdown("### 📊 Confirmación de Datos")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Datos Corporales", "✅ Registrados")
            
            with col2:
                st.metric("Actividad Física", "✅ Evaluada")
            
            with col3:
                st.metric("Estrés y Sueño", "✅ Analizados")
            
            # Mostrar objetivo detectado (información básica)
            if fbeo_ajustado < 0.95:
                objetivo = "Pérdida de grasa"
            elif fbeo_ajustado > 1.05:
                objetivo = "Ganancia muscular"
            else:
                objetivo = "Recomposición corporal"
            
            st.metric("Objetivo Detectado", objetivo)
            
            st.markdown("""
            ---
            ### 🎯 Próximos Pasos
            
            1. **Espera el contacto** de tu entrenador MUPAI
            2. **Mantén tu rutina actual** hasta recibir indicaciones
            3. **Prepárate para comenzar** tu transformación
            
            **¿Tienes preguntas urgentes?** Contacta a MUPAI por WhatsApp.
            """)
            
            # ENVIAR EMAIL COMPLETO SOLO AL ENTRENADOR
            if not email_destinatario:
                st.error("⚠️ **Error:** Debes proporcionar un correo electrónico para el seguimiento.")
            else:
                # EMAIL COMPLETO PARA EL ENTRENADOR
                contenido_email = f"""
========================================
📊 NUEVO CLIENTE - EVALUACIÓN FBEO

Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Email del cliente: {email_destinatario}

========================================
👤 PERFIL DEL CLIENTE

Sexo: {sexo}
Peso: {peso} kg
Estatura: {estatura} m
IMC: {peso/(estatura**2):.1f}
Grasa corporal: {grasa_corporal}%
Masa magra: {masa_magra:.1f} kg

========================================
🏃 PERFIL DE ACTIVIDAD FÍSICA

Nivel de actividad: {nivel_actividad}
Descripción: {datos_actividad['descripcion']}
Pasos diarios estimados: {datos_actividad['pasos']}
Factor GEAF aplicado: {geaf}
Días de entrenamiento semanal: {dias_entrenamiento}

========================================
😴 EVALUACIÓN DEL SUEÑO

Horas de sueño: {horas_sueno}
Tiempo para dormir: {tiempo_dormir}
Despertares nocturnos: {despertares_nocturnos}
Calidad percibida: {calidad_percibida}

PUNTUACIÓN TOTAL: {sueno_promedio:.1f}/5
EVALUACIÓN: {'⚠️ CALIDAD DEFICIENTE - Requiere intervención' if sueno_malo else '✅ CALIDAD ADECUADA'}

========================================
🧠 EVALUACIÓN DEL ESTRÉS (PSS-4)

Pregunta 1 (Control): {pss1}
Pregunta 2 (Confianza): {pss2}
Pregunta 3 (Las cosas van bien): {pss3}
Pregunta 4 (Dificultades acumuladas): {pss4}

PUNTUACIÓN TOTAL PSS-4: {pss_total}/16
EVALUACIÓN: {'⚠️ ESTRÉS ALTO - Requiere manejo activo' if estres_alto else '✅ ESTRÉS MANEJABLE'}

========================================
⚡ CÁLCULOS ENERGÉTICOS DETALLADOS

TMB (Katch-McArdle): {tmb:.0f} kcal
GER (Gasto en reposo): {ger:.0f} kcal
GEE por sesión: {gee_por_sesion:.0f} kcal
GET con entrenamiento: {get_con_entrenamiento:.0f} kcal
GET sin entrenamiento: {get_sin_entrenamiento:.0f} kcal
GET promedio semanal: {get_promedio:.0f} kcal

========================================
📊 FACTOR DE BALANCE ENERGÉTICO (FBEO) - ANÁLISIS DETALLADO

FBEO base según {grasa_corporal:.1f}% GC: {fbeo_base:.3f}

EVALUACIÓN DE FACTORES DE RECUPERACIÓN:
• Estrés (PSS-4): {pss_total}/16 {'- ALTO ⚠️' if estres_alto else '- Normal ✅'}
• Sueño: {sueno_promedio:.1f}/5 {'- DEFICIENTE ⚠️' if sueno_malo else '- Adecuado ✅'}

LÓGICA DE AJUSTE APLICADA:
"""
                
                if estres_alto and sueno_malo:
                    contenido_email += f"""• Estrés ALTO + Sueño MALO detectado
• Ajuste: {'+' if ajuste_fbeo > 0 else ''}{ajuste_fbeo:.2f} ({'Reduce déficit' if fbeo_base < 1.0 else 'Reduce superávit'})
• Razón: Recuperación comprometida requiere enfoque más conservador"""
                elif estres_alto or sueno_malo:
                    factor_problema = "Estrés ALTO" if estres_alto else "Sueño MALO"
                    contenido_email += f"""• {factor_problema} detectado
• Ajuste: {'+' if ajuste_fbeo > 0 else ''}{ajuste_fbeo:.2f} ({'Reduce déficit' if fbeo_base < 1.0 else 'Reduce superávit'})
• Razón: Recuperación parcialmente comprometida"""
                else:
                    contenido_email += f"""• Estrés Normal + Sueño Adecuado ✅
• Ajuste: {ajuste_fbeo:.2f} (Sin modificaciones)
• Razón: Buena recuperación permite protocolo estándar"""
                
                contenido_email += f"""

FBEO FINAL: {fbeo_ajustado:.3f}
INTERPRETACIÓN: {'DÉFICIT CALÓRICO' if fbeo_ajustado < 0.95 else 'SUPERÁVIT CALÓRICO' if fbeo_ajustado > 1.05 else 'MANTENIMIENTO/RECOMPOSICIÓN'}

ESTRATEGIA NUTRICIONAL:
{'• Pérdida de grasa con preservación muscular' if fbeo_ajustado < 0.95 else '• Ganancia muscular controlada' if fbeo_ajustado > 1.05 else '• Recomposición corporal (pérdida de grasa + ganancia muscular)'}
{'• Protocolo conservador por factores de recuperación' if (estres_alto or sueno_malo) else '• Protocolo estándar por buena recuperación'}

========================================
🍽️ PLAN NUTRICIONAL CALCULADO

CALORÍAS TOTALES: {calorias_totales:.0f} kcal/día

Distribución de Macronutrientes:
• Proteína: {proteinas_g_ajustadas:.0f}g ({proteinas_kcal_ajustadas:.0f} kcal) - {proteinas_kcal_ajustadas/calorias_totales*100:.0f}%
Factor aplicado: {factor_proteina:.1f}g/kg peso corporal
• Grasas: {grasas_g_ajustadas:.0f}g ({grasas_kcal_ajustadas:.0f} kcal) - {grasas_kcal_ajustadas/calorias_totales*100:.0f}%
• Carbohidratos: {carbs_g_ajustadas:.0f}g ({carbs_kcal_ajustadas:.0f} kcal) - {carbs_kcal_ajustadas/calorias_totales*100:.0f}%

Requerimientos adicionales:
• Fibra mínima: {25 if sexo == "Mujer" else 35}g/día
• Agua mínima: {peso * 35:.0f}ml/día

========================================
🎯 RECOMENDACIONES ESPECÍFICAS PARA EL CLIENTE

"""
                
                # Agregar tips personalizados
                if sueno_malo and tips_sueno:
                    contenido_email += "\n😴 ESTRATEGIAS PERSONALIZADAS PARA MEJORAR EL SUEÑO:\n"
                    for tip in tips_sueno:
                        contenido_email += f"   {tip}\n"
                
                if estres_alto and tips_estres:
                    contenido_email += "\n🧠 ESTRATEGIAS PERSONALIZADAS PARA MANEJAR EL ESTRÉS:\n"
                    for tip in tips_estres:
                        contenido_email += f"   {tip}\n"
                
                contenido_email += f"""

========================================
📝 NOTAS PARA EL ENTRENADOR

Cliente evaluado el {datetime.now().strftime('%Y-%m-%d %H:%M')}

Requiere seguimiento {'prioritario' if (estres_alto or sueno_malo) else 'estándar'}

Contactar en próximas 24-48 horas

========================================
"""
                
                # Enviar SOLO al entrenador (usando secrets para seguridad)
                try:
                    trainer_email = st.secrets.get("trainer_email", "mupaitraining@outlook.com")
                    enviar_email_resultados(trainer_email, 
                      f"NUEVO CLIENTE FBEO - {email_destinatario}", 
                      contenido_email)
                    st.success("✅ Evaluación enviada correctamente al entrenador")
                except Exception as e:
                    st.error(f"❌ Error al enviar email: {str(e)}")

# ==================== CUESTIONARIO PREFERENCIAS ALIMENTARIAS ====================
elif st.session_state.page == "preferencias_alimentarias":
    st.markdown("""
    <div class="section-header">
        <h2>🍽️ Cuestionario: Patrones y Preferencias Alimenticias</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="questionnaire-container">
        <h3>📋 Instrucciones</h3>
        <p><strong>Selecciona de cada lista los alimentos que prefieres o estás dispuesto(a) a consumir.</strong></p>
        <p>✅ Marca todos los que apliquen</p>
        <p>🔄 En caso de no tener problema con todos, marca "Todas las anteriores"</p>
        
        <h4>🎯 Objetivo</h4>
        <p>Este cuestionario nos permitirá crear tu <strong>perfil nutricional personalizado</strong> basado en tus gustos 
        y preferencias reales, garantizando que disfrutes tu plan alimentario.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("preferencias_alimentarias_form"):
        
        # --- PROTEÍNAS DE ORIGEN ANIMAL MAGRAS ---
        st.markdown("""
        <div class="questionnaire-container">
            <h3>🥩 Proteínas de origen animal magras</h3>
        </div>
        """, unsafe_allow_html=True)
        
        proteinas_magras_opciones = [
            "Todas las anteriores",
            "Pechuga de pollo",
            "Claras de huevo", 
            "Lomo de cerdo",
            "Lomo de res",
            "Top sirloin",
            "Bacalao",
            "Atún en agua",
            "Tilapia",
            "Mojarra",
            "Carne molida magra (90/10 a 97/3)",
            "Filete de merluza",
            "Pargo", 
            "Pez espada",
            "Lenguado",
            "Conejo",
            "Codorniz",
            "Pechuga de pavo",
            "Atún fresco",
            "Surimi light",
            "Ostras"
        ]
        
        proteinas_magras = st.multiselect(
            "Selecciona las proteínas magras que consumes o estarías dispuesto(a) a consumir:",
            proteinas_magras_opciones,
            key="proteinas_magras"
        )
        
        # --- PROTEÍNAS DE ORIGEN ANIMAL CON MÁS GRASA ---
        st.markdown("""
        <div class="questionnaire-container">
            <h3>🥓 Proteínas de origen animal con más grasa</h3>
        </div>
        """, unsafe_allow_html=True)
        
        proteinas_grasa_opciones = [
            "Todas las anteriores",
            "Huevo entero",
            "Costilla de cerdo",
            "Chuleta natural",
            "Chuleta ahumada", 
            "Muslo de pollo con piel",
            "Arrachera",
            "Rib-eye",
            "Salmón",
            "Sardinas",
            "T-bone",
            "Carne molida regular (80/20 a 85/15)",
            "Diezmillo",
            "Steak del 7",
            "Falda",
            "Picaña",
            "Tocino",
            "Pierna de pato",
            "Chorizo artesanal",
            "Longaniza de cerdo",
            "Atún en aceite"
        ]
        
        proteinas_grasa = st.multiselect(
            "Selecciona las proteínas con grasa que consumes o estarías dispuesto(a) a consumir:",
            proteinas_grasa_opciones,
            key="proteinas_grasa"
        )
        
               # --- FRUTAS ---
        st.markdown("""
        <div class="questionnaire-container">
            <h3>🍌 Frutas (elige tus favoritas o marca todas si no tienes restricciones)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        frutas_opciones = [
            "Todas las anteriores",
            "Plátano",
            "Manzana",
            "Pera",
            "Fresa",
            "Mango",
            "Papaya",
            "Sandía",
            "Piña",
            "Kiwi",
            "Moras (zarzamora, frambuesa, arándano)",
            "Uvas",
            "Granada",
            "Naranja",
            "Mandarina",
            "Guayaba",
            "Melón",
            "Higo",
            "Durazno",
            "Cereza",
            "Ciruela"
        ]
        
        frutas = st.multiselect(
            "Selecciona las frutas que prefieres:",
            frutas_opciones,
            key="frutas"
        )
        
        # --- VEGETALES ---
        st.markdown("""
        <div class="questionnaire-container">
            <h3>🥦 Vegetales (elige tus favoritos o marca todas si no tienes restricciones)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        vegetales_opciones = [
            "Todas las anteriores",
            "Espinaca",
            "Brócoli",
            "Zanahoria",
            "Calabaza",
            "Pepino",
            "Lechuga",
            "Jitomate",
            "Betabel",
            "Champiñones",
            "Espárragos",
            "Coliflor",
            "Acelga",
            "Ejotes",
            "Nopales",
            "Pimiento morrón (rojo, verde, amarillo)",
            "Apio",
            "Cebolla morada",
            "Cebolla blanca",
            "Rábanos",
            "Col de Bruselas"
        ]
        
        vegetales = st.multiselect(
            "Selecciona los vegetales que prefieres:",
            vegetales_opciones,
            key="vegetales"
        )
        
        # --- CARBOHIDRATOS ALTOS EN ALMIDÓN ---
        st.markdown("""
        <div class="questionnaire-container">
            <h3>🍠 Carbohidratos altos en almidón</h3>
        </div>
        """, unsafe_allow_html=True)
        
        carbohidratos_opciones = [
            "Todas las anteriores",
            "Arroz blanco",
            "Arroz integral",
            "Papa blanca",
            "Papa roja",
            "Papa amarilla",
            "Camote",
            "Tortilla de maíz",
            "Tortilla de nopal",
            "Pan integral",
            "Pan de centeno",
            "Pasta integral",
            "Avena",
            "Quinoa",
            "Trigo sarraceno",
            "Amaranto",
            "Pan pita integral",
            "Harina de avena",
            "Tapioca",
            "Yuca cocida",
            "Elote (mazorca)",
            "Tortilla de avena"
        ]
        
        carbohidratos = st.multiselect(
            "Selecciona los carbohidratos que prefieres:",
            carbohidratos_opciones,
            key="carbohidratos"
        )
        
        # --- LÁCTEOS BAJOS EN GRASA ---
        st.markdown("""
        <div class="questionnaire-container">
            <h3>🧀 Lácteos bajos en grasa</h3>
        </div>
        """, unsafe_allow_html=True)
        
        lacteos_light_opciones = [
            "Todas las anteriores",
            "Leche descremada",
            "Leche semidescremada",
            "Yogur griego sin azúcar (0–2% grasa)",
            "Yogur natural bajo en grasa",
            "Queso panela",
            "Queso cottage bajo en grasa",
            "Requesón bajo en grasa",
            "Leche de almendra sin azúcar",
            "Leche de soya sin azúcar",
            "Queso ricotta light",
            "Queso Oaxaca bajo en grasa",
            "Queso manchego light",
            "Queso mozzarella light"
        ]
        
        lacteos_light = st.multiselect(
            "Selecciona los lácteos bajos en grasa que prefieres:",
            lacteos_light_opciones,
            key="lacteos_light"
        )
        
        # --- LÁCTEOS ALTOS EN GRASA ---
        st.markdown("""
        <div class="questionnaire-container">
            <h3>🧀 Lácteos altos en grasa</h3>
        </div>
        """, unsafe_allow_html=True)
        
        lacteos_grasa_opciones = [
            "Todas las anteriores",
            "Leche entera",
            "Crema entera",
            "Mantequilla",
            "Yogur griego entero",
            "Yogur natural entero",
            "Queso manchego",
            "Queso cheddar",
            "Queso crema",
            "Queso Oaxaca",
            "Queso gouda"
        ]
        
        lacteos_grasa = st.multiselect(
            "Selecciona los lácteos altos en grasa que prefieres:",
            lacteos_grasa_opciones,
            key="lacteos_grasa"
        )
        
        # --- GRASAS SALUDABLES ---
        st.markdown("""
        <div class="questionnaire-container">
            <h3>🥑 Grasas saludables</h3>
        </div>
        """, unsafe_allow_html=True)
        
        grasas_opciones = [
            "Todas las anteriores",
            "Aguacate",
            "Aceite de oliva extra virgen",
            "Almendras",
            "Nueces",
            "Mantequilla de maní",
            "Mantequilla de almendra",
            "Chía",
            "Linaza molida",
            "Aceitunas",
            "Tahini (pasta de ajonjolí)",
            "Semillas de girasol",
            "Semillas de calabaza",
            "Pistaches",
            "Nueces de la India",
            "Avellanas",
            "Cacahuates naturales",
            "Ghee",
            "Aceite de aguacate",
            "Aceite de coco (con moderación)",
            "Crema de cacahuate sin azúcar"
        ]
        
        grasas = st.multiselect(
            "Selecciona las grasas saludables que prefieres:",
            grasas_opciones,
            key="grasas"
        )
        
        # --- SECCIÓN DE SUPLEMENTOS ---
        st.markdown("---")
        st.markdown("""
        <div class="questionnaire-container">
            <h3>💊 Suplementos</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            incluir_suplementos = st.radio(
                "¿Deseas incluir suplementos como parte de tu dieta (proteína en polvo, creatina, etc.)?",
                ["Sí", "No"]
            )
        
        with col2:
            marcas_preferidas = st.text_area(
                "¿Tienes alguna preferencia específica en marcas o tipos?",
                placeholder="Ej: Proteína ISO 100, Creatina Optimum Nutrition...",
                height=100
            )
        
        # --- ALIMENTOS ADICIONALES ---
        st.markdown("""
        <div class="questionnaire-container">
            <h3>➕ Alimentos Adicionales</h3>
        </div>
        """, unsafe_allow_html=True)
        
        alimentos_adicionales = st.text_area(
            "¿Hay algún otro alimento que suelas consumir con frecuencia que no se haya incluido en las listas anteriores y que te gustaría considerar en tu plan?",
            placeholder="Ej: Té verde, chocolate negro 85%, proteína vegetal, kombucha...",
            height=100
        )
        
        # --- ALERGIAS E INTOLERANCIAS ---
        st.markdown("---")
        st.markdown("""
        <div class="questionnaire-container">
            <h3>⚠️ Alergias e Intolerancias</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            tiene_alergias = st.radio(
                "¿Tienes alguna alergia o intolerancia a algún alimento?",
                ["No", "Sí"]
            )
        
        with col2:
            alergias_detalle = ""
            if tiene_alergias == "Sí":
                alergias_detalle = st.text_area(
                    "En caso afirmativo, indícalo aquí:",
                    placeholder="Ej: Lactosa, gluten, nueces, mariscos, huevos...",
                    height=100
                )
        
        # --- PATRONES ALIMENTARIOS ADICIONALES ---
        st.markdown("---")
        st.markdown("""
        <div class="questionnaire-container">
            <h3>🕒 Patrones Alimentarios</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            comidas_dia = st.selectbox(
                "¿Cuántas comidas prefieres hacer al día?",
                ["3 comidas principales", "3 comidas + 1 snack", "3 comidas + 2 snacks", 
                 "4-5 comidas pequeñas", "6 comidas pequeñas", "Ayuno intermitente"]
            )
            
            cocinar_frecuencia = st.selectbox(
                "¿Con qué frecuencia cocinas en casa?",
                ["Todos los días", "5-6 días por semana", "3-4 días por semana", 
                 "1-2 días por semana", "Rara vez", "Nunca"]
            )
        
        with col2:
            horario_comidas = st.selectbox(
                "¿Tienes horarios fijos para comer?",
                ["Sí, muy estrictos", "Sí, pero flexibles", "A veces", "No, como cuando puedo"]
            )
            
            presupuesto_comida = st.selectbox(
                "¿Cuál es tu presupuesto aproximado semanal para comida?",
                ["Menos de $500", "$500-$800", "$800-$1200", "$1200-$1800", "Más de $1800", "Sin límite específico"]
            )
        
        # EMAIL OBLIGATORIO
        st.markdown("---")
        st.markdown("""
        <div class="questionnaire-container">
            <h3>📧 Información de Contacto</h3>
        </div>
        """, unsafe_allow_html=True)
        
        email_destinatario = st.text_input("Email para seguimiento (obligatorio):", placeholder="tu@email.com")
        
        submitted = st.form_submit_button("🍽️ Enviar Evaluación al Entrenador", use_container_width=True)
        
        if submitted:
            # Procesar y limpiar las selecciones
            def procesar_seleccion(lista_seleccionada, lista_completa):
                if "Todas las anteriores" in lista_seleccionada:
                    return [item for item in lista_completa if item != "Todas las anteriores"]
                return lista_seleccionada
            
            proteinas_magras_final = procesar_seleccion(proteinas_magras, proteinas_magras_opciones)
            proteinas_grasa_final = procesar_seleccion(proteinas_grasa, proteinas_grasa_opciones)
            frutas_final = procesar_seleccion(frutas, frutas_opciones)
            vegetales_final = procesar_seleccion(vegetales, vegetales_opciones)
            carbohidratos_final = procesar_seleccion(carbohidratos, carbohidratos_opciones)
            lacteos_light_final = procesar_seleccion(lacteos_light, lacteos_light_opciones)
            lacteos_grasa_final = procesar_seleccion(lacteos_grasa, lacteos_grasa_opciones)
            grasas_final = procesar_seleccion(grasas, grasas_opciones)
            
            # MOSTRAR INFORMACIÓN MÍNIMA AL USUARIO
            st.success("✅ **¡Evaluación completada con éxito!**")
            
            st.info("""
            📧 **Tu evaluación nutricional ha sido enviada a tu entrenador personal.**
            
            **¿Qué sigue?**
            - Tu entrenador analizará tus preferencias alimentarias
            - Recibirás un plan nutricional personalizado
            - Te contactaremos para coordinar tu alimentación
            
            ⏰ **Tiempo estimado de respuesta: 24-48 horas**
            
            💡 **Importante:** Mantén tu teléfono disponible para coordinar detalles.
            """)
            
            # Resumen MÍNIMO para el usuario
            st.markdown("### 📊 Confirmación de Evaluación")
            col1, col2, col3 = st.columns(3)
            
            total_categorias = len([x for x in [proteinas_magras_final, proteinas_grasa_final, frutas_final, vegetales_final, carbohidratos_final, lacteos_light_final, lacteos_grasa_final, grasas_final] if len(x) > 0])
            total_alimentos = len(proteinas_magras_final + proteinas_grasa_final + frutas_final + vegetales_final + carbohidratos_final + lacteos_light_final + lacteos_grasa_final + grasas_final)
            
            with col1:
                st.metric("Categorías Evaluadas", f"{total_categorias}/8")
            
            with col2:
                st.metric("Alimentos Seleccionados", f"{total_alimentos}")
            
            with col3:
                variedad = "Excelente" if total_categorias >= 6 else "Buena" if total_categorias >= 4 else "Limitada"
                st.metric("Variedad Alimentaria", variedad)
            
            st.markdown("""
            ---
            ### 🎯 Próximos Pasos
            
            1. **Espera el contacto** de tu entrenador MUPAI
            2. **Mantén tu alimentación actual** hasta recibir indicaciones
            3. **Prepárate para disfrutar** de tu plan personalizado
            
            **¿Tienes preguntas urgentes?** Contacta a MUPAI por WhatsApp.
            """)
            
            # ENVIAR EMAIL COMPLETO SOLO AL ENTRENADOR
            if not email_destinatario:
                st.error("⚠️ **Error:** Debes proporcionar un correo electrónico para el seguimiento.")
            else:
                # EMAIL COMPLETO PARA EL ENTRENADOR
                contenido_email = f"""
========================================
📊 NUEVO CLIENTE - PREFERENCIAS ALIMENTARIAS

Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Email del cliente: {email_destinatario}

========================================
🥩 PROTEÍNAS MAGRAS SELECCIONADAS ({len(proteinas_magras_final)} items)

{', '.join(proteinas_magras_final) if proteinas_magras_final else 'Ninguna seleccionada'}

========================================
🥓 PROTEÍNAS CON GRASA SELECCIONADAS ({len(proteinas_grasa_final)} items)

{', '.join(proteinas_grasa_final) if proteinas_grasa_final else 'Ninguna seleccionada'}

========================================
🍌 FRUTAS SELECCIONADAS ({len(frutas_final)} items)

{', '.join(frutas_final) if frutas_final else 'Ninguna seleccionada'}

========================================
🥦 VEGETALES SELECCIONADOS ({len(vegetales_final)} items)

{', '.join(vegetales_final) if vegetales_final else 'Ninguna seleccionada'}

========================================
🍠 CARBOHIDRATOS SELECCIONADOS ({len(carbohidratos_final)} items)

{', '.join(carbohidratos_final) if carbohidratos_final else 'Ninguna seleccionada'}

========================================
🧀 LÁCTEOS BAJOS EN GRASA ({len(lacteos_light_final)} items)

{', '.join(lacteos_light_final) if lacteos_light_final else 'Ninguna seleccionada'}

========================================
🧀 LÁCTEOS ALTOS EN GRASA ({len(lacteos_grasa_final)} items)

{', '.join(lacteos_grasa_final) if lacteos_grasa_final else 'Ninguna seleccionada'}

========================================
🥑 GRASAS SALUDABLES ({len(grasas_final)} items)

{', '.join(grasas_final) if grasas_final else 'Ninguna seleccionada'}

========================================
💊 INFORMACIÓN DE SUPLEMENTOS

Incluye suplementos: {incluir_suplementos}
Marcas/tipos preferidos: {marcas_preferidas if marcas_preferidas else 'No especificado'}

========================================
➕ ALIMENTOS ADICIONALES

{alimentos_adicionales if alimentos_adicionales else 'No especificado'}

========================================
⚠️ ALERGIAS E INTOLERANCIAS

Tiene alergias/intolerancias: {tiene_alergias}
Detalle: {alergias_detalle if alergias_detalle else 'No especificado'}

========================================
🕒 PATRONES ALIMENTARIOS

Comidas preferidas al día: {comidas_dia}
Frecuencia cocinando: {cocinar_frecuencia}
Horarios de comida: {horario_comidas}
Presupuesto semanal: {presupuesto_comida}

========================================
📊 ANÁLISIS NUTRICIONAL

Total de categorías con selecciones: {total_categorias}/8
Total de alimentos seleccionados: {total_alimentos}
Variedad alimentaria: {variedad}

INTERPRETACIÓN:
• Proteínas: {'✅ Buena variedad' if len(proteinas_magras_final + proteinas_grasa_final) >= 10 else '⚠️ Limitada variedad' if len(proteinas_magras_final + proteinas_grasa_final) >= 5 else '🔴 Muy limitada'}
• Frutas y vegetales: {'✅ Excelente' if len(frutas_final + vegetales_final) >= 15 else '⚠️ Aceptable' if len(frutas_final + vegetales_final) >= 8 else '🔴 Insuficiente'}
• Carbohidratos: {'✅ Buena variedad' if len(carbohidratos_final) >= 8 else '⚠️ Limitada'}
• Lácteos: {'✅ Incluye lácteos' if len(lacteos_light_final + lacteos_grasa_final) > 0 else '⚠️ No incluye lácteos'}
• Grasas: {'✅ Buena variedad' if len(grasas_final) >= 8 else '⚠️ Limitada'}

RECOMENDACIONES PARA EL PLAN:
• {'Priorizar proteínas magras' if len(proteinas_magras_final) > len(proteinas_grasa_final) else 'Incluir más proteínas magras'}
• {'Aprovechar la gran variedad de frutas/vegetales' if len(frutas_final + vegetales_final) >= 15 else 'Incorporar gradualmente más frutas/vegetales'}
• {'Cliente acepta suplementos - considerar proteína en polvo' if incluir_suplementos == 'Sí' else 'Cliente no desea suplementos - plan 100% alimentos'}
• {'Considerar restricciones: ' + alergias_detalle if tiene_alergias == 'Sí' else 'Sin restricciones alimentarias'}

========================================
📝 NOTAS PARA EL ENTRENADOR

Cliente evaluado el {datetime.now().strftime('%Y-%m-%d %H:%M')}

Perfil nutricional {'completo' if total_categorias >= 6 else 'parcial'}

Prioridad: {'estándar' if total_categorias >= 4 else 'alta (variedad limitada)'}

Contactar en próximas 24-48 horas para plan personalizado

========================================
"""
                
                # Enviar SOLO al entrenador con seguridad mejorada
                try:
                    trainer_email = st.secrets.get("trainer_email", "mupaitraining@outlook.com")
                    enviar_email_resultados(trainer_email, 
                                          f"NUEVO CLIENTE PREFERENCIAS - {email_destinatario}", 
                                          contenido_email)
                    st.success("✅ Evaluación enviada correctamente al entrenador")
                except Exception as e:
                    st.error(f"❌ Error al enviar email: {str(e)}")

# ==================== CUESTIONARIO ANTOJOS ALIMENTARIOS ====================
elif st.session_state.page == "antojos_alimentarios":
    st.markdown("""
    <div class="section-header">
        <h2>🧁 Cuestionario de Antojos Alimentarios (Food Cravings)</h2>
        <h3>Versión Población Mexicana</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="questionnaire-container">
        <h3>🎯 Objetivo del Cuestionario</h3>
        <p>Este cuestionario tiene como objetivo identificar tu <strong>perfil personal de antojos alimentarios</strong>. 
        Responde con sinceridad para cada grupo de alimentos. Esto nos permitirá adaptar tu plan nutricional 
        considerando tus patrones de antojos y estrategias de manejo.</p>
        
        <h4>📋 Cada sección incluye:</h4>
        <ul>
            <li>🔄 Frecuencia del antojo</li>
            <li>⏰ Momento del día en que aparece</li>
            <li>💪 Intensidad del antojo</li>
            <li>🎯 Capacidad de controlarlo</li>
            <li>⚡ Conducta ante el antojo</li>
            <li>🎭 Emoción detonante principal</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    categorias_antojos_mexicanas = [
        {
            "emoji": "🧁",
            "nombre": "Panes dulces",
            "ejemplos": "Gansito, Donitas Bimbo, Barritas, Roles, Cuernitos, Bigotes, Pingüinos, Mantecadas"
        },
        {
            "emoji": "🍟",
            "nombre": "Frituras",
            "ejemplos": "Sabritas, Ruffles, Doritos, Chetos, Takis, Chips, Rancheritos"
        },
        {
            "emoji": "🍫",
            "nombre": "Chocolates y dulces",
            "ejemplos": "Carlos V, Snickers, Kinder Bueno, M&M's, Paletas Payaso, Trufas, Gomitas"
        },
        {
            "emoji": "🧀",
            "nombre": "Quesos grasos y snacks salados",
            "ejemplos": "Manchego, Oaxaca, Gouda, Queso crema, Queso con totopos, Queso fundido, Salchichas"
        },
        {
            "emoji": "🍞",
            "nombre": "Pan blanco, bolillos, teleras, baguettes",
            "ejemplos": "Bolillo, Telera, Baguette, Pan dulce, Concha, Empanada dulce"
        },
        {
            "emoji": "🥤",
            "nombre": "Refrescos y bebidas azucaradas",
            "ejemplos": "Coca-Cola, Pepsi, Sprite, Jarritos, Sidral, Boing, Del Valle, Jumex, Powerade, Gatorade"
        },
        {
            "emoji": "🍨",
            "nombre": "Helados y postres fríos",
            "ejemplos": "Helado de vainilla, Chocolate, Fresa, Paletas de hielo, Nieve, Magnum, Cornetto"
        },
        {
            "emoji": "🥙",
            "nombre": "Comida rápida mexicana",
            "ejemplos": "Tacos al pastor, Quesadillas, Tortas, Tamales, Pozole, Flautas, Sopes"
        },
        {
            "emoji": "🍕",
            "nombre": "Pizza y comida rápida internacional",
            "ejemplos": "Pizza, Hamburguesas, Hot dogs, Papas fritas, Alitas, Nuggets"
        },
        {
            "emoji": "🍺",
            "nombre": "Alcohol y bebidas fermentadas",
            "ejemplos": "Cerveza, Tequila, Mezcal, Vino, Micheladas, Pulque, Tepache"
        }
    ]
    
    with st.form("antojos_alimentarios_form"):
        resultados_antojos = {}
        
        for i, categoria in enumerate(categorias_antojos_mexicanas):
            st.markdown(f"""
            <div class="questionnaire-container">
                <h3>{categoria['emoji']} {categoria['nombre']}</h3>
                <p style="font-style: italic; color: #666;">Ejemplos: {categoria['ejemplos']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                frecuencia = st.selectbox(
                    f"¿Con qué frecuencia tienes antojos de {categoria['nombre'].lower()}?",
                    ["Nunca", "Rara vez (1-2 veces/mes)", "A veces (1-2 veces/semana)", 
                     "Frecuentemente (3-4 veces/semana)", "Muy frecuentemente (diario)"],
                    key=f"freq_{i}"
                )
                
                momento = st.selectbox(
                    "¿En qué momento del día aparece más?",
                    ["Mañana", "Media mañana", "Mediodía", "Tarde", "Noche", "Madrugada", "Todo el día"],
                    key=f"momento_{i}"
                )
                
                intensidad = st.slider(
                    "Intensidad del antojo (1 = Muy débil, 10 = Irresistible)",
                    1, 10, 5, key=f"intensidad_{i}"
                )
            
            with col2:
                control = st.selectbox(
                    "¿Qué tan fácil es controlar este antojo?",
                    ["Muy fácil", "Fácil", "Moderado", "Difícil", "Muy difícil"],
                    key=f"control_{i}"
                )
                
                conducta = st.selectbox(
                    "¿Qué haces cuando tienes este antojo?",
                    ["Lo ignoro completamente", "Trato de sustituirlo", "Cedo parcialmente", 
                     "Cedo completamente", "Como más de lo planeado"],
                    key=f"conducta_{i}"
                )
                
                emocion = st.selectbox(
                    "¿Qué emoción lo detona principalmente?",
                    ["Ninguna en particular", "Estrés", "Ansiedad", "Tristeza", "Aburrimiento", 
                     "Felicidad", "Nostalgia", "Cansancio"],
                    key=f"emocion_{i}"
                )
            
            resultados_antojos[categoria['nombre']] = {
                'frecuencia': frecuencia,
                'momento': momento,
                'intensidad': intensidad,
                'control': control,
                'conducta': conducta,
                'emocion': emocion
            }
            
            st.markdown("---")
        
        # EMAIL OBLIGATORIO
        st.markdown("""
        <div class="questionnaire-container">
            <h3>📧 Información de Contacto</h3>
        </div>
        """, unsafe_allow_html=True)
        
        email_destinatario = st.text_input("Email para seguimiento (obligatorio):", placeholder="tu@email.com")
        
        submitted = st.form_submit_button("🧁 Enviar Evaluación al Entrenador", use_container_width=True)
        
        if submitted:
            # MOSTRAR INFORMACIÓN MÍNIMA AL USUARIO
            st.success("✅ **¡Evaluación completada con éxito!**")
            
            st.info("""
            📧 **Tu evaluación de antojos ha sido enviada a tu entrenador personal.**
            
            **¿Qué sigue?**
            - Tu entrenador analizará tus patrones de antojos
            - Recibirás estrategias personalizadas de manejo
            - Te contactaremos para coordinar tu plan integral
            
            ⏰ **Tiempo estimado de respuesta: 24-48 horas**
            
            💡 **Importante:** Mantén tu teléfono disponible para coordinar detalles.
            """)
            
            # Análisis BÁSICO para el usuario
            antojos_frecuentes = [k for k, v in resultados_antojos.items() 
                                if v['frecuencia'] in ["Frecuentemente (3-4 veces/semana)", "Muy frecuentemente (diario)"]]
            
            intensidad_promedio = sum([v['intensidad'] for v in resultados_antojos.values()]) / len(resultados_antojos)
            
            antojos_dificiles = [k for k, v in resultados_antojos.items() 
                               if v['control'] in ["Difícil", "Muy difícil"]]
            
            # Resumen MÍNIMO para el usuario
            st.markdown("### 📊 Confirmación de Evaluación")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Categorías Evaluadas", "10/10")
            
            with col2:
                st.metric("Antojos Identificados", f"{len(antojos_frecuentes)}")
            
            with col3:
                nivel_riesgo = "Alto" if len(antojos_frecuentes) >= 4 else "Medio" if len(antojos_frecuentes) >= 2 else "Bajo"
                st.metric("Nivel de Manejo", nivel_riesgo)
            
            st.markdown("""
            ---
            ### 🎯 Próximos Pasos
            
            1. **Espera el contacto** de tu entrenador MUPAI
            2. **Mantén tu alimentación actual** hasta recibir indicaciones
            3. **Prepárate para aprender** estrategias de manejo efectivas
            
            **¿Tienes preguntas urgentes?** Contacta a MUPAI por WhatsApp.
            """)
            
            # ENVIAR EMAIL COMPLETO SOLO AL ENTRENADOR
            if not email_destinatario:
                st.error("⚠️ **Error:** Debes proporcionar un correo electrónico para el seguimiento.")
            else:
                # Calcular análisis detallado
                emociones_principales = [v['emocion'] for v in resultados_antojos.values() 
                                       if v['frecuencia'] != "Nunca"]
                emociones_frecuentes = Counter(emociones_principales).most_common(3)
                
                momentos_principales = [v['momento'] for v in resultados_antojos.values() 
                                      if v['frecuencia'] != "Nunca"]
                momentos_frecuentes = Counter(momentos_principales).most_common(3)
                
                # EMAIL COMPLETO PARA EL ENTRENADOR
                contenido_email = f"""
========================================
📊 NUEVO CLIENTE - ANTOJOS ALIMENTARIOS

Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Email del cliente: {email_destinatario}

========================================
🧁 ANÁLISIS DETALLADO POR CATEGORÍA

"""
                
                for categoria, datos in resultados_antojos.items():
                    emoji = next(c['emoji'] for c in categorias_antojos_mexicanas if c['nombre'] == categoria)
                    contenido_email += f"""
{emoji} {categoria.upper()}:
• Frecuencia: {datos['frecuencia']}
• Momento: {datos['momento']}
• Intensidad: {datos['intensidad']}/10
• Control: {datos['control']}
• Conducta: {datos['conducta']}
• Emoción detonante: {datos['emocion']}

"""
                
                contenido_email += f"""

========================================
📊 RESUMEN EJECUTIVO

Antojos frecuentes ({len(antojos_frecuentes)} categorías):
{', '.join(antojos_frecuentes) if antojos_frecuentes else 'Ninguno'}

Antojos difíciles de controlar ({len(antojos_dificiles)} categorías):
{', '.join(antojos_dificiles) if antojos_dificiles else 'Ninguno'}

Intensidad promedio: {intensidad_promedio:.1f}/10

Nivel de riesgo: {nivel_riesgo}

========================================
🎭 ANÁLISIS DE EMOCIONES DETONANTES

"""
                
                if emociones_frecuentes:
                    for emocion, frecuencia in emociones_frecuentes:
                        contenido_email += f"• {emocion}: {frecuencia} categorías afectadas\n"
                else:
                    contenido_email += "• No se identificaron emociones detonantes significativas\n"
                
                contenido_email += f"""

========================================
⏰ ANÁLISIS DE MOMENTOS DE MAYOR RIESGO

"""
                
                if momentos_frecuentes:
                    for momento, frecuencia in momentos_frecuentes:
                        contenido_email += f"• {momento}: {frecuencia} categorías afectadas\n"
                else:
                    contenido_email += "• No se identificaron momentos de mayor riesgo\n"
                
                contenido_email += f"""

========================================
🎯 RECOMENDACIONES ESPECÍFICAS

"""
                
                # Generar recomendaciones basadas en el análisis
                if len(antojos_frecuentes) >= 4:
                    contenido_email += "⚠️ PRIORIDAD ALTA - Múltiples antojos frecuentes\n"
                    contenido_email += "• Implementar estrategias de manejo emocional\n"
                    contenido_email += "• Planificar comidas estructuradas\n"
                    contenido_email += "• Considerar sustitutos saludables\n\n"
                
                if intensidad_promedio >= 7:
                    contenido_email += "⚠️ INTENSIDAD ALTA - Antojos muy fuertes\n"
                    contenido_email += "• Trabajar en técnicas de control de impulsos\n"
                    contenido_email += "• Identificar triggers específicos\n\n"
                
                if emociones_frecuentes:
                    emocion_principal = emociones_frecuentes[0][0]
                    if emocion_principal == "Estrés":
                        contenido_email += "🧘 ENFOQUE: Manejo del estrés\n"
                        contenido_email += "• Técnicas de respiración y mindfulness\n"
                        contenido_email += "• Ejercicio regular para reducir cortisol\n"
                        contenido_email += "• Planificar snacks anti-estrés\n\n"
                    elif emocion_principal == "Aburrimiento":
                        contenido_email += "🎯 ENFOQUE: Actividades alternativas\n"
                        contenido_email += "• Lista de actividades para momentos de aburrimiento\n"
                        contenido_email += "• Horarios estructurados\n"
                        contenido_email += "• Hobbies que mantengan las manos ocupadas\n\n"
                    elif emocion_principal == "Ansiedad":
                        contenido_email += "😌 ENFOQUE: Manejo de ansiedad\n"
                        contenido_email += "• Técnicas de grounding\n"
                        contenido_email += "• Infusiones relajantes\n"
                        contenido_email += "• Ejercicio de baja intensidad\n\n"
                
                contenido_email += f"""

========================================
🛡️ ESTRATEGIAS DE INTERVENCIÓN SUGERIDAS

1. SUSTITUCIÓN INTELIGENTE:
• Preparar versiones saludables de antojos principales
• Tener opciones disponibles en momentos de riesgo

2. CONTROL AMBIENTAL:
• Limitar acceso a alimentos problema
• Estructurar ambiente alimentario

3. MANEJO EMOCIONAL:
• Técnicas específicas para emociones detonantes
• Diario de antojos para identificar patrones

4. TIMING ESTRATÉGICO:
• Planificar pequeñas porciones en momentos controlados
• Evitar restricción extrema que intensifique antojos

5. APOYO NUTRICIONAL:
• Comidas balanceadas que reduzcan antojos
• Hidratación adecuada
• Sueño reparador

========================================
📝 NOTAS PARA EL ENTRENADOR

Cliente evaluado el {datetime.now().strftime('%Y-%m-%d %H:%M')}

Perfil de antojos {'complejo' if len(antojos_frecuentes) >= 3 else 'moderado' if len(antojos_frecuentes) >= 1 else 'simple'}

Prioridad de intervención: {'alta' if len(antojos_frecuentes) >= 4 or intensidad_promedio >= 7 else 'media' if len(antojos_frecuentes) >= 2 else 'baja'}

Requiere seguimiento {'semanal' if len(antojos_frecuentes) >= 3 else 'quincenal'}

Contactar en próximas 24-48 horas

ALERTAS ESPECIALES:
{'• Múltiples antojos frecuentes - requiere plan integral' if len(antojos_frecuentes) >= 4 else ''}
{'• Intensidad muy alta - riesgo de abandono' if intensidad_promedio >= 8 else ''}
{'• Dificultad de control - necesita apoyo emocional' if len(antojos_dificiles) >= 3 else ''}

========================================
"""
                
                # Enviar SOLO al entrenador con seguridad mejorada
                try:
                    trainer_email = st.secrets.get("trainer_email", "mupaitraining@outlook.com")
                    enviar_email_resultados(trainer_email, 
                                          f"NUEVO CLIENTE ANTOJOS - {email_destinatario}", 
                                          contenido_email)
                    st.success("✅ Evaluación enviada correctamente al entrenador")
                except Exception as e:
                    st.error(f"❌ Error al enviar email: {str(e)}")

# ==================== PÁGINAS ADICIONALES ====================
elif st.session_state.page == "about":
    st.markdown("""
    <div class="section-header">
        <h2>👨‍🎓 Acerca del Profesional</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="professional-profile">
        <h3>🎓 Erick Francisco De Luna Hernández</h3>
        <p><strong>Maestría en Fuerza y Acondicionamiento</strong></p>
        <p><strong>Ciencias del Ejercicio - UANL</strong></p>
        
        <h4>🏆 Especialidades:</h4>
        <ul>
            <li>Entrenamiento basado en evidencia científica</li>
            <li>Periodización del entrenamiento</li>
            <li>Nutrición deportiva y composición corporal</li>
            <li>Análisis biomecánico del movimiento</li>
            <li>Programas de recomposición corporal</li>
        </ul>
        
        <h4>📚 Formación Académica:</h4>
        <ul>
            <li>Maestría en Ciencias del Ejercicio - UANL</li>
            <li>Certificación en Fuerza y Acondicionamiento</li>
            <li>Especialización en Nutrición Deportiva</li>
            <li>Cursos avanzados en Biomecánica</li>
        </ul>
        
        <h4>💼 Experiencia Profesional:</h4>
        <ul>
            <li>+5 años en entrenamiento personalizado</li>
            <li>Desarrollo de programas digitales de fitness</li>
            <li>Consultoría nutricional especializada</li>
            <li>Investigación en ciencias del ejercicio</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "contacto":
    st.markdown("""
    <div class="section-header">
        <h2>📞 Contacto</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="results-container">
        <h3>💪 MUPAI - Entrenamiento Digital Basado en Ciencia</h3>
        <p><strong>Dirigido por:</strong> Erick Francisco De Luna Hernández</p>
        <p><strong>Especialidad:</strong> Maestría en Fuerza y Acondicionamiento | Ciencias del Ejercicio UANL</p>
        <br>
        <p>📧 <strong>Email:</strong> mupaitraining@outlook.com</p>
        <p>📱 <strong>WhatsApp:</strong> +52 XXX XXX XXXX</p>
        <p>🌐 <strong>Sitio Web:</strong> www.mupai.com</p>
        
        <h4>🕐 Horarios de Atención:</h4>
        <p>Lunes a Viernes: 9:00 AM - 6:00 PM</p>
        <p>Sábados: 9:00 AM - 2:00 PM</p>
        <p>Domingos: Solo emergencias</p>
        
        <h4>📍 Ubicación:</h4>
        <p>Monterrey, Nuevo León, México</p>
        <p>Consultas presenciales y virtuales disponibles</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 10px;">
    <h3 style="color: #000; margin-bottom: 1rem;">💪 MUPAI - Entrenamiento Digital Basado en Ciencia</h3>
    <p style="color: #666; margin-bottom: 0.5rem;">Dirigido por <strong>Erick Francisco De Luna Hernández</strong></p>
    <p style="color: #666; margin-bottom: 1rem;">Maestría en Fuerza y Acondicionamiento | Ciencias del Ejercicio UANL</p>
    <p style="color: #888; font-size: 0.9rem;">© 2025 MUPAI. Todos los derechos reservados.</p>
    <p style="color: #888; font-size: 0.8rem;">Respaldado por evidencia científica y tecnología avanzada</p>
</div>
""", unsafe_allow_html=True)
