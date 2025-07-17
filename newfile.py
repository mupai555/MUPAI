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

# ==================== NUEVAS FUNCIONES PARA CUESTIONARIO AVANZADO ====================

def ajustar_grasa_corporal(porcentaje_grasa, metodo_medicion, sexo, numero_pliegues=None):
    """
    Ajusta automáticamente el porcentaje de grasa corporal según el método de medición
    """
    if metodo_medicion == "DEXA":
        return porcentaje_grasa  # DEXA es la referencia, no necesita ajuste
    
    elif metodo_medicion == "BIA":
        # Ajustes para BIA según rangos
        if sexo == "Masculino":
            if porcentaje_grasa < 15:
                return porcentaje_grasa + 2.5
            elif porcentaje_grasa < 25:
                return porcentaje_grasa + 1.8
            else:
                return porcentaje_grasa + 1.2
        else:  # Femenino
            if porcentaje_grasa < 20:
                return porcentaje_grasa + 3.0
            elif porcentaje_grasa < 30:
                return porcentaje_grasa + 2.2
            else:
                return porcentaje_grasa + 1.5
    
    elif metodo_medicion == "Fórmula Naval":
        # Ajustes para Fórmula Naval
        if sexo == "Masculino":
            if porcentaje_grasa < 15:
                return porcentaje_grasa + 1.5
            elif porcentaje_grasa < 25:
                return porcentaje_grasa + 1.0
            else:
                return porcentaje_grasa + 0.5
        else:  # Femenino
            if porcentaje_grasa < 20:
                return porcentaje_grasa + 2.0
            elif porcentaje_grasa < 30:
                return porcentaje_grasa + 1.5
            else:
                return porcentaje_grasa + 1.0
    
    elif metodo_medicion == "Antropometría":
        # Ajustes según número de pliegues
        if numero_pliegues == 3:
            return porcentaje_grasa + 2.0
        elif numero_pliegues == 4:
            return porcentaje_grasa + 1.5
        elif numero_pliegues == 7:
            return porcentaje_grasa + 1.0
        else:
            return porcentaje_grasa + 1.8  # Valor por defecto
    
    return porcentaje_grasa

def calcular_ffmi(peso, estatura, porcentaje_grasa):
    """
    Calcula el Fat-Free Mass Index (FFMI)
    """
    masa_magra = peso * (1 - porcentaje_grasa / 100)
    ffmi = masa_magra / (estatura ** 2)
    return ffmi

def calcular_factor_actividad(nivel_actividad, sexo):
    """
    Calcula el factor de actividad específico por género
    """
    factores = {
        "Sedentario": {"Masculino": 1.40, "Femenino": 1.35},
        "Ligeramente activo": {"Masculino": 1.55, "Femenino": 1.50},
        "Moderadamente activo": {"Masculino": 1.70, "Femenino": 1.65},
        "Muy activo": {"Masculino": 1.85, "Femenino": 1.80},
        "Extremadamente activo": {"Masculino": 2.00, "Femenino": 1.95}
    }
    
    return factores.get(nivel_actividad, {}).get(sexo, 1.40)

def evaluar_pittsburgh(horas_sueno, tiempo_dormir, despertares, calidad_percibida):
    """
    Evalúa la calidad del sueño usando escala Pittsburgh abreviada (0-16)
    """
    # Mapeo de respuestas a puntuaciones
    horas_map = {
        "Más de 9h": 0, "8-9h": 1, "7-8h": 2, "6-7h": 3, "5-6h": 4, "Menos de 5h": 5
    }
    
    tiempo_map = {
        "Menos de 15 min": 0, "15-30 min": 1, "30-45 min": 2, "45-60 min": 3, "Más de 60 min": 4
    }
    
    despertares_map = {
        "Nunca": 0, "1 vez": 1, "2 veces": 2, "3 veces": 3, "Más de 3 veces": 4
    }
    
    calidad_map = {
        "Excelente": 0, "Buena": 1, "Regular": 2, "Mala": 3, "Muy mala": 4
    }
    
    puntuacion = (horas_map.get(horas_sueno, 3) + 
                  tiempo_map.get(tiempo_dormir, 2) + 
                  despertares_map.get(despertares, 1) + 
                  calidad_map.get(calidad_percibida, 2))
    
    return puntuacion

