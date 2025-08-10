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
import os
# Temporarily comment out if the module doesn't exist yet
# from cuestionario_fbeo import mostrar_cuestionario_fbeo

def load_banking_image_base64():
    """
    Loads the banking data image and returns it as base64 encoded string.
    Returns a fallback message if the image file is not found.
    """
    banking_image_path = 'Copia de Copia de Copia de Copia de Copia de Copia de Tarjeta GYM_20250715_074925_0000.png'
    
    try:
        with open(banking_image_path, 'rb') as f:
            image_data = f.read()
            encoded_image = base64.b64encode(image_data).decode()
            return f'<img src="data:image/png;base64,{encoded_image}" alt="Cuenta bancaria Muscle Up Gym" style="max-width:320px;border-radius:12px;">'
    except FileNotFoundError:
        return '''
        <div style="padding: 15px; background-color: #ffe6e6; border: 2px solid #ff9999; border-radius: 8px; text-align: center; max-width: 320px; margin: 10px 0;">
            <h4 style="color: #cc0000; margin: 0 0 10px 0; font-size: 16px;">⚠️ Imagen de datos bancarios no disponible</h4>
            <p style="color: #666; margin: 0 0 10px 0; font-size: 14px;">Por favor contacta directamente para obtener los datos bancarios:</p>
            <p style="color: #000; font-weight: bold; margin: 0; font-size: 14px;">
                📧 administracion@muscleupgym.fitness<br>
                📱 WhatsApp: 8662580594
            </p>
        </div>
        '''
    except Exception as e:
        return f'''
        <div style="padding: 15px; background-color: #fff3cd; border: 2px solid #ffc107; border-radius: 8px; text-align: center; max-width: 320px; margin: 10px 0;">
            <h4 style="color: #856404; margin: 0 0 10px 0; font-size: 16px;">⚠️ Error al cargar datos bancarios</h4>
            <p style="color: #666; margin: 0 0 10px 0; font-size: 14px;">Contacta directamente para obtener la información de pago:</p>
            <p style="color: #000; font-weight: bold; margin: 0; font-size: 14px;">
                📧 administracion@muscleupgym.fitness<br>
                📱 WhatsApp: 8662580594
            </p>
        </div>
        '''

def load_logo_image_base64():
    """
    Loads the logo image and returns it as base64 encoded string.
    Returns a fallback message if the image file is not found.
    """
    logo_image_path = 'LOGO.png'
    
    try:
        with open(logo_image_path, 'rb') as f:
            image_data = f.read()
            encoded_image = base64.b64encode(image_data).decode()
            return f'data:image/png;base64,{encoded_image}'
    except FileNotFoundError:
        return None
    except Exception as e:
        return None

