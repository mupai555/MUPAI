import streamlit as st
import pandas as pd
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import base64
from collections import Counter
from cuestionario_fbeo import mostrar_cuestionario_fbeo

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

# FUNCIÓN DE EMAIL CORREGIDA
def enviar_email_resultados(destinatario, asunto, contenido):
    """Función para enviar resultados por email - CORREGIDA"""
    try:
        # CONFIGURACIÓN CORREGIDA
        email_origen = "mupaitraining@outlook.com"
        password = "MuscleUp55"
        
        # Crear mensaje con encoding correcto
        mensaje = MIMEMultipart()
        mensaje['From'] = email_origen
        mensaje['To'] = destinatario
        mensaje['Subject'] = asunto
        
        # Adjuntar contenido con encoding UTF-8
        mensaje.attach(MIMEText(contenido, 'plain', 'utf-8'))
        
        # SERVIDOR SMTP CORREGIDO
        with smtplib.SMTP("smtp.office365.com", 587) as servidor:
            servidor.starttls()
            servidor.login(email_origen, password)
            servidor.send_message(mensaje)
        
        st.success(f"✅ Email enviado exitosamente a {destinatario}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        st.error("❌ Error de autenticación - Verifica credenciales")
        return False
    except smtplib.SMTPException as e:
        st.error(f"❌ Error SMTP: {str(e)}")
        return False
    except Exception as e:
        st.error(f"❌ Error general: {str(e)}")
        return False

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
    
    if st.button("📊 Cuestionario FBEO", use_container_width=True):
        st.session_state.page = "cuestionario_fbeo"
    
    st.markdown("---")
    
    if st.button("👨‍🎓 Acerca del Profesional", use_container_width=True):
        st.session_state.page = "about"
    
    if st.button("📞 Contacto", use_container_width=True):
        st.session_state.page = "contacto"

# ==================== PÁGINA DE INICIO ====================
if st.session_state.page == "inicio":
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
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("""
        <div class="corporate-section">
            <h3>📘 Política del Servicio</h3>
            <ul style="font-size: 1rem; line-height: 1.8;">
                <li><strong>🔬 Diseñamos entrenamientos digitales</strong> que combinan personalización, datos confiables y ciencia del ejercicio.</li>
                <li><strong>💻 Aprovechamos la tecnología</strong> para ofrecer un servicio accesible y adaptable a las necesidades de cada usuario.</li>
                <li><strong>🔒 Respetamos y protegemos la privacidad</strong> de los datos personales, garantizando su uso responsable.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Servicios
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
            <p>Cálculo personalizado de tu ingesta calórica ideal usando fórmulas científicas avanzadas.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🍽️ Preferencias Alimentarias</h3>
            <p>Análisis detallado de tus gustos alimentarios con más de 150 opciones organizadas.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🧁 Antojos Alimentarios</h3>
            <p>Evaluación especializada para población mexicana que analiza patrones emocionales.</p>
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
        actividad física, frecuencia de entrenamiento, calidad de la dieta, y estado de recuperación fisiológica.</p>
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
            # TODOS LOS CÁLCULOS INTERNOS
            tmb = 370 + (21.6 * masa_magra)
            ger = tmb * 1.1
            
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
            gee = masa_magra * 5
            get_con_entrenamiento = ger * geaf + gee
            get_sin_entrenamiento = ger * geaf
            get_promedio = ((get_con_entrenamiento * dias_entrenamiento) + 
                           (get_sin_entrenamiento * (7 - dias_entrenamiento))) / 7
            
            # FBEO base
            if sexo == "Hombre":
                if grasa_corporal > 25:
                    fbeo_base = 0.875
                elif 18 <= grasa_corporal <= 24:
                    fbeo_base = 0.975
                elif 12 <= grasa_corporal < 18:
                    fbeo_base = 1.05
                else:
                    fbeo_base = 1.125
            else:
                if grasa_corporal > 32:
                    fbeo_base = 0.875
                elif 25 <= grasa_corporal <= 31:
                    fbeo_base = 0.975
                elif 20 <= grasa_corporal < 25:
                    fbeo_base = 1.05
                else:
                    fbeo_base = 1.125
            
            # Evaluación estrés y sueño
            pss_valores = {
                "Nunca (0)": 0, "Casi nunca (1)": 1, "A veces (2)": 2, 
                "Frecuentemente (3)": 3, "Muy frecuentemente (4)": 4,
                "Nunca (4)": 4, "Casi nunca (3)": 3, "Frecuentemente (1)": 1, 
                "Muy frecuentemente (0)": 0
            }
            
            pss_total = (pss_valores[pss1] + pss_valores[pss2] + 
                        pss_valores[pss3] + pss_valores[pss4])
            estres_alto = pss_total > 13
            
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
            
            # Ajustes FBEO
            ajuste_fbeo = 0
            if estres_alto and sueno_malo:
                if fbeo_base < 1.0:
                    ajuste_fbeo = 0.10
                else:
                    ajuste_fbeo = -0.10
            elif estres_alto or sueno_malo:
                if fbeo_base < 1.0:
                    ajuste_fbeo = 0.05
                else:
                    ajuste_fbeo = -0.05
            
            fbeo_ajustado = fbeo_base + ajuste_fbeo
            fbeo_ajustado = max(0.80, min(fbeo_ajustado, 1.20))
            calorias_totales = get_promedio * fbeo_ajustado
            
            # Macronutrientes
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
            
            # MOSTRAR SOLO INFORMACIÓN BÁSICA AL USUARIO
            st.success("✅ **¡Evaluación completada exitosamente!**")
            
            st.info("""
            🎯 **Tu evaluación ha sido procesada y enviada a tu entrenador MUPAI**
            
            **Próximos pasos:**
            1. ⏰ Recibirás contacto en 24-48 horas
            2. 📋 Tu entrenador analizará todos tus datos
            3. 🎯 Obtendrás tu plan personalizado completo
            4. 🚀 ¡Comenzarás tu transformación!
            
            **Importante:** Mantén tu teléfono disponible para el contacto inicial.
            """)
            
            # Mostrar objetivo básico
            if fbeo_ajustado < 0.95:
                objetivo_simple = "🎯 Objetivo: Optimización de composición corporal"
            elif fbeo_ajustado > 1.05:
                objetivo_simple = "🎯 Objetivo: Desarrollo muscular"
            else:
                objetivo_simple = "🎯 Objetivo: Recomposición corporal"
            
            st.info(objetivo_simple)
            
            # Confirmación básica
            st.markdown("### ✅ Confirmación")
            st.write("📊 Evaluación completa enviada al entrenador")
            st.write("📧 Revisa tu email para confirmación")
            
            # ENVIAR EMAIL COMPLETO SOLO AL ENTRENADOR
            if not email_destinatario:
                st.error("⚠️ **Error:** Debes proporcionar un correo electrónico para el seguimiento.")
            else:
                contenido_email = f"""
========================================
📊 NUEVO CLIENTE - EVALUACIÓN FBEO
========================================
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Email del cliente: {email_destinatario}

========================================
👤 PERFIL DEL CLIENTE
========================================
Sexo: {sexo}
Peso: {peso} kg
Estatura: {estatura} m
IMC: {peso/(estatura**2):.1f}
Grasa corporal: {grasa_corporal}%
Masa magra: {masa_magra:.1f} kg

========================================
🏃 PERFIL DE ACTIVIDAD FÍSICA
========================================
Nivel de actividad: {nivel_actividad}
Descripción: {datos_actividad['descripcion']}
Pasos diarios estimados: {datos_actividad['pasos']}
Factor GEAF aplicado: {geaf}
Días de entrenamiento semanal: {dias_entrenamiento}

========================================
😴 EVALUACIÓN DEL SUEÑO
========================================
Horas de sueño: {horas_sueno}
Tiempo para dormir: {tiempo_dormir}
Despertares nocturnos: {despertares_nocturnos}
Calidad percibida: {calidad_percibida}

PUNTUACIÓN TOTAL: {sueno_promedio:.1f}/5
EVALUACIÓN: {'⚠️ CALIDAD DEFICIENTE - Requiere intervención' if sueno_malo else '✅ CALIDAD ADECUADA'}

========================================
🧠 EVALUACIÓN DEL ESTRÉS (PSS-4)
========================================
Pregunta 1 (Control): {pss1}
Pregunta 2 (Confianza): {pss2}
Pregunta 3 (Las cosas van bien): {pss3}
Pregunta 4 (Dificultades acumuladas): {pss4}

PUNTUACIÓN TOTAL PSS-4: {pss_total}/16
EVALUACIÓN: {'⚠️ ESTRÉS ALTO - Requiere manejo activo' if estres_alto else '✅ ESTRÉS MANEJABLE'}

========================================
⚡ CÁLCULOS ENERGÉTICOS DETALLADOS
========================================
TMB (Katch-McArdle): {tmb:.0f} kcal
GER (Gasto en reposo): {ger:.0f} kcal
GEE por sesión: {gee:.0f} kcal
GET con entrenamiento: {get_con_entrenamiento:.0f} kcal
GET sin entrenamiento: {get_sin_entrenamiento:.0f} kcal
GET promedio semanal: {get_promedio:.0f} kcal

========================================
📊 FACTOR DE BALANCE ENERGÉTICO (FBEO)
========================================
FBEO base según {grasa_corporal:.1f}% GC: {fbeo_base:.3f}
Ajuste por estrés/sueño: {'+' if ajuste_fbeo > 0 else ''}{ajuste_fbeo:.2f}
FBEO FINAL: {fbeo_ajustado:.3f}

========================================
🍽️ PLAN NUTRICIONAL CALCULADO
========================================
CALORÍAS TOTALES: {calorias_totales:.0f} kcal/día

• Proteína: {proteinas_g_ajustadas:.0f}g ({proteinas_kcal_ajustadas:.0f} kcal)
• Grasas: {grasas_g_ajustadas:.0f}g ({grasas_kcal_ajustadas:.0f} kcal)
• Carbohidratos: {carbs_g_ajustadas:.0f}g ({carbs_kcal_ajustadas:.0f} kcal)

========================================
📝 NOTAS PARA EL ENTRENADOR
========================================
- Cliente evaluado el {datetime.now().strftime('%Y-%m-%d %H:%M')}
- Requiere seguimiento {'prioritario' if (estres_alto or sueno_malo) else 'estándar'}
- Contactar en próximas 24-48 horas
========================================
"""
                
                try:
                    enviar_email_resultados("mupaitraining@outlook.com", 
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
        <h3>🎯 Objetivo</h3>
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
            "Todas las anteriores", "Pechuga de pollo", "Claras de huevo", "Lomo de cerdo",
            "Lomo de res", "Top sirloin", "Bacalao", "Atún en agua", "Tilapia", "Mojarra",
            "Carne molida magra (90/10 a 97/3)", "Filete de merluza", "Pargo", "Pez espada",
            "Lenguado", "Conejo", "Codorniz", "Pechuga de pavo", "Atún fresco", "Surimi light", "Ostras"
        ]
        
        proteinas_magras = st.multiselect(
            "Selecciona las proteínas magras que consumes:",
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
            "Todas las anteriores", "Huevo entero", "Costilla de cerdo", "Chuleta natural",
            "Chuleta ahumada", "Muslo de pollo con piel", "Arrachera", "Rib-eye", "Salmón",
            "Sardinas", "T-bone", "Carne molida regular (80/20 a 85/15)", "Diezmillo",
            "Steak del 7", "Falda", "Picaña", "Tocino", "Pierna de pato", "Chorizo artesanal",
            "Longaniza de cerdo", "Atún en aceite"
        ]
        
        proteinas_grasa = st.multiselect(
            "Selecciona las proteínas con grasa que consumes:",
            proteinas_grasa_opciones,
            key="proteinas_grasa"
        )
        
        # --- FRUTAS ---
        st.markdown("""
        <div class="questionnaire-container">
            <h3>🍌 Frutas</h3>
        </div>
        """, unsafe_allow_html=True)
        
        frutas_opciones = [
            "Todas las anteriores", "Plátano", "Manzana", "Pera", "Fresa", "Mango", "Papaya",
            "Sandía", "Piña", "Kiwi", "Moras (zarzamora, frambuesa, arándano)", "Uvas",
            "Granada", "Naranja", "Mandarina", "Guayaba", "Melón", "Higo", "Durazno", "Cereza", "Ciruela"
        ]
        
        frutas = st.multiselect(
            "Selecciona las frutas que prefieres:",
            frutas_opciones,
            key="frutas"
        )
        
        # --- VEGETALES ---
        st.markdown("""
        <div class="questionnaire-container">
            <h3>🥦 Vegetales</h3>
        </div>
        """, unsafe_allow_html=True)
        
        vegetales_opciones = [
            "Todas las anteriores", "Espinaca", "Brócoli", "Zanahoria", "Calabaza", "Pepino",
            "Lechuga", "Jitomate", "Betabel", "Champiñones", "Espárragos", "Coliflor",
            "Acelga", "Ejotes", "Nopales", "Pimiento morrón (rojo, verde, amarillo)",
            "Apio", "Cebolla morada", "Cebolla blanca", "Rábanos", "Col de Bruselas"
        ]
        
        vegetales = st.multiselect(
            "Selecciona los vegetales que prefieres:",
            vegetales_opciones,
            key="vegetales"
        )
        
        # --- CARBOHIDRATOS ---
        st.markdown("""
        <div class="questionnaire-container">
            <h3>🍠 Carbohidratos altos en almidón</h3>
        </div>
        """, unsafe_allow_html=True)
        
        carbohidratos_opciones = [
            "Todas las anteriores", "Arroz blanco", "Arroz integral", "Papa blanca", "Papa roja",
            "Papa amarilla", "Camote", "Tortilla de maíz", "Tortilla de nopal", "Pan integral",
            "Pan de centeno", "Pasta integral", "Avena", "Quinoa", "Trigo sarraceno",
            "Amaranto", "Pan pita integral", "Harina de avena", "Tapioca", "Yuca cocida",
            "Elote (mazorca)", "Tortilla de avena"
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
            "Todas las anteriores", "Leche descremada", "Leche semidescremada",
            "Yogur griego sin azúcar (0–2% grasa)", "Yogur natural bajo en grasa",
            "Queso panela", "Queso cottage bajo en grasa", "Requesón bajo en grasa",
            "Leche de almendra sin azúcar", "Leche de soya sin azúcar", "Queso ricotta light",
            "Queso Oaxaca bajo en grasa", "Queso manchego light", "Queso mozzarella light"
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
            "Todas las anteriores", "Leche entera", "Crema entera", "Mantequilla",
            "Yogur griego entero", "Yogur natural entero", "Queso manchego",
            "Queso cheddar", "Queso crema", "Queso Oaxaca", "Queso gouda"
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
            "Todas las anteriores", "Aguacate", "Aceite de oliva extra virgen", "Almendras",
            "Nueces", "Mantequilla de maní", "Mantequilla de almendra", "Chía",
            "Linaza molida", "Aceitunas", "Tahini (pasta de ajonjolí)", "Semillas de girasol",
            "Semillas de calabaza", "Pistaches", "Nueces de la India", "Avellanas",
            "Cacahuates naturales", "Ghee", "Aceite de aguacate", "Aceite de coco (con moderación)",
            "Crema de cacahuate sin azúcar"
        ]
        
        grasas = st.multiselect(
            "Selecciona las grasas saludables que prefieres:",
            grasas_opciones,
            key="grasas"
        )
        
        # --- INFORMACIÓN ADICIONAL ---
        st.markdown("---")
        st.markdown("""
        <div class="questionnaire-container">
            <h3>📧 Información de Contacto</h3>
        </div>
        """, unsafe_allow_html=True)
        
        email_destinatario = st.text_input("Email para seguimiento (obligatorio):", placeholder="tu@email.com")
        
        submitted = st.form_submit_button("🍽️ Enviar Evaluación al Entrenador", use_container_width=True)
        
        if submitted:
            # Procesar selecciones
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
            
            # MOSTRAR INFORMACIÓN BÁSICA AL USUARIO
            st.success("✅ **¡Preferencias alimentarias registradas!**")
            
            st.info("""
            🍽️ **Tu perfil nutricional ha sido creado exitosamente**
            
            **Lo que sigue:**
            1. 📊 Tu entrenador analizará tus preferencias
            2. 🎯 Creará un plan adaptado a tus gustos
            3. 📞 Te contactará para coordinar detalles
            4. 🚀 ¡Disfrutarás de una alimentación personalizada!
            
            **Tiempo estimado:** 24-48 horas para contacto inicial
            """)
            
            # Confirmación básica
            total_seleccionados = len(proteinas_magras_final + proteinas_grasa_final + 
                                    frutas_final + vegetales_final + carbohidratos_final + 
                                    lacteos_light_final + lacteos_grasa_final + grasas_final)
            
            st.metric("✅ Perfil Nutricional", f"{total_seleccionados} alimentos registrados")
            
            # ENVIAR EMAIL COMPLETO SOLO AL ENTRENADOR
            if not email_destinatario:
                st.error("⚠️ **Error:** Debes proporcionar un correo electrónico para el seguimiento.")
            else:
                contenido_email = f"""
========================================
📊 NUEVO CLIENTE - PREFERENCIAS ALIMENTARIAS
========================================
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Email del cliente: {email_destinatario}

========================================
🥩 PROTEÍNAS MAGRAS SELECCIONADAS ({len(proteinas_magras_final)} items)
========================================
{', '.join(proteinas_magras_final) if proteinas_magras_final else 'Ninguna seleccionada'}

========================================
🥓 PROTEÍNAS CON GRASA SELECCIONADAS ({len(proteinas_grasa_final)} items)
========================================
{', '.join(proteinas_grasa_final) if proteinas_grasa_final else 'Ninguna seleccionada'}

========================================
🍌 FRUTAS SELECCIONADAS ({len(frutas_final)} items)
========================================
{', '.join(frutas_final) if frutas_final else 'Ninguna seleccionada'}

========================================
🥦 VEGETALES SELECCIONADOS ({len(vegetales_final)} items)
========================================
{', '.join(vegetales_final) if vegetales_final else 'Ninguna seleccionada'}

========================================
🍠 CARBOHIDRATOS SELECCIONADOS ({len(carbohidratos_final)} items)
========================================
{', '.join(carbohidratos_final) if carbohidratos_final else 'Ninguna seleccionada'}

========================================
🧀 LÁCTEOS BAJOS EN GRASA ({len(lacteos_light_final)} items)
========================================
{', '.join(lacteos_light_final) if lacteos_light_final else 'Ninguna seleccionada'}

========================================
🧀 LÁCTEOS ALTOS EN GRASA ({len(lacteos_grasa_final)} items)
========================================
{', '.join(lacteos_grasa_final) if lacteos_grasa_final else 'Ninguna seleccionada'}

========================================
🥑 GRASAS SALUDABLES ({len(grasas_final)} items)
========================================
{', '.join(grasas_final) if grasas_final else 'Ninguna seleccionada'}

========================================
📊 ANÁLISIS NUTRICIONAL
========================================
Total de alimentos seleccionados: {total_seleccionados}
Variedad alimentaria: {'Excelente' if total_seleccionados >= 50 else 'Buena' if total_seleccionados >= 30 else 'Limitada'}

========================================
📝 NOTAS PARA EL ENTRENADOR
========================================
- Cliente evaluado el {datetime.now().strftime('%Y-%m-%d %H:%M')}
- Contactar en próximas 24-48 horas para plan personalizado
========================================
"""
                
                try:
                    enviar_email_resultados("mupaitraining@outlook.com", 
                                          f"NUEVO CLIENTE PREFERENCIAS - {email_destinatario}", 
                                          contenido_email)
                    st.success("✅ Evaluación enviada correctamente al entrenador")
                except Exception as e:
                    st.error(f"❌ Error al enviar email: {str(e)}")

# ==================== CUESTIONARIO ANTOJOS ALIMENTARIOS ====================
elif st.session_state.page == "antojos_alimentarios":
    st.markdown("""
    <div class="section-header">
        <h2>🧁 Cuestionario de Antojos Alimentarios - Versión Población Mexicana</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="questionnaire-container">
        <h3>🎯 Objetivo</h3>
        <p>Identificar tu <strong>perfil personal de antojos alimentarios</strong> para adaptar tu plan nutricional 
        considerando tus patrones y estrategias de manejo.</p>
    </div>
    """, unsafe_allow_html=True)
    
    categorias_antojos_mexicanas = [
        {"emoji": "🧁", "nombre": "Panes dulces", "ejemplos": "Gansito, Donitas Bimbo, Barritas, Roles"},
        {"emoji": "🍟", "nombre": "Frituras", "ejemplos": "Sabritas, Ruffles, Doritos, Chetos, Takis"},
        {"emoji": "🍫", "nombre": "Chocolates y dulces", "ejemplos": "Carlos V, Snickers, Kinder Bueno, M&M's"},
        {"emoji": "🧀", "nombre": "Quesos grasos", "ejemplos": "Manchego, Oaxaca, Gouda, Queso crema"},
        {"emoji": "🍞", "nombre": "Pan blanco", "ejemplos": "Bolillo, Telera, Baguette, Pan dulce"},
        {"emoji": "🥤", "nombre": "Refrescos", "ejemplos": "Coca-Cola, Pepsi, Sprite, Jarritos"},
        {"emoji": "🍨", "nombre": "Helados", "ejemplos": "Helado de vainilla, Chocolate, Fresa, Paletas"},
        {"emoji": "🥙", "nombre": "Comida rápida mexicana", "ejemplos": "Tacos al pastor, Quesadillas, Tortas"},
        {"emoji": "🍕", "nombre": "Pizza y comida internacional", "ejemplos": "Pizza, Hamburguesas, Hot dogs"},
        {"emoji": "🍺", "nombre": "Alcohol", "ejemplos": "Cerveza, Tequila, Mezcal, Vino, Micheladas"}
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
                
                intensidad = st.slider(
                    "Intensidad del antojo (1-10)",
                    1, 10, 5, key=f"intensidad_{i}"
                )
                
                control = st.selectbox(
                    "¿Qué tan fácil es controlar este antojo?",
                    ["Muy fácil", "Fácil", "Moderado", "Difícil", "Muy difícil"],
                    key=f"control_{i}"
                )
            
            with col2:
                momento = st.selectbox(
                    "¿En qué momento del día aparece más?",
                    ["Mañana", "Media mañana", "Mediodía", "Tarde", "Noche", "Madrugada"],
                    key=f"momento_{i}"
                )
                
                emocion = st.selectbox(
                    "¿Qué emoción lo detona principalmente?",
                    ["Ninguna", "Estrés", "Ansiedad", "Tristeza", "Aburrimiento", "Felicidad"],
                    key=f"emocion_{i}"
                )
            
            resultados_antojos[categoria['nombre']] = {
                'frecuencia': frecuencia,
                'intensidad': intensidad,
                'control': control,
                'momento': momento,
                'emocion': emocion
            }
            
            st.markdown("---")
        
        st.markdown("""
        <div class="questionnaire-container">
            <h3>📧 Información de Contacto</h3>
        </div>
        """, unsafe_allow_html=True)
        
        email_destinatario = st.text_input("Email para seguimiento (obligatorio):", placeholder="tu@email.com")
        
        submitted = st.form_submit_button("🧁 Enviar Evaluación al Entrenador", use_container_width=True)
        
        if submitted:
            # MOSTRAR INFORMACIÓN BÁSICA AL USUARIO
            st.success("✅ **¡Evaluación de antojos completada!**")
            
            st.info("""
            🧁 **Tu perfil de antojos ha sido analizado**
            
            **Beneficios que obtendrás:**
            1. 🎯 Estrategias personalizadas de manejo
            2. 🔄 Alternativas saludables para tus antojos
            3. 🧠 Técnicas de control emocional
            4. 📋 Plan integral adaptado a tus patrones
            
            **Tu entrenador te contactará pronto con tu plan personalizado**
            """)
            
            # Análisis básico
            antojos_frecuentes = [k for k, v in resultados_antojos.items() 
                                if v['frecuencia'] in ["Frecuentemente (3-4 veces/semana)", "Muy frecuentemente (diario)"]]
            
            st.metric("✅ Análisis Completado", f"{len(antojos_frecuentes)} antojos frecuentes identificados")
            
            # ENVIAR EMAIL COMPLETO SOLO AL ENTRENADOR
            if not email_destinatario:
                st.error("⚠️ **Error:** Debes proporcionar un correo electrónico para el seguimiento.")
            else:
                contenido_email = f"""
========================================
📊 NUEVO CLIENTE - ANTOJOS ALIMENTARIOS
========================================
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Email del cliente: {email_destinatario}

========================================
🧁 ANÁLISIS DETALLADO POR CATEGORÍA
========================================
"""
                
                for categoria, datos in resultados_antojos.items():
                    emoji = next(c['emoji'] for c in categorias_antojos_mexicanas if c['nombre'] == categoria)
                    contenido_email += f"""
{emoji} {categoria.upper()}:
  • Frecuencia: {datos['frecuencia']}
  • Intensidad: {datos['intensidad']}/10
  • Control: {datos['control']}
  • Momento: {datos['momento']}
  • Emoción: {datos['emocion']}

"""
                
                intensidad_promedio = sum([v['intensidad'] for v in resultados_antojos.values()]) / len(resultados_antojos)
                nivel_riesgo = "Alto" if len(antojos_frecuentes) >= 4 else "Medio" if len(antojos_frecuentes) >= 2 else "Bajo"
                
                contenido_email += f"""
========================================
📊 RESUMEN EJECUTIVO
========================================
Antojos frecuentes: {len(antojos_frecuentes)} categorías
Intensidad promedio: {intensidad_promedio:.1f}/10
Nivel de riesgo: {nivel_riesgo}

Categorías frecuentes:
{', '.join(antojos_frecuentes) if antojos_frecuentes else 'Ninguna'}

========================================
📝 NOTAS PARA EL ENTRENADOR
========================================
- Cliente evaluado el {datetime.now().strftime('%Y-%m-%d %H:%M')}
- Prioridad: {'alta' if len(antojos_frecuentes) >= 4 else 'media' if len(antojos_frecuentes) >= 2 else 'baja'}
- Contactar en próximas 24-48 horas
========================================
"""
                
                try:
                    enviar_email_resultados("mupaitraining@outlook.com", 
                                          f"NUEVO CLIENTE ANTOJOS - {email_destinatario}", 
                                          contenido_email)
                    st.success("✅ Evaluación enviada correctamente al entrenador")
                except Exception as e:
                    st.error(f"❌ Error al enviar email: {str(e)}")

# ==================== CUESTIONARIO FBEO ====================
elif st.session_state.page == "cuestionario_fbeo":
    mostrar_cuestionario_fbeo()

# ==================== ACERCA DEL PROFESIONAL ====================
elif st.session_state.page == "about":
    st.markdown("""
    <div class="section-header">
        <h2>👨‍🎓 Acerca del Profesional</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="professional-profile">
        <h3>Erick Francisco De Luna Hernández</h3>
        <p><strong>Maestría en Fuerza y Acondicionamiento | Ciencias del Ejercicio UANL</strong></p>
        <p>Especialista en entrenamiento digital basado en ciencia</p>
    </div>
    """, unsafe_