def evaluar_pss4(respuesta1, respuesta2, respuesta3, respuesta4):
    """
    Evalúa estrés usando PSS-4 con ítems invertidos 2 y 3
    """
    # Mapeo de respuestas a puntuaciones
    normal_map = {
        "Nunca": 0, "Casi nunca": 1, "A veces": 2, "Frecuentemente": 3, "Muy frecuentemente": 4
    }
    
    # Ítems invertidos (2 y 3)
    invertido_map = {
        "Nunca": 4, "Casi nunca": 3, "A veces": 2, "Frecuentemente": 1, "Muy frecuentemente": 0
    }
    
    puntuacion = (normal_map.get(respuesta1, 2) + 
                  invertido_map.get(respuesta2, 2) + 
                  invertido_map.get(respuesta3, 2) + 
                  normal_map.get(respuesta4, 2))
    
    return puntuacion

def calcular_fri(puntuacion_sueno, puntuacion_estres):
    """
    Calcula el Factor de Recuperación Inteligente (FRI)
    """
    puntuacion_total = puntuacion_sueno + puntuacion_estres
    
    if puntuacion_total <= 6:
        return {"nivel": "Excelente", "factor": 1.0, "descripcion": "Recuperación óptima"}
    elif puntuacion_total <= 12:
        return {"nivel": "Bueno", "factor": 0.95, "descripcion": "Recuperación adecuada"}
    elif puntuacion_total <= 18:
        return {"nivel": "Regular", "factor": 0.90, "descripcion": "Recuperación comprometida"}
    elif puntuacion_total <= 24:
        return {"nivel": "Deficiente", "factor": 0.85, "descripcion": "Recuperación muy comprometida"}
    else:
        return {"nivel": "Crítico", "factor": 0.80, "descripcion": "Recuperación crítica"}

def determinar_objetivo_automatico(porcentaje_grasa, sexo, nivel_entrenamiento):
    """
    Determina automáticamente el objetivo según tabla de criterios
    """
    if sexo == "Masculino":
        if porcentaje_grasa > 25:
            return {"objetivo": "Definición", "deficit": 0.125, "descripcion": "Pérdida de grasa prioritaria"}
        elif 18 <= porcentaje_grasa <= 25:
            return {"objetivo": "Definición", "deficit": 0.075, "descripcion": "Pérdida de grasa moderada"}
        elif 12 <= porcentaje_grasa < 18:
            return {"objetivo": "Recomposición", "deficit": 0.025, "descripcion": "Recomposición corporal"}
        else:  # < 12%
            return {"objetivo": "Volumen", "surplus": 0.125, "descripcion": "Ganancia muscular"}
    else:  # Femenino
        if porcentaje_grasa > 32:
            return {"objetivo": "Definición", "deficit": 0.125, "descripcion": "Pérdida de grasa prioritaria"}
        elif 25 <= porcentaje_grasa <= 32:
            return {"objetivo": "Definición", "deficit": 0.075, "descripcion": "Pérdida de grasa moderada"}
        elif 20 <= porcentaje_grasa < 25:
            return {"objetivo": "Recomposición", "deficit": 0.025, "descripcion": "Recomposición corporal"}
        else:  # < 20%
            return {"objetivo": "Volumen", "surplus": 0.125, "descripcion": "Ganancia muscular"}