# Configuración de la página
st.set_page_config(
    page_title="MUPAI - Entrenamiento Digital Basado en Ciencia",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado con tema negro y amarillo mostaza
st.markdown("""
<style>  
    /* Tema principal: Negro, amarillo mostaza, blanco */
    .stApp > div:first-child {
        background-color: #000000;
    }
    
    .main-header {  
        background: #000000;  
        padding: 2rem;  
        border-radius: 15px;  
        text-align: center;  
        margin-bottom: 2rem;  
        box-shadow: 0 4px 15px rgba(255,204,0,0.3);  
        border: 2px solid #FFCC00;
    }  
      
    .main-header h1 {  
        color: #FFCC00;  
        font-size: 3rem;  
        font-weight: bold;  
        margin: 0;  
        text-shadow: 2px 2px 4px rgba(255,204,0,0.5);  
    }  
      
    .main-header p {  
        color: #FFFFFF;  
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
        box-shadow: 0 3px 10px rgba(255,204,0,0.2);  
        border: 1px solid #FFCC00;
    }  
      
    .questionnaire-container {  
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);  
        padding: 1.5rem;  
        border-radius: 12px;  
        border-left: 5px solid #FFCC00;  
        margin: 1rem 0;  
        box-shadow: 0 2px 8px rgba(255,204,0,0.1);  
        color: #FFFFFF;
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
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);  
        padding: 1.5rem;  
        border-radius: 12px;  
        box-shadow: 0 3px 12px rgba(255,204,0,0.1);  
        border-left: 6px solid #FFCC00;  
        margin: 1rem 0;  
        transition: transform 0.2s ease;  
        color: #FFFFFF;
    }  
      
    .metric-card:hover {  
        transform: translateY(-2px);  
        box-shadow: 0 5px 20px rgba(255,204,0,0.2);  
    }  
      
    .corporate-section {  
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);  
        padding: 2rem;  
        border-radius: 15px;  
        margin: 1.5rem 0;  
        border: 2px solid #FFCC00;  
        box-shadow: 0 4px 15px rgba(255,204,0,0.1);  
        color: #FFFFFF;
    }  
      
    .corporate-section h3 {  
        color: #FFCC00;  
        border-bottom: 3px solid #FFCC00;  
        padding-bottom: 0.5rem;  
        margin-bottom: 1rem;  
    }  
      
    .logo-container {  
        text-align: center;  
        padding: 2rem;  
        background: #000000;  
        border-radius: 15px;  
        margin-bottom: 2rem;  
        border: 2px solid #FFCC00;
        box-shadow: 0 4px 15px rgba(255,204,0,0.2);
    }  
    
    .logo-img {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        box-shadow: 0 8px 25px rgba(255,204,0,0.4);
        border: 3px solid #FFCC00;
        transition: transform 0.3s ease;
        object-fit: cover;
    }
    
    .logo-img:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 35px rgba(255,204,0,0.6);
    }
      
    .professional-profile {  
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);  
        padding: 2rem;  
        border-radius: 15px;  
        border-left: 6px solid #FFCC00;  
        margin: 1rem 0;  
        color: #FFFFFF;
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
    
    /* Estilos para texto en elementos principales */
    .stMarkdown {
        color: #FFFFFF;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1a1a1a;
    }
    
    /* Botones del sidebar */
    .stButton > button {
        background: linear-gradient(135deg, #FFCC00 0%, #FFD700 100%);
        color: #000000;
        border: none;
        border-radius: 8px;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #FFD700 0%, #FFCC00 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(255,204,0,0.3);
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

PROTEÍNA (g/kg):
- Déficit: 2.2 - 2.6 g/kg
- Recomposición: 2.0 - 2.4 g/kg
- Superávit: 1.8 - 2.0 g/kg

GRASA (g/kg):
- Déficit: 0.8 - 1.0 g/kg
- Recomposición: 0.9 - 1.2 g/kg
- Superávit: 1.0 - 1.2 g/kg

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



def main():
    """Main application interface with page navigation."""
    
    # =============================================================================
    # MAIN NAVIGATION WITH TABS
    # =============================================================================
    
    # Create main tabs for navigation
    tab1, tab2, tab3 = st.tabs(["🏠 Inicio", "📊 Cuestionario", "ℹ️ Sobre MUPAI"])
    
    with tab1:
        show_home_page()
    
    with tab2:
        show_main_questionnaire()
    
    with tab3:
        show_about_page()


def show_home_page():
    """Display the action-oriented home page."""
    
    # =============================================================================
    # HERO SECTION WITH LOGO AND CTA
    # =============================================================================
    
    # Logo Section - Large and Prominent
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        logo_base64 = load_logo_image_base64()
        if logo_base64:
            st.markdown(f"""
            <div style="text-align: center;">
                <img src="{logo_base64}" style="width: 500px; max-width: 100%; height: auto;">
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #FFCC00 0%, #FFD700 100%); border-radius: 15px;">
                <h1 style="color: #000; font-size: 3rem; margin: 0;">🏢 MUPAI</h1>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Hero Header with CTA
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFCC00 0%, #FFD700 50%, #FFA500 100%);
                padding: 3rem 2rem; border-radius: 20px; text-align: center; margin-bottom: 3rem;
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);">
        <h1 style="color: #000; font-size: 3rem; font-weight: bold; margin-bottom: 1rem;
                   text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            ⚡ Transforma Tu Composición Corporal
        </h1>
        <h2 style="color: #333; font-size: 1.5rem; margin-bottom: 2rem; font-weight: 400;">
            Sistema Científico Avanzado de Balance Energético y Macronutrientes
        </h2>
        <p style="color: #444; font-size: 1.2rem; margin-bottom: 2rem; max-width: 800px; margin-left: auto; margin-right: auto;">
            Obtén un análisis personalizado basado en ciencia para alcanzar tus objetivos de composición corporal 
            con precisión y resultados garantizados.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # =============================================================================
    # CALL TO ACTION SECTION
    # =============================================================================
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 ¡COMENZAR EVALUACIÓN AHORA!", type="primary", use_container_width=True):
            st.session_state.switch_to_questionnaire = True
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Secondary CTA
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💰 Ver Planes y Precios", use_container_width=True):
            st.session_state.show_plans = True
            st.rerun()
    
    # =============================================================================
    # BENEFITS SECTION
    # =============================================================================
    
    st.markdown("""
    <div style="margin: 3rem 0;">
        <h2 style="text-align: center; color: #333; font-size: 2.5rem; margin-bottom: 2rem;">
            🎯 ¿Por Qué Elegir MUPAI?
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Benefits cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #74b9ff 0%, #a29bfe 100%);
                    padding: 2rem; border-radius: 15px; color: white; height: 300px;
                    box-shadow: 0 6px 20px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🔬</div>
            <h3 style="margin-bottom: 1rem;">Ciencia Avanzada</h3>
            <p>Evaluación basada en las metodologías científicas más actualizadas:
            Mifflin-St Jeor, Katch-McArdle, Pittsburgh Sleep Quality, PSS-4 Stress Scale.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
                    padding: 2rem; border-radius: 15px; color: white; height: 300px;
                    box-shadow: 0 6px 20px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🎯</div>
            <h3 style="margin-bottom: 1rem;">100% Personalizado</h3>
            <p>Análisis único basado en tu composición corporal, actividad física, 
            calidad de sueño, nivel de estrés y objetivos específicos.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%);
                    padding: 2rem; border-radius: 15px; color: white; height: 300px;
                    box-shadow: 0 6px 20px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
            <h3 style="margin-bottom: 1rem;">Resultados Precisos</h3>
            <p>Asignación inteligente de macronutrientes con Factor de Recuperación 
            Inteligente (FRI) y determinación automática de objetivos.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # =============================================================================
    # HOW IT WORKS SECTION
    # =============================================================================
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                padding: 3rem 2rem; border-radius: 20px; margin: 3rem 0;
                border-left: 5px solid #FFCC00; box-shadow: 0 6px 20px rgba(0,0,0,0.1);">
        <h2 style="text-align: center; color: #333; font-size: 2.5rem; margin-bottom: 3rem;">
            🔍 ¿Cómo Funciona?
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Process steps
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 4px solid #FFCC00;">
            <h3 style="color: #FFCC00; margin-bottom: 1rem;">
                <span style="background: #FFCC00; color: #000; padding: 0.5rem; border-radius: 50%; margin-right: 1rem;">1</span>
                Evaluación Integral
            </h3>
            <p style="color: #555; font-size: 1.1rem;">
                Completa un cuestionario científico avanzado que evalúa tu composición corporal, 
                actividad física, calidad de sueño y nivel de estrés.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 4px solid #74b9ff;">
            <h3 style="color: #74b9ff; margin-bottom: 1rem;">
                <span style="background: #74b9ff; color: #fff; padding: 0.5rem; border-radius: 50%; margin-right: 1rem;">3</span>
                Plan Personalizado
            </h3>
            <p style="color: #555; font-size: 1.1rem;">
                Recibe un plan de macronutrientes completamente personalizado con 
                justificación científica y recomendaciones específicas.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 4px solid #00b894;">
            <h3 style="color: #00b894; margin-bottom: 1rem;">
                <span style="background: #00b894; color: #fff; padding: 0.5rem; border-radius: 50%; margin-right: 1rem;">2</span>
                Análisis Científico
            </h3>
            <p style="color: #555; font-size: 1.1rem;">
                Nuestro sistema aplica algoritmos avanzados para calcular tu gasto energético 
                total y determinar automáticamente tu objetivo corporal óptimo.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 4px solid #fd79a8;">
            <h3 style="color: #fd79a8; margin-bottom: 1rem;">
                <span style="background: #fd79a8; color: #fff; padding: 0.5rem; border-radius: 50%; margin-right: 1rem;">4</span>
                Seguimiento Profesional
            </h3>
            <p style="color: #555; font-size: 1.1rem;">
                Nuestro coach MUPAI revisa tus resultados y te contacta en 24-48 horas 
                para el seguimiento y ajustes necesarios.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # =============================================================================
    # PROFESSIONAL SHOWCASE
    # =============================================================================
    
    st.markdown("""
    <div style="margin: 3rem 0;">
        <h2 style="text-align: center; color: #333; font-size: 2.5rem; margin-bottom: 2rem;">
            👨‍⚕️ Tu Coach Profesional
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        try:
            st.image("Copia de Anfitrión_20250809_125513_0000.png", width=400, caption="Coach Profesional MUPAI")
        except:
            st.markdown("""
            <div style="background: #f8f9fa; padding: 2rem; border-radius: 15px; text-align: center;">
                <h3>👨‍⚕️ Coach Profesional MUPAI</h3>
                <p>Imagen no disponible</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        try:
            st.image("20250728_220454.jpg", width=400, caption="Entrenamiento Profesional")
        except:
            st.markdown("""
            <div style="background: #f8f9fa; padding: 2rem; border-radius: 15px; text-align: center;">
                <h3>💪 Entrenamiento Profesional</h3>
                <p>Imagen no disponible</p>
            </div>
            """, unsafe_allow_html=True)
    
    # =============================================================================
    # FINAL CTA
    # =============================================================================
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
                padding: 3rem 2rem; border-radius: 20px; text-align: center; margin: 3rem 0;
                color: white; box-shadow: 0 8px 25px rgba(0,0,0,0.2);">
        <h2 style="color: #FFCC00; font-size: 2.5rem; margin-bottom: 1rem;">
            🏆 ¡Comienza Tu Transformación Hoy!
        </h2>
        <p style="font-size: 1.3rem; margin-bottom: 2rem; opacity: 0.9;">
            Únete a cientos de personas que ya han transformado su composición corporal con MUPAI
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 ¡EMPEZAR AHORA - ES GRATIS!", type="primary", use_container_width=True):
            st.session_state.switch_to_questionnaire = True
            st.rerun()


def show_about_page():
    """Display the About MUPAI page with institutional information."""
    
    # Logo
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        logo_base64 = load_logo_image_base64()
        if logo_base64:
            st.markdown(f"""
            <div style="text-align: center;">
                <img src="{logo_base64}" style="width: 300px; max-width: 100%; height: auto;">
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #FFCC00 0%, #FFD700 100%); border-radius: 15px;">
                <h1 style="color: #000; font-size: 2rem; margin: 0;">🏢 MUPAI</h1>
            </div>
            """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFCC00 0%, #FFD700 50%, #FFA500 100%);
                padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 2rem;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h1 style="color: #000; font-size: 2.5rem; font-weight: bold; margin: 0;
                   text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            ℹ️ Sobre MUPAI
        </h1>
        <p style="color: #333; font-size: 1.2rem; margin-top: 1rem;">
            Conoce nuestra misión, visión y compromiso contigo
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # =============================================================================
    # MISSION
    # =============================================================================
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #74b9ff 0%, #a29bfe 100%);
                padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h2 style="margin-bottom: 1rem;">🎯 Nuestra Misión</h2>
        <p style="font-size: 1.1rem; line-height: 1.6;">
            En MUPAI, nos dedicamos a democratizar el acceso a la nutrición deportiva científica 
            y personalizada. Nuestra misión es proporcionar herramientas avanzadas de evaluación 
            nutricional basadas en evidencia científica para que cada persona pueda alcanzar sus 
            objetivos de composición corporal de manera segura, efectiva y sostenible.
        </p>
        <p style="font-size: 1.1rem; line-height: 1.6; margin-top: 1rem;">
            Creemos que la nutrición personalizada no debe ser un privilegio, sino un derecho 
            accesible para todos aquellos que buscan mejorar su salud y rendimiento físico.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # =============================================================================
    # VISION
    # =============================================================================
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
                padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h2 style="margin-bottom: 1rem;">🔮 Nuestra Visión</h2>
        <p style="font-size: 1.1rem; line-height: 1.6;">
            Ser la plataforma líder en Latinoamérica para la evaluación científica avanzada del 
            balance energético y asignación inteligente de macronutrientes, reconocida por la 
            precisión de nuestros algoritmos y la efectividad de nuestros resultados.
        </p>
        <p style="font-size: 1.1rem; line-height: 1.6; margin-top: 1rem;">
            Aspiramos a transformar la forma en que las personas abordan su nutrición deportiva, 
            reemplazando las aproximaciones genéricas con soluciones verdaderamente personalizadas 
            que consideren la individualidad bioquímica, fisiológica y de estilo de vida de cada usuario.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # =============================================================================
    # INSTITUTIONAL POLICY
    # =============================================================================
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%);
                padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h2 style="margin-bottom: 1rem;">📋 Política Institucional</h2>
        <p style="font-size: 1.1rem; line-height: 1.6;">
            MUPAI se compromete a mantener los más altos estándares de excelencia científica y 
            ética profesional en todos nuestros servicios. Nuestras evaluaciones se basan 
            exclusivamente en metodologías validadas por la literatura científica peer-reviewed.
        </p>
        <h3 style="margin-top: 1.5rem; margin-bottom: 1rem;">Principios Fundamentales:</h3>
        <ul style="font-size: 1.1rem; line-height: 1.6;">
            <li><strong>Evidencia Científica:</strong> Todas nuestras metodologías están respaldadas por investigación científica actual y validada.</li>
            <li><strong>Transparencia:</strong> Proporcionamos justificación científica completa para cada recomendación.</li>
            <li><strong>Individualización:</strong> Cada evaluación es única y considera múltiples factores biológicos y de estilo de vida.</li>
            <li><strong>Actualización Continua:</strong> Nuestros algoritmos se actualizan regularmente con los últimos avances científicos.</li>
            <li><strong>Confidencialidad:</strong> Toda la información personal se maneja con estricta confidencialidad y seguridad.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # =============================================================================
    # SERVICE POLICY
    # =============================================================================
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                padding: 2rem; border-radius: 15px; color: #333; margin-bottom: 2rem;
                border-left: 5px solid #FFCC00; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h2 style="color: #333; margin-bottom: 1rem;">⚖️ Política del Servicio</h2>
        
        <h3 style="color: #FFCC00; margin-top: 1.5rem; margin-bottom: 1rem;">Alcance del Servicio</h3>
        <p style="font-size: 1.1rem; line-height: 1.6;">
            MUPAI proporciona evaluaciones científicas para optimización del balance energético y 
            asignación de macronutrientes con fines de mejora de la composición corporal y rendimiento 
            deportivo. Nuestros servicios son complementarios y no sustituyen el consejo médico profesional.
        </p>
        
        <h3 style="color: #FFCC00; margin-top: 1.5rem; margin-bottom: 1rem;">Limitaciones y Advertencias</h3>
        <ul style="font-size: 1.1rem; line-height: 1.6;">
            <li>Nuestras evaluaciones son para personas sanas entre 16-80 años sin condiciones médicas especiales.</li>
            <li>Los resultados requieren supervisión profesional para implementación segura.</li>
            <li>No proporcionamos diagnósticos médicos ni tratamientos para condiciones de salud.</li>
            <li>Se requiere consulta médica previa si existe cualquier condición de salud diagnosticada.</li>
        </ul>
        
        <h3 style="color: #FFCC00; margin-top: 1.5rem; margin-bottom: 1rem;">Responsabilidades del Usuario</h3>
        <ul style="font-size: 1.1rem; line-height: 1.6;">
            <li>Proporcionar información precisa y completa en todas las evaluaciones.</li>
            <li>Implementar las recomendaciones bajo supervisión profesional apropiada.</li>
            <li>Notificar cualquier cambio significativo en el estado de salud.</li>
            <li>Seguir las pautas de seguridad y las advertencias proporcionadas.</li>
        </ul>
        
        <h3 style="color: #FFCC00; margin-top: 1.5rem; margin-bottom: 1rem;">Garantías del Servicio</h3>
        <ul style="font-size: 1.1rem; line-height: 1.6;">
            <li>Análisis basado en las metodologías científicas más actualizadas.</li>
            <li>Contacto profesional en 24-48 horas posterior a la evaluación.</li>
            <li>Soporte técnico durante todo el proceso de evaluación.</li>
            <li>Revisión y ajustes según evolución del usuario.</li>
        </ul>
        
        <h3 style="color: #FFCC00; margin-top: 1.5rem; margin-bottom: 1rem;">Contacto Profesional</h3>
        <p style="font-size: 1.1rem; line-height: 1.6;">
            <strong>Email:</strong> mupaitraining@outlook.com<br>
            <strong>Tiempo de respuesta:</strong> 24-48 horas<br>
            <strong>Disponibilidad:</strong> Lunes a Viernes, 9:00 AM - 6:00 PM
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # =============================================================================
    # PLANS SECTION
    # =============================================================================
    
    show_plans_page()


def show_main_questionnaire():
    """Display the main questionnaire interface."""
    
    # Check if user came from home page CTA
    if hasattr(st.session_state, 'switch_to_questionnaire') and st.session_state.switch_to_questionnaire:
        st.session_state.switch_to_questionnaire = False
        st.success("🎉 ¡Perfecto! Comencemos con tu evaluación científica personalizada.")
        st.markdown("---")
    
    # Check if user wants to see plans
    if hasattr(st.session_state, 'show_plans') and st.session_state.show_plans:
        st.session_state.show_plans = False
        show_plans_page()
        return
    
    # Logo
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        logo_base64 = load_logo_image_base64()
        if logo_base64:
            st.markdown(f"""
            <div style="text-align: center;">
                <img src="{logo_base64}" style="width: 300px; max-width: 100%; height: auto;">
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #FFCC00 0%, #FFD700 100%); border-radius: 15px;">
                <h1 style="color: #000; font-size: 2rem; margin: 0;">🏢 MUPAI</h1>
            </div>
            """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFCC00 0%, #FFD700 50%, #FFA500 100%);
                padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 2rem;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h1 style="color: #000; font-size: 2.5rem; font-weight: bold; margin: 0;
                   text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            ⚡ CUESTIONARIO AVANZADO DE BALANCE ENERGÉTICO
        </h1>
        <p style="color: #333; font-size: 1.2rem; margin-top: 1rem;">
            Sistema Científico Inteligente para Asignación de Macronutrientes
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show existing questionnaire content
    show_original_content()


def show_plans_page():
    """Display the plans and pricing page."""
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFCC00 0%, #FFD700 50%, #FFA500 100%);
                padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 2rem;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h1 style="color: #000; font-size: 2.5rem; font-weight: bold; margin: 0;
                   text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            💰 PLANES Y TARIFAS
        </h1>
        <p style="color: #333; font-size: 1.2rem; margin-top: 1rem;">
            Servicios Profesionales de Nutrición y Entrenamiento Personalizado
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # =============================================================================
    # PLANS AND PRICING CONTENT
    # =============================================================================
    
    # Nutrition Plan
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFCC00 0%, #FFE066 100%); 
                padding: 2rem; border-radius: 15px; margin-bottom: 2rem; color: #000;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h2>🍽️ Plan de Nutrición Personalizada – 6 semanas</h2>
        <ul style="margin: 1rem 0; padding-left: 2rem; font-size: 1.1rem;">
            <li>Evaluación inicial (bioimpedancia + cuestionarios)</li>
            <li>6 menús adaptados (calorías, macros, micronutrientes, preferencias)</li>
            <li>Evaluación final con medición corporal</li>
            <li>Ajustes desde $150 MXN | Menús extra desde $100 MXN</li>
        </ul>
        <h2 style="text-align: center; margin-top: 2rem; background: rgba(0,0,0,0.1); 
                   padding: 1rem; border-radius: 10px;">💰 Precio: $750 MXN</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Training Plan
    st.markdown("""
    <div style="background: linear-gradient(135deg, #74b9ff 0%, #a29bfe 100%); 
                padding: 2rem; border-radius: 15px; margin-bottom: 2rem; color: white;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h2>💪 Plan de Entrenamiento Personalizado – 8 semanas</h2>
        <ul style="margin: 1rem 0; padding-left: 2rem; font-size: 1.1rem;">
            <li>Evaluación inicial con Designing Your Training</li>
            <li>Plan personalizado en volumen, frecuencia, intensidad</li>
            <li>Entrega profesional en PDF</li>
            <li>Evaluación final de progresos</li>
        </ul>
        <h2 style="text-align: center; margin-top: 2rem; background: rgba(255,255,255,0.2); 
                   padding: 1rem; border-radius: 10px;">💰 Precio: $850 MXN</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Combined Plan
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ff7675 0%, #fd79a8 100%); 
                padding: 2rem; border-radius: 15px; margin-bottom: 2rem; color: white;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h2>🔥 Plan Combinado – Entrenamiento + Nutrición</h2>
        <ul style="margin: 1rem 0; padding-left: 2rem; font-size: 1.1rem;">
            <li>Incluye ambos planes completos</li>
            <li>Evaluación inicial y final con bioimpedancia</li>
            <li>Integración total entre dieta y entrenamiento</li>
        </ul>
        <h2 style="text-align: center; margin-top: 2rem; background: rgba(255,255,255,0.3); 
                   padding: 1rem; border-radius: 10px;">💰 Precio único: $1,500 MXN</h2>
        <p style="text-align: center; font-weight: bold; background: rgba(255,255,255,0.2); 
                  padding: 1rem; border-radius: 10px; margin-top: 1rem; font-size: 1.2rem;">
            🎁 Ahorro: $100 MXN
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Purchase Process
    st.markdown("""
    <div style="background: #f8f9fa; padding: 2rem; border-radius: 15px; 
                border-left: 5px solid #FFCC00; color: #000; margin-bottom: 2rem;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h2>📝 Mecánica de Adquisición:</h2>
        <ol style="margin: 1rem 0; padding-left: 2rem; font-size: 1.1rem;">
            <li>Selecciona el plan que mejor se adapte a ti</li>
            <li>Realiza la transferencia a la tarjeta bancaria</li>
            <li>Programa tu medición corporal (en Muscle Up Gym o por tu cuenta si eres foráneo)</li>
            <li>Se autoriza el acceso a los cuestionarios para personalizar tu plan</li>
            <li>Tras contestar los cuestionarios, el plan se entrega en 3 a 5 días hábiles</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Bank Card Image
    st.markdown("### 💳 Información de Transferencia")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
        """ + load_banking_image_base64() + """
        </div>
        """, unsafe_allow_html=True)


def show_original_content():
    """Display the original questionnaire content from the current page structure."""
    
    # This displays the original content based on the existing page structure
    if st.session_state.page == "balance_energetico":
        # Show the balance energético questionnaire content
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
    
    else:
        # Default questionnaire content - show the main page navigation
        st.markdown("""
        <div class="questionnaire-container">
            <h3>🧪 Cuestionarios MUPAI Disponibles</h3>
            <p>Selecciona el cuestionario que corresponde a tu plan:</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("⚡ BODY AND ENERGY", use_container_width=True):
                st.session_state.page = "body_and_energy"
                st.rerun()
        
        with col2:
            if st.button("🍽️ FOOD PREFERENCES", use_container_width=True):
                st.session_state.page = "food_preferences"
                st.rerun()
        
        with col3:
            if st.button("💪 DESIGNING TRAINING", use_container_width=True):
                st.session_state.page = "designing_training"
                st.rerun()
        
        st.markdown("---")
        
        # Show original "inicio" content if no specific page is selected
        # Encabezado moderno con logo centrado
        logo_base64 = load_logo_image_base64()
        if logo_base64:
            st.markdown(f"""
            <div class="logo-container">
                <img src="{logo_base64}" class="logo-img" alt="Muscle Up Gym Logo">
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="logo-container">
                <div style="padding: 20px; background-color: #ffe6e6; border: 2px solid #ff9999; border-radius: 8px; text-align: center;">
                    <h4 style="color: #cc0000; margin: 0;">⚠️ Logo no disponible</h4>
                    <p style="color: #666; margin: 5px 0 0 0;">MUSCLE UP GYM</p>
                </div>
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

# Call the main function with tab navigation
main()


# Footer
st.markdown("---")
logo_base64_footer = load_logo_image_base64()
if logo_base64_footer:
    footer_logo_html = f'<img src="{logo_base64_footer}" style=\'width: 60px; height: 60px; border-radius: 50%; box-shadow: 0 4px 15px rgba(255,204,0,0.3);\'>'
else:
    footer_logo_html = '<div style="width: 60px; height: 60px; border-radius: 50%; background-color: #ffcc00; display: flex; align-items: center; justify-content: center; color: #000; font-weight: bold;">MUP</div>'

st.markdown(f"""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 10px; border: 1px solid #FFCC00;">
    <div style='margin-bottom: 1rem;'>
        {footer_logo_html}
    </div>
    <h3 style="color: #FFCC00; margin-bottom: 1rem;">💪 MUSCLE UP GYM</h3>
    <p style="color: #FFFFFF; margin-bottom: 0.5rem;">Tu gimnasio de confianza</p>
    <p style="color: #FFFFFF; margin-bottom: 1rem;">Fuerza • Resistencia • Bienestar • Comunidad</p>
    <div style="display: flex; justify-content: center; gap: 1rem; margin: 1rem 0; flex-wrap: wrap;">
        <a href="https://www.facebook.com/share/16WtR5TLw5/" target="_blank" style="color: #4267B2; text-decoration: none;">📘 Facebook</a>
        <a href="https://www.instagram.com/mup_lindavista" target="_blank" style="color: #E4405F; text-decoration: none;">📷 Instagram</a>
        <a href="https://wa.me/528662580594" target="_blank" style="color: #25D366; text-decoration: none;">📱 WhatsApp</a>
        <a href="mailto:administracion@muscleupgym.fitness" style="color: #EA4335; text-decoration: none;">📧 Email</a>
    </div>
    <p style="color: #CCCCCC; font-size: 0.9rem;">© 2025 Muscle Up Gym. Todos los derechos reservados.</p>
    <p style="color: #CCCCCC; font-size: 0.8rem;">Comprometidos con tu salud y bienestar integral</p>
</div>
""", unsafe_allow_html=True)
