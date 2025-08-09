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



# Navegación principal
st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Navegación")

if st.sidebar.button("🏠 Inicio", use_container_width=True):
    st.session_state.page = "inicio"

if st.sidebar.button("💸 Planes y Costos", use_container_width=True):
    st.session_state.page = "planes_costos"

st.sidebar.markdown("### 📋 Cuestionarios Especializados")

if st.sidebar.button("⚡ Balance Energético Óptimo", use_container_width=True):
    st.session_state.page = "balance_energetico"

if st.sidebar.button("🍽️ Patrones y Preferencias Alimenticias", use_container_width=True):
    st.session_state.page = "preferencias_alimentarias"

if st.sidebar.button("🧁 Antojos Alimentarios", use_container_width=True):
    st.session_state.page = "antojos_alimentarios"

st.sidebar.markdown("---")

if st.sidebar.button("👨‍🎓 Acerca del Profesional", use_container_width=True):
    st.session_state.page = "about"

if st.sidebar.button("📞 Contacto", use_container_width=True):
    st.session_state.page = "contacto"

# ==================== PÁGINA DE INICIO ====================
if st.session_state.page == "inicio":
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
            
            # Mostrar información de proteínas y grasas
            st.markdown("### 🍽️ Guía de Macronutrientes")
            st.markdown("""
            **PROTEÍNA (g/kg):**
            - Déficit: 2.2 - 2.6 g/kg
            - Recomposición: 2.0 - 2.4 g/kg
            - Superávit: 1.8 - 2.0 g/kg
            
            **GRASA (g/kg):**
            - Déficit: 0.8 - 1.0 g/kg
            - Recomposición: 0.9 - 1.2 g/kg
            - Superávit: 1.0 - 1.2 g/kg
            """)
            
            st.markdown("---")
            
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
        
        # =============================================================================
        # SECTION 3: ACTIVITY LEVEL AND ENERGY EXPENDITURE
        # =============================================================================
        
        st.markdown("""
        <div class="section-container">
            <h2>🏃‍♂️ Sección 3: Nivel de Actividad y Gasto Energético</h2>
            <p>Evaluación integral de tu actividad física y cálculo del gasto energético total.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            activity_level = st.selectbox("Nivel de actividad física diaria*", [
                "Sedentario", "Ligeramente activo", "Moderadamente activo", 
                "Muy activo", "Extremadamente activo"
            ])
            
            occupation = st.selectbox("Tipo de ocupación/trabajo*", [
                "Oficina/Escritorio", "Trabajo de pie", "Trabajo activo", 
                "Trabajo físico pesado", "Estudiante", "Jubilado/Pensionado"
            ])
            
            training_minutes = st.number_input("Minutos de entrenamiento por sesión*", 
                                             min_value=0, max_value=180, value=60)
            
        with col2:
            training_days = st.number_input("Días de entrenamiento por semana*", 
                                          min_value=0, max_value=7, value=4)
            
            daily_steps = st.selectbox("Pasos diarios promedio*", [
                "< 5,000", "5,000-7,500", "7,500-10,000", "10,000-12,500", "> 12,500"
            ])
            
            # Energy expenditure calculations
            # GER using both methods
            ger_mifflin = calculate_mifflin_st_jeor(weight, height, age, gender)
            ger_katch = calculate_katch_mcardle(lean_mass)
            
            # Use Katch-McArdle if reliable body composition data, otherwise Mifflin-St Jeor
            if bf_method in ["DEXA", "Antropometría"] and num_folds == 7:
                ger_final = ger_katch
                ger_method = "Katch-McArdle"
            else:
                ger_final = ger_mifflin
                ger_method = "Mifflin-St Jeor"
            
            # Apply ETA factor
            ger_with_eta = ger_final * ETA_FACTOR
            
            # GEAF calculation
            geaf = calculate_geaf_factor(activity_level, gender)
            
            # GEE calculation
            gee_weekly = calculate_gee(lean_mass, training_minutes, training_days)
            gee_daily = gee_weekly / 7
            
            # GET calculation
            get_total = (ger_with_eta * geaf) + gee_daily
            
            # Display calculations
            st.metric("GER", f"{ger_final:.0f} kcal")
            st.caption(f"Método: {ger_method}")
            st.metric("GEAF", f"{geaf:.2f}")
            st.metric("GEE", f"{gee_daily:.0f} kcal/día")
            st.metric("GET", f"{get_total:.0f} kcal/día")
        
        # Cross-validation warning
        if activity_level == "Sedentario" and training_days > 5:
            st.warning("⚠️ **Validación cruzada:** Inconsistencia entre actividad diaria y entrenamiento")
        elif activity_level == "Extremadamente activo" and training_days < 3:
            st.warning("⚠️ **Validación cruzada:** Inconsistencia entre actividad diaria y entrenamiento")
        
        # =============================================================================
        # SECTION 4: SLEEP QUALITY (PITTSBURGH ABBREVIATED)
        # =============================================================================
        
        st.markdown("""
        <div class="section-container">
            <h2>💤 Sección 4: Calidad del Sueño (Pittsburgh Abreviado)</h2>
            <p>Evaluación científica de la calidad del sueño para ajustar objetivos energéticos.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            sleep_hours = st.selectbox("¿Cuántas horas duermes por noche habitualmente?*", [
                "Más de 9h", "8-9h", "7-8h", "6-7h", "5-6h", "Menos de 5h"
            ])
            
            time_to_sleep = st.selectbox("¿Cuánto tiempo tardas en quedarte dormido?*", [
                "Menos de 15 min", "15-30 min", "30-45 min", "45-60 min", "Más de 60 min"
            ])
            
        with col2:
            night_awakenings = st.selectbox("¿Cuántas veces te despiertas durante la noche?*", [
                "Nunca", "1 vez", "2 veces", "3 veces", "Más de 3 veces"
            ])
            
            sleep_quality = st.selectbox("¿Cómo calificarías tu calidad de sueño general?*", [
                "Excelente", "Buena", "Regular", "Mala", "Muy mala"
            ])
        
        # Calculate Pittsburgh score
        sleep_score = evaluate_pittsburgh_sleep(sleep_hours, time_to_sleep, night_awakenings, sleep_quality)
        
        if sleep_score >= 10:
            st.markdown(f"""
            <div class="warning-container">
                <h4>⚠️ Calidad de Sueño Deficiente</h4>
                <p><strong>Puntuación Pittsburgh: {sleep_score}/16</strong></p>
                <p>Tu calidad de sueño está comprometida, lo que puede afectar tu recuperación y objetivos nutricionales.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="info-container">
                <h4>✅ Calidad de Sueño Adecuada</h4>
                <p><strong>Puntuación Pittsburgh: {sleep_score}/16</strong></p>
                <p>Tu calidad de sueño es buena y apoya tus objetivos de recuperación.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # =============================================================================
        # SECTION 5: PERCEIVED STRESS (PSS-4)
        # =============================================================================
        
        st.markdown("""
        <div class="section-container">
            <h2>😖 Sección 5: Estrés Percibido (PSS-4)</h2>
            <p>Evaluación del estrés percibido durante el último mes para ajustar el Factor de Recuperación Inteligente.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**En el último mes, ¿con qué frecuencia...**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            pss1 = st.selectbox("¿Has estado molesto/a debido a algo que ha pasado inesperadamente?*", [
                "Nunca", "Casi nunca", "A veces", "Frecuentemente", "Muy frecuentemente"
            ])
            
            pss2 = st.selectbox("¿Te has sentido incapaz de controlar las cosas importantes de tu vida?*", [
                "Nunca", "Casi nunca", "A veces", "Frecuentemente", "Muy frecuentemente"
            ])
            
        with col2:
            pss3 = st.selectbox("¿Te has sentido nervioso/a y estresado/a?*", [
                "Nunca", "Casi nunca", "A veces", "Frecuentemente", "Muy frecuentemente"
            ])
            
            pss4 = st.selectbox("¿Has manejado exitosamente los pequeños problemas irritantes de la vida?*", [
                "Nunca", "Casi nunca", "A veces", "Frecuentemente", "Muy frecuentemente"
            ])
        
        # Calculate PSS-4 score
        stress_score = evaluate_pss4_stress(pss1, pss4, pss3, pss2)  # Note: pss2 and pss4 are inverted
        
        if stress_score >= 10:
            st.markdown(f"""
            <div class="warning-container">
                <h4>⚠️ Nivel de Estrés Elevado</h4>
                <p><strong>Puntuación PSS-4: {stress_score}/16</strong></p>
                <p>Tu nivel de estrés es alto, lo que puede impactar tu recuperación y objetivos nutricionales.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="info-container">
                <h4>✅ Nivel de Estrés Manejable</h4>
                <p><strong>Puntuación PSS-4: {stress_score}/16</strong></p>
                <p>Tu nivel de estrés es adecuado y no interfiere significativamente con tu recuperación.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # =============================================================================
        # INTELLIGENT RECOVERY FACTOR (FRI)
        # =============================================================================
        
        # Calculate FRI
        fri = calculate_fri(sleep_score, stress_score)
        
        st.markdown("""
        <div class="section-container">
            <h2>🧠 Factor de Recuperación Inteligente (FRI)</h2>
            <p>Cálculo automático basado en tu calidad de sueño y nivel de estrés.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Nivel FRI", fri["level"])
        with col2:
            st.metric("Factor de Ajuste", f"{fri['factor']:.2f}")
        with col3:
            st.metric("Descripción", fri["description"])
        
        # FRI impact explanation
        if fri["factor"] < 0.90:
            fri_adjustment_percent = (1 - fri["factor"]) * 100
            st.markdown(f"""
            <div class="warning-container">
                <h4>⚠️ Impacto del FRI</h4>
                <p>Tu Factor de Recuperación Inteligente indica que la severidad de tus objetivos energéticos será 
                reducida automáticamente en un <strong>{fri_adjustment_percent:.0f}%</strong> para optimizar tu recuperación.</p>
                <p>Esto significa que tanto los déficits como los superávits serán menos agresivos para permitir una mejor recuperación.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # =============================================================================
        # FORM SUBMISSION AND CALCULATIONS
        # =============================================================================
        
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
            
            # Mostrar resultados básicos
            st.success("✅ **¡Análisis completado exitosamente!**")
            st.info("📧 **Tu evaluación ha sido enviada a tu entrenador MUPAI.**")
            
            # Enviar al coach
            try:
                trainer_email = "mupaitraining@outlook.com"
                reporte_simple = f"Evaluación de {nombre_completo} - {email_destinatario}"
                enviar_email_resultados(trainer_email, 
                  f"EVALUACIÓN AVANZADA - {nombre_completo}", 
                  reporte_simple)
            except Exception as e:
                st.error(f"❌ Error al enviar reporte: {str(e)}")

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
        st.info("🚧 **Cuestionario en construcción** - Pronto disponible")
        
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
            st.success("✅ **¡Evaluación completada con éxito!**")
            st.info("📧 **Tu evaluación nutricional será enviada a tu entrenador personal.**")

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
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("antojos_alimentarios_form"):
        st.info("🚧 **Cuestionario en construcción** - Pronto disponible")
        
        # EMAIL OBLIGATORIO
        st.markdown("---")
        st.markdown("""
        <div class="questionnaire-container">
            <h3>📧 Información de Contacto</h3>
        </div>
        """, unsafe_allow_html=True)
        
        email_destinatario = st.text_input("Email para seguimiento (obligatorio):", placeholder="tu@email.com")
        
        submitted = st.form_submit_button("🧁 Enviar Evaluación al Entrenador", use_container_width=True)
        
        if submitted:
            st.success("✅ **¡Evaluación completada con éxito!**")
            st.info("📧 **Tu evaluación de antojos será enviada a tu entrenador personal.**")

# ==================== PÁGINA DE PLANES Y COSTOS ====================
elif st.session_state.page == "planes_costos":
    st.markdown("""
    <div class="section-header">
        <h2>💸 Planes y Costos</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="questionnaire-container">
        <h3>🎯 Primer Paso: Elije el Plan Adecuado</h3>
        <p>El primer paso para transformar tu físico y salud es <strong>elegir el plan que mejor se adapte a tus objetivos</strong>. 
        Una vez seleccionado, realiza la transferencia del monto exacto a la tarjeta bancaria que se muestra a continuación.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #fff3cd; border: 2px solid #ffc107; border-radius: 8px; padding: 15px; margin: 15px 0;">
        <h4 style="color: #856404; margin: 0 0 10px 0;">📋 Instrucciones de Pago</h4>
        <p style="color: #856404; margin: 0 0 10px 0; font-size: 16px;">
            <strong>Paso importante:</strong> Después de realizar la transferencia del monto exacto, 
            debes enviar el comprobante de pago a:
        </p>
        <ul style="color: #856404; margin: 0; font-size: 16px; font-weight: bold;">
            <li>📱 <strong>WhatsApp/Teléfono:</strong> 8662580594</li>
            <li>📧 <strong>Correo:</strong> administracion@muscleupgym.fitness</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Imagen de la tarjeta bancaria
    st.markdown("### 💳 Información de Transferencia")
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
    """ + load_banking_image_base64() + """
    </div>
    """, unsafe_allow_html=True)
    
    # Planes detallados
    st.markdown("""
    <div class="section-header">
        <h2>📋 Nuestros Planes Profesionales</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Plan 1: Nutrición Personalizada
    st.markdown("""
    <div class="corporate-section">
        <h3>🍽️ Plan de Nutrición Personalizada</h3>
        <p><strong>Duración:</strong> 6 semanas</p>
        <p><strong>Descripción:</strong> Plan alimentario completamente personalizado basado en tus objetivos, composición corporal, preferencias alimentarias y estilo de vida.</p>
        
        <h4>💰 Precios:</h4>
        <ul>
            <li><strong>Usuarios Internos (miembros del gym):</strong> $350 MXN</li>
            <li><strong>Usuarios Externos:</strong> $450 MXN</li>
        </ul>
        <h4>✅ Beneficios Incluidos:</h4>
        <ul>
            <li>Evaluación inicial completa con bioimpedancia</li>
            <li>6 menús semanales adaptados (calorías, macros, micronutrientes)</li>
            <li>Personalización según preferencias alimentarias</li>
            <li>Evaluación final con medición corporal</li>
            <li>Ajustes adicionales desde $150 MXN</li>
            <li>Menús extra desde $100 MXN</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Plan 2: Entrenamiento Personalizado
    st.markdown("""
    <div class="corporate-section">
        <h3>💪 Plan de Entrenamiento Personalizado</h3>
        <p><strong>Duración:</strong> 8 semanas</p>
        <p><strong>Descripción:</strong> Programa de entrenamiento científicamente diseñado según tu nivel, objetivos, disponibilidad de tiempo y equipamiento.</p>
        
        <h4>💰 Precios:</h4>
        <ul>
            <li><strong>Usuarios Internos (miembros del gym):</strong> $350 MXN</li>
            <li><strong>Usuarios Externos:</strong> $450 MXN</li>
        </ul>
        <h4>✅ Beneficios Incluidos:</h4>
        <ul>
            <li>Evaluación inicial con cuestionario "Designing Your Training"</li>
            <li>Plan personalizado en volumen, frecuencia e intensidad</li>
            <li>Adaptación a tu horario y nivel de experiencia</li>
            <li>Entrega profesional en formato PDF</li>
            <li>Evaluación final de progresos</li>
            <li>Progresiones y variaciones incluidas</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Plan 3: Plan Combinado
    st.markdown("""
    <div class="corporate-section">
        <h3>🔥 Plan Combinado - Entrenamiento + Nutrición</h3>
        <p><strong>Duración:</strong> Nutrición 6 semanas + Entrenamiento 8 semanas</p>
        <p><strong>Descripción:</strong> La solución completa que integra nutrición y entrenamiento personalizado para resultados óptimos y sostenibles.</p>
        
        <h4>💰 Precios:</h4>
        <ul>
            <li><strong>Usuarios Internos (miembros del gym):</strong> $600 MXN</li>
            <li><strong>Usuarios Externos:</strong> $800 MXN</li>
        </ul>
        <h4>✅ Beneficios Incluidos:</h4>
        <ul>
            <li>Ambos planes completos (nutrición + entrenamiento)</li>
            <li>Evaluación inicial y final con bioimpedancia</li>
            <li>Integración total entre dieta y entrenamiento</li>
            <li>Seguimiento coordinado de progreso</li>
            <li><strong>Ahorro de $100 MXN (internos) o $100 MXN (externos)</strong></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Mecánica de adquisición
    st.markdown("""
    <div class="section-header">
        <h2>📝 Mecánica de Adquisición - Paso a Paso</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="questionnaire-container">
        <h3>🔄 Proceso Completo de Adquisición</h3>
        <ol style="font-size: 1.1rem; line-height: 1.8;">
            <li><strong>Selección del Plan:</strong> Elige el plan que mejor se adapte a tus objetivos y presupuesto</li>
            <li><strong>Transferencia Bancaria:</strong> Realiza la transferencia del monto exacto a la cuenta mostrada arriba</li>
            <li><strong>Envío de Comprobante:</strong> Envía tu comprobante de pago por:
                <ul>
                    <li>📧 Correo: administracion@muscleupgym.fitness</li>
                    <li>📱 WhatsApp: 8662580594</li>
                </ul>
            </li>
            <li><strong>Programación de Medición:</strong> Agenda tu medición corporal inicial (ver detalles abajo)</li>
            <li><strong>Acceso a Cuestionarios:</strong> Se autoriza el acceso a los cuestionarios especializados</li>
            <li><strong>Llenado de Cuestionarios:</strong> Completa los cuestionarios correspondientes a tu plan</li>
            <li><strong>Entrega del Plan:</strong> Recibe tu plan personalizado en 3 a 5 días hábiles</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Explicación sobre medición corporal
    st.markdown("""
    <div class="section-header">
        <h2>📏 Medición Corporal</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🏠 Usuarios Internos (Miembros del Gym)</h3>
            <p><strong>Ubicación:</strong> Instalaciones de Muscle Up Gym</p>
            <p><strong>Equipo:</strong> Bioimpedancia profesional</p>
            <p><strong>Incluye:</strong></p>
            <ul>
                <li>Medición con bioimpedancia</li>
                <li>Antropometría completa</li>
                <li>Asesoría presencial</li>
                <li>Programación de cita incluida</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🌍 Usuarios Externos (Foráneos)</h3>
            <p><strong>Modalidad:</strong> Por cuenta propia</p>
            <p><strong>Requerimiento:</strong> Medición local</p>
            <p><strong>Incluye:</strong></p>
            <ul>
                <li>Guía detallada para medición</li>
                <li>Recomendaciones de equipos</li>
                <li>Asesoría virtual incluida</li>
                <li>Validación de datos por el profesional</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Direccionamiento a cuestionarios
    st.markdown("""
    <div class="section-header">
        <h2>📝 Acceso a Cuestionarios Especializados</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="questionnaire-container">
        <h3>🎯 Cuestionarios Según Tu Plan</h3>
        <p>Una vez confirmado tu pago y programada tu medición, tendrás acceso a los siguientes cuestionarios:</p>
        
        <h4>📊 Para TODOS los planes:</h4>
        <ul>
            <li><strong>MUPAI BODY AND ENERGY:</strong> Evaluación avanzada de balance energético y composición corporal</li>
        </ul>
        <h4>🍽️ Para planes de ALIMENTACIÓN:</h4>
        <ul>
            <li><strong>FOOD PREFERENCES:</strong> Análisis detallado de patrones y preferencias alimentarias</li>
            <li><strong>FOOD CRAVINGS:</strong> Evaluación de antojos alimentarios (versión población mexicana)</li>
        </ul>
        <h4>💪 Para planes de ENTRENAMIENTO:</h4>
        <ul>
            <li><strong>DESIGNING YOUR TRAINING:</strong> Cuestionario especializado para diseño de rutinas de entrenamiento</li>
        </ul>
        <h4>🔥 Para plan COMBINADO:</h4>
        <ul>
            <li><strong>TODOS los cuestionarios anteriores</strong> para una evaluación integral completa</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Nota final
    st.markdown("""
    <div class="results-container">
        <h3>⏰ Tiempo de Entrega</h3>
        <p style="font-size: 1.2rem; text-align: center; margin: 0;">
            <strong>Los planes se entregan de 3 a 5 días hábiles</strong> tras completar la medición corporal y los cuestionarios correspondientes.
        </p>
        <p style="text-align: center; margin-top: 1rem;">
            💡 <strong>Nota:</strong> La calidad de tu plan depende de la precisión de la información proporcionada en los cuestionarios y mediciones.
        </p>
    </div>
    """, unsafe_allow_html=True)

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
    
    # Sección de contacto renovada
    st.markdown("""
    ### 📞 Contacto Muscle Up Gym

    - **Correo:** [administracion@muscleupgym.fitness](mailto:administracion@muscleupgym.fitness)
    - **WhatsApp:** [8662580594](https://wa.me/528662580594)
    - **Facebook:** [Muscle Up Gym](https://www.facebook.com/share/16WtR5TLw5/)
    - **Instagram:** [@mup_lindavista](https://www.instagram.com/mup_lindavista?igsh=MWVhaHBvMmxib3hweQ==) | [@erickmuscleup](https://www.instagram.com/erickmuscleup?igsh=MXZrZ2l0bmZ3MGtleQ==)
    - **Sitio Web:** [www.muscleupgym.fitness](https://www.muscleupgym.fitness)

    > ¡Agenda tu cita y recibe asesoría profesional!
    """, unsafe_allow_html=True)

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