def calcular_macronutrientes_avanzados(calorias_totales, peso, objetivo, sexo):
    """
    Calcula macronutrientes con distribución inteligente según objetivo
    """
    # Proteína ajustada por objetivo
    if objetivo == "Definición":
        factor_proteina = 2.6
    elif objetivo == "Recomposición":
        factor_proteina = 2.2
    else:  # Volumen
        factor_proteina = 1.8
    
    proteina_g = peso * factor_proteina
    proteina_kcal = proteina_g * 4
    
    # Grasa ajustada por objetivo
    if objetivo == "Definición":
        factor_grasa = 0.8
    elif objetivo == "Recomposición":
        factor_grasa = 1.0
    else:  # Volumen
        factor_grasa = 1.2
    
    grasa_g = peso * factor_grasa
    grasa_kcal = grasa_g * 9
    
    # Carbohidratos por diferencia
    carbs_kcal = calorias_totales - proteina_kcal - grasa_kcal
    carbs_g = carbs_kcal / 4
    
    return {
        "proteina_g": proteina_g,
        "proteina_kcal": proteina_kcal,
        "grasa_g": grasa_g,
        "grasa_kcal": grasa_kcal,
        "carbs_g": carbs_g,
        "carbs_kcal": carbs_kcal
    }

def generar_reporte_completo(datos_usuario, calculos, fri, objetivo, macronutrientes):
    """
    Genera reporte completo detallado para el coach
    """
    reporte = f"""
========================================
📊 NUEVO CLIENTE - EVALUACIÓN AVANZADA
========================================

📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}
👤 Cliente: {datos_usuario.get('nombre', 'N/A')}
📧 Email: {datos_usuario.get('email', 'N/A')}

========================================
🆔 DATOS PERSONALES
========================================
Edad: {datos_usuario.get('edad', 'N/A')} años
Sexo: {datos_usuario.get('sexo', 'N/A')}

========================================
🧍‍♂️ COMPOSICIÓN CORPORAL
========================================
Peso: {datos_usuario.get('peso', 'N/A')} kg
Estatura: {datos_usuario.get('estatura', 'N/A')} cm
IMC: {calculos.get('imc', 'N/A'):.1f}
Método BF: {datos_usuario.get('metodo_bf', 'N/A')}
BF original: {datos_usuario.get('bf_original', 'N/A')}%
BF ajustado: {datos_usuario.get('bf_ajustado', 'N/A')}%
Masa magra: {calculos.get('masa_magra', 'N/A'):.1f} kg
FFMI: {calculos.get('ffmi', 'N/A'):.1f}

========================================
🏃‍♂️ ACTIVIDAD FÍSICA
========================================
Nivel: {datos_usuario.get('nivel_actividad', 'N/A')}
Ocupación: {datos_usuario.get('ocupacion', 'N/A')}
Entrenamiento: {datos_usuario.get('minutos_entrenamiento', 'N/A')} min x {datos_usuario.get('dias_entrenamiento', 'N/A')} días
Pasos diarios: {datos_usuario.get('pasos_diarios', 'N/A')}

========================================
⚡ CÁLCULOS ENERGÉTICOS
========================================
GER: {calculos.get('ger', 'N/A'):.0f} kcal
GEAF: {calculos.get('geaf', 'N/A'):.2f}
GEE: {calculos.get('gee', 'N/A'):.0f} kcal
GET: {calculos.get('get', 'N/A'):.0f} kcal

========================================
💤 EVALUACIÓN DE SUEÑO
========================================
Puntuación Pittsburgh: {calculos.get('puntuacion_sueno', 'N/A')}/16
Clasificación: {calculos.get('clasificacion_sueno', 'N/A')}

========================================
😖 EVALUACIÓN DE ESTRÉS
========================================
Puntuación PSS-4: {calculos.get('puntuacion_estres', 'N/A')}/16
Clasificación: {calculos.get('clasificacion_estres', 'N/A')}

========================================
🧠 FACTOR DE RECUPERACIÓN INTELIGENTE
========================================
Nivel FRI: {fri.get('nivel', 'N/A')}
Factor: {fri.get('factor', 'N/A')}
Descripción: {fri.get('descripcion', 'N/A')}

========================================
🎯 OBJETIVO AUTOMÁTICO
========================================
Objetivo: {objetivo.get('objetivo', 'N/A')}
Descripción: {objetivo.get('descripcion', 'N/A')}
Ajuste calórico: {objetivo.get('deficit', objetivo.get('surplus', 0)):.1%}

========================================
🍽️ MACRONUTRIENTES AVANZADOS
========================================
Calorías totales: {calculos.get('calorias_finales', 'N/A'):.0f} kcal

Proteína: {macronutrientes.get('proteina_g', 'N/A'):.0f}g ({macronutrientes.get('proteina_kcal', 'N/A'):.0f} kcal)
Grasas: {macronutrientes.get('grasa_g', 'N/A'):.0f}g ({macronutrientes.get('grasa_kcal', 'N/A'):.0f} kcal)
Carbohidratos: {macronutrientes.get('carbs_g', 'N/A'):.0f}g ({macronutrientes.get('carbs_kcal', 'N/A'):.0f} kcal)

========================================
📝 NOTAS PARA EL COACH
========================================
Prioridad: {calculos.get('prioridad', 'Estándar')}
Seguimiento: {calculos.get('seguimiento', 'Rutinario')}
Contactar en: 24-48 horas

========================================
"""
    
    return reporte

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
    
    if st.button("📊 Cuestionario FBEO", use_container_width=True):
        st.session_state.page = "cuestionario_fbeo"
    
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
        <h2>🧮 Cuestionario Científico Avanzado - Balance Energético Óptimo</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="questionnaire-container">
        <h3>🎯 Objetivo</h3>
        <p>Evaluación científicamente fundamentada que integra <strong>composición corporal, actividad física, 
        calidad del sueño, estrés percibido y factor de recuperación inteligente</strong> para determinar 
        automáticamente tu objetivo nutricional y plan de macronutrientes personalizado.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("balance_energetico_avanzado"):
        # =================  DATOS PERSONALES INICIALES =================
        st.subheader("🆔 Datos Personales Iniciales")
        col1, col2 = st.columns(2)
        
        with col1:
            nombre_completo = st.text_input("Nombre completo*", placeholder="Tu nombre completo")
            email_destinatario = st.text_input("Correo electrónico*", placeholder="tu@email.com")
            edad = st.number_input("Edad*", min_value=16, max_value=80, value=25)
            
        with col2:
            sexo = st.selectbox("Sexo*", ["Masculino", "Femenino"])
            st.markdown("")
            st.markdown("")
            condiciones_aceptadas = st.checkbox("Acepto los términos y condiciones y autorizo el procesamiento de mis datos*")
        
        # =================  SECCIÓN 1: COMPOSICIÓN CORPORAL =================
        st.subheader("🧍‍♂️ Sección 1: Composición Corporal")
        col1, col2 = st.columns(2)
        
        with col1:
            estatura = st.number_input("Estatura (cm)*", min_value=140, max_value=220, value=170)
            peso = st.number_input("Peso (kg)*", min_value=40.0, max_value=200.0, value=70.0, step=0.1)
            metodo_bf = st.selectbox("Método de medición de grasa corporal*", [
                "DEXA", "BIA", "Fórmula Naval", "Antropometría"
            ])
            
        with col2:
            grasa_corporal_original = st.number_input("Porcentaje de grasa corporal (%)*", 
                                                     min_value=5.0, max_value=50.0, value=20.0, step=0.1)
            
            if metodo_bf == "Antropometría":
                numero_pliegues = st.selectbox("Número de pliegues", [3, 4, 7])
            else:
                numero_pliegues = None
            
            # Aplicar corrección automática
            grasa_corporal_ajustada = ajustar_grasa_corporal(
                grasa_corporal_original, metodo_bf, sexo, numero_pliegues
            )
            
            if grasa_corporal_ajustada != grasa_corporal_original:
                st.info(f"💡 **Ajuste automático aplicado:** {grasa_corporal_original}% → {grasa_corporal_ajustada:.1f}%")
                st.caption(f"Corrección por método {metodo_bf}")
            
            # Cálculos automáticos
            masa_magra = peso * (1 - grasa_corporal_ajustada/100)
            ffmi = calcular_ffmi(peso, estatura/100, grasa_corporal_ajustada)
            
            st.metric("Masa Magra", f"{masa_magra:.1f} kg")
            st.metric("FFMI", f"{ffmi:.1f}")
        
        # =================  SECCIÓN 2: ACTIVIDAD FÍSICA Y GET =================
        st.subheader("🏃‍♂️ Sección 2: Nivel de Actividad y GET")
        col1, col2 = st.columns(2)
        
        with col1:
            nivel_actividad = st.selectbox("Nivel de actividad diaria*", [
                "Sedentario", "Ligeramente activo", "Moderadamente activo", 
                "Muy activo", "Extremadamente activo"
            ])
            
            ocupacion = st.selectbox("Ocupación/Trabajo*", [
                "Oficina/Escritorio", "Trabajo de pie", "Trabajo activo", 
                "Trabajo físico pesado", "Estudiante", "Jubilado/Pensionado"
            ])
            
            minutos_entrenamiento = st.number_input("Minutos de entrenamiento por sesión*", 
                                                   min_value=0, max_value=180, value=60)
            
        with col2:
            dias_entrenamiento = st.number_input("Días de entrenamiento por semana*", 
                                               min_value=0, max_value=7, value=4)
            
            pasos_diarios = st.selectbox("Pasos diarios promedio*", [
                "< 5,000", "5,000-7,500", "7,500-10,000", "10,000-12,500", "> 12,500"
            ])
            
            # Cálculos automáticos
            geaf = calcular_factor_actividad(nivel_actividad, sexo)
            
            # GER usando Katch-McArdle
            tmb = 370 + (21.6 * masa_magra)
            ger = tmb * 1.15  # ETA fijo personalizado por coach
            
            # GEE por entrenamiento
            gee_por_sesion = masa_magra * (minutos_entrenamiento / 60) * 7
            gee_semanal = gee_por_sesion * dias_entrenamiento
            
            # GET final
            get_total = (ger * geaf) + (gee_semanal / 7)
            
            st.metric("GER", f"{ger:.0f} kcal")
            st.metric("GET", f"{get_total:.0f} kcal")
        
        # =================  SECCIÓN 3: CALIDAD DEL SUEÑO =================
        st.subheader("💤 Sección 3: Calidad del Sueño (Pittsburgh abreviado)")
        col1, col2 = st.columns(2)
        
        with col1:
            horas_sueno = st.selectbox("¿Cuántas horas duermes por noche?*", [
                "Más de 9h", "8-9h", "7-8h", "6-7h", "5-6h", "Menos de 5h"
            ])
            
            tiempo_dormir = st.selectbox("¿Cuánto tardas en quedarte dormido?*", [
                "Menos de 15 min", "15-30 min", "30-45 min", "45-60 min", "Más de 60 min"
            ])
            
        with col2:
            despertares_nocturnos = st.selectbox("¿Cuántas veces te despiertas por noche?*", [
                "Nunca", "1 vez", "2 veces", "3 veces", "Más de 3 veces"
            ])
            
            calidad_percibida = st.selectbox("¿Cómo percibes la calidad de tu sueño?*", [
                "Excelente", "Buena", "Regular", "Mala", "Muy mala"
            ])
        
        # Calcular puntuación Pittsburgh
        puntuacion_sueno = evaluar_pittsburgh(horas_sueno, tiempo_dormir, despertares_nocturnos, calidad_percibida)
        
        if puntuacion_sueno >= 10:
            st.warning(f"⚠️ **Puntuación sueño: {puntuacion_sueno}/16** - Calidad deficiente detectada")
        else:
            st.success(f"✅ **Puntuación sueño: {puntuacion_sueno}/16** - Calidad adecuada")
        
        # =================  SECCIÓN 4: ESTRÉS PERCIBIDO =================
        st.subheader("😖 Sección 4: Estrés Percibido (PSS-4)")
        st.markdown("**En el último mes, ¿con qué frecuencia...**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            pss1 = st.selectbox("¿Has sentido que no podías controlar las cosas importantes de tu vida?*", [
                "Nunca", "Casi nunca", "A veces", "Frecuentemente", "Muy frecuentemente"
            ])
            
            pss2 = st.selectbox("¿Te has sentido confiado/a sobre tu capacidad para manejar tus problemas personales?*", [
                "Nunca", "Casi nunca", "A veces", "Frecuentemente", "Muy frecuentemente"
            ])
            
        with col2:
            pss3 = st.selectbox("¿Has sentido que las cosas van como tú quieres?*", [
                "Nunca", "Casi nunca", "A veces", "Frecuentemente", "Muy frecuentemente"
            ])
            
            pss4 = st.selectbox("¿Has sentido que las dificultades se acumulan tanto que no puedes superarlas?*", [
                "Nunca", "Casi nunca", "A veces", "Frecuentemente", "Muy frecuentemente"
            ])
        
        # Calcular puntuación PSS-4
        puntuacion_estres = evaluar_pss4(pss1, pss2, pss3, pss4)
        
        if puntuacion_estres >= 10:
            st.warning(f"⚠️ **Puntuación estrés: {puntuacion_estres}/16** - Nivel alto detectado")
        else:
            st.success(f"✅ **Puntuación estrés: {puntuacion_estres}/16** - Nivel manejable")
        
        # =================  EVALUACIÓN FRI =================
        fri = calcular_fri(puntuacion_sueno, puntuacion_estres)
        
        st.subheader("🧠 Factor de Recuperación Inteligente (FRI)")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Nivel FRI", fri["nivel"])
        with col2:
            st.metric("Factor", f"{fri['factor']:.2f}")
        with col3:
            st.metric("Descripción", fri["descripcion"])
        
        # Penalización energética si es necesario
        if puntuacion_sueno >= 10:
            get_total *= 0.95  # Penalización por sueño deficiente
            st.info("💡 **Ajuste aplicado:** Penalización energética por sueño deficiente")
        
        submitted = st.form_submit_button("🚀 Generar Análisis Completo", type="primary")
        
        if submitted:
            # Validaciones
            if not nombre_completo:
                st.error("❌ **Error:** El nombre completo es obligatorio")
                st.stop()
            
            if not email_destinatario:
                st.error("❌ **Error:** El correo electrónico es obligatorio")
                st.stop()
            
            if not condiciones_aceptadas:
                st.error("❌ **Error:** Debes aceptar los términos y condiciones")
                st.stop()
            
            # =================  DETERMINACIÓN AUTOMÁTICA DEL OBJETIVO =================
            objetivo = determinar_objetivo_automatico(grasa_corporal_ajustada, sexo, dias_entrenamiento)
            
            # Aplicar FRI y calcular calorías finales
            if "deficit" in objetivo:
                calorias_finales = get_total * (1 - objetivo["deficit"]) * fri["factor"]
            elif "surplus" in objetivo:
                calorias_finales = get_total * (1 + objetivo["surplus"]) * fri["factor"]
            else:
                calorias_finales = get_total * fri["factor"]
            
            # =================  MACRONUTRIENTES AVANZADOS =================
            macronutrientes = calcular_macronutrientes_avanzados(
                calorias_finales, peso, objetivo["objetivo"], sexo
            )
            
            # =================  MOSTRAR RESULTADOS AL USUARIO =================
            st.success("✅ **¡Análisis completado exitosamente!**")
            
            st.info("""
            📧 **Tu evaluación completa ha sido enviada a tu entrenador MUPAI.**
            
            **Próximos pasos:**
            - Revisión detallada por parte del equipo técnico
            - Plan nutricional personalizado
            - Seguimiento y ajustes continuos
            
            ⏰ **Tiempo de respuesta: 24-48 horas**
            """)
            
            # Resumen para el usuario
            st.markdown("### 📊 Resumen de tu Evaluación")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Composición Corporal", f"{grasa_corporal_ajustada:.1f}% GC")
            with col2:
                st.metric("FFMI", f"{ffmi:.1f}")
            with col3:
                st.metric("Nivel FRI", fri["nivel"])
            with col4:
                st.metric("Objetivo", objetivo["objetivo"])
            
            # =================  GENERAR REPORTE COMPLETO =================
            datos_usuario = {
                "nombre": nombre_completo,
                "email": email_destinatario,
                "edad": edad,
                "sexo": sexo,
                "peso": peso,
                "estatura": estatura,
                "metodo_bf": metodo_bf,
                "bf_original": grasa_corporal_original,
                "bf_ajustado": grasa_corporal_ajustada,
                "nivel_actividad": nivel_actividad,
                "ocupacion": ocupacion,
                "minutos_entrenamiento": minutos_entrenamiento,
                "dias_entrenamiento": dias_entrenamiento,
                "pasos_diarios": pasos_diarios
            }
            
            calculos = {
                "imc": peso / ((estatura/100) ** 2),
                "masa_magra": masa_magra,
                "ffmi": ffmi,
                "tmb": tmb,
                "ger": ger,
                "geaf": geaf,
                "gee": gee_semanal,
                "get": get_total,
                "calorias_finales": calorias_finales,
                "puntuacion_sueno": puntuacion_sueno,
                "puntuacion_estres": puntuacion_estres,
                "clasificacion_sueno": "Deficiente" if puntuacion_sueno >= 10 else "Adecuada",
                "clasificacion_estres": "Alto" if puntuacion_estres >= 10 else "Manejable",
                "prioridad": "Prioritario" if (puntuacion_sueno >= 10 or puntuacion_estres >= 10) else "Estándar",
                "seguimiento": "Inmediato" if fri["nivel"] in ["Deficiente", "Crítico"] else "Rutinario"
            }
            
            # Generar reporte completo
            reporte_completo = generar_reporte_completo(datos_usuario, calculos, fri, objetivo, macronutrientes)
            
            # Enviar al coach
            try:
                trainer_email = st.secrets.get("trainer_email", "mupaitraining@outlook.com")
                enviar_email_resultados(trainer_email, 
                  f"EVALUACIÓN AVANZADA - {nombre_completo}", 
                  reporte_completo)
                st.success("✅ Reporte enviado correctamente al equipo técnico")
            except Exception as e:
                st.error(f"❌ Error al enviar reporte: {str(e)}")
            
            # Mostrar próximos pasos
            st.markdown("""
            ---
            ### 🎯 Próximos Pasos
            
            1. **Revisión técnica** de tu evaluación completa
            2. **Elaboración** de tu plan nutricional personalizado
            3. **Contacto directo** para coordinar inicio del programa
            4. **Seguimiento continuo** y ajustes según evolución
            
            **¿Dudas urgentes?** Contacta a MUPAI Training.
            """)

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

# ==================== CUESTIONARIO FBEO ====================
elif st.session_state.page == "cuestionario_fbeo":
    try:
        from cuestionario_fbeo import mostrar_cuestionario_fbeo
        mostrar_cuestionario_fbeo()
    except ImportError:
        st.error("⚠️ El módulo cuestionario_fbeo no está disponible. Por favor, verifica que el archivo existe.")
        st.info("Esta funcionalidad estará disponible próximamente.")

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
