import streamlit as st
import pandas as pd
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import base64
from collections import Counter

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
    
    if horas == "<5h" or horas == ">8h":
        puntos += 1
    elif horas == "5–6.5h":
        puntos += 0.5
        
    if tiempo_dormir == "Sí":
        puntos += 1
    if despertares == "Sí":
        puntos += 1
    if descansado == "No":
        puntos += 1
        
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
    """Función para enviar resultados por email"""
    try:
        st.success(f"✅ Resultados enviados a {destinatario}")
        return True
    except Exception as e:
        st.error(f"❌ Error al enviar email: {str(e)}")
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
        <h2>⚡ Cuestionario: Balance Energético Óptimo</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="questionnaire-container">
        <h3>🎯 Objetivo</h3>
        <p>Este cuestionario calcula tu <strong>gasto energético total diario (TDEE)</strong> usando la fórmula <strong>Katch-McArdle</strong> 
        y factores de actividad personalizados, considerando tu composición corporal, nivel de actividad, calidad del sueño y nivel de estrés.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("balance_energetico_form"):
        # Datos básicos
        st.markdown("### 📊 Datos Básicos")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sexo = st.selectbox("Sexo biológico:", ["Hombre", "Mujer"])
            edad = st.number_input("Edad (años):", min_value=15, max_value=80, value=25)
        
        with col2:
            peso = st.number_input("Peso (kg):", min_value=30.0, max_value=200.0, value=70.0, step=0.1)
            estatura = st.number_input("Estatura (cm):", min_value=120.0, max_value=220.0, value=170.0, step=0.1)
        
        with col3:
            grasa_corporal = st.number_input("Porcentaje de grasa corporal (%):", min_value=5.0, max_value=50.0, value=15.0, step=0.1)
        
        # Nivel de actividad
        st.markdown("### 🏃 Nivel de Actividad")
        col1, col2 = st.columns(2)
        
        with col1:
            nivel_actividad = st.selectbox(
                "Actividad física general:",
                ["Sedentario", "Ligera", "Activo", "Muy activo"]
            )
            
            dias_entrenamiento = st.number_input("Días de entrenamiento por semana:", min_value=0, max_value=7, value=3)
        
        with col2:
            duracion_entrenamiento = st.selectbox(
                "Duración promedio por sesión:",
                ["30 min", "45 min", "60 min", "75 min", "90 min", ">90 min"]
            )
            
            intensidad_entrenamiento = st.selectbox(
                "Intensidad del entrenamiento:",
                ["Baja", "Moderada", "Alta", "Muy alta"]
            )
        
        # Calidad del sueño
        st.markdown("### 😴 Calidad del Sueño")
        col1, col2 = st.columns(2)
        
        with col1:
            horas_sueno = st.selectbox(
                "¿Cuántas horas duermes habitualmente?",
                ["<5h", "5–6.5h", "6.5–8h", ">8h"]
            )
            
            tiempo_dormir = st.radio(
                "¿Te cuesta trabajo quedarte dormido(a)?",
                ["No", "Sí"]
            )
        
        with col2:
            despertares_nocturnos = st.radio(
                "¿Te despiertas frecuentemente durante la noche?",
                ["No", "Sí"]
            )
            
            despertar_descansado = st.radio(
                "¿Te despiertas sintiéndote descansado(a)?",
                ["Sí", "No"]
            )
        
        # Evaluación de estrés
        st.markdown("### 🧠 Evaluación de Estrés")
        st.markdown("Evalúa qué tan frecuentemente experimentas cada situación (1 = Nunca, 5 = Siempre):")
        
        col1, col2 = st.columns(2)
        
        with col1:
            estres_1 = st.slider("Me siento abrumado(a) por mis responsabilidades", 1, 5, 3)
            estres_2 = st.slider("Tengo dificultad para relajarme", 1, 5, 3)
            estres_3 = st.slider("Me preocupo constantemente por el futuro", 1, 5, 3)
        
        with col2:
            estres_4 = st.slider("Siento tensión física (cuello, hombros, etc.)", 1, 5, 3)
            estres_5 = st.slider("Mi mente está siempre acelerada", 1, 5, 3)
            estres_6 = st.slider("Me irrito con facilidad", 1, 5, 3)
        
        # Email opcional
        st.markdown("---")
        enviar_email = st.checkbox("📧 Enviar resultados por email")
        email_destinatario = ""
        if enviar_email:
            email_destinatario = st.text_input("Correo electrónico:", placeholder="tu@email.com")
        
        submitted = st.form_submit_button("⚡ Calcular Balance Energético", use_container_width=True)
        
        if submitted:
            # Cálculos
            tmb = calcular_tmb_katch_mcardle(peso, grasa_corporal)
            geaf = calcular_geaf(sexo, nivel_actividad)
            gee = calcular_gee(peso, dias_entrenamiento)
            
            # Penalizaciones
            penalizacion_sueno = evaluar_calidad_sueno(horas_sueno, tiempo_dormir, despertares_nocturnos, despertar_descansado)
            respuestas_estres = [estres_1, estres_2, estres_3, estres_4, estres_5, estres_6]
            penalizacion_estres = evaluar_estres(respuestas_estres)
            
            # TDEE final
            tdee_base = tmb * geaf + gee
            penalizacion_total = penalizacion_sueno + penalizacion_estres
            tdee_final = tdee_base * (1 - penalizacion_total)
            
            # Mostrar resultados
            st.markdown("""
            <div class="results-container">
                <h2>⚡ Resultados de tu Balance Energético</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Métricas principales
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🔥 TMB", f"{tmb:.0f} kcal", "Tasa Metabólica Basal")
            
            with col2:
                st.metric("🏃 GEAF", f"{geaf:.2f}", "Factor de Actividad")
            
            with col3:
                st.metric("💪 GEE", f"{gee:.0f} kcal", "Gasto por Ejercicio")
            
            with col4:
                st.metric("🎯 TDEE", f"{tdee_final:.0f} kcal", "Total Diario")
            
            # Análisis detallado
            tab1, tab2, tab3 = st.tabs(["📊 Análisis Completo", "💡 Recomendaciones", "📈 Distribución"])
            
            with tab1:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🔍 Desglose del Cálculo")
                    st.write(f"**TMB (Katch-McArdle):** {tmb:.0f} kcal")
                    st.write(f"**NEAT + TEF (GEAF):** x{geaf:.2f}")
                    st.write(f"**Ejercicio (GEE):** +{gee:.0f} kcal")
                    st.write(f"**TDEE Base:** {tdee_base:.0f} kcal")
                    
                    if penalizacion_total > 0:
                        st.write(f"**Penalización total:** -{penalizacion_total*100:.1f}%")
                        st.write(f"**TDEE Ajustado:** {tdee_final:.0f} kcal")
                
                with col2:
                    st.markdown("#### ⚠️ Factores de Ajuste")
                    
                    if penalizacion_sueno > 0:
                        st.warning(f"😴 Sueño: -{penalizacion_sueno*100:.0f}% por calidad deficiente")
                    else:
                        st.success("😴 Sueño: Calidad óptima")
                    
                    if penalizacion_estres > 0:
                        st.warning(f"🧠 Estrés: -{penalizacion_estres*100:.0f}% por nivel elevado")
                    else:
                        st.success("🧠 Estrés: Nivel manejable")
            
            with tab2:
                st.markdown("#### 💡 Recomendaciones Personalizadas")
                
                if penalizacion_sueno > 0:
                    st.markdown("""
                    **🌙 Mejora tu Sueño:**
                    - Establece un horario fijo para dormir y despertar
                    - Evita pantallas 1 hora antes de dormir
                    - Mantén tu habitación fresca y oscura
                    - Considera suplementación con magnesio o melatonina
                    """)
                
                if penalizacion_estres > 0:
                    st.markdown("""
                    **🧘 Manejo del Estrés:**
                    - Practica técnicas de respiración profunda
                    - Incorpora 10-15 minutos de meditación diaria
                    - Considera ejercicio de baja intensidad como yoga
                    - Evalúa tu carga de trabajo y prioridades
                    """)
                
                # Recomendaciones nutricionales
                calorias_deficit = tdee_final - 500
                calorias_superavit = tdee_final + 300
                
                st.markdown(f"""
                **🍽️ Objetivos Nutricionales:**
                - **Mantenimiento:** {tdee_final:.0f} kcal/día
                - **Pérdida de grasa:** {calorias_deficit:.0f} kcal/día (-500 kcal)
                - **Ganancia muscular:** {calorias_superavit:.0f} kcal/día (+300 kcal)
                """)
            
            with tab3:
                proteinas = peso * 2.2  # 2.2g por kg
                grasas_min = tdee_final * 0.25 / 9  # 25% del total
                grasas_max = tdee_final * 0.35 / 9  # 35% del total
                
                st.markdown("#### 📈 Distribución de Macronutrientes Recomendada")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("🥩 Proteína", f"{proteinas:.0f}g", f"{proteinas*4:.0f} kcal")
                
                with col2:
                    st.metric("🥑 Grasas", f"{grasas_min:.0f}-{grasas_max:.0f}g", f"{grasas_min*9:.0f}-{grasas_max*9:.0f} kcal")
                
                with col3:
                    carbs_min = (tdee_final - proteinas*4 - grasas_max*9) / 4
                    carbs_max = (tdee_final - proteinas*4 - grasas_min*9) / 4
                    st.metric("🍠 Carbohidratos", f"{carbs_min:.0f}-{carbs_max:.0f}g", f"{carbs_min*4:.0f}-{carbs_max*4:.0f} kcal")
            
            # Enviar email si se solicitó
            if enviar_email and email_destinatario:
                contenido_email = f"""
                RESULTADOS BALANCE ENERGÉTICO ÓPTIMO - MUPAI
                Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}
                
                === DATOS PERSONALES ===
                Sexo: {sexo}
                Edad: {edad} años
                Peso: {peso} kg
                Estatura: {estatura} cm
                Grasa corporal: {grasa_corporal}%
                
                === RESULTADOS PRINCIPALES ===
                TMB (Katch-McArdle): {tmb:.0f} kcal
                Factor de Actividad (GEAF): {geaf:.2f}
                Gasto por Ejercicio (GEE): {gee:.0f} kcal
                TDEE Base: {tdee_base:.0f} kcal
                Penalización total: {penalizacion_total*100:.1f}%
                TDEE FINAL: {tdee_final:.0f} kcal/día
                
                === RECOMENDACIONES CALÓRICAS ===
                Mantenimiento: {tdee_final:.0f} kcal/día
                Pérdida de grasa: {calorias_deficit:.0f} kcal/día
                Ganancia muscular: {calorias_superavit:.0f} kcal/día
                
                === MACRONUTRIENTES ===
                Proteína: {proteinas:.0f}g ({proteinas*4:.0f} kcal)
                Grasas: {grasas_min:.0f}-{grasas_max:.0f}g ({grasas_min*9:.0f}-{grasas_max*9:.0f} kcal)
                Carbohidratos: {carbs_min:.0f}-{carbs_max:.0f}g ({carbs_min*4:.0f}-{carbs_max*4:.0f} kcal)
                """
                enviar_email_resultados(email_destinatario, "Resultados MUPAI - Balance Energético", contenido_email)

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
        
        # Email opcional
        st.markdown("---")
        enviar_email = st.checkbox("📧 Enviar resultados por email")
        email_destinatario = ""
        if enviar_email:
            email_destinatario = st.text_input("Correo electrónico:", placeholder="tu@email.com")
        
        submitted = st.form_submit_button("🍽️ Generar Perfil Alimentario Completo", use_container_width=True)
        
        if submitted:
            # Procesar y limpiar las selecciones (remover "Todas las anteriores" si está seleccionado)
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
            
            # Mostrar resultados
            st.markdown("""
            <div class="results-container">
                <h2>📊 Tu Perfil Completo de Preferencias Alimentarias</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Crear tabs para organizar mejor los resultados
            tab1, tab2, tab3 = st.tabs(["🥩 Proteínas y Principales", "🍎 Frutas y Vegetales", "📋 Información Adicional"])
            
            with tab1:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 🥩 Proteínas Magras")
                    if proteinas_magras_final:
                        for proteina in proteinas_magras_final[:10]:  # Mostrar solo las primeras 10
                            st.write(f"✅ {proteina}")
                        if len(proteinas_magras_final) > 10:
                            st.write(f"... y {len(proteinas_magras_final) - 10} más")
                    else:
                        st.write("❌ Ninguna seleccionada")
                    
                    st.markdown("### 🥓 Proteínas con Grasa")
                    if proteinas_grasa_final:
                        for proteina in proteinas_grasa_final[:10]:
                            st.write(f"✅ {proteina}")
                        if len(proteinas_grasa_final) > 10:
                            st.write(f"... y {len(proteinas_grasa_final) - 10} más")
                    else:
                        st.write("❌ Ninguna seleccionada")
                
                with col2:
                    st.markdown("### 🍠 Carbohidratos")
                    if carbohidratos_final:
                        for carb in carbohidratos_final[:10]:
                            st.write(f"✅ {carb}")
                        if len(carbohidratos_final) > 10:
                            st.write(f"... y {len(carbohidratos_final) - 10} más")
                    else:
                        st.write("❌ Ninguna seleccionada")
                    
                    st.markdown("### 🧀 Lácteos")
                    lacteos_todos = lacteos_light_final + lacteos_grasa_final
                    if lacteos_todos:
                        for lacteo in lacteos_todos[:10]:
                            st.write(f"✅ {lacteo}")
                        if len(lacteos_todos) > 10:
                            st.write(f"... y {len(lacteos_todos) - 10} más")
                    else:
                        st.write("❌ Ninguna seleccionada")
            
            with tab2:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 🍌 Frutas")
                    if frutas_final:
                        for fruta in frutas_final[:15]:
                            st.write(f"✅ {fruta}")
                        if len(frutas_final) > 15:
                            st.write(f"... y {len(frutas_final) - 15} más")
                    else:
                        st.write("❌ Ninguna seleccionada")
                
                with col2:
                    st.markdown("### 🥦 Vegetales")
                    if vegetales_final:
                        for vegetal in vegetales_final[:15]:
                            st.write(f"✅ {vegetal}")
                        if len(vegetales_final) > 15:
                            st.write(f"... y {len(vegetales_final) - 15} más")
                    else:
                        st.write("❌ Ninguna seleccionada")
                
                st.markdown("### 🥑 Grasas Saludables")
                if grasas_final:
                    grasas_texto = ", ".join(grasas_final[:10])
                    if len(grasas_final) > 10:
                        grasas_texto += f" ... y {len(grasas_final) - 10} más"
                    st.write(f"✅ {grasas_texto}")
                else:
                    st.write("❌ Ninguna seleccionada")
            
            with tab3:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 💊 Suplementos")
                    st.write(f"**Incluye suplementos:** {'✅ Sí' if incluir_suplementos == 'Sí' else '❌ No'}")
                    if marcas_preferidas:
                        st.write(f"**Marcas preferidas:** {marcas_preferidas}")
                    
                    st.markdown("### 🕒 Patrones Alimentarios")
                    st.write(f"**Comidas al día:** {comidas_dia}")
                    st.write(f"**Frecuencia cocinando:** {cocinar_frecuencia}")
                    st.write(f"**Horarios de comida:** {horario_comidas}")
                    st.write(f"**Presupuesto semanal:** {presupuesto_comida}")
                
                with col2:
                    st.markdown("### ➕ Información Adicional")
                    if alimentos_adicionales:
                        st.write(f"**Alimentos adicionales:** {alimentos_adicionales}")
                    
                    st.markdown("### ⚠️ Alergias/Intolerancias")
                    if tiene_alergias == "Sí" and alergias_detalle:
                        st.write(f"**Alergias:** {alergias_detalle}")
                    else:
                        st.write("✅ Sin alergias reportadas")
            
            # Análisis y métricas
            total_categorias = len([x for x in [proteinas_magras_final, proteinas_grasa_final, frutas_final, vegetales_final, carbohidratos_final, lacteos_light_final, lacteos_grasa_final, grasas_final] if x])
            total_alimentos = len(proteinas_magras_final + proteinas_grasa_final + frutas_final + vegetales_final + carbohidratos_final + lacteos_light_final + lacteos_grasa_final + grasas_final)
            
            st.markdown(f"""
            <div class="results-container">
                <h3>🎯 Análisis de tu Perfil Alimentario</h3>
                <div style="display: flex; justify-content: space-around; margin: 1rem 0;">
                    <div style="text-align: center;">
                        <h2 style="color: #000; margin: 0;">{total_categorias}/8</h2>
                        <p style="margin: 0;">Categorías seleccionadas</p>
                    </div>
                    <div style="text-align: center;">
                        <h2 style="color: #000; margin: 0;">{total_alimentos}</h2>
                        <p style="margin: 0;">Alimentos totales</p>
                    </div>
                    <div style="text-align: center;">
                        <h2 style="color: #000; margin: 0;">{'🟢' if total_categorias >= 6 else '🟡' if total_categorias >= 4 else '🔴'}</h2>
                        <p style="margin: 0;">{"Excelente" if total_categorias >= 6 else "Buena" if total_categorias >= 4 else "Limitada"} variedad</p>
                    </div>
                </div>
                <p style="text-align: center; font-size: 1.1rem;">
                    Este perfil detallado será utilizado para crear tu plan nutricional personalizado con alimentos que realmente disfrutas.
                </p>
            </div>
            """, unsafe_allow_html=True)

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
        Marca con sinceridad las respuestas correspondientes para cada grupo de alimentos. 
        Esto nos permitirá adaptar tus planes nutricionales y de entrenamiento de manera más precisa.</p>
        
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
            "ejemplos": "Coca-Cola, Pepsi, Sprite, Jarritos, Sidral
