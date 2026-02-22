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
import glob
import textwrap
import json
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

def load_muscle_up_logo_base64():
    """
    Loads the muscle up logo image and returns it as base64 encoded string.
    Returns None if file is not found or any error occurs.
    """
    logo_path = 'LOGO MUSCLE UP GYM.png'
    
    try:
        with open(logo_path, 'rb') as f:
            image_data = f.read()
            encoded_image = base64.b64encode(image_data).decode()
            return f'data:image/png;base64,{encoded_image}'
    except (FileNotFoundError, Exception):
        return None

def load_mupai_logo_base64():
    """
    Loads the MUPAI logo image and returns it as base64 encoded string.
    Returns None if file is not found or any error occurs.
    """
    logo_path = 'LOGO MUPAI.png'
    
    try:
        with open(logo_path, 'rb') as f:
            image_data = f.read()
            encoded_image = base64.b64encode(image_data).decode()
            return f'data:image/png;base64,{encoded_image}'
    except (FileNotFoundError, Exception):
        return None


# =============================================================================
# BIBLIOTECA DE EJERCICIOS MUPAI (Datos Estructurados)
# =============================================================================
# Cada ejercicio: nombre, equipo necesario, nivel minimo, musculos principales

BIBLIOTECA_EJERCICIOS = {
    "Empuje Horizontal": {
        "Pecho / Triceps / Deltoides Anterior": [
            {"nombre": "Press de banca con barra", "equipo": "Barra + Banco", "nivel": "Intermedio", "musculos": ["Pecho", "Triceps", "Deltoides anterior"]},
            {"nombre": "Press de banca con mancuernas", "equipo": "Mancuernas + Banco", "nivel": "Principiante", "musculos": ["Pecho", "Triceps", "Deltoides anterior"]},
            {"nombre": "Press inclinado con barra", "equipo": "Barra + Banco inclinado", "nivel": "Intermedio", "musculos": ["Pecho superior", "Deltoides anterior"]},
            {"nombre": "Press inclinado con mancuernas", "equipo": "Mancuernas + Banco inclinado", "nivel": "Principiante", "musculos": ["Pecho superior", "Deltoides anterior"]},
            {"nombre": "Press declinado con barra", "equipo": "Barra + Banco declinado", "nivel": "Intermedio", "musculos": ["Pecho inferior", "Triceps"]},
            {"nombre": "Aperturas con mancuernas", "equipo": "Mancuernas + Banco", "nivel": "Principiante", "musculos": ["Pecho"]},
            {"nombre": "Aperturas inclinadas con mancuernas", "equipo": "Mancuernas + Banco inclinado", "nivel": "Principiante", "musculos": ["Pecho superior"]},
            {"nombre": "Crossover en polea alta", "equipo": "Poleas", "nivel": "Principiante", "musculos": ["Pecho"]},
            {"nombre": "Crossover en polea baja", "equipo": "Poleas", "nivel": "Principiante", "musculos": ["Pecho superior"]},
            {"nombre": "Press en maquina", "equipo": "Maquina", "nivel": "Principiante", "musculos": ["Pecho", "Triceps"]},
            {"nombre": "Fondos en paralelas", "equipo": "Paralelas", "nivel": "Intermedio", "musculos": ["Pecho inferior", "Triceps"]},
            {"nombre": "Lagartijas (push-ups)", "equipo": "Peso corporal", "nivel": "Principiante", "musculos": ["Pecho", "Triceps"]},
        ]
    },
    "Empuje Vertical": {
        "Deltoides / Triceps": [
            {"nombre": "Press militar con barra", "equipo": "Barra", "nivel": "Intermedio", "musculos": ["Deltoides anterior", "Triceps"]},
            {"nombre": "Press militar con mancuernas", "equipo": "Mancuernas", "nivel": "Principiante", "musculos": ["Deltoides anterior", "Triceps"]},
            {"nombre": "Press Arnold", "equipo": "Mancuernas", "nivel": "Intermedio", "musculos": ["Deltoides anterior", "Deltoides lateral"]},
            {"nombre": "Elevaciones laterales con mancuernas", "equipo": "Mancuernas", "nivel": "Principiante", "musculos": ["Deltoides lateral"]},
            {"nombre": "Elevaciones laterales en polea", "equipo": "Polea", "nivel": "Principiante", "musculos": ["Deltoides lateral"]},
            {"nombre": "Elevaciones frontales", "equipo": "Mancuernas", "nivel": "Principiante", "musculos": ["Deltoides anterior"]},
            {"nombre": "Press en maquina de hombro", "equipo": "Maquina", "nivel": "Principiante", "musculos": ["Deltoides", "Triceps"]},
            {"nombre": "Face pulls", "equipo": "Polea", "nivel": "Principiante", "musculos": ["Deltoides posterior", "Rotadores externos"]},
            {"nombre": "Pajaros (reverse fly)", "equipo": "Mancuernas", "nivel": "Principiante", "musculos": ["Deltoides posterior"]},
            {"nombre": "Pajaros en maquina (pec deck inverso)", "equipo": "Maquina", "nivel": "Principiante", "musculos": ["Deltoides posterior"]},
        ]
    },
    "Jalon Horizontal": {
        "Espalda / Biceps": [
            {"nombre": "Remo con barra", "equipo": "Barra", "nivel": "Intermedio", "musculos": ["Dorsal", "Romboides", "Biceps"]},
            {"nombre": "Remo con mancuerna a una mano", "equipo": "Mancuerna + Banco", "nivel": "Principiante", "musculos": ["Dorsal", "Romboides"]},
            {"nombre": "Remo en maquina", "equipo": "Maquina", "nivel": "Principiante", "musculos": ["Dorsal", "Romboides"]},
            {"nombre": "Remo en polea baja (sentado)", "equipo": "Polea", "nivel": "Principiante", "musculos": ["Dorsal", "Romboides", "Biceps"]},
            {"nombre": "Remo T-bar", "equipo": "Barra T / Landmine", "nivel": "Intermedio", "musculos": ["Dorsal", "Romboides"]},
            {"nombre": "Remo Pendlay", "equipo": "Barra", "nivel": "Avanzado", "musculos": ["Dorsal", "Romboides", "Erectores"]},
            {"nombre": "Remo invertido (bodyweight row)", "equipo": "Barra fija / Smith", "nivel": "Principiante", "musculos": ["Dorsal", "Romboides"]},
        ]
    },
    "Jalon Vertical": {
        "Espalda / Biceps": [
            {"nombre": "Jalon al pecho (lat pulldown)", "equipo": "Polea alta", "nivel": "Principiante", "musculos": ["Dorsal", "Biceps"]},
            {"nombre": "Jalon con agarre cerrado", "equipo": "Polea alta", "nivel": "Principiante", "musculos": ["Dorsal", "Biceps"]},
            {"nombre": "Dominadas (pull-ups)", "equipo": "Barra fija", "nivel": "Intermedio", "musculos": ["Dorsal", "Biceps"]},
            {"nombre": "Dominadas con agarre supino (chin-ups)", "equipo": "Barra fija", "nivel": "Intermedio", "musculos": ["Dorsal", "Biceps"]},
            {"nombre": "Dominadas asistidas", "equipo": "Maquina asistida / Banda", "nivel": "Principiante", "musculos": ["Dorsal", "Biceps"]},
            {"nombre": "Pullover con mancuerna", "equipo": "Mancuerna + Banco", "nivel": "Intermedio", "musculos": ["Dorsal", "Pecho"]},
            {"nombre": "Pullover en polea", "equipo": "Polea alta", "nivel": "Principiante", "musculos": ["Dorsal"]},
        ]
    },
    "Sentadilla / Dominante de Rodilla": {
        "Cuadriceps / Gluteos": [
            {"nombre": "Sentadilla con barra (back squat)", "equipo": "Barra + Rack", "nivel": "Intermedio", "musculos": ["Cuadriceps", "Gluteos", "Erectores"]},
            {"nombre": "Sentadilla frontal (front squat)", "equipo": "Barra + Rack", "nivel": "Avanzado", "musculos": ["Cuadriceps", "Core"]},
            {"nombre": "Sentadilla goblet", "equipo": "Mancuerna / Kettlebell", "nivel": "Principiante", "musculos": ["Cuadriceps", "Gluteos"]},
            {"nombre": "Sentadilla bulgara", "equipo": "Mancuernas + Banco", "nivel": "Intermedio", "musculos": ["Cuadriceps", "Gluteos"]},
            {"nombre": "Sentadilla en Smith", "equipo": "Maquina Smith", "nivel": "Principiante", "musculos": ["Cuadriceps", "Gluteos"]},
            {"nombre": "Prensa de pierna (leg press)", "equipo": "Maquina", "nivel": "Principiante", "musculos": ["Cuadriceps", "Gluteos"]},
            {"nombre": "Hack squat", "equipo": "Maquina", "nivel": "Intermedio", "musculos": ["Cuadriceps"]},
            {"nombre": "Extension de pierna", "equipo": "Maquina", "nivel": "Principiante", "musculos": ["Cuadriceps"]},
            {"nombre": "Zancadas (lunges) con mancuernas", "equipo": "Mancuernas", "nivel": "Principiante", "musculos": ["Cuadriceps", "Gluteos"]},
            {"nombre": "Step-ups", "equipo": "Mancuernas + Cajon", "nivel": "Principiante", "musculos": ["Cuadriceps", "Gluteos"]},
            {"nombre": "Sentadilla con peso corporal", "equipo": "Peso corporal", "nivel": "Principiante", "musculos": ["Cuadriceps", "Gluteos"]},
        ]
    },
    "Bisagra de Cadera / Dominante de Cadera": {
        "Isquiotibiales / Gluteos / Erectores": [
            {"nombre": "Peso muerto convencional", "equipo": "Barra", "nivel": "Intermedio", "musculos": ["Isquiotibiales", "Gluteos", "Erectores"]},
            {"nombre": "Peso muerto sumo", "equipo": "Barra", "nivel": "Intermedio", "musculos": ["Gluteos", "Aductores", "Isquiotibiales"]},
            {"nombre": "Peso muerto rumano (RDL) con barra", "equipo": "Barra", "nivel": "Intermedio", "musculos": ["Isquiotibiales", "Gluteos"]},
            {"nombre": "Peso muerto rumano con mancuernas", "equipo": "Mancuernas", "nivel": "Principiante", "musculos": ["Isquiotibiales", "Gluteos"]},
            {"nombre": "Hip thrust con barra", "equipo": "Barra + Banco", "nivel": "Intermedio", "musculos": ["Gluteos"]},
            {"nombre": "Hip thrust en maquina", "equipo": "Maquina", "nivel": "Principiante", "musculos": ["Gluteos"]},
            {"nombre": "Puente de gluteos (glute bridge)", "equipo": "Peso corporal / Barra", "nivel": "Principiante", "musculos": ["Gluteos"]},
            {"nombre": "Curl de pierna acostado", "equipo": "Maquina", "nivel": "Principiante", "musculos": ["Isquiotibiales"]},
            {"nombre": "Curl de pierna sentado", "equipo": "Maquina", "nivel": "Principiante", "musculos": ["Isquiotibiales"]},
            {"nombre": "Hiperextensiones", "equipo": "Banco de hiperextensiones", "nivel": "Principiante", "musculos": ["Erectores", "Gluteos"]},
            {"nombre": "Swing con kettlebell", "equipo": "Kettlebell", "nivel": "Intermedio", "musculos": ["Gluteos", "Isquiotibiales"]},
        ]
    },
    "Brazos - Biceps": {
        "Biceps": [
            {"nombre": "Curl con barra recta", "equipo": "Barra", "nivel": "Principiante", "musculos": ["Biceps"]},
            {"nombre": "Curl con barra Z", "equipo": "Barra Z", "nivel": "Principiante", "musculos": ["Biceps"]},
            {"nombre": "Curl con mancuernas alterno", "equipo": "Mancuernas", "nivel": "Principiante", "musculos": ["Biceps"]},
            {"nombre": "Curl martillo", "equipo": "Mancuernas", "nivel": "Principiante", "musculos": ["Biceps", "Braquial"]},
            {"nombre": "Curl concentrado", "equipo": "Mancuerna", "nivel": "Principiante", "musculos": ["Biceps"]},
            {"nombre": "Curl en banco Scott (predicador)", "equipo": "Barra / Mancuerna + Banco Scott", "nivel": "Principiante", "musculos": ["Biceps"]},
            {"nombre": "Curl en polea baja", "equipo": "Polea", "nivel": "Principiante", "musculos": ["Biceps"]},
            {"nombre": "Curl inclinado con mancuernas", "equipo": "Mancuernas + Banco inclinado", "nivel": "Intermedio", "musculos": ["Biceps"]},
        ]
    },
    "Brazos - Triceps": {
        "Triceps": [
            {"nombre": "Press frances con barra Z", "equipo": "Barra Z + Banco", "nivel": "Intermedio", "musculos": ["Triceps"]},
            {"nombre": "Press frances con mancuernas", "equipo": "Mancuernas + Banco", "nivel": "Principiante", "musculos": ["Triceps"]},
            {"nombre": "Extension de triceps en polea (pushdown)", "equipo": "Polea", "nivel": "Principiante", "musculos": ["Triceps"]},
            {"nombre": "Extension de triceps con cuerda", "equipo": "Polea + Cuerda", "nivel": "Principiante", "musculos": ["Triceps"]},
            {"nombre": "Patada de triceps (kickback)", "equipo": "Mancuerna", "nivel": "Principiante", "musculos": ["Triceps"]},
            {"nombre": "Press cerrado con barra", "equipo": "Barra + Banco", "nivel": "Intermedio", "musculos": ["Triceps", "Pecho"]},
            {"nombre": "Fondos en banco (bench dips)", "equipo": "Banco", "nivel": "Principiante", "musculos": ["Triceps"]},
            {"nombre": "Extension overhead con mancuerna", "equipo": "Mancuerna", "nivel": "Principiante", "musculos": ["Triceps"]},
        ]
    },
    "Core / Abdomen": {
        "Core": [
            {"nombre": "Plancha frontal (plank)", "equipo": "Peso corporal", "nivel": "Principiante", "musculos": ["Recto abdominal", "Transverso"]},
            {"nombre": "Plancha lateral", "equipo": "Peso corporal", "nivel": "Principiante", "musculos": ["Oblicuos"]},
            {"nombre": "Crunch en maquina", "equipo": "Maquina", "nivel": "Principiante", "musculos": ["Recto abdominal"]},
            {"nombre": "Crunch en polea alta", "equipo": "Polea", "nivel": "Intermedio", "musculos": ["Recto abdominal"]},
            {"nombre": "Elevacion de piernas colgado", "equipo": "Barra fija", "nivel": "Intermedio", "musculos": ["Recto abdominal inferior"]},
            {"nombre": "Elevacion de piernas en banco", "equipo": "Banco", "nivel": "Principiante", "musculos": ["Recto abdominal inferior"]},
            {"nombre": "Ab wheel rollout", "equipo": "Rueda abdominal", "nivel": "Intermedio", "musculos": ["Recto abdominal", "Core"]},
            {"nombre": "Pallof press", "equipo": "Polea / Banda", "nivel": "Intermedio", "musculos": ["Core anti-rotacion"]},
            {"nombre": "Dead bug", "equipo": "Peso corporal", "nivel": "Principiante", "musculos": ["Core estabilizacion"]},
        ]
    },
    "Pantorrillas": {
        "Gemelos / Soleo": [
            {"nombre": "Elevacion de pantorrillas de pie", "equipo": "Maquina / Smith", "nivel": "Principiante", "musculos": ["Gastrocnemio"]},
            {"nombre": "Elevacion de pantorrillas sentado", "equipo": "Maquina", "nivel": "Principiante", "musculos": ["Soleo"]},
            {"nombre": "Elevacion de pantorrillas en prensa", "equipo": "Prensa de pierna", "nivel": "Principiante", "musculos": ["Gastrocnemio"]},
        ]
    }
}

# Splits de entrenamiento sugeridos por frecuencia semanal
SPLITS_ENTRENAMIENTO = {
    2: {"nombre": "Full Body (2 dias)", "descripcion": "Cuerpo completo 2 veces por semana",
        "dias": {
            "Dia A - Full Body": ["Sentadilla / Dominante de Rodilla", "Empuje Horizontal", "Jalon Vertical", "Bisagra de Cadera / Dominante de Cadera", "Core / Abdomen"],
            "Dia B - Full Body": ["Bisagra de Cadera / Dominante de Cadera", "Empuje Vertical", "Jalon Horizontal", "Sentadilla / Dominante de Rodilla", "Core / Abdomen"]
        }},
    3: {"nombre": "Full Body (3 dias)", "descripcion": "Cuerpo completo 3 veces con variacion",
        "dias": {
            "Dia A - Full Body (Fuerza)": ["Sentadilla / Dominante de Rodilla", "Empuje Horizontal", "Jalon Vertical", "Bisagra de Cadera / Dominante de Cadera", "Core / Abdomen"],
            "Dia B - Full Body (Volumen)": ["Empuje Vertical", "Jalon Horizontal", "Sentadilla / Dominante de Rodilla", "Bisagra de Cadera / Dominante de Cadera", "Brazos - Biceps", "Brazos - Triceps"],
            "Dia C - Full Body (Hipertrofia)": ["Sentadilla / Dominante de Rodilla", "Empuje Horizontal", "Jalon Vertical", "Bisagra de Cadera / Dominante de Cadera", "Empuje Vertical", "Core / Abdomen"]
        }},
    4: {"nombre": "Upper/Lower (4 dias)", "descripcion": "Tren superior / tren inferior, 4 dias",
        "dias": {
            "Dia A - Tren Superior (Fuerza)": ["Empuje Horizontal", "Jalon Vertical", "Empuje Vertical", "Jalon Horizontal", "Brazos - Biceps", "Brazos - Triceps"],
            "Dia B - Tren Inferior (Fuerza)": ["Sentadilla / Dominante de Rodilla", "Bisagra de Cadera / Dominante de Cadera", "Sentadilla / Dominante de Rodilla", "Pantorrillas", "Core / Abdomen"],
            "Dia C - Tren Superior (Hipertrofia)": ["Empuje Horizontal", "Jalon Vertical", "Empuje Vertical", "Jalon Horizontal", "Brazos - Biceps", "Brazos - Triceps"],
            "Dia D - Tren Inferior (Hipertrofia)": ["Sentadilla / Dominante de Rodilla", "Bisagra de Cadera / Dominante de Cadera", "Bisagra de Cadera / Dominante de Cadera", "Pantorrillas", "Core / Abdomen"]
        }},
    5: {"nombre": "Upper/Lower + PPL (5 dias)", "descripcion": "Upper-Lower + Push-Pull-Legs, 5 dias",
        "dias": {
            "Dia A - Tren Superior": ["Empuje Horizontal", "Jalon Vertical", "Empuje Vertical", "Jalon Horizontal", "Brazos - Biceps", "Brazos - Triceps"],
            "Dia B - Tren Inferior": ["Sentadilla / Dominante de Rodilla", "Bisagra de Cadera / Dominante de Cadera", "Sentadilla / Dominante de Rodilla", "Pantorrillas", "Core / Abdomen"],
            "Dia C - Push": ["Empuje Horizontal", "Empuje Horizontal", "Empuje Vertical", "Empuje Vertical", "Brazos - Triceps"],
            "Dia D - Pull": ["Jalon Vertical", "Jalon Horizontal", "Jalon Vertical", "Jalon Horizontal", "Brazos - Biceps"],
            "Dia E - Legs": ["Sentadilla / Dominante de Rodilla", "Bisagra de Cadera / Dominante de Cadera", "Sentadilla / Dominante de Rodilla", "Bisagra de Cadera / Dominante de Cadera", "Pantorrillas", "Core / Abdomen"]
        }},
    6: {"nombre": "Push/Pull/Legs x2 (6 dias)", "descripcion": "PPL dos veces por semana",
        "dias": {
            "Dia A - Push (Fuerza)": ["Empuje Horizontal", "Empuje Horizontal", "Empuje Vertical", "Empuje Vertical", "Brazos - Triceps"],
            "Dia B - Pull (Fuerza)": ["Jalon Vertical", "Jalon Horizontal", "Jalon Vertical", "Jalon Horizontal", "Brazos - Biceps"],
            "Dia C - Legs (Fuerza)": ["Sentadilla / Dominante de Rodilla", "Bisagra de Cadera / Dominante de Cadera", "Sentadilla / Dominante de Rodilla", "Pantorrillas", "Core / Abdomen"],
            "Dia D - Push (Hipertrofia)": ["Empuje Horizontal", "Empuje Horizontal", "Empuje Vertical", "Empuje Vertical", "Brazos - Triceps"],
            "Dia E - Pull (Hipertrofia)": ["Jalon Vertical", "Jalon Horizontal", "Jalon Vertical", "Jalon Horizontal", "Brazos - Biceps"],
            "Dia F - Legs (Hipertrofia)": ["Sentadilla / Dominante de Rodilla", "Bisagra de Cadera / Dominante de Cadera", "Bisagra de Cadera / Dominante de Cadera", "Pantorrillas", "Core / Abdomen"]
        }}
}

# Guias de volumen por nivel (series por grupo muscular por semana)
GUIAS_VOLUMEN = {
    "Principiante": {"min_series": 10, "max_series": 14, "rpe": "6-7", "descripcion": "Volumen bajo-moderado, enfoque en tecnica"},
    "Intermedio": {"min_series": 14, "max_series": 20, "rpe": "7-8", "descripcion": "Volumen moderado, progresion de cargas"},
    "Avanzado": {"min_series": 18, "max_series": 26, "rpe": "8-9", "descripcion": "Volumen alto, tecnicas avanzadas de intensidad"}
}

# Opciones de equipo disponible
OPCIONES_EQUIPO = [
    "Barras (recta y Z)",
    "Mancuernas",
    "Maquinas de cables/poleas",
    "Maquinas de placas (press, extension, curl, etc.)",
    "Rack de sentadillas / Power rack",
    "Banco plano e inclinado",
    "Barra fija (dominadas)",
    "Paralelas (fondos)",
    "Kettlebells",
    "Bandas de resistencia",
    "Maquina Smith",
    "Prensa de pierna (leg press)",
    "Hack squat (maquina)",
    "Solo peso corporal"
]


def filtrar_ejercicios_por_nivel(nivel):
    """Filtra ejercicios disponibles segun nivel del usuario."""
    jerarquia = {"Principiante": 0, "Intermedio": 1, "Avanzado": 2}
    nivel_usuario = jerarquia.get(nivel, 0)
    filtrado = {}
    for patron, grupos in BIBLIOTECA_EJERCICIOS.items():
        filtrado[patron] = {}
        for grupo, ejercicios in grupos.items():
            filtrado[patron][grupo] = [
                ej for ej in ejercicios
                if jerarquia.get(ej["nivel"], 0) <= nivel_usuario
            ]
    return filtrado


def filtrar_ejercicios_por_equipo(ejercicios_dict, equipo_disponible):
    """Filtra ejercicios segun equipo disponible del usuario."""
    mapa_equipo = {
        "Barras (recta y Z)": ["barra"],
        "Mancuernas": ["mancuerna"],
        "Maquinas de cables/poleas": ["polea"],
        "Maquinas de placas (press, extension, curl, etc.)": ["maquina"],
        "Rack de sentadillas / Power rack": ["rack"],
        "Banco plano e inclinado": ["banco"],
        "Barra fija (dominadas)": ["barra fija"],
        "Paralelas (fondos)": ["paralelas"],
        "Kettlebells": ["kettlebell"],
        "Bandas de resistencia": ["banda"],
        "Maquina Smith": ["smith"],
        "Prensa de pierna (leg press)": ["prensa"],
        "Hack squat (maquina)": ["hack"],
        "Solo peso corporal": ["peso corporal"]
    }
    keywords = set()
    for eq in equipo_disponible:
        for kw in mapa_equipo.get(eq, []):
            keywords.add(kw)
    keywords.add("peso corporal")

    filtrado = {}
    for patron, grupos in ejercicios_dict.items():
        filtrado[patron] = {}
        for grupo, ejercicios in grupos.items():
            filtrado[patron][grupo] = [
                ej for ej in ejercicios
                if any(kw in ej["equipo"].lower() for kw in keywords)
            ]
    return filtrado


def calcular_distribucion_volumen(objetivo, nivel, musculos_prioritarios):
    """Calcula series semanales por patron de movimiento."""
    vol = GUIAS_VOLUMEN[nivel]
    base = (vol["min_series"] + vol["max_series"]) // 2
    dist = {
        "Empuje Horizontal": base,
        "Empuje Vertical": max(base - 2, vol["min_series"]),
        "Jalon Horizontal": base,
        "Jalon Vertical": max(base - 2, vol["min_series"]),
        "Sentadilla / Dominante de Rodilla": base,
        "Bisagra de Cadera / Dominante de Cadera": base,
        "Brazos - Biceps": max(base - 4, 6),
        "Brazos - Triceps": max(base - 4, 6),
        "Core / Abdomen": max(base - 4, 6),
        "Pantorrillas": max(base - 6, 4),
    }
    if objetivo == "Hipertrofia":
        for k in dist:
            dist[k] = min(dist[k] + 2, vol["max_series"])
    elif objetivo == "Fuerza":
        for k in dist:
            dist[k] = max(dist[k] - 2, vol["min_series"])
    mapa_musculo = {
        "Pecho": ["Empuje Horizontal"], "Espalda": ["Jalon Horizontal", "Jalon Vertical"],
        "Hombros": ["Empuje Vertical"], "Cuadriceps": ["Sentadilla / Dominante de Rodilla"],
        "Isquiotibiales / Gluteos": ["Bisagra de Cadera / Dominante de Cadera"],
        "Biceps": ["Brazos - Biceps"], "Triceps": ["Brazos - Triceps"],
        "Core": ["Core / Abdomen"], "Pantorrillas": ["Pantorrillas"]
    }
    for musculo in musculos_prioritarios:
        for p in mapa_musculo.get(musculo, []):
            if p in dist:
                dist[p] = min(dist[p] + 4, vol["max_series"] + 2)
    return dist


def determinar_esquema_reps(objetivo, nivel):
    """Determina rangos de repeticiones y descansos segun objetivo."""
    esquemas = {
        "Fuerza": {"reps_compuesto": "3-6", "series_compuesto": "4-5", "reps_aislamiento": "6-10", "series_aislamiento": "3-4",
                    "descanso_compuesto": "3-5 min", "descanso_aislamiento": "2-3 min",
                    "rpe": "8-9" if nivel != "Principiante" else "7-8", "tempo": "2-0-1-1"},
        "Hipertrofia": {"reps_compuesto": "8-12", "series_compuesto": "3-4", "reps_aislamiento": "10-15", "series_aislamiento": "3-4",
                         "descanso_compuesto": "2-3 min", "descanso_aislamiento": "1-2 min",
                         "rpe": "7-9" if nivel != "Principiante" else "6-8", "tempo": "3-1-1-0"},
        "Resistencia muscular": {"reps_compuesto": "12-20", "series_compuesto": "3", "reps_aislamiento": "15-25", "series_aislamiento": "2-3",
                                   "descanso_compuesto": "1-2 min", "descanso_aislamiento": "45-90 seg",
                                   "rpe": "6-7", "tempo": "2-0-2-0"},
        "Recomposicion": {"reps_compuesto": "6-10", "series_compuesto": "3-4", "reps_aislamiento": "10-15", "series_aislamiento": "3",
                           "descanso_compuesto": "2-3 min", "descanso_aislamiento": "1.5-2 min",
                           "rpe": "7-8", "tempo": "2-1-1-0"}
    }
    return esquemas.get(objetivo, esquemas["Hipertrofia"])


def generar_reporte_entrenamiento(datos):
    """Genera reporte completo de entrenamiento para el coach."""
    esquema = datos["esquema_reps"]
    reporte = f"""
========================================
DESIGNING YOUR TRAINING - REPORTE MUPAI
========================================

Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Cliente: {datos['nombre']}
Email: {datos.get('email', 'N/A')}

========================================
DATOS DEL CLIENTE
========================================
Edad: {datos['edad']} | Sexo: {datos['genero']}
Peso: {datos['peso']} kg | Estatura: {datos['estatura']} cm

========================================
PERFIL DE ENTRENAMIENTO
========================================
Nivel: {datos['nivel']}
Experiencia: {datos['experiencia']}
Objetivo: {datos['objetivo']}
Frecuencia: {datos['frecuencia']} dias/semana
Duracion sesion: {datos['duracion_sesion']}
Consistencia reciente: {datos['consistencia']}
Rutina actual: {datos['rutina_actual']}

========================================
EQUIPO DISPONIBLE
========================================
Ubicacion: {datos['ubicacion']}
{chr(10).join('- ' + eq for eq in datos['equipo'])}

========================================
MUSCULOS PRIORITARIOS
========================================
{chr(10).join('- ' + m for m in datos['prioridades']) if datos['prioridades'] else '- Sin prioridades especificas'}

Puntos debiles: {', '.join(datos.get('puntos_debiles', [])) if datos.get('puntos_debiles') else 'No reportados'}

========================================
SPLIT SUGERIDO
========================================
{datos['split_nombre']}
{datos['split_descripcion']}

========================================
VOLUMEN SEMANAL (series/grupo)
========================================
"""
    for patron, series in datos["distribucion_volumen"].items():
        reporte += f"- {patron}: {series} series/semana\n"

    reporte += f"""
========================================
ESQUEMA DE REPETICIONES
========================================
Compuestos: {esquema['reps_compuesto']} reps x {esquema['series_compuesto']} series | Descanso: {esquema['descanso_compuesto']}
Aislamiento: {esquema['reps_aislamiento']} reps x {esquema['series_aislamiento']} series | Descanso: {esquema['descanso_aislamiento']}
RPE objetivo: {esquema['rpe']}
Tempo: {esquema['tempo']} (excentrica-pausa-concentrica-pausa)

========================================
EJERCICIOS SELECCIONADOS
========================================
"""
    if datos.get("ejercicios_seleccionados"):
        for patron, ejercicios in datos["ejercicios_seleccionados"].items():
            if ejercicios:
                reporte += f"\n--- {patron} ---\n"
                for ej in ejercicios:
                    reporte += f"  - {ej}\n"
    else:
        reporte += "Pendiente de seleccion por el coach\n"

    if datos.get("pruebas_funcionales"):
        reporte += "\n========================================\nPRUEBAS FUNCIONALES\n========================================\n"
        for nombre, valor in datos["pruebas_funcionales"].items():
            if valor and valor > 0:
                reporte += f"- {nombre}: {valor}\n"

    reporte += f"""
========================================
LESIONES Y LIMITACIONES
========================================
{datos.get('lesiones', 'Sin lesiones reportadas')}

========================================
INFORMACION ADICIONAL
========================================
Cardio adicional: {datos.get('cardio', 'No')}
Conoce deload: {datos.get('deload', 'No')}
Conoce RPE: {datos.get('conoce_rpe', 'No')}
Suplementos: {', '.join(datos.get('suplementos', [])) if datos.get('suplementos') else 'Ninguno'}
Horas de sueno: {datos.get('sueno', 'No reportado')}

Observaciones: {datos.get('observaciones', 'Sin observaciones')}

========================================
NOTAS PARA EL COACH
========================================
- Nivel: {datos['nivel']} - {GUIAS_VOLUMEN[datos['nivel']]['descripcion']}
- RPE sugerido: {GUIAS_VOLUMEN[datos['nivel']]['rpe']}
- Volumen semanal: {GUIAS_VOLUMEN[datos['nivel']]['min_series']}-{GUIAS_VOLUMEN[datos['nivel']]['max_series']} series/grupo
- Ajustar seleccion de ejercicios segun limitaciones
- Verificar tecnica antes de prescribir cargas
========================================
"""
    return reporte


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
    /* Tema principal: Negro, amarillo mostaza, blanco - aplicado a toda la página */
    .stApp {
        background-color: #000000;
    }
    
    .stApp > div:first-child {
        background-color: #000000;
    }
    
    /* Header negro para que coincida con el tema */
    [data-testid="stHeader"] {
        background-color: #000000 !important;
    }
    
    /* PRIMERO: Todo el toolbar en amarillo */
    [data-testid="stToolbar"],
    [data-testid="stToolbar"] *,
    [data-testid="stToolbar"] button,
    [data-testid="stToolbar"] span {
        color: #FFCC00 !important;
    }
    
    /* SEGUNDO: Solo iconos SVG en negro (excepto el del >>) */
    [data-testid="stToolbar"] svg,
    [data-testid="stToolbar"] path {
        fill: #000000 !important;
        stroke: #000000 !important;
    }
    
    /* TERCERO: Restaurar el SVG del >> en amarillo */
    button[kind="header"] svg,
    button[kind="header"] path {
        fill: #FFCC00 !important;
        stroke: #FFCC00 !important;
    }
    
    /* CUARTO: Poner los botones de estrella, edit y GitHub SOLO en color negro */
    [data-testid="stToolbar"] button[kind="tertiary"],
    [data-testid="stToolbar"] button[kind="tertiary"] *,
    [data-testid="stToolbar"] button[kind="tertiary"] svg,
    [data-testid="stToolbar"] button[kind="tertiary"] path,
    [data-testid="stToolbar"] a[href*="github"],
    [data-testid="stToolbar"] a[href*="github"] *,
    [data-testid="stToolbar"] a[href*="github"] svg,
    [data-testid="stToolbar"] a[href*="github"] path {
        color: #000000 !important;
        fill: #000000 !important;
        stroke: #000000 !important;
        background-color: transparent !important;
    }

    
    /* Ocultar menú de tres puntos */
    #MainMenu,
    button[aria-label="More options"] {
        display: none !important;
    }
</style>

<script>
// JavaScript para ocultar elementos del toolbar preservando el botón sidebar
(function() {
    function hideToolbarElements() {
        // Buscar en el documento padre (puede estar en iframe)
        const doc = window.parent.document || document;
        const toolbar = doc.querySelector('[data-testid="stToolbar"]');
        
        if (!toolbar) {
            return false;
        }
        
        // Obtener todos los hijos directos
        const children = Array.from(toolbar.children);
        
        // Ocultar todos excepto el primero
        children.forEach((child, index) => {
            if (index > 0) {
                child.style.display = 'none';
                child.style.visibility = 'hidden';
                child.style.opacity = '0';
            }
        });
        
        return true;
    }
    
    // Ejecutar múltiples veces para asegurar que funcione
    setTimeout(hideToolbarElements, 100);
    setTimeout(hideToolbarElements, 500);
    setTimeout(hideToolbarElements, 1000);
    setTimeout(hideToolbarElements, 2000);
    
    // Observador para cambios en el DOM
    const observer = new MutationObserver(hideToolbarElements);
    
    setTimeout(() => {
        const doc = window.parent.document || document;
        observer.observe(doc.body, { childList: true, subtree: true });
    }, 100);
})();
</script>
""", unsafe_allow_html=True)

# Indicador flotante amarillo sobre el botón de sidebar
st.markdown("""
<div style="position: fixed; top: 5px; left: 10px; z-index: 9999; 
            font-size: 2.5rem; color: #FFCC00; font-weight: bold;
            text-shadow: 0 0 15px #FFCC00, 0 0 25px #FFCC00;
            animation: pulse-indicator 2s ease-in-out infinite;
            pointer-events: none;">
    »
</div>
<style>
@keyframes pulse-indicator {
    0%, 100% { 
        opacity: 1;
        transform: scale(1);
    }
    50% { 
        opacity: 0.6;
        transform: scale(1.1);
    }
}
</style>
""", unsafe_allow_html=True)

# CSS completo para toda la aplicación
st.markdown("""
<style>
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
        max-width: 400px;
        width: 100%;
        height: auto;
        box-shadow: 0 8px 25px rgba(255,204,0,0.4);
        transition: transform 0.3s ease;
        object-fit: contain;
    }
    
    .logo-img:hover {
        transform: scale(1.02);
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
    
    /* Attractive button styles for external links */
    .attractive-button {
        background: linear-gradient(135deg, #FFCC00 0%, #FFD700 50%, #FFF2A6 100%);
        padding: 2rem 3rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(255,204,0,0.4);
        border: 3px solid #FFD700;
        transition: all 0.3s ease;
        cursor: pointer;
        max-width: 600px;
        margin: 0 auto;
        display: block;
    }
    
    .attractive-button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 35px rgba(255,204,0,0.6);
        border-color: #FFCC00;
    }
    
    /* Professional About Section */
    .professional-header {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        border-left: 5px solid #FFCC00;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .professional-header h2 {
        color: #333;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 0;
    }
    
    /* Contact Section */
    .contact-section {
        background: linear-gradient(135deg, #FFCC00 0%, #FFE066 50%, #FFF2A6 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .contact-title {
        color: #000;
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .contact-description {
        color: #333;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    .contact-icons {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2rem;
        flex-wrap: wrap;
        margin: 2rem 0;
    }
    
    .contact-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 100px;
        height: 100px;
        border-radius: 50%;
        text-decoration: none;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        font-size: 3rem;
        color: white;
    }
    
    .contact-icon:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 12px 30px rgba(0,0,0,0.4);
        text-decoration: none;
        color: white;
    }
    
    .contact-icon.whatsapp {
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
    }
    
    .contact-icon.email {
        background: linear-gradient(135deg, #EA4335 0%, #D33B2C 100%);
    }
    
    .contact-icon.facebook {
        background: linear-gradient(135deg, #1877F2 0%, #0C63D4 100%);
    }
    
    .contact-icon.instagram {
        background: linear-gradient(135deg, #E4405F 0%, #C13584 100%);
    }
    
    .contact-icon.website {
        background: linear-gradient(135deg, #FFCC00 0%, #FFD700 100%);
        color: #000000;
    }
    
    /* Enhanced sidebar styling for premium experience */
    .css-1d391kg, .stSidebar > div:first-child {
        background: linear-gradient(180deg, #1a1a1a 0%, #000000 100%);
        border-right: 3px solid #FFCC00;
        box-shadow: 3px 0 15px rgba(255,204,0,0.2);
        padding-top: 0.5rem !important;
    }
    
    /* Compact sidebar separators */
    .css-1d391kg hr {
        margin: 0.5rem 0 !important;
        border-color: #FFCC00;
        opacity: 0.3;
    }
    
    /* Reduce spacing in sidebar markdown elements */
    .css-1d391kg .stMarkdown {
        margin-bottom: 0.5rem !important;
    }
    
    /* Sidebar content styling */
    .css-1d391kg .stMarkdown h3 {
        color: #FFCC00;
        font-size: 1.2rem;
        font-weight: bold;
        text-shadow: 1px 1px 3px rgba(255,204,0,0.5);
        border-bottom: 2px solid #FFCC00;
        padding-bottom: 0.3rem;
        margin-bottom: 0.8rem;
        text-align: center;
    }
    
    /* Special styling for professional section title */
    .css-1d391kg .stMarkdown h3:first-of-type {
        color: #FFD700;
        font-size: 1.1rem;
        background: rgba(255,204,0,0.1);
        padding: 0.6rem;
        border-radius: 8px;
        border: 2px solid #FFCC00;
        margin-bottom: 1rem;
    }
    
    /* Enhanced sidebar buttons */
    .css-1d391kg .stButton > button {
        background: linear-gradient(135deg, #FFCC00 0%, #FFD700 100%);
        color: #000000;
        border: 2px solid #FFCC00;
        border-radius: 12px;
        font-weight: bold;
        font-size: 1rem;
        padding: 0.5rem 1rem;
        margin: 0.2rem 0;
        box-shadow: 0 4px 12px rgba(255,204,0,0.3);
        transition: all 0.3s ease;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .css-1d391kg .stButton > button:hover {
        background: linear-gradient(135deg, #FFD700 0%, #FFCC00 100%);
        transform: translateY(-2px) scale(1.03);
        box-shadow: 0 8px 20px rgba(255,204,0,0.5);
        border-color: #FFD700;
    }
    
    /* ========================================================================== */
    /* ENHANCED MOBILE RESPONSIVE STYLES FOR PERFECT MOBILE EXPERIENCE */
    /* ========================================================================== */
    
    /* ========================================================================== */
    /* MOBILE FIXES FOR SPECIFIC ISSUES - ADDED FOR ISSUE RESOLUTION */
    /* ========================================================================== */
    
    /* Global responsive image styling */
    img {
        max-width: 100% !important;
        height: auto !important;
        object-fit: contain !important;
        display: block;
    }
    
    /* Enhanced logo responsiveness */
    .logo-img {
        max-width: 100% !important;
        width: auto !important;
        height: auto !important;
        object-fit: contain !important;
    }
    
    /* MOBILE FIX: Professional images always responsive */
    /* Ensures all images in professional section are properly responsive */
    .professional-images img, 
    .stImage img, 
    [data-testid="stImage"] img,
    img {
        max-width: 100% !important;
        height: auto !important;
        object-fit: contain !important;
        border-radius: 15px;
    }
    
    /* Ensure text wrapping for long content */
    * {
        word-wrap: break-word !important;
        word-break: break-word !important;
        overflow-wrap: break-word !important;
    }
    
    /* Mobile First Approach - Tablet and Mobile */
    @media (max-width: 768px) {
        /* Force column stacking */
        .stColumns {
            flex-direction: column !important;
            gap: 1rem !important;
        }
        
        .stColumn {
            width: 100% !important;
            max-width: 100% !important;
            margin-bottom: 1rem !important;
            padding: 0 0.5rem !important;
        }
        
        /* Header responsive adjustments */
        .main-header {
            padding: 1.5rem 1rem !important;
            margin-bottom: 1rem !important;
            border-radius: 10px !important;
        }
        
        .main-header h1 {
            font-size: 2rem !important;
            line-height: 1.2 !important;
        }
        
        .main-header p {
            font-size: 1rem !important;
            line-height: 1.4 !important;
        }
        
        /* Professional header responsive */
        .professional-header {
            padding: 1.5rem 1rem !important;
            margin-bottom: 1.5rem !important;
        }
        
        .professional-header h2 {
            font-size: 1.5rem !important;
            line-height: 1.3 !important;
        }
        
        /* Contact section responsive */
        .contact-section {
            padding: 1.5rem 1rem !important;
            margin: 1.5rem 0.5rem !important;
        }
        
        .contact-title {
            font-size: 1.5rem !important;
        }
        
        .contact-description {
            font-size: 1rem !important;
            margin-bottom: 1.5rem !important;
        }
        
        .contact-icons {
            gap: 1rem !important;
            flex-wrap: wrap !important;
            justify-content: center !important;
        }
        
        .contact-icon {
            width: 80px !important;
            height: 80px !important;
            font-size: 2.2rem !important;
            margin: 0.5rem !important;
        }
        
        /* Button responsive adjustments */
        .attractive-button {
            padding: 1.5rem 1rem !important;
            margin: 1.5rem 0.5rem !important;
            max-width: calc(100% - 1rem) !important;
            border-radius: 15px !important;
        }
        
        .attractive-button h2 {
            font-size: 1.4rem !important;
            line-height: 1.3 !important;
        }
        
        .attractive-button p {
            font-size: 1rem !important;
            line-height: 1.4 !important;
        }
        
        /* Cards and sections responsive */
        .corporate-section, .questionnaire-container, .metric-card {
            padding: 1rem !important;
            margin: 0.5rem 0 !important;
            border-radius: 10px !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
        }
        
        .professional-profile {
            padding: 1.5rem 1rem !important;
            margin: 1rem 0 !important;
        }
        
        .results-container {
            padding: 1.5rem 1rem !important;
            margin: 1rem 0 !important;
        }
        
        /* Logo container responsive */
        .logo-container {
            padding: 1.5rem 1rem !important;
            margin-bottom: 1.5rem !important;
        }
        
        /* Sidebar responsive */
        .css-1d391kg .stButton > button {
            font-size: 0.9rem !important;
            padding: 0.6rem 1rem !important;
            width: 100% !important;
            margin: 0.2rem 0 !important;
        }
        
        .css-1d391kg .stMarkdown h3 {
            font-size: 1.1rem !important;
            text-align: center !important;
        }
        
        /* Enhanced sidebar for mobile */
        .css-1d391kg, .stSidebar > div:first-child {
            padding: 0.5rem !important;
        }
        
        /* Achievement badges responsive */
        .achievement-badge {
            font-size: 0.8rem !important;
            padding: 0.4rem 0.8rem !important;
            margin: 0.2rem !important;
            display: inline-block !important;
        }
    }
    
    /* Mobile Phone Specific - Extra Small Screens */
    @media (max-width: 480px) {
        /* Header ultra-mobile adjustments */
        .main-header {
            padding: 1rem 0.5rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        .main-header h1 {
            font-size: 1.6rem !important;
        }
        
        .main-header p {
            font-size: 0.9rem !important;
        }
        
        /* Professional header ultra-mobile */
        .professional-header {
            padding: 1rem 0.5rem !important;
        }
        
        .professional-header h2 {
            font-size: 1.3rem !important;
        }
        
        /* Contact section ultra-mobile */
        .contact-section {
            padding: 1rem 0.5rem !important;
            margin: 1rem 0.25rem !important;
        }
        
        .contact-title {
            font-size: 1.3rem !important;
        }
        
        .contact-description {
            font-size: 0.9rem !important;
        }
        
        .contact-icon {
            width: 70px !important;
            height: 70px !important;
            font-size: 2rem !important;
        }
        
        .contact-icons {
            gap: 0.8rem !important;
        }
        
        /* Button ultra-mobile adjustments */
        .attractive-button {
            padding: 1rem 0.8rem !important;
            margin: 1rem 0.25rem !important;
            max-width: calc(100% - 0.5rem) !important;
        }
        
        .attractive-button h2 {
            font-size: 1.2rem !important;
        }
        
        .attractive-button p {
            font-size: 0.9rem !important;
        }
        
        /* Cards ultra-mobile */
        .corporate-section, .questionnaire-container, .metric-card {
            padding: 0.8rem 0.6rem !important;
            margin: 0.3rem 0 !important;
        }
        
        .professional-profile {
            padding: 1rem 0.8rem !important;
        }
        
        .results-container {
            padding: 1rem 0.8rem !important;
        }
        
        /* Logo container ultra-mobile */
        .logo-container {
            padding: 1rem 0.5rem !important;
        }
        
        /* Sidebar ultra-mobile */
        .css-1d391kg .stButton > button {
            font-size: 0.8rem !important;
            padding: 0.5rem 0.8rem !important;
        }
        
        .css-1d391kg .stMarkdown h3 {
            font-size: 1rem !important;
        }
        
        /* Achievement badges ultra-mobile */
        .achievement-badge {
            font-size: 0.7rem !important;
            padding: 0.3rem 0.6rem !important;
        }
        
        /* Column adjustments for ultra-mobile */
        .stColumn {
            padding: 0 0.25rem !important;
        }
    }
    
    /* High contrast mode for better visibility */
    @media (prefers-contrast: high) {
        .css-1d391kg .stButton > button {
            border-width: 3px !important;
            font-weight: 900 !important;
        }
        
        .css-1d391kg .stMarkdown h3 {
            text-shadow: 2px 2px 4px rgba(255,204,0,0.8) !important;
        }
        
        .attractive-button {
            border-width: 4px !important;
            box-shadow: 0 10px 30px rgba(255,204,0,0.6) !important;
        }
    }
    
    /* ========================================================================== */
    /* COMPREHENSIVE MOBILE RESPONSIVENESS BLOCK - FINAL OPTIMIZATIONS */
    /* ========================================================================== */
    
    /* Universal mobile responsiveness reset */
    @media screen and (max-width: 768px) {
        /* Prevent horizontal overflow */
        body, html, .stApp {
            overflow-x: hidden !important;
            max-width: 100vw !important;
        }
        
        /* Universal container responsiveness */
        .main .block-container {
            padding: 1rem 0.5rem !important;
            max-width: 100% !important;
        }
        
        /* Universal image responsiveness with object-fit */
        img, .stImage > div > img {
            max-width: 100% !important;
            width: auto !important;
            height: auto !important;
            object-fit: contain !important;
            border-radius: 10px !important;
        }
        
        /* Force all columns to stack vertically */
        [data-testid="column"] {
            width: 100% !important;
            min-width: 100% !important;
            flex: none !important;
            margin-bottom: 1rem !important;
        }
        
        /* Prevent button and card overflow */
        .stButton, .stSelectbox, .stTextInput, .stNumberInput {
            width: 100% !important;
            max-width: 100% !important;
        }
        
        .stButton > button {
            width: 100% !important;
            max-width: 100% !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }
        
        /* Universal text wrapping */
        p, span, div, h1, h2, h3, h4, h5, h6 {
            word-wrap: break-word !important;
            word-break: break-word !important;
            overflow-wrap: break-word !important;
            hyphens: auto !important;
        }
        
        /* Responsive spacing */
        .stMarkdown {
            padding: 0 0.5rem !important;
        }
        
        /* Mobile form elements */
        .stForm {
            padding: 1rem 0.5rem !important;
        }
        
        /* Mobile metrics */
        [data-testid="metric-container"] {
            padding: 0.5rem !important;
            margin: 0.25rem 0 !important;
        }
        
        /* Mobile tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.5rem !important;
            font-size: 0.9rem !important;
        }
    }
    
    /* Extra small mobile devices */
    @media screen and (max-width: 480px) {
        .main .block-container {
            padding: 0.5rem 0.25rem !important;
        }
        
        [data-testid="column"] {
            margin-bottom: 0.5rem !important;
        }
        
        .stMarkdown {
            padding: 0 0.25rem !important;
        }
        
        .stForm {
            padding: 0.8rem 0.25rem !important;
        }
        
        [data-testid="metric-container"] {
            padding: 0.3rem !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.3rem !important;
            font-size: 0.8rem !important;
        }
    }
    
    /* Landscape mobile optimization */
    @media screen and (max-height: 500px) and (orientation: landscape) {
        .main-header {
            padding: 0.8rem !important;
        }
        
        .main-header h1 {
            font-size: 1.4rem !important;
        }
        
        .corporate-section, .questionnaire-container, .metric-card {
            padding: 0.6rem !important;
        }
    }
    
    /* ========================================================================== */
    /* PROFESSIONAL BANNER STYLES */
    /* ========================================================================== */
    
    .professional-banner {
        background: linear-gradient(135deg, #FFCC00 0%, #FFD700 50%, #FFF2A6 100%);
        padding: 1.5rem 2rem;
        border-radius: 15px;
        margin: 1rem 0 2rem 0;
        border: 2px solid #FFD700;
        box-shadow: 0 6px 20px rgba(255,204,0,0.4);
        text-align: center;
        color: #000;
        font-weight: 500;
        animation: subtle-pulse 3s ease-in-out infinite;
    }
    
    .professional-banner h4 {
        color: #000;
        margin: 0 0 0.5rem 0;
        font-size: 1.3rem;
        font-weight: bold;
    }
    
    .professional-banner p {
        color: #333;
        margin: 0;
        font-size: 1.1rem;
        line-height: 1.5;
    }
    
    .sidebar-icon {
        font-size: 1.4rem;
        font-weight: bold;
        color: #FFCC00;
        background: #000000;
        padding: 0.2rem 0.5rem;
        border-radius: 8px;
        display: inline-block;
        margin: 0 0.3rem;
    }
    
    /* Show/hide instructions based on device */
    .desktop-instruction {
        display: inline;
    }
    
    .mobile-instruction {
        display: none;
    }
    
    @keyframes subtle-pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    /* Mobile responsive banner */
    @media (max-width: 768px) {
        .professional-banner {
            padding: 1rem 1.5rem;
            margin: 0.5rem 0 1.5rem 0;
            border-radius: 12px;
        }
        
        .professional-banner h4 {
            font-size: 1.1rem;
        }
        
        .professional-banner p {
            font-size: 1rem;
        }
        
        .sidebar-icon {
            font-size: 1.2rem;
        }
        
        /* Switch instructions for mobile */
        .desktop-instruction {
            display: none;
        }
        
        .mobile-instruction {
            display: inline;
        }
        
        .sidebar-icon-mobile {
            font-size: 1.4rem;
            animation: gentle-glow 1.5s ease-in-out infinite alternate;
        }
    }
    
    @media (max-width: 480px) {
        .professional-banner {
            padding: 0.8rem 1rem;
            margin: 0.5rem 0 1rem 0;
        }
        
        .professional-banner h4 {
            font-size: 1rem;
        }
        
        .professional-banner p {
            font-size: 0.9rem;
            line-height: 1.4;
        }
    }
    
    /* ========================================================================== */
    /* HOW TO GET YOUR PLAN BLOCK STYLES */
    /* ========================================================================== */
    
    .how-to-get-plan-container {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin: 2.5rem 0;
        border: 3px solid #FFCC00;
        box-shadow: 0 8px 25px rgba(255,204,0,0.3);
    }
    
    .how-to-get-plan-title {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    
    .how-to-get-plan-title h2 {
        color: #FFCC00;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(255,204,0,0.3);
    }
    
    .how-to-get-plan-title p {
        color: #FFFFFF;
        font-size: 1.2rem;
        margin: 0;
        font-weight: 400;
    }
    
    .steps-container {
        display: flex;
        justify-content: space-between;
        gap: 2rem;
        margin-top: 2rem;
    }
    
    .step-card {
        flex: 1;
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
        padding: 2rem 1.5rem;
        border-radius: 15px;
        border: 2px solid #FFCC00;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255,204,0,0.2);
    }
    
    .step-card:hover {
        transform: translateY(-5px);
        border-color: #FFD700;
        box-shadow: 0 8px 25px rgba(255,204,0,0.4);
    }
    
    .step-number {
        background: linear-gradient(135deg, #FFCC00 0%, #FFD700 100%);
        color: #000;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        font-weight: bold;
        margin: 0 auto 1.5rem auto;
        box-shadow: 0 4px 12px rgba(255,204,0,0.5);
    }
    
    .step-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .step-card h3 {
        color: #FFCC00;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    
    .step-card p {
        color: #FFFFFF;
        font-size: 1.1rem;
        line-height: 1.6;
        margin: 0;
    }
    
    /* Responsive design for steps */
    @media (max-width: 768px) {
        .steps-container {
            flex-direction: column;
            gap: 1.5rem;
        }
        
        .how-to-get-plan-container {
            padding: 2rem 1.5rem;
        }
        
        .how-to-get-plan-title h2 {
            font-size: 2rem;
        }
        
        .step-card {
            padding: 1.5rem 1rem;
        }
        
        .step-number {
            width: 50px;
            height: 50px;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .step-icon {
            font-size: 2.5rem;
        }
        
        .step-card h3 {
            font-size: 1.3rem;
        }
        
        .step-card p {
            font-size: 1rem;
        }
    }
    
    @media (max-width: 480px) {
        .how-to-get-plan-container {
            padding: 1.5rem 1rem;
            margin: 1.5rem 0;
        }
        
        .how-to-get-plan-title h2 {
            font-size: 1.6rem;
        }
        
        .how-to-get-plan-title p {
            font-size: 1rem;
        }
        
        .step-card {
            padding: 1.2rem 0.8rem;
        }
        
        .step-number {
            width: 45px;
            height: 45px;
            font-size: 1.3rem;
        }
        
        .step-icon {
            font-size: 2rem;
        }
        
        .step-card h3 {
            font-size: 1.2rem;
        }
        
        .step-card p {
            font-size: 0.95rem;
        }
    }
    
    /* ========================================================================== */
    /* INFORMATIVE BANNER STYLES (HOME PAGE ONLY) */
    /* ========================================================================== */
    
    .informative-banner {
        background: linear-gradient(135deg, #74b9ff 0%, #a29bfe 50%, #6c5ce7 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin: 1rem 0 2rem 0;
        border: 2px solid #0984e3;
        box-shadow: 0 4px 15px rgba(116, 185, 255, 0.3);
        text-align: center;
        color: white;
        font-weight: 500;
        position: relative;
    }
    
    .informative-banner p {
        color: #ffffff;
        margin: 0;
        font-size: 1.1rem;
        line-height: 1.6;
        font-weight: 500;
    }
    
    /* Mobile responsive informative banner */
    @media (max-width: 768px) {
        .informative-banner {
            padding: 1rem 1.5rem;
            margin: 0.5rem 0 1.5rem 0;
            border-radius: 10px;
        }
        
        .informative-banner p {
            font-size: 1rem;
            line-height: 1.5;
        }
    }
    
    @media (max-width: 480px) {
        .informative-banner {
            padding: 0.8rem 1rem;
            margin: 0.5rem 0 1rem 0;
        }
        
        .informative-banner p {
            font-size: 0.9rem;
            line-height: 1.4;
        }
    }
    
    /* ========================================================================== */
    /* FLOATING SIDEBAR LABEL (HOME PAGE ONLY) */
    /* ========================================================================== */
    
    .floating-sidebar-label {
        position: fixed;
        top: 15px;
        left: 60px;
        background: linear-gradient(135deg, #FFCC00 0%, #FFD700 100%);
        color: #000;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(255,204,0,0.6);
        z-index: 1000;
        animation: floating-bounce 2s ease-in-out infinite;
        border: 2px solid #000;
        pointer-events: none;
        white-space: nowrap;
    }
    
    .floating-sidebar-label::before {
        content: '';
        position: absolute;
        left: -8px;
        top: 50%;
        transform: translateY(-50%);
        border: 8px solid transparent;
        border-right-color: #FFCC00;
    }
    
    @keyframes floating-bounce {
        0%, 100% { 
            transform: translateY(0px) scale(1);
            box-shadow: 0 4px 15px rgba(255,204,0,0.6);
        }
        50% { 
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 8px 25px rgba(255,204,0,0.8);
        }
    }
    
    /* Mobile responsive floating label */
    @media (max-width: 768px) {
        .floating-sidebar-label {
            top: 12px;
            left: 55px;
            padding: 0.4rem 0.8rem;
            font-size: 0.8rem;
            border-radius: 15px;
        }
        
        .floating-sidebar-label::before {
            left: -6px;
            border-width: 6px;
        }
    }
    
    @media (max-width: 480px) {
        .floating-sidebar-label {
            top: 10px;
            left: 50px;
            padding: 0.3rem 0.6rem;
            font-size: 0.75rem;
            border-radius: 12px;
        }
        
        .floating-sidebar-label::before {
            left: -5px;
            border-width: 5px;
        }
    }
    
    /* ========================================================================== */
    /* IMPROVED "BIENVENIDO A MUPAI" TITLE STYLES */
    /* ========================================================================== */
    
    .welcome-title-container {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem auto;
        border: 2px solid #FFCC00;
        box-shadow: 0 4px 15px rgba(255,204,0,0.3);
        max-width: 1200px;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .welcome-title-container h1 {
        color: #FFCC00;
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(255,204,0,0.5);
        text-align: center;
        line-height: 1.2;
        width: 100%;
    }
    
    .welcome-title-container h2 {
        color: #FFFFFF;
        font-size: 1.8rem;
        margin-bottom: 2rem;
        font-weight: 500;
        text-align: center;
        line-height: 1.4;
        width: 100%;
    }
    
    .welcome-title-container p {
        color: #FFFFFF;
        font-size: 1.3rem;
        line-height: 1.6;
        max-width: 900px;
        margin: 0 auto;
        text-align: center;
        width: 100%;
    }
    
    /* Mobile responsive welcome title */
    @media (max-width: 768px) {
        .welcome-title-container {
            padding: 2rem 1.5rem;
            margin: 1.5rem auto;
            border-radius: 15px;
        }
        
        .welcome-title-container h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        
        .welcome-title-container h2 {
            font-size: 1.4rem;
            margin-bottom: 1.5rem;
        }
        
        .welcome-title-container p {
            font-size: 1.1rem;
            line-height: 1.5;
        }
    }
    
    @media (max-width: 480px) {
        .welcome-title-container {
            padding: 1.5rem 1rem;
            margin: 1rem auto;
            border-radius: 12px;
        }
        
        .welcome-title-container h1 {
            font-size: 2rem;
            margin-bottom: 0.8rem;
            line-height: 1.1;
        }
        
        .welcome-title-container h2 {
            font-size: 1.2rem;
            margin-bottom: 1rem;
        }
        
        .welcome-title-container p {
            font-size: 1rem;
            line-height: 1.4;
        }
    }
    
    /* Ensure proper centering on all devices */
    @media (max-width: 320px) {
        .welcome-title-container {
            padding: 1rem 0.8rem;
        }
        
        .welcome-title-container h1 {
            font-size: 1.8rem;
        }
        
        .welcome-title-container h2 {
            font-size: 1.1rem;
        }
        
        .welcome-title-container p {
            font-size: 0.9rem;
        }
    }

    /* ========================================================================== */
    /* MOBILE FIXES FOR SPECIFIC ISSUES - TARGETED SOLUTIONS */
    /* ========================================================================== */
    
    /* MOBILE FIX 1: Black and Yellow Contact Tags - Adaptive styling */
    @media (max-width: 768px) {
        /* Contact section black and yellow tags - Email and WhatsApp */
        div[style*="background: #000; color: #FFCC00"] {
            max-width: 90% !important;
            padding: 1rem !important;
            font-size: 1rem !important;
            margin: 0 auto !important;
            text-align: center !important;
            border-radius: 10px !important;
        }
        
        /* Contact information sections */
        div[style*="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)"] {
            padding: 1.5rem 1rem !important;
            margin: 1rem 0.5rem !important;
        }
    }
    
    /* MOBILE FIX 2: Service Policy Grid - Single Column Layout */
    @media (max-width: 768px) {
        /* Service Policy 6-box grid - Force single column */
        div[style*="display: grid; grid-template-columns: 1fr 1fr"] {
            display: grid !important;
            grid-template-columns: 1fr !important;
            gap: 1rem !important;
            margin-top: 1rem !important;
        }
        
        /* Individual policy boxes - Reduced padding and margins */
        div[style*="background: rgba(255,204,0,0.1); padding: 2rem"] {
            padding: 1rem !important;
            margin-bottom: 1rem !important;
            border-radius: 10px !important;
        }
        
        /* Policy box headings */
        div[style*="background: rgba(255,204,0,0.1)"] h4 {
            font-size: 1.1rem !important;
            margin-bottom: 0.8rem !important;
        }
        
        /* Policy box content */
        div[style*="background: rgba(255,204,0,0.1)"] p {
            font-size: 0.95rem !important;
            line-height: 1.5 !important;
        }
    }
    
    /* MOBILE FIX 3: Contact Icons - Improved spacing and sizing */
    @media (max-width: 768px) {
        .contact-icons {
            gap: 1rem !important;
            padding: 1rem 0.5rem !important;
        }
        
        .contact-icon {
            width: 70px !important;
            height: 70px !important;
            font-size: 2rem !important;
            margin: 0.5rem !important;
        }
        
        /* Contact section title and description */
        .contact-title {
            font-size: 1.4rem !important;
            margin-bottom: 1rem !important;
        }
        
        .contact-description {
            font-size: 1rem !important;
            margin-bottom: 1.5rem !important;
        }
    }
    
    /* MOBILE FIX 4: Ultra-small mobile devices (480px and below) */
    @media (max-width: 480px) {
        /* Contact tags - Even more compact */
        div[style*="background: #000; color: #FFCC00"] {
            font-size: 0.9rem !important;
            padding: 0.8rem !important;
            line-height: 1.4 !important;
        }
        
        /* Policy boxes - Ultra compact */
        div[style*="background: rgba(255,204,0,0.1); padding: 2rem"] {
            padding: 0.8rem !important;
        }
        
        /* Policy headings - Smaller text */
        div[style*="background: rgba(255,204,0,0.1)"] h4 {
            font-size: 1rem !important;
        }
        
        /* Contact icons - Smaller for tiny screens */
        .contact-icon {
            width: 60px !important;
            height: 60px !important;
            font-size: 1.8rem !important;
        }
        
        /* Add small top margin to main content to account for sticky header */
        .stApp > div:first-child {
            padding-top: 0.5rem !important;
        }
    }
</style>  
""", unsafe_allow_html=True)


def mostrar_banner_profesional():
    """
    Displays a professional banner encouraging users to access the sidebar menu.
    Visible on all pages and devices.
    """
    st.markdown("""
    <div class="professional-banner">
        <h4>👉 ¡Descubre Todo el Contenido de MUPAI!</h4>
        <p>
            Haz clic en el ícono <span class="sidebar-icon">>></span> en la esquina superior izquierda 
            para desplegar el menú lateral y acceder a todo el contenido y menús detallados de MUPAI.
        </p>
    </div>
    """, unsafe_allow_html=True)


def mostrar_banner_informativo():
    """
    Displays an informative banner only on the home page with overview and sidebar instructions.
    """
    st.markdown("""
    <div class="professional-banner">
        <p>
            Esta página te muestra un overview general de MUPAI y nuestros servicios principales. 
            Si quieres conocer más detalles, despliega la barra lateral (haz clic en <span class="sidebar-icon">>></span> arriba a la izquierda) 
            y elige el apartado que quieras conocer a fondo.
        </p>
    </div>
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
    """Función simulada de envío de email"""
    st.success("✅ Email enviado exitosamente")
    return True

# Inicializar session state con soporte para query parameters
if 'page' not in st.session_state:
    # Leer el parámetro 'page' de la URL si existe
    query_params = st.query_params
    page_from_url = query_params.get("page", "inicio")
    
    # Validar que la página existe
    valid_pages = [
        "inicio", "planes_costos", "protocolos_medicion", "mupcamp_1a1", 
        "quienes_somos", "about", "contacto", "body_and_energy", 
        "food_preferences", "designing_training"
    ]
    
    if page_from_url in valid_pages:
        st.session_state.page = page_from_url
    else:
        st.session_state.page = "inicio"

# Navegación principal - reorganizada según requerimientos
st.sidebar.markdown("### 📋 NAVEGACIÓN")

if st.sidebar.button("🏠 Inicio", use_container_width=True):
    st.session_state.page = "inicio"
    st.query_params.clear()

if st.sidebar.button("💸 Planes y Costos", use_container_width=True):
    st.session_state.page = "planes_costos"
    st.query_params["page"] = "planes_costos"

# botón nuevo: Protocolos de medición MUPAI (colocar justo debajo de "💸 Planes y Costos")
if st.sidebar.button("📐 Protocolos de medición MUPAI", use_container_width=True):
    st.session_state.page = "protocolos_medicion"
    st.query_params["page"] = "protocolos_medicion"

if st.sidebar.button("🔴 MUPcamp 1:1", use_container_width=True):
    st.session_state.page = "mupcamp_1a1"
    st.query_params["page"] = "mupcamp_1a1"

if st.sidebar.button("🏢 ¿Quiénes somos?", use_container_width=True):
    st.session_state.page = "quienes_somos"
    st.query_params["page"] = "quienes_somos"

st.sidebar.markdown("---")
st.sidebar.markdown("### 👨‍🎓 SOBRE EL PROFESIONAL Y CONTACTO")

if st.sidebar.button("👨‍🎓 Acerca del Profesional", use_container_width=True):
    st.session_state.page = "about"
    st.query_params["page"] = "about"

if st.sidebar.button("📞 Contacto", use_container_width=True):
    st.session_state.page = "contacto"
    st.query_params["page"] = "contacto"

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧪 TEST MUPAI")

if st.sidebar.button("BODY AND ENERGY", use_container_width=True):
    st.session_state.page = "body_and_energy"
    st.query_params["page"] = "body_and_energy"

if st.sidebar.button("FOOD PREFERENCES", use_container_width=True):
    st.session_state.page = "food_preferences"
    st.query_params["page"] = "food_preferences"

if st.sidebar.button("DESIGNING YOUR TRAINING", use_container_width=True):
    st.session_state.page = "designing_training"
    st.query_params["page"] = "designing_training"

st.sidebar.markdown("---")

# ==================== PÁGINA DE INICIO ====================
if st.session_state.page == "inicio":
    # Floating sidebar label - only on home page
    st.markdown("""
    <div class="floating-sidebar-label">
        👈 ¡Haz clic aquí!
    </div>
    """, unsafe_allow_html=True)
    
    # Logo grande y centrado sin marco circular
    logo_base64 = load_logo_image_base64()
    if logo_base64:
        st.markdown(f"""
        <div class="logo-container">
            <img src="{logo_base64}" class="logo-img" alt="MUPAI Logo">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="logo-container">
            <div style="padding: 30px; background-color: #333; border: 2px solid #FFCC00; border-radius: 15px; text-align: center;">
                <h1 style="color: #FFCC00; margin: 0; font-size: 4rem;">💪 MUPAI</h1>
                <p style="color: #FFFFFF; margin: 10px 0 0 0; font-size: 1.5rem;">Muscle Up AI</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Informative banner - only on home page, replacing professional banner
    mostrar_banner_informativo()
    
    # Título de bienvenida - improved styling and alignment
    st.markdown("""
    <div class="welcome-title-container">
        <h1>🎯 Bienvenido a MUPAI</h1>
        <h2>Tu Transformación Física Basada en Ciencia e Inteligencia Artificial</h2>
        <p>
            <strong>MUPAI</strong> revoluciona el entrenamiento digital combinando 
            <strong style="color: #FFCC00;">ciencias del ejercicio actualizada</strong>, 
            <strong style="color: #FFCC00;">inteligencia artificial</strong> y 
            <strong style="color: #FFCC00;">personalización optimizada</strong> para 
            llevarte a tu máximo potencial físico de manera segura, efectiva y sostenible.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sección del profesional/encargado
    st.markdown("""
    <div class="section-header">
        <h2>👨‍🎓 Nuestro Profesional Especializado</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="professional-profile">
            <h3 style="color: #FFCC00; font-size: 2rem; margin-bottom: 1rem;">
                🏆 Coach Erick - MUPAI Training
            </h3>
            <p style="color: #FFFFFF; font-size: 1.2rem; line-height: 1.8; margin-bottom: 1.5rem;">
                <strong>Especialista en Entrenamiento de Fuerza, Acondicionamiento, Ganancia de Masa Muscular y Pérdida de Grasa 
                Basado en Ciencias del Ejercicio y la Salud.</strong><br>
                Especialista en fisiología del ejercicio y nutrición deportiva avanzada.
            </p>
            <div style="margin-bottom: 1.5rem;">
                <div class="achievement-badge">🎯 +5 años experiencia</div>
                <div class="achievement-badge">🔬 Ciencias del Ejercicio</div>
                <div class="achievement-badge">🥇 Nutrición Deportiva</div>
                <div class="achievement-badge">🤖 IA Aplicada</div>
            </div>
            <p style="color: #FFFFFF; font-size: 1.1rem; line-height: 1.6;">
                Experto en transformación corporal mediante metodologías científicas avanzadas, 
                especializado en <strong style="color: #FFCC00;">balance energético inteligente</strong> 
                y <strong style="color: #FFCC00;">asignación de macronutrientes personalizada</strong>. 
                Pionero en la aplicación de IA para optimización de resultados físicos.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Aquí se muestran las imágenes del profesional
        st.image("Copia de Anfitrión_20250809_125513_0000.png", caption="Coach Erick - Especialista MUPAI", use_container_width=True)

    # Plans notice - directing to sidebar menu
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFD700 0%, #FFCC00 50%, #FFF2A6 100%); 
                padding: 2rem; border-radius: 15px; margin: 2rem 0; 
                border: 3px solid #FFCC00; box-shadow: 0 6px 20px rgba(255,204,0,0.4);
                text-align: center; color: #000;">
        <h3 style="color: #000; font-size: 1.6rem; margin-bottom: 1rem; font-weight: bold;">
            📋 ¿Quieres conocer todos los detalles y el proceso para adquirir un plan?
        </h3>
        <p style="color: #333; font-size: 1.2rem; line-height: 1.6; margin: 0; font-weight: 500;">
            Consulta el menú lateral <strong>'Planes y Costos'</strong> para ver información detallada 
            y la mecánica de adquisición paso a paso.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ==================== NUEVA SECCIÓN RESPONSIVE CON ESTILOS INLINE ====================
    # Sección completamente responsive con narrativa emocional y motivacional
    # Incluye imagen bancaria, todos los detalles de planes y mecánica de adquisición
    
    st.markdown("""
    <style>
        /* Media queries embebidas para adaptabilidad móvil */
        @media (max-width: 768px) {
            .plan-card-container {
                flex-direction: column !important;
            }
            .plan-card-item {
                width: 100% !important;
                margin-bottom: 1.5rem !important;
            }
            .steps-flex-container {
                flex-direction: column !important;
            }
            .step-item {
                width: 100% !important;
                margin-bottom: 1.5rem !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Título principal emocional y motivacional
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                padding: 3rem 2rem; border-radius: 20px; margin: 2.5rem 0; 
                border: 3px solid #FFCC00; box-shadow: 0 8px 25px rgba(255,204,0,0.4);
                text-align: center;">
        <h2 style="color: #FFCC00; font-size: 2.8rem; font-weight: bold; margin-bottom: 1rem;
                   text-shadow: 2px 2px 4px rgba(255,204,0,0.3);">
            ✨ ¿Cómo Obtener Tu Plan de Transformación?
        </h2>
        <p style="color: #FFFFFF; font-size: 1.3rem; margin: 0; font-weight: 400; line-height: 1.6;">
            🎯 Tu cambio físico comienza con una decisión. <strong style="color: #FFCC00;">Sigue estos pasos simples</strong> 
            y comienza tu viaje hacia el cuerpo que siempre has soñado, respaldado por ciencia e inteligencia artificial.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pasos con estilos inline - Paso 1
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                padding: 3rem 2rem; border-radius: 20px; margin: 2.5rem 0; 
                border: 3px solid #FFCC00; box-shadow: 0 8px 25px rgba(255,204,0,0.3);">
        <div style="display: flex; justify-content: space-between; gap: 2rem; flex-wrap: wrap;">
    """, unsafe_allow_html=True)
    
    # Using columns for better Streamlit compatibility
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%); 
                        padding: 2rem 1.5rem; border-radius: 15px; border: 2px solid #FFCC00; 
                        text-align: center; box-shadow: 0 4px 15px rgba(255,204,0,0.2); min-height: 350px;">
                <div style="background: linear-gradient(135deg, #FFCC00 0%, #FFD700 100%); 
                           color: #000; width: 60px; height: 60px; border-radius: 50%; 
                           display: flex; align-items: center; justify-content: center; 
                           font-size: 2rem; font-weight: bold; margin: 0 auto 1.5rem auto; 
                           box-shadow: 0 4px 12px rgba(255,204,0,0.5);">
                    1
                </div>
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
                <h3 style="color: #FFCC00; font-size: 1.5rem; margin-bottom: 1rem; font-weight: bold;">
                    Elige Tu Plan Ideal
                </h3>
                <p style="color: #FFFFFF; font-size: 1.1rem; line-height: 1.6; margin: 0;">
                    💪 Selecciona el plan que mejor se adapte a tus objetivos: nutrición, entrenamiento 
                    o el plan combinado para resultados óptimos y sostenibles.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%); 
                        padding: 2rem 1.5rem; border-radius: 15px; border: 2px solid #FFCC00; 
                        text-align: center; box-shadow: 0 4px 15px rgba(255,204,0,0.2); min-height: 350px;">
                <div style="background: linear-gradient(135deg, #FFCC00 0%, #FFD700 100%); 
                           color: #000; width: 60px; height: 60px; border-radius: 50%; 
                           display: flex; align-items: center; justify-content: center; 
                           font-size: 2rem; font-weight: bold; margin: 0 auto 1.5rem auto; 
                           box-shadow: 0 4px 12px rgba(255,204,0,0.5);">
                    2
                </div>
                <div style="font-size: 3rem; margin-bottom: 1rem;">💳</div>
                <h3 style="color: #FFCC00; font-size: 1.5rem; margin-bottom: 1rem; font-weight: bold;">
                    Realiza Tu Pago Seguro
                </h3>
                <p style="color: #FFFFFF; font-size: 1.1rem; line-height: 1.6; margin: 0;">
                    🔒 Efectúa la transferencia del monto exacto a nuestra cuenta bancaria. 
                    Encontrarás los datos completos más abajo. ¡Es rápido y seguro!
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%); 
                        padding: 2rem 1.5rem; border-radius: 15px; border: 2px solid #FFCC00; 
                        text-align: center; box-shadow: 0 4px 15px rgba(255,204,0,0.2); min-height: 350px;">
                <div style="background: linear-gradient(135deg, #FFCC00 0%, #FFD700 100%); 
                           color: #000; width: 60px; height: 60px; border-radius: 50%; 
                           display: flex; align-items: center; justify-content: center; 
                           font-size: 2rem; font-weight: bold; margin: 0 auto 1.5rem auto; 
                           box-shadow: 0 4px 12px rgba(255,204,0,0.5);">
                    3
                </div>
                <div style="font-size: 3rem; margin-bottom: 1rem;">🚀</div>
                <h3 style="color: #FFCC00; font-size: 1.5rem; margin-bottom: 1rem; font-weight: bold;">
                    ¡Comienza Tu Transformación!
                </h3>
                <p style="color: #FFFFFF; font-size: 1.1rem; line-height: 1.6; margin: 0;">
                    🎉 Una vez confirmado tu pago, recibirás tu plan personalizado y podrás 
                    comenzar tu transformación con el respaldo de ciencia e IA.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sección de Planes con narrativa emocional y motivacional
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFD700 0%, #FFCC00 50%, #FFF2A6 100%); 
                padding: 2.5rem 2rem; border-radius: 20px; margin: 2.5rem 0; 
                border: 3px solid #FFCC00; box-shadow: 0 8px 25px rgba(255,204,0,0.5);
                text-align: center;">
        <h2 style="color: #000; font-size: 2.5rem; font-weight: bold; margin-bottom: 1rem;">
            🚀 Nuestros Planes de Transformación Científica
        </h2>
        <p style="color: #333; font-size: 1.3rem; margin: 0; font-weight: 500; line-height: 1.6;">
            💎 Planes diseñados con ciencia actualizada para <strong>maximizar tus resultados</strong>. 
            Cada plan está personalizado según tus objetivos, preferencias y estilo de vida.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Planes detallados con estilos inline usando st.columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                    padding: 2.5rem 2rem; border-radius: 20px; border: 3px solid #FFCC00; 
                    box-shadow: 0 6px 20px rgba(255,204,0,0.3); text-align: center; 
                    min-height: 600px; display: flex; flex-direction: column;">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">🍽️</div>
            <h3 style="color: #FFCC00; font-size: 1.8rem; margin-bottom: 1rem; font-weight: bold;">
                Nutrición Personalizada
            </h3>
            <div style="background: #FFCC00; color: #000; padding: 1rem; border-radius: 10px; 
                        margin-bottom: 1.5rem; font-weight: bold; font-size: 1.4rem;">
                💰 $700 - $900 MXN
            </div>
            <div style="color: #FFFFFF; font-size: 1.05rem; line-height: 1.6; margin-bottom: 1.5rem; 
                      text-align: left; flex-grow: 1;">
                <p style="margin: 0 0 1rem 0;"><strong style="color: #FFCC00;">Duración:</strong> Ciclo de 5 semanas (4 semanas de ejecución + 1 semana de reevaluación)</p>
                <p style="margin: 0 0 1rem 0;"><strong style="color: #FFCC00;">✅ Beneficios:</strong></p>
                <ul style="margin: 0; padding-left: 1.2rem;">
                    <li>Evaluación inicial con bioimpedancia</li>
                    <li>7 menús personalizados (semana tipo)</li>
                    <li>Personalización según preferencias</li>
                    <li>Evaluación final con medición</li>
                    <li>Menús extra: <strong>Internos:</strong> desde $200 MXN / <strong>Externos:</strong> desde $400 MXN</li>
                </ul>
                <p style="margin: 1rem 0 0 0;"><strong style="color: #FFCC00;">💰 Precios:</strong></p>
                <ul style="margin: 0.5rem 0 0 0; padding-left: 1.2rem;">
                    <li><strong>Internos:</strong> $700 MXN</li>
                    <li><strong>Externos:</strong> $900 MXN</li>
                </ul>
            </div>
            <div style="background: rgba(255,204,0,0.2); padding: 1rem; border-radius: 10px;">
                <p style="color: #FFCC00; font-weight: bold; margin: 0; font-size: 1.1rem;">
                    ✨ Perfecto para optimizar tu alimentación
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                    padding: 2.5rem 2rem; border-radius: 20px; border: 3px solid #FFCC00; 
                    box-shadow: 0 6px 20px rgba(255,204,0,0.3); text-align: center; 
                    min-height: 600px; display: flex; flex-direction: column;">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">💪</div>
            <h3 style="color: #FFCC00; font-size: 1.8rem; margin-bottom: 1rem; font-weight: bold;">
                Entrenamiento Personalizado
            </h3>
            <div style="background: #FFCC00; color: #000; padding: 1rem; border-radius: 10px; 
                        margin-bottom: 1.5rem; font-weight: bold; font-size: 1.4rem;">
                💰 $950 - $1,100 MXN
            </div>
            <div style="color: #FFFFFF; font-size: 1.05rem; line-height: 1.6; margin-bottom: 1.5rem; 
                      text-align: left; flex-grow: 1;">
                <p style="margin: 0 0 1rem 0;"><strong style="color: #FFCC00;">Duración:</strong> 10 semanas</p>
                <p style="margin: 0 0 1rem 0;"><strong style="color: #FFCC00;">✅ Beneficios:</strong></p>
                <ul style="margin: 0; padding-left: 1.2rem;">
                    <li>Evaluación inicial completa</li>
                    <li>Plan personalizado volumen/intensidad</li>
                    <li>Adaptación a tu horario y nivel</li>
                    <li>Entrega profesional en PDF</li>
                    <li>Evaluación final de progresos</li>
                    <li>Progresiones incluidas</li>
                </ul>
                <p style="margin: 1rem 0 0 0;"><strong style="color: #FFCC00;">💰 Precios:</strong></p>
                <ul style="margin: 0.5rem 0 0 0; padding-left: 1.2rem;">
                    <li><strong>Internos:</strong> $950 MXN</li>
                    <li><strong>Externos:</strong> $1,100 MXN</li>
                </ul>
            </div>
            <div style="background: rgba(255,204,0,0.2); padding: 1rem; border-radius: 10px;">
                <p style="color: #FFCC00; font-weight: bold; margin: 0; font-size: 1.1rem;">
                    🔥 Ideal para maximizar tu rendimiento
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                    padding: 2.5rem 2rem; border-radius: 20px; border: 3px solid #FFD700; 
                    box-shadow: 0 6px 20px rgba(255,215,0,0.4); text-align: center; 
                    min-height: 600px; display: flex; flex-direction: column; position: relative; overflow: hidden;">
            <div style="position: absolute; top: 10px; right: -35px; background: #FFD700; 
                        color: #000; padding: 0.5rem 3rem; font-weight: bold; font-size: 0.9rem;
                        transform: rotate(45deg); box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
                🌟 POPULAR
            </div>
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">🔥</div>
            <h3 style="color: #FFD700; font-size: 1.8rem; margin-bottom: 1rem; font-weight: bold;">
                Plan Combinado
            </h3>
            <div style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); 
                        color: #000; padding: 1rem; border-radius: 10px; 
                        margin-bottom: 1.5rem; font-weight: bold; font-size: 1.4rem;">
                💰 $1,500 - $1,850 MXN
                <div style="font-size: 1rem; margin-top: 0.5rem;">💸 Ahorra $100 MXN</div>
            </div>
            <div style="color: #FFFFFF; font-size: 1.05rem; line-height: 1.6; margin-bottom: 1.5rem; 
                      text-align: left; flex-grow: 1;">
                <p style="margin: 0 0 1rem 0;"><strong style="color: #FFD700;">Duración:</strong> 10 semanas (Nutrición 5 semanas + Entrenamiento 10 semanas)</p>
                <p style="margin: 0 0 1rem 0;"><strong style="color: #FFD700;">✅ Beneficios:</strong></p>
                <ul style="margin: 0; padding-left: 1.2rem;">
                    <li>Ambos planes completos</li>
                    <li>Evaluación inicial y final completa</li>
                    <li>Integración total dieta/entrenamiento</li>
                    <li>Seguimiento coordinado</li>
                    <li><strong>Ahorro de $100 MXN</strong></li>
                </ul>
                <p style="margin: 1rem 0 0 0;"><strong style="color: #FFD700;">💰 Precios:</strong></p>
                <ul style="margin: 0.5rem 0 0 0; padding-left: 1.2rem;">
                    <li><strong>Internos:</strong> $1,500 MXN</li>
                    <li><strong>Externos:</strong> $1,850 MXN</li>
                </ul>
            </div>
            <div style="background: rgba(255,215,0,0.2); padding: 1rem; border-radius: 10px;">
                <p style="color: #FFD700; font-weight: bold; margin: 0; font-size: 1.1rem;">
                    ⭐ La solución completa más efectiva
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    
    # Información de Transferencia Bancaria con imagen
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                padding: 3rem 2rem; border-radius: 20px; margin: 2.5rem 0; 
                border: 3px solid #FFCC00; box-shadow: 0 8px 25px rgba(255,204,0,0.4);
                text-align: center;">
        <h2 style="color: #FFCC00; font-size: 2.5rem; font-weight: bold; margin-bottom: 1rem;">
            💳 Información de Transferencia Bancaria
        </h2>
        <p style="color: #FFFFFF; font-size: 1.2rem; margin-bottom: 2rem; line-height: 1.6;">
            🔒 Realiza tu transferencia segura del <strong style="color: #FFCC00;">monto exacto</strong> 
            según el plan elegido. A continuación encontrarás todos los datos necesarios.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Imagen de cuenta bancaria
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0; padding: 2rem; 
                background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%); 
                border-radius: 15px; border: 2px solid #FFCC00;">
    """ + load_banking_image_base64() + """
    </div>
    """, unsafe_allow_html=True)
    
    # Instrucciones de envío de comprobante
    st.markdown("""
    <div style="background: #fff3cd; border: 3px solid #ffc107; border-radius: 15px; 
                padding: 2rem; margin: 2rem 0; box-shadow: 0 6px 20px rgba(255,193,7,0.3);">
        <h3 style="color: #856404; margin: 0 0 1.5rem 0; font-size: 1.8rem; text-align: center;">
            📋 ¡Importante! Después de Realizar Tu Pago
        </h3>
        <p style="color: #856404; margin: 0 0 1.5rem 0; font-size: 1.2rem; line-height: 1.8; text-align: center;">
            <strong>Envía tu comprobante de pago</strong> para confirmar tu adquisición y comenzar tu transformación:
        </p>
        <div style="display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap; margin-top: 1.5rem;">
            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">📱</div>
                <p style="color: #856404; margin: 0; font-size: 1.1rem; font-weight: bold;">
                    WhatsApp/Teléfono
                </p>
                <p style="color: #000; margin: 0.5rem 0 0 0; font-size: 1.3rem; font-weight: bold;">
                    8662580594
                </p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">📧</div>
                <p style="color: #856404; margin: 0; font-size: 1.1rem; font-weight: bold;">
                    Correo Electrónico
                </p>
                <p style="color: #000; margin: 0.5rem 0 0 0; font-size: 1.3rem; font-weight: bold;">
                    administracion@muscleupgym.fitness
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mecánica de Adquisición Detallada
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                padding: 3rem 2rem; border-radius: 20px; margin: 2.5rem 0; 
                border: 3px solid #FFCC00; box-shadow: 0 8px 25px rgba(255,204,0,0.4);">
        <h2 style="color: #FFCC00; font-size: 2.5rem; font-weight: bold; margin-bottom: 1.5rem; text-align: center;">
            📝 Mecánica de Adquisición - Paso a Paso
        </h2>
        <p style="color: #FFFFFF; font-size: 1.2rem; margin-bottom: 2rem; text-align: center; line-height: 1.6;">
            🎯 Sigue este proceso completo para obtener tu plan personalizado y comenzar tu transformación física.
        </p>
        <ol style="color: #FFFFFF; font-size: 1.1rem; line-height: 2; margin: 0; padding-left: 1.5rem;">
            <li><strong style="color: #FFCC00;">Elige tu plan</strong></li>
            <li><strong style="color: #FFCC00;">Realiza el pago</strong></li>
            <li><strong style="color: #FFCC00;">Envía comprobante</strong> (WhatsApp o correo)</li>
            <li><strong style="color: #FFCC00;">Abre en la barra lateral: </strong> "Protocolo de Medición MUPAI"</li>
            <li><strong style="color: #FFCC00;">Agenda tu medición</strong> (Lun–Mié; Jue si hay cupo)</li>
            <li><strong style="color: #FFCC00;">Contesta tus cuestionarios</strong> y carga lo obligatorio (especialmente fotos)</li>
            <li><strong style="color: #FFCC00;">Recibe tu plan</strong> en ventana Vie–Sáb–Dom</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Información sobre Medición Corporal
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                padding: 3rem 2rem; border-radius: 20px; margin: 2.5rem 0; 
                border: 3px solid #FFCC00; box-shadow: 0 8px 25px rgba(255,204,0,0.4);">
        <h2 style="color: #FFCC00; font-size: 2.5rem; font-weight: bold; margin-bottom: 2rem; text-align: center;">
            📏 Medición Corporal
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%); 
                    padding: 2rem; border-radius: 15px; border: 2px solid #FFCC00; min-height: 320px;">
            <h3 style="color: #FFCC00; font-size: 1.8rem; margin-bottom: 1rem; text-align: center;">
                🏠 Usuarios Internos
            </h3>
            <div style="color: #FFFFFF; font-size: 1.05rem; line-height: 1.8; margin: 0;">
                <p style="margin: 0 0 1rem 0;"><strong style="color: #FFCC00;">Ubicación:</strong> Instalaciones de Muscle Up Gym</p>
                <p style="margin: 0 0 1rem 0;"><strong style="color: #FFCC00;">Equipo:</strong> Bioimpedancia profesional</p>
                <p style="margin: 0 0 0.5rem 0;"><strong style="color: #FFCC00;">Incluye:</strong></p>
                <ul style="margin: 0; padding-left: 1.2rem;">
                    <li>Medición con bioimpedancia</li>
                    <li>Antropometría completa</li>
                    <li>Asesoría presencial</li>
                    <li>Programación de cita incluida</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%); 
                    padding: 2rem; border-radius: 15px; border: 2px solid #FFCC00; min-height: 320px;">
            <h3 style="color: #FFCC00; font-size: 1.8rem; margin-bottom: 1rem; text-align: center;">
                🌍 Usuarios Externos
            </h3>
            <div style="color: #FFFFFF; font-size: 1.05rem; line-height: 1.8; margin: 0;">
                <p style="margin: 0 0 1rem 0;"><strong style="color: #FFCC00;">Modalidad:</strong> Por cuenta propia</p>
                <p style="margin: 0 0 1rem 0;"><strong style="color: #FFCC00;">Requerimiento:</strong> Medición local</p>
                <p style="margin: 0 0 0.5rem 0;"><strong style="color: #FFCC00;">Incluye:</strong></p>
                <ul style="margin: 0; padding-left: 1.2rem;">
                    <li>Guía detallada para medición</li>
                    <li>Recomendaciones de equipos</li>
                    <li>Asesoría virtual incluida</li>
                    <li>Validación de datos por el profesional</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Cuestionarios Especializados
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                padding: 3rem 2rem; border-radius: 20px; margin: 2.5rem 0; 
                border: 3px solid #FFCC00; box-shadow: 0 8px 25px rgba(255,204,0,0.4);">
        <h2 style="color: #FFCC00; font-size: 2.5rem; font-weight: bold; margin-bottom: 1.5rem; text-align: center;">
            📝 Cuestionarios Especializados
        </h2>
        <p style="color: #FFFFFF; font-size: 1.2rem; margin-bottom: 2rem; text-align: center; line-height: 1.6;">
            🎯 Una vez confirmado tu pago y programada tu medición, tendrás acceso a cuestionarios según tu plan:
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Para todos los planes
    st.markdown("""
    <div style="background: rgba(255,204,0,0.1); padding: 2rem; border-radius: 15px; margin: 1.5rem 0;">
        <h3 style="color: #FFCC00; font-size: 1.5rem; margin-bottom: 1rem;">
            📊 Para TODOS los planes:
        </h3>
        <p style="color: #FFFFFF; font-size: 1.1rem; line-height: 1.8; margin: 0;">
            • <strong>MUPAI BODY AND ENERGY:</strong> Evaluación avanzada de balance energético y composición corporal
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Para planes de alimentación
    st.markdown("""
    <div style="background: rgba(255,204,0,0.1); padding: 2rem; border-radius: 15px; margin: 1.5rem 0;">
        <h3 style="color: #FFCC00; font-size: 1.5rem; margin-bottom: 1rem;">
            🍽️ Para planes de ALIMENTACIÓN:
        </h3>
        <p style="color: #FFFFFF; font-size: 1.1rem; line-height: 1.8; margin: 0;">
            • <strong>FOOD PREFERENCES:</strong> Análisis detallado de patrones y preferencias alimentarias<br>
            • <strong>FOOD CRAVINGS:</strong> Evaluación de antojos alimentarios (versión población mexicana)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Para planes de entrenamiento
    st.markdown("""
    <div style="background: rgba(255,204,0,0.1); padding: 2rem; border-radius: 15px; margin: 1.5rem 0;">
        <h3 style="color: #FFCC00; font-size: 1.5rem; margin-bottom: 1rem;">
            💪 Para planes de ENTRENAMIENTO:
        </h3>
        <p style="color: #FFFFFF; font-size: 1.1rem; line-height: 1.8; margin: 0;">
            • <strong>DESIGNING YOUR TRAINING:</strong> Cuestionario especializado para diseño de rutinas de entrenamiento
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Para plan combinado
    st.markdown("""
    <div style="background: rgba(255,215,0,0.15); padding: 2rem; border-radius: 15px; border: 2px solid #FFD700; margin: 1.5rem 0;">
        <h3 style="color: #FFD700; font-size: 1.5rem; margin-bottom: 1rem;">
            🔥 Para plan COMBINADO:
        </h3>
        <p style="color: #FFFFFF; font-size: 1.1rem; line-height: 1.8; margin: 0;">
            • <strong>TODOS los cuestionarios anteriores</strong> para una evaluación integral completa
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Nota final sobre tiempo de entrega
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFD700 0%, #FFCC00 50%, #FFF2A6 100%); 
                padding: 2.5rem 2rem; border-radius: 20px; margin: 2.5rem 0; 
                border: 3px solid #FFCC00; box-shadow: 0 8px 25px rgba(255,204,0,0.5);
                text-align: center;">
        <h3 style="color: #000; font-size: 2rem; margin-bottom: 1rem; font-weight: bold;">
            ⏰ Tiempo de Entrega (Ventana oficial)
        </h3>
        <p style="color: #333; font-size: 1.3rem; margin-bottom: 1rem; font-weight: 500; line-height: 1.6;">
            <strong>Entregamos planes en Viernes, Sábado o Domingo.</strong>
        </p>
        <p style="color: #333; font-size: 1.1rem; margin-bottom: 1rem; line-height: 1.6;">
            Para recibir tu plan ese fin de semana, necesitas:
        </p>
        <ul style="color: #333; font-size: 1.1rem; margin: 0 auto 1rem auto; max-width: 600px; text-align: left; display: inline-block;">
            <li>Medición a más tardar miércoles</li>
            <li>Cuestionarios completos</li>
            <li>Fotos/archivos obligatorios cargados</li>
        </ul>
        <p style="color: #333; font-size: 1.1rem; margin: 0; font-weight: 400;">
            💡 <strong>Importante:</strong> Si completas tarde, tu entrega pasa al siguiente fin de semana.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Llamada a la acción final
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFCC00 0%, #FFD700 100%); 
                padding: 3rem 2rem; border-radius: 20px; text-align: center; 
                margin: 3rem 0; color: #000; box-shadow: 0 8px 25px rgba(255,204,0,0.3);">
        <h2 style="font-size: 2.5rem; margin-bottom: 1rem; font-weight: bold;">
            🎯 ¡Comienza Tu Transformación Hoy!
        </h2>
        <p style="font-size: 1.3rem; margin-bottom: 2rem; font-weight: 500;">
            Únete a cientos de personas que ya han transformado su físico con MUPAI
        </p>
        <div style="background: #000; color: #FFCC00; padding: 1.5rem; border-radius: 15px; 
                    font-size: 1.2rem; font-weight: bold; display: inline-block;">
            📧 administracion@muscleupgym.fitness<br>
            📱 WhatsApp: 8662580594
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== PÁGINA ¿QUIÉNES SOMOS? ====================
elif st.session_state.page == "quienes_somos":
    # Logo institucional
    logo_base64 = load_logo_image_base64()
    if logo_base64:
        st.markdown(f"""
        <div class="logo-container">
            <img src="{logo_base64}" class="logo-img" alt="MUPAI Logo">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="logo-container">
            <div style="padding: 30px; background-color: #333; border: 2px solid #FFCC00; border-radius: 15px; text-align: center;">
                <h1 style="color: #FFCC00; margin: 0; font-size: 4rem;">💪 MUPAI</h1>
                <p style="color: #FFFFFF; margin: 10px 0 0 0; font-size: 1.5rem;">Muscle Up AI</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Título principal
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                padding: 3rem 2rem; border-radius: 20px; text-align: center; 
                margin: 2rem 0; border: 2px solid #FFCC00; 
                box-shadow: 0 4px 15px rgba(255,204,0,0.3);">
        <h1 style="color: #FFCC00; font-size: 3.5rem; font-weight: bold; 
                   margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(255,204,0,0.5);">
            🏢 ¿Quiénes Somos?
        </h1>
        <h2 style="color: #FFFFFF; font-size: 1.8rem; margin-bottom: 0; font-weight: 500;">
            Conoce la filosofía y valores que nos impulsan
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # Misión
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                padding: 3rem 2rem; border-radius: 20px; margin: 2rem 0; 
                border: 3px solid #FFCC00; box-shadow: 0 6px 20px rgba(255,204,0,0.3);">
        <h2 style="color: #FFCC00; font-size: 2.8rem; font-weight: bold; 
                   margin-bottom: 1.5rem; text-align: center; text-shadow: 2px 2px 4px rgba(255,204,0,0.3);">
            🎯 Nuestra Misión
        </h2>
        <p style="color: #FFFFFF; font-size: 1.4rem; line-height: 1.8; margin-bottom: 1.5rem; text-align: center;">
            Hacer accesible el <strong style="color: #FFCC00;">entrenamiento basado en ciencia</strong>, 
            proporcionando planes completamente personalizados a través de herramientas digitales 
            respaldadas por <strong style="color: #FFCC00;">inteligencia artificial</strong>, 
            datos precisos y la investigación más actualizada en ciencias del ejercicio.
        </p>
        <p style="color: #FFFFFF; font-size: 1.4rem; line-height: 1.8; text-align: center;">
            Nos enfocamos en promover el <strong style="color: #FFCC00;">desarrollo integral</strong> 
            de nuestros usuarios y su bienestar físico y mental, democratizando el acceso a 
            soluciones nutricionales y de entrenamiento de clase mundial.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Visión
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                padding: 3rem 2rem; border-radius: 20px; margin: 2rem 0; 
                border: 3px solid #FFCC00; box-shadow: 0 6px 20px rgba(255,204,0,0.3);">
        <h2 style="color: #FFCC00; font-size: 2.8rem; font-weight: bold; 
                   margin-bottom: 1.5rem; text-align: center; text-shadow: 2px 2px 4px rgba(255,204,0,0.3);">
            🔮 Nuestra Visión
        </h2>
        <p style="color: #FFFFFF; font-size: 1.4rem; line-height: 1.8; margin-bottom: 1.5rem; text-align: center;">
            Convertirnos en uno de los <strong style="color: #FFCC00;">máximos referentes a nivel global</strong> 
            en entrenamiento digital personalizado, aprovechando las nuevas tecnologías para hacer más 
            accesible el fitness basado en ciencia.
        </p>
        <p style="color: #FFFFFF; font-size: 1.4rem; line-height: 1.8; text-align: center;">
            Aspiramos a <strong style="color: #FFCC00;">transformar la experiencia del entrenamiento físico</strong>, 
            integrando inteligencia artificial, investigación científica y herramientas digitales avanzadas 
            que permitan a cualquier persona alcanzar su máximo potencial físico de manera segura y sostenible.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Política Institucional
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                padding: 3rem 2rem; border-radius: 20px; margin: 2rem 0; 
                border: 3px solid #FFCC00; box-shadow: 0 6px 20px rgba(255,204,0,0.3);">
        <h2 style="color: #FFCC00; font-size: 2.8rem; font-weight: bold; 
                   margin-bottom: 1.5rem; text-align: center; text-shadow: 2px 2px 4px rgba(255,204,0,0.3);">
            📋 Nuestra Política Institucional
        </h2>
        <p style="color: #FFFFFF; font-size: 1.4rem; line-height: 1.8; margin-bottom: 2rem; text-align: center;">
            En MUPAI, nuestra política está fundamentada en el <strong style="color: #FFCC00;">compromiso con la excelencia</strong>, 
            la ética y el servicio centrado en el usuario.
        </p>
        <p style="color: #FFFFFF; font-size: 1.4rem; line-height: 1.8; text-align: center;">
            Actuamos con <strong style="color: #FFCC00;">responsabilidad y transparencia</strong> para ofrecer 
            soluciones tecnológicas que integren ciencia, personalización y accesibilidad, contribuyendo 
            al bienestar integral de quienes confían en nosotros.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Política del Servicio
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                padding: 3rem 2rem; border-radius: 20px; margin: 2rem 0; 
                border: 3px solid #FFCC00; box-shadow: 0 6px 20px rgba(255,204,0,0.3);">
        <h2 style="color: #FFCC00; font-size: 2.8rem; font-weight: bold; 
                   margin-bottom: 1.5rem; text-align: center; text-shadow: 2px 2px 4px rgba(255,204,0,0.3);">
            📘 Política del Servicio
        </h2>
        <p style="color: #FFFFFF; font-size: 1.3rem; line-height: 1.8; margin-bottom: 2rem; text-align: center;">
            En MUPAI, guiamos nuestras acciones por los siguientes principios fundamentales:
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 2rem;">
            <div style="background: rgba(255,204,0,0.1); padding: 2rem; border-radius: 15px; border-left: 4px solid #FFCC00;">
                <h4 style="color: #FFCC00; font-size: 1.4rem; margin-bottom: 1rem;">🔬 Ciencia y Evidencia</h4>
                <p style="color: #FFFFFF; font-size: 1.1rem; line-height: 1.6;">
                    Diseñamos entrenamientos digitales que combinan personalización, datos confiables y ciencia del ejercicio 
                    respaldada por investigación peer-reviewed.
                </p>
            </div>
            <div style="background: rgba(255,204,0,0.1); padding: 2rem; border-radius: 15px; border-left: 4px solid #FFCC00;">
                <h4 style="color: #FFCC00; font-size: 1.4rem; margin-bottom: 1rem;">💻 Tecnología Avanzada</h4>
                <p style="color: #FFFFFF; font-size: 1.1rem; line-height: 1.6;">
                    Aprovechamos la tecnología e inteligencia artificial para ofrecer un servicio accesible 
                    y adaptable a las necesidades de cada usuario.
                </p>
            </div>
            <div style="background: rgba(255,204,0,0.1); padding: 2rem; border-radius: 15px; border-left: 4px solid #FFCC00;">
                <h4 style="color: #FFCC00; font-size: 1.4rem; margin-bottom: 1rem;">🔒 Privacidad y Seguridad</h4>
                <p style="color: #FFFFFF; font-size: 1.1rem; line-height: 1.6;">
                    Respetamos y protegemos la privacidad de los datos personales, garantizando su uso 
                    responsable bajo los más altos estándares de seguridad.
                </p>
            </div>
            <div style="background: rgba(255,204,0,0.1); padding: 2rem; border-radius: 15px; border-left: 4px solid #FFCC00;">
                <h4 style="color: #FFCC00; font-size: 1.4rem; margin-bottom: 1rem;">🚀 Innovación Continua</h4>
                <p style="color: #FFFFFF; font-size: 1.1rem; line-height: 1.6;">
                    Innovamos de forma continua para mejorar la experiencia y los resultados de nuestros usuarios, 
                    manteniéndonos a la vanguardia tecnológica.
                </p>
            </div>
            <div style="background: rgba(255,204,0,0.1); padding: 2rem; border-radius: 15px; border-left: 4px solid #FFCC00;">
                <h4 style="color: #FFCC00; font-size: 1.4rem; margin-bottom: 1rem;">🤝 Valores Fundamentales</h4>
                <p style="color: #FFFFFF; font-size: 1.1rem; line-height: 1.6;">
                    Promovemos valores como el esfuerzo, la constancia y el respeto en cada interacción, 
                    fomentando un ambiente de crecimiento y bienestar.
                </p>
            </div>
            <div style="background: rgba(255,204,0,0.1); padding: 2rem; border-radius: 15px; border-left: 4px solid #FFCC00;">
                <h4 style="color: #FFCC00; font-size: 1.4rem; margin-bottom: 1rem;">⭐ Compromiso Total</h4>
                <p style="color: #FFFFFF; font-size: 1.1rem; line-height: 1.6;">
                    Mantenemos un compromiso inquebrantable con la excelencia, proporcionando resultados 
                    medibles y transformaciones reales en nuestros usuarios.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Llamada a la acción
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFCC00 0%, #FFD700 100%); 
                padding: 3rem 2rem; border-radius: 20px; text-align: center; 
                margin: 3rem 0; color: #000; box-shadow: 0 8px 25px rgba(255,204,0,0.3);">
        <h2 style="font-size: 2.5rem; margin-bottom: 1rem; font-weight: bold;">
            🤝 ¡Únete a la Revolución MUPAI!
        </h2>
        <p style="font-size: 1.3rem; margin-bottom: 2rem; font-weight: 500;">
            Descubre por qué somos la elección de miles de personas que buscan transformar su físico con ciencia
        </p>
        <div style="background: #000; color: #FFCC00; padding: 1.5rem; border-radius: 15px; 
                    font-size: 1.2rem; font-weight: bold; display: inline-block;">
            📧 administracion@muscleupgym.fitness<br>
            📱 WhatsApp: 8662580594
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== PÁGINA DE PLANES Y COSTOS ====================
elif st.session_state.page == "planes_costos":
    # Professional banner - visible on all pages
    mostrar_banner_profesional()
    
    st.markdown("""
    <div class="section-header">
        <h2>💸 Planes y Costos</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="questionnaire-container">
        <h3>🎯 Primer Paso: Elige el Plan Adecuado</h3>
        <p>Elige el plan que mejor se adapte a tus objetivos.   Después realiza la transferencia del monto exacto y envía tu comprobante para iniciar tu proceso.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Nueva sección: Organización Semanal
    st.markdown("""
    <div class="section-header">
        <h2>🗓️ Organización Semanal (Importante)</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="questionnaire-container">
        <p>Cada plan se construye a la medida con tus mediciones y cuestionarios.  Por eso trabajamos por ciclos semanales con cupo limitado.</p>
        <ul style="font-size: 1.05rem; line-height: 1.8;">
            <li><strong>Mediciones:</strong> Lunes, Martes y Miércoles</li>
            <li><strong>Jueves:</strong> solo si hay cupo disponible esa semana</li>
            <li><strong>No hay mediciones</strong> viernes, sábado ni domingo</li>
            <li><strong>Entrega del plan:</strong> Viernes, Sábado o Domingo</li>
        </ul>
        <p style="margin-top: 1rem; font-size: 1.05rem;">
            <strong>Nota:</strong> Pagos confirmados en fin de semana (Vie–Dom): se procesan el lunes y la medición se agenda para la siguiente semana.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Instrucciones de pago actualizadas
    st.markdown("""
    <div style="background-color: #fff3cd; border:  2px solid #ffc107; border-radius: 8px; padding: 15px; margin:  15px 0;">
        <h4 style="color: #856404; margin:  0 0 10px 0;">🧾 Instrucciones de Pago</h4>
        <p style="color: #856404; margin: 0 0 10px 0; font-size: 16px;">
            Después de transferir, envía tu comprobante a: 
        </p>
        <ul style="color: #856404; margin: 0; font-size: 16px; font-weight: bold;">
            <li>📱 <strong>WhatsApp: </strong> 8662580594</li>
            <li>📧 <strong>Correo:</strong> administracion@muscleupgym.fitness</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Imagen de la tarjeta bancaria
    st.markdown("### 🏦 Información de Transferencia")
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
    """ + load_banking_image_base64() + """
    </div>
    """, unsafe_allow_html=True)
    
    # NUEVA SECCIÓN:  Protocolo OBLIGATORIO
    st.markdown("""
    <div style="background-color: #f8d7da; border: 2px solid #dc3545; border-radius: 8px; padding: 15px; margin: 15px 0;">
        <h4 style="color: #721c24; margin: 0 0 10px 0;">📌 Antes de contestar cuestionarios (OBLIGATORIO)</h4>
        <p style="color: #721c24; margin: 0 0 10px 0; font-size: 16px;">
            Después de pagar, ve a la barra lateral y abre:  <strong>"Protocolo de Medición MUPAI"</strong>.  
        </p>
        <p style="color: #721c24; margin: 0 0 10px 0; font-size:  16px;">
            Ahí verás cómo preparar:  
        </p>
        <ul style="color: #721c24; margin: 0 0 10px 0; font-size: 16px;">
            <li>Tu medición (bioimpedancia/perímetros, según modalidad)</li>
            <li>Tus fotografías obligatorias (se cargan dentro del cuestionario)</li>
            <li>Tus pruebas funcionales (aplican para TODOS los planes, porque forman parte del cálculo)</li>
        </ul>
        <p style="color: #721c24; margin: 0; font-size: 16px;">
            <strong>Importante: </strong> Si se te complica realizar las pruebas porque eres muy novato o por alguna condición,
            en el apartado de pruebas funcionales de tus cuestionarios escribe las repeticiones en <strong>0 (cero)</strong>. No adivines datos.  
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Planes detallados
    st.markdown("""
    <div class="section-header">
        <h2>📋 Nuestros Planes Profesionales</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Plan 1: Nutrición Personalizada (ACTUALIZADO)
    st.markdown("""
    <div class="corporate-section">
        <h3>🍽️ Plan de Nutrición Personalizada</h3>
        <p><strong>Duración:</strong> Ciclo de 5 semanas (4 semanas de ejecución + 1 semana de reevaluación)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="corporate-section">
        <h4>💰 Precios: </h4>
        <ul>
            <li><strong>Usuarios Internos (miembros del gym):</strong> $700 MXN</li>
            <li><strong>Usuarios Externos:</strong> $900 MXN</li>
        </ul>
        <h4>✅ Incluye:</h4>
        <ul>
            <li>Evaluación inicial (según modalidad): medición + perímetros + fotos (si aplica)</li>
            <li>7 menús personalizados (semana tipo)</li>
            <li>Lista de despensa</li>
            <li>Calorías + macronutrientes optimizados</li>
            <li>Micronutrientes priorizados para salud/rendimiento</li>
            <li>Semana 5: reevaluación para decidir ajustes o continuidad</li>
        </ul>
        <h4>➕ Menús extra (opcional):</h4>
        <ul>
            <li><strong>Internos:</strong> desde $200 MXN</li>
            <li><strong>Externos:</strong> desde $400 MXN</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Plan 2: Diseño de Entrenamiento Personalizado (ACTUALIZADO)
    st.markdown("""
    <div class="corporate-section">
        <h3>💪 Plan de Entrenamiento Personalizado</h3>
        <p><strong>Duración:</strong> 10 semanas</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="corporate-section">
        <h4>💰 Precios:</h4>
        <ul>
            <li><strong>Usuarios Internos (miembros del gym):</strong> $950 MXN</li>
            <li><strong>Usuarios Externos:</strong> $1,100 MXN</li>
        </ul>
        <h4>✅ Incluye:</h4>
        <ul>
            <li>Cuestionario Designing Your Training</li>
            <li>Programa personalizado (volumen, frecuencia, intensidad)</li>
            <li>Progresiones y variaciones</li>
            <li>Entrega en PDF</li>
            <li>Evaluación final</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Plan 3: Plan Combinado (ACTUALIZADO)
    st.markdown("""
    <div class="corporate-section">
        <h3>🔥 Plan Combinado:  Entrenamiento + Nutrición</h3>
        <p><strong>Duración total:</strong> 10 semanas (Nutrición 5 semanas + Entrenamiento 10 semanas)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="corporate-section">
        <h4>💰 Precios:</h4>
        <ul>
            <li><strong>Usuarios Internos (miembros del gym):</strong> $1,500 MXN</li>
            <li><strong>Usuarios Externos:</strong> $1,850 MXN</li>
        </ul>
        <h4>✅ Incluye:</h4>
        <ul>
            <li>Ambos planes completos (nutrición + entrenamiento)</li>
            <li>Planes integrados y coordinados</li>
            <li>Evaluación inicial y final con bioimpedancia</li>
            <li>Seguimiento coordinado de progreso</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Mecánica de adquisición (ACTUALIZADA)
    st.markdown("""
    <div class="section-header">
        <h2>🧩 Mecánica de Adquisición — Paso a Paso</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="questionnaire-container">
        <ol style="font-size: 1.1rem; line-height: 1.8;">
            <li><strong>Elige tu plan</strong></li>
            <li><strong>Realiza el pago</strong></li>
            <li><strong>Envía comprobante</strong> (WhatsApp o correo)</li>
            <li><strong>Abre en la barra lateral: </strong> "Protocolo de Medición MUPAI"</li>
            <li><strong>Agenda tu medición</strong> (Lun–Mié; Jue si hay cupo)</li>
            <li><strong>Contesta tus cuestionarios</strong> y carga lo obligatorio (especialmente fotos)</li>
            <li><strong>Recibe tu plan</strong> en ventana Vie–Sáb–Dom</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Cuestionarios según plan (ACTUALIZADO)
    st.markdown("""
    <div class="section-header">
        <h2>🧠 Cuestionarios (según tu plan)</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="questionnaire-container">
        <ul style="font-size: 1.05rem; line-height: 1.8;">
            <li><strong>Todos: </strong> MUPAI BODY AND ENERGY</li>
            <li><strong>Alimentación:</strong> FoodPreference + FoodCravings</li>
            <li><strong>Entrenamiento:</strong> Designing Your Training</li>
            <li><strong>Combinado:</strong> todos los anteriores</li>
        </ul>
        <p style="margin-top:  1rem; font-size:  1.05rem;">
            <strong>Nota:</strong> Las pruebas funcionales se registran en los cuestionarios y aplican para Nutrición, Entrenamiento y Combinado.
            Si eres muy novato y se te complica, coloca <strong>0</strong> en repeticiones en ese apartado.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tiempo de entrega (ACTUALIZADO)
    st.markdown("""
    <div class="results-container">
        <h3>⏱️ Tiempo de Entrega (Ventana oficial)</h3>
        <p style="font-size: 1.15rem; text-align: center; margin:  1rem 0;">
            <strong>Entregamos planes en Viernes, Sábado o Domingo. </strong>
        </p>
        <p style="font-size: 1.05rem; text-align: center; margin: 0.5rem 0;">
            Para recibir tu plan ese fin de semana, necesitas:
        </p>
        <ul style="font-size:  1.05rem; margin: 1rem auto; max-width: 600px;">
            <li>Medición a más tardar miércoles</li>
            <li>Cuestionarios completos</li>
            <li>Fotos/archivos obligatorios cargados</li>
        </ul>
        <p style="text-align: center; margin-top: 1rem; font-size: 1.05rem;">
            💡 <strong>Importante:</strong> Si completas tarde, tu entrega pasa al siguiente fin de semana.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # NUEVA SECCIÓN: FAQ
    st.markdown("""
    <div class="section-header">
        <h2>❓ Preguntas Frecuentes (FAQ)</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # FAQ 1
    st.markdown("""
    <div class="corporate-section">
        <h4>¿Cuántos menús incluye mi Plan de Nutrición?</h4>
        <p>Incluye 7 menús totalmente personalizados (una semana tipo) + lista de despensa. </p>
    </div>
    """, unsafe_allow_html=True)
    
    # FAQ 2
    st.markdown("""
    <div class="corporate-section">
        <h4>¿Cuántas comidas tiene cada menú (frecuencia diaria)?</h4>
        <p>La cantidad y distribución de comidas por día se define con tu información, usando lo que reportas en cuestionarios y mediciones
        (objetivo, horarios, apetito, estilo de vida, composición corporal, etc.). No es una cifra fija para todos.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # FAQ 3
    st.markdown("""
    <div class="corporate-section">
        <h4>¿Cuándo se toma el baseline (referencia inicial)?</h4>
        <p>Tu referencia inicial se toma el mismo día de tu primera medición, ya sea lunes, martes, miércoles o jueves (según cupo).
        Ese día se consideran tus mediciones iniciales y, cuando aplique, tus fotos iniciales.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # FAQ 4
    st.markdown("""
    <div class="corporate-section">
        <h4>¿Cuándo se repite la medición y las fotos?</h4>
        <p>En la Semana 5 se realiza la reevaluación:  se repite la medición y se toman/actualizan fotografías para comparar progreso
        y decidir ajustes o continuidad. </p>
    </div>
    """, unsafe_allow_html=True)
    
    # FAQ 5
    st.markdown("""
    <div class="corporate-section">
        <h4>¿Cuánto tiempo tarda la medición con bioimpedancia?</h4>
        <p>La medición en el equipo toma aprox.  2 a 5 minutos.  Considera 10 a 15 minutos en total para el proceso completo
        (registro, preparación rápida, medición y anotación de datos).</p>
    </div>
    """, unsafe_allow_html=True)
    
    # FAQ 6
    st.markdown("""
    <div class="corporate-section">
        <h4>¿Tengo que ir en ayunas para la bioimpedancia?</h4>
        <p>Es lo más recomendable.  Seguir el protocolo mejora precisión (hidratación y retención de agua influyen en el resultado).
        El protocolo completo se muestra en la barra lateral en "Protocolo de Medición MUPAI".</p>
    </div>
    """, unsafe_allow_html=True)
    
    # FAQ 7 (ACTUALIZADA CON VESTIMENTA)
    st.markdown("""
    <div class="corporate-section">
        <h4>¿Qué debo llevar o cómo debo ir vestido a la medición?</h4>
        <p><strong>Vestimenta requerida:</strong></p>
        <ul>
            <li><strong>Hombres:</strong> Sin camisa y short</li>
            <li><strong>Mujeres:</strong> Top deportivo y short</li>
        </ul>
        <p style="margin-top: 10px;">
            <strong>Importante: </strong> Consulta el <strong>Protocolo de Vestimenta completo</strong> en el apartado 
            <strong>"Protocolos de Evaluación MUPAI"</strong> en la barra lateral para conocer todos los detalles 
            y especificaciones adicionales (calzado, accesorios, etc.).
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # FAQ 8
    st.markdown("""
    <div class="corporate-section">
        <h4>¿Puedo estimar datos en los cuestionarios?</h4>
        <p>Puedes estimar únicamente datos difíciles de medir (por ejemplo:  horarios, hábitos, nivel de actividad diaria).
        Los datos que dependen de mediciones o pruebas deben ser reales y obtenidos, no aproximados.</p>
        <p><strong>Regla clave:</strong> los datos deben ser verídicos y realistas.  Si se ingresan datos inventados,
        los cálculos pueden quedar mal calibrados y el plan no reflejará tu situación real.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # FAQ 9
    st.markdown("""
    <div class="corporate-section">
        <h4>¿Son obligatorias las fotografías?  ¿Por qué?</h4>
        <p>Sí.  Las fotografías son obligatorias cuando el cuestionario las solicita. En composición corporal, la evaluación más útil es multidimensional: 
        la foto complementa mediciones como cintura/perímetros y bioimpedancia, y permite interpretar mejor el progreso
        (forma, proporciones y distribución), incluso cuando hay cambios de agua o variaciones normales.</p>
        <p><strong>Para que la comparación sea válida:</strong></p>
        <ul>
            <li>Fotos de frente/lado/espalda</li>
            <li>Buena luz, fondo limpio, sin filtros</li>
            <li>Cuerpo completo, postura relajada</li>
        </ul>
        <p>Si no se cargan las fotos requeridas, no es posible cerrar el análisis con el nivel de personalización esperado.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # FAQ 10
    st.markdown("""
    <div class="corporate-section">
        <h4>¿Qué pasa si no puedo tomarme fotos el mismo día?</h4>
        <p>Puedes tomar las fotos ese mismo día o lo más cercano posible, siguiendo el protocolo.  Si el sistema solicita fotos
        y no las cargas, tu evaluación queda incompleta y el plan puede pasar a la siguiente ventana de entrega.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # FAQ 11
    st.markdown("""
    <div class="corporate-section">
        <h4>¿Qué pasa si soy muy novato y se me complican las pruebas funcionales?</h4>
        <p>Las pruebas funcionales forman parte del cálculo y ayudan a calibrar tu plan con datos reales. 
        Si se te complica por ser muy novato o por alguna condición, en el apartado de pruebas funcionales de tus cuestionarios
        escribe las repeticiones en <strong>0 (cero)</strong>. No adivines datos. </p>
    </div>
    """, unsafe_allow_html=True)
    
    # FAQ 12
    st.markdown("""
    <div class="corporate-section">
        <h4>¿Qué pasa si pongo números inventados o "aproximados" en pruebas? </h4>
        <p>El sistema asumirá capacidades que no tienes y el plan puede quedar irreal (cargas/volúmenes mal calibrados).
        Por eso es clave registrar datos reales o usar 0 cuando aplique. </p>
    </div>
    """, unsafe_allow_html=True)
    
    # FAQ 13
    st.markdown("""
    <div class="corporate-section">
        <h4>¿Qué puede retrasar mi entrega?</h4>
        <p>Cuestionarios incompletos, fotos/archivos obligatorios sin cargar, o reprogramación de medición. </p>
    </div>
    """, unsafe_allow_html=True)
    
    # FAQ 14
    st.markdown("""
    <div class="corporate-section">
        <h4>¿Puedo pagar cualquier día?</h4>
        <p>Sí.  Si pagas viernes a domingo, se procesa el lunes y tu medición se agenda para la siguiente semana. </p>
    </div>
    """, unsafe_allow_html=True)
    
    # FAQ 15
    st.markdown("""
    <div class="corporate-section">
        <h4>¿Qué días miden? </h4>
        <p>Lun–Mié; Jue solo si hay cupo. No Vie–Dom.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # FAQ 16
    st. markdown("""
    <div class="corporate-section">
        <h4>¿Qué es el ciclo de 5 semanas?</h4>
        <p>4 semanas de ejecución + semana 5 de reevaluación para ajustar o continuar. </p>
    </div>
    """, unsafe_allow_html=True)
    
       # Nota final
    st. markdown("""
    <div class="results-container">
        <h3 style="text-align: center;">💪 Tu salud y bienestar son nuestra misión</h3>
    </div>
    """, unsafe_allow_html=True)
# ==================== PÁGINA DE PROTOCOLOS DE MEDICIÓN MUPAI ====================
elif st.session_state.page == "protocolos_medicion":
    # Professional banner
    mostrar_banner_profesional()
    
    # Main header
    st.markdown(textwrap.dedent("""
<div class="section-header">
<h2>📏 Protocolos de Medición MUPAI</h2>
</div>
    """).strip(), unsafe_allow_html=True)
    
    # Introduction
    st.markdown(textwrap.dedent("""
<div class="corporate-section">
<p style="font-size: 1.2rem; line-height: 1.8; text-align: center;">
En MUPAI medimos tu progreso con <strong style="color: #FFCC00;">protocolos científicos y reproducibles</strong> 
para asegurar que cada evaluación sea comparable en el tiempo y te permita tomar decisiones informadas 
sobre tu entrenamiento y nutrición.
</p>
</div>
    """).strip(), unsafe_allow_html=True)
    
    # Protocol 1: Functional Performance
    st.markdown(textwrap.dedent("""
<div class="section-header">
<h2>💪 1) PROTOCOLO DE PRUEBA DE RENDIMIENTO FUNCIONAL (MUPAI-FUNC)</h2>
</div>
    """).strip(), unsafe_allow_html=True)
    
    st.markdown(textwrap.dedent("""
<div class="corporate-section">
<h3 style="color: #FFCC00; border-bottom: 3px solid #FFCC00; padding-bottom: 0.5rem; margin-bottom: 1rem;">🎯 Objetivo</h3>
<p style="font-size: 1.1rem; line-height: 1.8;">
Medir tu rendimiento físico real (fuerza–resistencia y control) de forma comparable en el tiempo 
para ajustar entrenamiento.
</p>
        
<h3 style="color: #FFCC00; border-bottom: 3px solid #FFCC00; padding-bottom: 0.5rem; margin-bottom: 1rem;">⚙️ Método</h3>
<p style="font-size: 1.1rem; line-height: 1.8;">
<strong style="color: #FFCC00;">AMRAP (As Many Reps As Possible):</strong> máximo de repeticiones 
válidas con técnica correcta.
</p>
<p style="font-size: 1.1rem; line-height: 1.8;">
La prueba termina cuando:
</p>
<ul style="font-size: 1.05rem; line-height: 1.7;">
<li>Se rompe la técnica (repetición no válida), o</li>
<li>Te detienes &gt; 3 segundos</li>
</ul>
<p style="font-size: 1.1rem; line-height: 1.8;">
<strong>Core:</strong> se mide tiempo máximo manteniendo forma válida.
</p>
</div>
    """).strip(), unsafe_allow_html=True)
    
    st.markdown(textwrap.dedent("""
<div class="questionnaire-container">
<h3 style="color: #FFCC00; border-bottom: 2px solid #FFCC00; padding-bottom: 0.5rem; margin-bottom: 1rem;">✅ Condiciones previas (para que sea comparable)</h3>
<ul style="font-size: 1.05rem; line-height: 1.7;">
<li>Realizar pruebas antes de entrenar (sin fatiga acumulada)</li>
<li>Calentamiento ligero 5–10 min (movilidad + 1–2 series suaves del patrón)</li>
<li>Mismo calzado y superficie (si aplica)</li>
<li>Mismo ejercicio elegido por dominio en cada reevaluación</li>
</ul>
        
<h3 style="color: #FFCC00; border-bottom: 2px solid #FFCC00; padding-bottom: 0.5rem; margin-bottom: 1rem; margin-top: 1.5rem;">📋 Reglas de validez (lo que hace que una repetición cuente)</h3>
<ul style="font-size: 1.05rem; line-height: 1.7;">
<li>Reps con rango de movimiento completo (ROM) y control</li>
<li>Sin "trampa" (rebotes, kipping, acortar ROM)</li>
<li>Ritmo libre, pero sin pausas largas</li>
</ul>
        
<h3 style="color: #FFCC00; border-bottom: 2px solid #FFCC00; padding-bottom: 0.5rem; margin-bottom: 1rem; margin-top: 1.5rem;">📊 Qué registramos (siempre)</h3>
<ul style="font-size: 1.05rem; line-height: 1.7;">
<li>Reps o tiempo final</li>
<li>Opción elegida por dominio (push-ups vs dips, etc.)</li>
<li>Nota rápida: "técnica sólida / falló ROM / dolor / fatiga"</li>
<li>(Opcional) RPE final (0–10): esfuerzo percibido</li>
</ul>
</div>
    """).strip(), unsafe_allow_html=True)
    
    st.markdown(textwrap.dedent("""
<div class="corporate-section">
<h3 style="color: #FFCC00; border-bottom: 3px solid #FFCC00; padding-bottom: 0.5rem; margin-bottom: 1rem;">🏋️ PRUEBAS (elige UNA por dominio)</h3>
</div>
    """).strip(), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(textwrap.dedent("""
<div class="metric-card">
<h4 style="color: #FFCC00; margin-bottom: 0.8rem; font-size: 1.1rem;">1️⃣ Tren superior — EMPUJE</h4>
<p><strong>Elige una:</strong></p>
<ul>
<li><a href="https://youtu.be/WDIpL0pjun0?si=bcBYm0k00TN0Pp6Z" target="_blank" style="color: #FFCC00;">Push-ups</a></li>
<li><a href="https://youtube.com/shorts/1xKgLFm4Hg4?si=btuWz7uG6u2tBwzU" target="_blank" style="color: #FFCC00;">Dips</a></li>
</ul>
<p>📌 <strong>Método: AMRAP</strong></p>
</div>
        """).strip(), unsafe_allow_html=True)
        
        st.markdown(textwrap.dedent("""
<div class="metric-card">
<h4 style="color: #FFCC00; margin-bottom: 0.8rem; font-size: 1.1rem;">3️⃣ Tren inferior — EMPUJE UNILATERAL</h4>
<p><a href="https://youtu.be/kBQ1krvKFBU?si=SzBAJmMXnep2NwET" target="_blank" style="color: #FFCC00;">Búlgara</a></p>
<p>📌 <strong>Método: AMRAP por pierna</strong> (misma altura de apoyo siempre)</p>
</div>
        """).strip(), unsafe_allow_html=True)
        
        st.markdown(textwrap.dedent("""
<div class="metric-card">
<h4 style="color: #FFCC00; margin-bottom: 0.8rem; font-size: 1.1rem;">5️⃣ CORE</h4>
<p><a href="https://youtu.be/ao5nY7lb088?si=vomVIsycB1a8ORd0" target="_blank" style="color: #FFCC00;">Plancha</a></p>
<p>📌 <strong>Método: tiempo máximo con forma correcta</strong></p>
</div>
        """).strip(), unsafe_allow_html=True)
    
    with col2:
        st.markdown(textwrap.dedent("""
<div class="metric-card">
<h4 style="color: #FFCC00; margin-bottom: 0.8rem; font-size: 1.1rem;">2️⃣ Tren superior — TRACCIÓN</h4>
<p><strong>Elige una:</strong></p>
<ul>
<li><a href="https://youtu.be/jgFel4wZl3I?si=BUGSZnaYLSIrD3Iu" target="_blank" style="color: #FFCC00;">Pull-ups estrictas</a></li>
<li><a href="https://youtube.com/shorts/vZy_Eu_Z0WA?si=NsyS8SKwfjpA6E5j" target="_blank" style="color: #FFCC00;">Inverted row</a></li>
</ul>
<p>📌 <strong>Método: AMRAP</strong></p>
</div>
        """).strip(), unsafe_allow_html=True)
        
        st.markdown(textwrap.dedent("""
<div class="metric-card">
<h4 style="color: #FFCC00; margin-bottom: 0.8rem; font-size: 1.1rem;">4️⃣ Tren inferior — HIP-DOMINANTE UNILATERAL</h4>
<p><a href="https://youtube.com/shorts/54XDbJgwIj4?si=OpxDW6gTccdJR6-A" target="_blank" style="color: #FFCC00;">Hip thrust unilateral</a></p>
<p>📌 <strong>Método: AMRAP por pierna</strong></p>
</div>
        """).strip(), unsafe_allow_html=True)
    
    st.markdown(textwrap.dedent("""
<div class="results-container">
<h3 style="text-align: center;">⚠️ Regla clave</h3>
<p style="font-size: 1.2rem; text-align: center; margin: 0;">
El ejercicio elegido <strong>NO se cambia en futuras evaluaciones</strong> para mantener la comparabilidad.
</p>
</div>
    """).strip(), unsafe_allow_html=True)
    
    # Protocol 2: Body Composition
    st.markdown(textwrap.dedent("""
<div class="section-header">
<h2>📸 2) PROTOCOLO DE MEDICIÓN DE COMPOSICIÓN CORPORAL — MUPAI</h2>
</div>
    """).strip(), unsafe_allow_html=True)
    
    st.markdown(textwrap.dedent("""
<div class="corporate-section">
<p style="font-size: 1.1rem; line-height: 1.8;">
Cómo medimos composición corporal de forma fiable, con instrucciones claras para el cliente y para staff.
</p>
</div>
    """).strip(), unsafe_allow_html=True)
    
    # PHOTO4 Protocol with Pose Libre
    st.markdown(textwrap.dedent("""
<div class="section-header">
<h3 style="color: #FFCC00; margin: 0; font-size: 1.3rem;">A) FOTO-PROGRESO: MUPAI PHOTO4 (obligatorio)</h3>
</div>
    """).strip(), unsafe_allow_html=True)
    
    st.markdown(textwrap.dedent("""
<div class="corporate-section">
<h3 style="color: #FFCC00; border-bottom: 3px solid #FFCC00; padding-bottom: 0.5rem; margin-bottom: 1rem;">🎯 Objetivo</h3>
<p style="font-size: 1.1rem; line-height: 1.8;">
Registrar cambios reales de grasa y forma corporal con comparabilidad longitudinal.
</p>
        
<h3 style="color: #FFCC00; border-bottom: 3px solid #FFCC00; padding-bottom: 0.5rem; margin-bottom: 1rem;">📷 Fotos requeridas (4)</h3>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin: 1.5rem 0;">
<div style="background: rgba(255,204,0,0.1); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #FFCC00;">
<h4 style="color: #FFCC00; margin-bottom: 0.8rem;">1. Frontal relajado</h4>
<p style="font-size: 1rem; line-height: 1.6;">
Posición frontal completamente relajada, brazos a los lados, vista al frente.
</p>
</div>
<div style="background: rgba(255,204,0,0.1); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #FFCC00;">
<h4 style="color: #FFCC00; margin-bottom: 0.8rem;">2. Perfil lateral relajado (derecho)</h4>
<p style="font-size: 1rem; line-height: 1.6;">
Vista de perfil del lado derecho, completamente relajado, brazos a los lados.
</p>
</div>
<div style="background: rgba(255,204,0,0.1); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #FFCC00;">
<h4 style="color: #FFCC00; margin-bottom: 0.8rem;">3. Posterior relajado</h4>
<p style="font-size: 1rem; line-height: 1.6;">
Vista de espalda completamente relajada, brazos a los lados.
</p>
</div>
<div style="background: rgba(255,204,0,0.1); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #FFD700;">
<h4 style="color: #FFD700; margin-bottom: 0.8rem;">4. Pose Libre ⭐</h4>
<p style="font-size: 1rem; line-height: 1.6;">
<strong>NUEVA:</strong> Una pose de tu elección que muestre tu progreso. 
Puede ser con tensión muscular, una pose estética o funcional que te represente. 
<strong>Mantén la misma pose en cada evaluación.</strong>
</p>
</div>
</div>
</div>
    """).strip(), unsafe_allow_html=True)
    
    st.markdown(textwrap.dedent("""
<div class="questionnaire-container">
<h3 style="color: #FFCC00; border-bottom: 2px solid #FFCC00; padding-bottom: 0.5rem; margin-bottom: 1rem;">🌟 Guía para la Pose Libre</h3>
<p style="font-size: 1.05rem; line-height: 1.7;">
La <strong style="color: #FFCC00;">Pose Libre</strong> te permite mostrar tu progreso de forma personalizada:
</p>
<ul style="font-size: 1.05rem; line-height: 1.7;">
<li><strong>Poses de fuerza:</strong> Flexión de bíceps frontal, doble bíceps posterior, abdominales contraídos</li>
<li><strong>Poses estéticas:</strong> Pose de vacío abdominal, cuádriceps contraído, poses de culturismo clásicas</li>
<li><strong>Poses funcionales:</strong> Posición atlética, pose de tu deporte favorito</li>
<li><strong>Lo más importante:</strong> Mantén exactamente la misma pose en cada evaluación para ver tu progreso real</li>
</ul>
<p style="font-size: 1rem; line-height: 1.6; color: #888; margin-top: 1rem; font-style: italic;">
💡 <strong>Consejo:</strong> Elige una pose que te motive y en la que quieras ver mejoras específicas.
</p>
</div>
    """).strip(), unsafe_allow_html=True)
    
    # Timing section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(textwrap.dedent("""
<div class="metric-card">
<h4 style="color: #FFCC00; margin-bottom: 0.8rem; font-size: 1.1rem;">⏰ Momento OFICIAL (óptima)</h4>
<ul style="font-size: 1rem; line-height: 1.6;">
<li>Por la mañana</li>
<li>Antes de entrenar</li>
<li>Sin comida grande previa</li>
</ul>
</div>
        """).strip(), unsafe_allow_html=True)
    
    with col2:
        st.markdown(textwrap.dedent("""
<div class="metric-card">
<h4 style="color: #FFCC00; margin-bottom: 0.8rem; font-size: 1.1rem;">⏰ Momento ESTÁNDAR (válida)</h4>
<ul style="font-size: 1rem; line-height: 1.6;">
<li>Antes de entrenar el mismo día</li>
<li>Evitar comida grande 2–3 h antes</li>
<li>No entrenar antes (evitar "pump")</li>
</ul>
</div>
        """).strip(), unsafe_allow_html=True)
    
    st.markdown(textwrap.dedent("""
<div class="corporate-section">
<h3 style="color: #FFCC00; border-bottom: 3px solid #FFCC00; padding-bottom: 0.5rem; margin-bottom: 1rem;">📐 Set-up técnico (NO negociable)</h3>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0;">
<div style="background: rgba(255,204,0,0.05); padding: 1rem; border-radius: 8px;">
<p style="margin: 0;"><strong style="color: #FFCC00;">📷 Cámara:</strong> Altura del ombligo</p>
</div>
<div style="background: rgba(255,204,0,0.05); padding: 1rem; border-radius: 8px;">
<p style="margin: 0;"><strong style="color: #FFCC00;">📏 Distancia:</strong> 2.5 metros fija</p>
</div>
<div style="background: rgba(255,204,0,0.05); padding: 1rem; border-radius: 8px;">
<p style="margin: 0;"><strong style="color: #FFCC00;">🔍 Zoom:</strong> 1x (sin zoom)</p>
</div>
<div style="background: rgba(255,204,0,0.05); padding: 1rem; border-radius: 8px;">
<p style="margin: 0;"><strong style="color: #FFCC00;">💡 Luz:</strong> Frontal homogénea</p>
</div>
<div style="background: rgba(255,204,0,0.05); padding: 1rem; border-radius: 8px;">
<p style="margin: 0;"><strong style="color: #FFCC00;">🎨 Fondo:</strong> Liso y neutro</p>
</div>
<div style="background: rgba(255,204,0,0.05); padding: 1rem; border-radius: 8px;">
<p style="margin: 0;"><strong style="color: #FFCC00;">📱 Formato:</strong> Vertical</p>
</div>
</div>
<p style="font-size: 1rem; margin-top: 1rem;"><strong>Ángulo:</strong> Horizontal (sin inclinar)</p>
<p style="font-size: 1rem;"><strong>Encuadre:</strong> Cuerpo completo (pies y cabeza visibles)</p>
</div>
    """).strip(), unsafe_allow_html=True)
    
    st.markdown(textwrap.dedent("""
<div class="questionnaire-container">
<h3 style="color: #FFCC00; border-bottom: 2px solid #FFCC00; padding-bottom: 0.5rem; margin-bottom: 1rem;">👕 Vestimenta (precisión)</h3>
<h4 style="color: #FFCC00;">Recomendado (máxima precisión):</h4>
<ul style="font-size: 1.05rem; line-height: 1.7;">
<li><strong>Hombre:</strong> sin camisa + short ajustado no compresivo</li>
<li><strong>Mujer:</strong> top ajustado + short/licra corta no compresiva</li>
</ul>
<h4 style="color: #FFCC00;">Alternativa válida (menos precisa):</h4>
<ul style="font-size: 1.05rem; line-height: 1.7;">
<li>Playera athletic/slim + short ajustado</li>
<li><strong style="color: #FFD700;">Regla:</strong> misma prenda/talla siempre</li>
</ul>
        
<h3 style="color: #FFCC00; border-bottom: 2px solid #FFCC00; padding-bottom: 0.5rem; margin-bottom: 1rem; margin-top: 1.5rem;">💬 Instrucción estándar</h3>
<p style="font-size: 1.1rem; line-height: 1.8; text-align: center; background: rgba(255,204,0,0.1); padding: 1rem; border-radius: 8px;">
<em>"Colócate natural, relajado, sin posar. Mantén respiración normal."</em><br>
<strong style="color: #FFD700;">(Excepto en la Pose Libre, donde sí puedes tensar)</strong>
</p>
        
<h3 style="color: #FFCC00; border-bottom: 2px solid #FFCC00; padding-bottom: 0.5rem; margin-bottom: 1rem; margin-top: 1.5rem;">✅ Control de calidad</h3>
<p style="font-size: 1.05rem; line-height: 1.7;">
Si falla cualquiera: luz muy distinta, cámara inclinada, distancia distinta, ropa distinta → <strong style="color: #FFCC00;">repetir</strong>.
</p>
</div>
    """).strip(), unsafe_allow_html=True)
    
    # Bioimpedance section
    st.markdown(textwrap.dedent("""
<div class="section-header">
<h3 style="color: #FFCC00; margin: 0; font-size: 1.3rem;">B) BIOIMPEDANCIA: OMRON HBF-516 (obligatorio)</h3>
</div>
    """).strip(), unsafe_allow_html=True)
    
    st.markdown(textwrap.dedent("""
<div class="corporate-section">
<h3 style="color: #FFCC00; border-bottom: 3px solid #FFCC00; padding-bottom: 0.5rem; margin-bottom: 1rem;">🎯 Objetivo</h3>
<p style="font-size: 1.1rem; line-height: 1.8;">
Medición reproducible para seguimiento (tendencia). No se interpreta como verdad absoluta aislada.
</p>
</div>
    """).strip(), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(textwrap.dedent("""
<div class="metric-card">
<h4 style="color: #FFCC00; margin-bottom: 0.8rem; font-size: 1.1rem;">⏰ Preparación OFICIAL (óptima)</h4>
<ul style="font-size: 1rem; line-height: 1.6;">
<li><b>Mañana</b> (idealmente en la misma franja horaria para maximizar comparabilidad)</li>
<li><b>Ayuno 8–10 h</b> (reduce variación aguda por ingesta reciente y cambios transitorios de fluidos)</li>
<li><b>No entrenar antes de medir</b> (evita sesgo por “pump”, sudoración y redistribución de líquidos)</li>
<li><b>Recomendado:</b> 12–24 h sin entrenamiento intenso (especialmente pierna o sesiones con sudoración alta)</li>
<li><b>Evitar</b> ducha caliente/sauna/vapor 2–3 h antes (puede alterar conductancia y perfusión periférica)</li>
<li><b>Sin alcohol 24 h</b> (disminuye variación por cambios en hidratación)</li>
<li><strong>Vestimenta para medición precisa/Hombre:</strong> sin camisa + short ajustado no compresivo (alternativa: Playera athletic/slim + short ajustado, NOTA:MEDICIÓN MENOS PRECISA)</li>
<li><strong>Vestimenta para medición precisa/Mujer:</strong> top ajustado + short/licra corta no compresiva (alternativa: Playera athletic/slim + short ajustado, NOTA:MEDICIÓN MENOS PRECISA)</li>
</ul>
</div>
        """).strip(), unsafe_allow_html=True)

    with col2:
        st.markdown(textwrap.dedent("""
<div class="metric-card">
<h4 style="color: #FFCC00; margin-bottom: 0.8rem; font-size: 1.1rem;">⏰ Preparación ESTÁNDAR (válida)</h4>
<ul style="font-size: 1rem; line-height: 1.6;">
<li><b>Antes de entrenar ese día</b> (sin ejercicio previo; condición crítica)</li>
<li><b>Sin comida grande 3–4 h antes</b> (ideal: patrón similar entre mediciones)</li>
<li><b>Vejiga vacía</b> (30–60 min antes; reduce variación por contenido de líquidos)</li>
<li><b>Registrar</b> si entrenaste fuerte el día anterior (contextualiza variaciones por fatiga/sudoración)</li>
</ul>
</div>
        """).strip(), unsafe_allow_html=True)

    st.markdown(textwrap.dedent("""
<div class="questionnaire-container">
<h3 style="color: #FFCC00; border-bottom: 2px solid #FFCC00; padding-bottom: 0.5rem; margin-bottom: 1rem;">✅ Checklist crítico (siempre)</h3>
<ul style="font-size: 1.05rem; line-height: 1.7;">
<li><b>Piso duro y nivelado</b> (no alfombra)</li>
<li><b>Pies/manos limpios y secos</b> (sin crema/aceite/gel; sin sudor)</li>
<li><b>Retirar metales externos</b>: reloj, anillos, pulseras, collares/cadenas, aretes y piercings removibles (evitar también monedas/llaves en bolsillos)</li>
<li><b>Mismo perfil</b> (edad/sexo/estatura correctos; no improvisar)</li>
</ul>
        
<h3 style="color: #FFCC00; border-bottom: 2px solid #FFCC00; padding-bottom: 0.5rem; margin-bottom: 1rem; margin-top: 1.5rem;">🔄 Ejecución exacta (paso a paso)</h3>
<ol style="font-size: 1.05rem; line-height: 1.7;">
<li><b>Encender</b> y esperar 0.0</li>
<li><b>Seleccionar perfil</b> (usuario correcto)</li>
<li><b>Subir descalzo</b>, pies centrados en electrodos</li>
<li><b>Tomar manerales</b> con contacto completo en los sensores</li>
<li><b>Quedarte quieto</b> y respirar normal hasta finalizar</li>
<li><b>Registrar resultados</b> (exactamente lo que muestre el equipo)</li>
</ol>
        
<h3 style="color: #FFCC00; border-bottom: 2px solid #FFCC00; padding-bottom: 0.5rem; margin-bottom: 1rem; margin-top: 1.5rem;">📊 Qué registramos</h3>
<ul style="font-size: 1.05rem; line-height: 1.7;">
<li><b>Fecha y hora</b></li>
<li><b>Peso del día</b></li>
<li><b>Resultado OMRON</b> (lo que muestre el equipo)</li>
<li><b>Calidad:</b> OFICIAL o ESTÁNDAR</li>
<li><b>Observaciones:</b> ayuno (sí/no), cafeína (sí/no), ejercicio previo ese día (sí/no), entrenamiento fuerte el día anterior (sí/no), ducha caliente reciente (sí/no)</li>
</ul>
</div>
    """).strip(), unsafe_allow_html=True)

    
    st.markdown(textwrap.dedent("""
<div class="results-container">
<h3 style="text-align: center;">⚠️ Regla de interpretación (muy importante)</h3>
<p style="font-size: 1.2rem; text-align: center; margin: 0;">
No ajustar dieta/entrenamiento por un solo número. Se decide con:<br>
<strong>tendencia OMRON + PHOTO4 + rendimiento funcional</strong>
</p>
</div>
    """).strip(), unsafe_allow_html=True)
    
    # Recommended order
    st.markdown(textwrap.dedent("""
<div class="section-header">
<h3 style="color: #FFCC00; margin: 0; font-size: 1.3rem;">C) ORDEN RECOMENDADO EL DÍA DE EVALUACIÓN</h3>
</div>
    """).strip(), unsafe_allow_html=True)
    
    st.markdown(textwrap.dedent("""
<div class="corporate-section">
<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1.5rem; margin: 1.5rem 0;">
<div style="background: linear-gradient(135deg, #FFCC00 0%, #FFD700 100%); 
padding: 2rem; border-radius: 15px; text-align: center; color: #000;">
<h2 style="margin: 0 0 0.5rem 0; font-size: 2rem;">1️⃣</h2>
<h4 style="margin: 0 0 0.5rem 0;">PHOTO4</h4>
<p style="margin: 0; font-size: 0.9rem;">(incluye Pose Libre)</p>
</div>
<div style="background: linear-gradient(135deg, #FFCC00 0%, #FFD700 100%); 
padding: 2rem; border-radius: 15px; text-align: center; color: #000;">
<h2 style="margin: 0 0 0.5rem 0; font-size: 2rem;">2️⃣</h2>
<h4 style="margin: 0;">OMRON HBF-516</h4>
</div>
<div style="background: linear-gradient(135deg, #FFCC00 0%, #FFD700 100%); 
padding: 2rem; border-radius: 15px; text-align: center; color: #000;">
<h2 style="margin: 0 0 0.5rem 0; font-size: 2rem;">3️⃣</h2>
<h4 style="margin: 0 0 0.5rem 0;">MUPAI-FUNC</h4>
<p style="margin: 0; font-size: 0.9rem;">(con calentamiento breve)</p>
</div>
</div>
</div>
    """).strip(), unsafe_allow_html=True)
    
    # Example images display block for PHOTO3
    st.markdown(textwrap.dedent("""
<div class="section-header">
<h2>📸 Ejemplos de Fotos PHOTO4</h2>
</div>
    """).strip(), unsafe_allow_html=True)
    
    st.markdown(textwrap.dedent("""
<div class="corporate-section">
<p style="font-size: 1.1rem; line-height: 1.8; text-align: center;">
A continuación se muestran ejemplos de las <strong style="color: #FFCC00;">4 fotos requeridas</strong> 
para el protocolo PHOTO4. Sigue estos ejemplos para asegurar la comparabilidad de tus mediciones.
</p>
</div>
    """).strip(), unsafe_allow_html=True)
    
    # Define image list with updated descriptions
    example_images = [
        ("1. Frontal relajado", "FRONTAL.png", "Posición frontal relajada, brazos a los lados"),
        ("2. Perfil lateral (derecho)", "PERFIL.png", "Vista de perfil del lado derecho relajado"),
        ("3. Posterior relajado", "POSTERIOR.png", "Vista de espalda completamente relajada"),
        ("4. Pose Libre - Ejemplo 1 ⭐", "LIBRE 1.png", "Ejemplo de Pose Libre con tensión muscular"),
        ("4. Pose Libre - Ejemplo 2 ⭐", "LIBRE 2.png", "Otro ejemplo de Pose Libre personalizada")
    ]
    
    # Display first three standard images in 3 columns
    st.markdown(textwrap.dedent("""
<div class="questionnaire-container">
<h3 style="color: #FFCC00; border-bottom: 2px solid #FFCC00; padding-bottom: 0.5rem; margin-bottom: 1rem;">🔹 Fotos Estándar Relajadas (Obligatorias)</h3>
</div>
    """).strip(), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    for idx, (label, fname, description) in enumerate(example_images[:3]):
        with [col1, col2, col3][idx]:
            if os.path.exists(fname):
                try:
                    st.image(fname, caption=label, use_container_width=True)
                    st.markdown(f"""
                    <div style="text-align: center; padding: 0.5rem; background: rgba(255,204,0,0.05); 
                                border-radius: 8px; margin-top: 0.5rem;">
                        <p style="margin: 0; font-size: 0.9rem; color: #FFFFFF;">{description}</p>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.info(f"Ejemplo: {label} — Error al cargar: {fname}")
            else:
                st.info(f"Ejemplo: {label} — Archivo no encontrado: {fname}")
    
    # Display Pose Libre images in 2 columns with special highlighting
    st.markdown(textwrap.dedent("""
<div class="questionnaire-container" style="margin-top: 2rem;">
<h3 style="color: #FFD700; border-bottom: 2px solid #FFD700; padding-bottom: 0.5rem; margin-bottom: 1rem;">⭐ Pose Libre (Nueva - Obligatoria)</h3>
<p style="font-size: 1.05rem; line-height: 1.7;">
Estos son ejemplos de <strong style="color: #FFCC00;">Pose Libre</strong>. Elige una pose que te represente 
y <strong>mantenla en cada evaluación</strong> para ver tu progreso.
</p>
</div>
    """).strip(), unsafe_allow_html=True)
    
    # Display remaining images (Pose Libre examples) - typically images 4 and 5
    pose_libre_images = example_images[3:]  # Get all images after the first 3
    if len(pose_libre_images) > 0:
        col4, col5 = st.columns(2)
        for idx, (label, fname, description) in enumerate(pose_libre_images[:2]):
            with [col4, col5][idx]:
                if os.path.exists(fname):
                    try:
                        st.image(fname, caption=label, use_container_width=True)
                        st.markdown(f"""
                        <div style="text-align: center; padding: 0.8rem; 
                                    background: linear-gradient(135deg, rgba(255,204,0,0.2) 0%, rgba(255,215,0,0.1) 100%); 
                                    border-radius: 8px; margin-top: 0.5rem; border: 1px solid #FFD700;">
                            <p style="margin: 0; font-size: 0.95rem; color: #FFFFFF; font-weight: 500;">{description}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.info(f"Ejemplo: {label} — Error al cargar: {fname}")
                else:
                    st.info(f"Ejemplo: {label} — Archivo no encontrado: {fname}")
    
    # Final note about Pose Libre
    st.markdown(textwrap.dedent("""
<div class="results-container" style="margin-top: 2rem;">
<h3 style="text-align: center;">💡 Recuerda</h3>
<p style="font-size: 1.1rem; text-align: center; margin: 0;">
Las primeras <strong>3 fotos son relajadas</strong> (frontal, perfil, posterior).<br>
La Pose Libre</strong> es donde puedes mostrar tu mejor versión con tensión muscular o pose estética.<br>
<strong>Mantén siempre la misma pose libre para comparar tu progreso.</strong>
</p>
</div>
    """).strip(), unsafe_allow_html=True)

# ==================== PÁGINA DE MUPCAMP 1:1 ====================
elif st.session_state.page == "mupcamp_1a1":
    # Professional banner - visible on all pages
    mostrar_banner_profesional()
    
    # Page title
    st.markdown("""
    <div class="section-header">
        <h2>🔴 MUPCAMP 1:1 — Seguimiento presencial personalizado (10 semanas)</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Intro paragraph
    st.markdown("""
    <div class="corporate-section">
        <p style="font-size: 1.1rem; line-height: 1.8;">
            Programa exclusivo de Muscle Up Gym / MUPAI.
        </p>
        <p style="font-size: 1.1rem; line-height: 1.8;">
            Este no es un "mes de rutina" más. Es un acompañamiento 100% 1:1 durante 10 semanas, donde trabajamos tu cuerpo como un sistema completo: entrenamiento, nutrición, sueño, estrés, trabajo, familia y contexto real de tu vida.
        </p>
        <p style="font-size: 1.1rem; line-height: 1.8;">
            👤 Todas las sesiones son 1:1. En tu horario estoy trabajando únicamente contigo: correcciones técnicas, ajustes en tiempo real y feedback constante.
        </p>
        <p style="font-size: 1.1rem; line-height: 1.8;">
            📌 Cupo máximo: 5 personas al mismo tiempo. Cuando los lugares están completos, se abre lista de espera hasta que termina algún proceso.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enfoques posibles section
    st.markdown("""
    <div class="section-header">
        <h2>Enfoques posibles del MUPCAMP</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="questionnaire-container">
        <ul style="font-size: 1.1rem; line-height: 1.8;">
       
 <li><strong>Fitness y fisicoculturismo natural:</strong> 
    Desarrollo de masa muscular, pérdida de grasa y recomposición corporal, así como preparación específica para <em>competencias de fisicoculturismo natural</em> bajo enfoques de entrenamiento y nutrición basados en evidencia.
  </li>

 
  <li><strong>Rendimiento deportivo:</strong> 
    Optimización de capacidades físicas (fuerza, potencia, velocidad, resistencia, agilidad) y de la composición corporal para competir en diferentes niveles: recreativo, amateur, semiprofesional y alto rendimiento, en deportes individuales y de equipo.
  </li>

  
  <li><strong>Salud y bienestar:</strong> 
    Mejora de la composición corporal y de la salud músculo-esquelética, articular, inmunológica y hormonal a través de programas integrales de entrenamiento y nutrición, adaptados al contexto de vida y, cuando aplica, en coordinación con el criterio médico del usuario.
  </li>
        </ul>
        <p style="font-size: 0.9rem; color: #888; margin-top: 1.5rem; font-style: italic;">
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # What is included section
    st.markdown("""
    <div class="section-header">
        <h2>¿Qué incluye exactamente?</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="questionnaire-container">
        <ul style="font-size: 1.1rem; line-height: 1.8;">
            <li><strong>Evaluación inicial completa:</strong> Composición corporal, historial de entrenamiento, alimentación actual, patrones de sueño, nivel de estrés, lesiones, contexto laboral y familiar</li>
            <li><strong>Sesiones de entrenamiento 1:1:</strong> De 3 a 5 sesiones semanales según tu disponibilidad y objetivo (explicado más abajo)</li>
            <li><strong>Plan de alimentación personalizado:</strong> Ajustado semana a semana según tu progreso, preferencias y contexto</li>
            <li><strong>Planificación de entrenamiento periodizada:</strong> Diseñada para las 10 semanas con progresiones lógicas</li>
            <li><strong>Ajustes semanales:</strong> Revisión de progreso, ajuste de cargas, volumen, calorías, macros</li>
            <li><strong>Educación continua:</strong> Entiendes el porqué de cada decisión (no solo sigues instrucciones)</li>
            <li><strong>Acceso directo vía WhatsApp:</strong> Para dudas, reportar cómo te sientes, ajustar algo urgente</li>
            <li><strong>Evaluación final:</strong> Con reporte completo de cambios físicos, de rendimiento y aprendizajes clave</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    
""", unsafe_allow_html=True)
    
    # Horarios disponibles
    st.markdown("""
    <div class="section-header">
        <h2>Horarios disponibles</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="corporate-section">
        <p style="font-size: 1.1rem; line-height: 1.8;">
            Los bloques de horario son los siguientes (se elige 1 bloque, y ese bloque queda reservado exclusivamente para ti):
        </p>
        <ul style="font-size: 1.05rem; line-height: 1.7;">
            <li>7:30 AM - 9:00 AM</li>
            <li>9:00 AM - 10:30 AM</li>
            <li>3:00 PM - 4:30 PM</li>
            <li>4:30 PM - 6:00 PM</li>
            <li>6:00 PM - 7:30 PM</li>
            <li>8:30 PM - 10:00 PM</li>
        </ul>
        <p style="font-size: 1.05rem; line-height: 1.7; margin-top: 1rem; font-weight: 500;">
            Una vez que eliges tu bloque, ese horario es tuyo durante las 10 semanas. Si hay días que no puedes asistir, se puede reprogramar dentro de la misma semana según disponibilidad.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Frequency decision
    st.markdown("""
    <div class="questionnaire-container">
        <h3>¿Cómo decido si entreno 3, 4 o 5 veces por semana?</h3>
        <p style="font-size: 1.05rem; line-height: 1.7;">
            Esto depende de tu disponibilidad real de tiempo, tu capacidad de recuperación actual, tu experiencia previa y tu objetivo.
        </p>
        <ul style="font-size: 1.05rem; line-height: 1.7;">
            <li><strong>3 sesiones:</strong> Ideal si tienes poco tiempo, eres principiante, o tu prioridad es crear el hábito sin saturarte. Se puede progresar perfectamente.</li>
            <li><strong>4 sesiones:</strong> El punto medio. Suficiente estímulo para progresar de forma consistente sin generar fatiga excesiva. Funciona bien para la mayoría de personas.</li>
            <li><strong>5 sesiones:</strong> Para quienes tienen experiencia previa, alta capacidad de recuperación, o un objetivo muy específico (competencia, evento importante, etc.).</li>
        </ul>
        <p style="font-size: 1.05rem; line-height: 1.7; margin-top: 1rem; font-style: italic;">
            Lo importante no es "cuántas más mejor", sino que puedas sostenerlo durante 10 semanas y que tu cuerpo responda bien. Esto se decide en la evaluación inicial.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Investment and policy
    st.markdown("""
    <div class="results-container">
        <h3 style="text-align: center; font-size: 1.5rem; margin-bottom: 1rem;">💰 MUPCAMP 1:1 – Vigencia 10 semanas: Desde $232 por sesiónMXN</h3>
        <p style="font-size: 1.1rem; line-height: 1.7; text-align: center;">
           $11,599 MXN Pago único por adelantado para reservar tu lugar y tu horario.
        </p>
        <p style="font-size: 1.05rem; line-height: 1.7; text-align: center; margin-top: 1rem; font-weight: 500;">
        </p>
        <p style="font-size: 1.05rem; line-height: 1.7; text-align: center; margin-top: 1rem; font-weight: 500;">
            Debido al cupo reducido y al formato 100% 1:1, la inversión no es reembolsable. En casos de fuerza mayor (lesión grave, enfermedad, etc.) se puede valorar una pausa del proceso, pero no devolución.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p>
        ✅ El pago incluye la membresía al Muscle Up Gym durante las 10 semanas del programa, con acceso completo a las instalaciones en el horario reservado.
    </p>
    <p>
        ✨ Atención 100% personalizada: seguimiento 1:1, ajustes semanales y comunicación directa por WhatsApp. 
        <strong>Desde $232 MXN por sesión</strong> — una forma simple y clara de entender el valor real de tu inversión.
    </p>
    <p>
        *Pago total: $11,599 MXN. Mostramos el costo por sesión para facilitar la comparación y ayudar a decidir con confianza.
    </p>
""", unsafe_allow_html=True)
    
    # Who is not a good candidate
    st.markdown("""
    <div class="section-header">
        <h2>¿Para quién NO es el MUPcamp?</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="questionnaire-container">
        <p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 1rem;">
            Este programa NO es para ti si:
        </p>
        <ul style="font-size: 1.05rem; line-height: 1.7;">
            <li>Solo quieres "un mes de rutina" para hacer por tu cuenta sin seguimiento</li>
            <li>No estás dispuesto a comprometerte 10 semanas completas</li>
            <li>Buscas resultados milagrosos sin esfuerzo ni consistencia</li>
            <li>No puedes ajustar tu horario para asistir a las sesiones (el cupo es limitado y el horario es fijo)</li>
            <li>Esperas que el coach "haga magia" sin que tú pongas de tu parte en alimentación, descanso y adherencia</li>
        </ul>
        <p style="font-size: 1.05rem; line-height: 1.7; margin-top: 1rem; font-weight: 500;">
            Este programa es intenso, personalizado y requiere compromiso real. Si no estás en ese momento de tu vida, mejor espera a estarlo.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Banking data and acquisition mechanic
    st.markdown("""
    <div class="section-header">
        <h2>💳 Datos para Transferencia</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
    """ + load_banking_image_base64() + """
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-header">
        <h2>📝 Mecánica de Adquisición - Paso a Paso</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="questionnaire-container">
        <ol style="font-size: 1.1rem; line-height: 1.8;">
            <li><strong>Realiza la transferencia:</strong> $11,599 MXN a la cuenta mostrada arriba (vigencia: 10 semanas)</li>
            <li><strong>Llena el formulario de esta página:</strong> Con tus datos y sube el comprobante de pago</li>
            <li><strong>Confirmación de pago:</strong> En máximo 24 horas hábiles recibirás confirmación de que tu lugar está reservado</li>
            <li><strong>Programación de evaluación inicial:</strong> Se agenda tu primera sesión de evaluación completa</li>
            <li><strong>Evaluación inicial (presencial):</strong> Composición corporal, historial, objetivos, contexto de vida</li>
            <li><strong>Diseño del plan:</strong> En 3-5 días hábiles recibes tu plan de entrenamiento y alimentación inicial</li>
            <li><strong>Inicio oficial del MUPcamp:</strong> Comienzas tus sesiones 1:1 en el horario reservado</li>
        </ol>
        <p style="font-size: 1.05rem; line-height: 1.7; margin-top: 1.5rem; font-weight: 500; text-align: center;">
            ⚠️ El pago reserva tu lugar. Si el cupo está completo, entras a lista de espera hasta que se abra un lugar.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Contact CTA section for reservation and availability verification
    st.markdown("""
    <div class="section-header">
        <h2>📩 Reserva y Verificación de Disponibilidad</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="questionnaire-container">
        <p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 1.5rem;">
            Para verificar disponibilidad de lugares y horarios, o para reservar tu espacio en el 
            <strong>MUPCAMP 1:1</strong>, envíanos un mensaje por correo electrónico o WhatsApp.
        </p>
        <p style="font-size: 1.05rem; line-height: 1.7; margin-bottom: 1.5rem;">
            <strong style="color: #FFCC00;">Por favor incluye en tu mensaje:</strong>
        </p>
        <ul style="font-size: 1.05rem; line-height: 1.7; margin-bottom: 1.5rem;">
            <li>Tu nombre completo</li>
            <li>Horario(s) preferido(s)</li>
            <li>Tu correo electrónico o número de teléfono</li>
            <li>Si ya realizaste el pago (adjunta el comprobante) o solo deseas consultar disponibilidad</li>
        </ul>
        <p style="font-size: 1rem; line-height: 1.6; color: #888; margin-top: 1.5rem; font-style: italic;">
            💡 <strong>Nota:</strong> Recibirás una respuesta dentro de las siguientes 24 horas hábiles con la 
            confirmación de disponibilidad o instrucciones para completar tu reserva.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Contact buttons
    st.markdown("""
    <div style="display: flex; justify-content: center; gap: 2rem; margin: 2rem 0; flex-wrap: wrap;">
        <a href="mailto:administracion@muscleupgym.fitness?subject=Consulta%20MUPCAMP%201%3A1&body=Hola%2C%20me%20interesa%20el%20MUPCAMP%201%3A1.%0A%0ANombre%20completo%3A%20%0AHorario%20preferido%3A%20%0ATeléfono%2FEmail%3A%20%0AEstatus%20de%20pago%3A%20" 
           target="_blank" 
           style="text-decoration: none;">
            <div style="background: linear-gradient(135deg, #EA4335 0%, #D33B2C 100%); 
                        padding: 1.5rem 2rem; 
                        border-radius: 15px; 
                        box-shadow: 0 4px 15px rgba(234, 67, 53, 0.4); 
                        text-align: center; 
                        transition: all 0.3s ease;
                        border: 2px solid #EA4335;
                        cursor: pointer;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📧</div>
                <div style="color: white; font-size: 1.2rem; font-weight: bold;">Enviar Email</div>
                <div style="color: rgba(255,255,255,0.9); font-size: 0.9rem; margin-top: 0.3rem;">
                    administracion@muscleupgym.fitness
                </div>
            </div>
        </a>
        <a href="https://wa.me/528662580594?text=Hola%2C%20me%20interesa%20el%20MUPCAMP%201%3A1.%0A%0ANombre%20completo%3A%20%0AHorario%20preferido%3A%20%0ATeléfono%2FEmail%3A%20%0AEstatus%20de%20pago%3A%20" 
           target="_blank" 
           style="text-decoration: none;">
            <div style="background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); 
                        padding: 1.5rem 2rem; 
                        border-radius: 15px; 
                        box-shadow: 0 4px 15px rgba(37, 211, 102, 0.4); 
                        text-align: center; 
                        transition: all 0.3s ease;
                        border: 2px solid #25D366;
                        cursor: pointer;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📱</div>
                <div style="color: white; font-size: 1.2rem; font-weight: bold;">WhatsApp</div>
                <div style="color: rgba(255,255,255,0.9); font-size: 0.9rem; margin-top: 0.3rem;">
                    8662580594
                </div>
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="questionnaire-container" style="margin-top: 2rem;">
        <p style="font-size: 1rem; text-align: center; color: #888;">
            <strong>Si ya realizaste el pago:</strong> Adjunta tu comprobante de transferencia en el mensaje 
            junto con tu información de contacto y horario preferido.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Diplomas and certifications section
    st.markdown("""
    <div class="section-header">
        <h2>📜 Certificaciones y Formación del Coach</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Try to find and display diploma images
    diploma_patterns = [
        "*diploma*",
        "*cert*",
        "*certificacion*",
        "Copia de Anfitrión_20250809_125513_0000.png",
        "20250728_220454.jpg"
    ]
    
    diploma_files = []
    for pattern in diploma_patterns:
        matches = glob.glob(pattern)
        diploma_files.extend(matches)
    
    # Remove duplicates
    diploma_files = list(set(diploma_files))
    
    if diploma_files:
        st.markdown("""
        <div class="questionnaire-container">
            <p style="font-size: 1.05rem; margin-bottom: 1rem;">
             Quién te va a acompañar en el MUPCAMP 1:1

Erick Francisco De Luna Hernández
Responsable del área de metodología de entrenamiento y nutrición en Muscle Up Gym (más de 6 años de experiencia).

Formación académica

Licenciado en Ciencias del Ejercicio por la UANL, con:

Reconocimiento al Mérito Académico por el promedio más alto de su generación.

1er lugar de generación en la Licenciatura en Ciencias del Ejercicio.

Pertenencia al Programa Institucional Desarrollo de Talentos Universitarios durante 3 años, con beca del 100 % para titulación.

Estancia académica en la Universidad de Sevilla (España) en Ciencias de la Actividad Física y del Deporte.

Especialización y formación continua

ICEN Institute – Instituto de Ciencias del Ejercicio y Nutrición

Diplomado en Entrenamiento para Hipertrofia y Fisiología del Ejercicio.

Curso “Nutrición Inteligente para Mujeres: Ciencia, Ciclo Menstrual y Disponibilidad Energética”.

Participación en el I International Congress for the Improvement of Body Composition ICEN x MASS (enfoque en mejora de composición corporal basada en evidencia).

Football Science Institute (FSI) – Granada, España

Alumno del programa FSI Master Football Strength and Conditioning Coach (fuerza y acondicionamiento aplicados al fútbol).

Asistencia a la IV FSI Conference on High Performance in Football en el Estadio Benito Villamarín (Sevilla).

🎓 Formación destacada: <strong>Master FSI (Football Strength and Conditioning Coach)</strong> — concluido y aplicado en la práctica profesional.

Otros cursos y certificaciones en:

Acondicionamiento cardiovascular y rendimiento.

Evaluación y mejora de la composición corporal.

Actualización continua en entrenamiento de fuerza, nutrición deportiva y disponibilidad energética.

Experiencia profesional

Más de 6 años como encargado del área de metodología de entrenamiento y nutrición en Muscle Up Gym:

Diseño de sistemas de entrenamiento de fuerza y acondicionamiento para:

Fitness estético (ganancia de músculo y pérdida de grasa, únicamente con enfoque natural).

Salud y bienestar (mejora de marcadores de salud, calidad de vida y función).

Rendimiento deportivo, con énfasis en deportes de campo como el fútbol.

Planificación nutricional personalizada (déficit, mantenimiento, superávit) integrada al entrenamiento.

Seguimiento 1:1 de procesos de cambio de composición corporal y preparación para fases específicas (mini-cuts, recomposición, fases de volumen controlado).

Enfoque de trabajo

Integra ciencia del ejercicio, nutrición y contexto real de la persona (estrés, sueño, trabajo, familia).

Aplica principios de sistemas complejos y planificación inteligente, ajustando la dosis de entrenamiento (3, 4 o 5 sesiones/sem) y la nutrición al sistema de vida de cada persona.

Trabaja con cupos muy limitados para poder ofrecer un seguimiento cercano, detallado y profesional, similar al esquema de consulta de un especialista.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display diplomas in columns
        cols = st.columns(2)
        for idx, diploma_file in enumerate(diploma_files):
            try:
                with cols[idx % 2]:
                    st.image(diploma_file, use_container_width=True, caption=f"Certificación {idx + 1}")
            except (FileNotFoundError, Exception):
                pass
    else:
        st.markdown("""
        <div class="questionnaire-container">
            <p style="font-size: 1.05rem; text-align: center; color: #888;">
                Las certificaciones están disponibles para consulta en la evaluación inicial presencial.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Final CTA
    st.markdown("""
    <div class="results-container">
        <h3 style="text-align: center; font-size: 1.5rem; margin-bottom: 1rem;">📞 Contacto Directo</h3>
        <p style="font-size: 1.2rem; text-align: center; margin: 1rem 0;">
            <strong>📧 Email:</strong> administracion@muscleupgym.fitness
        </p>
        <p style="font-size: 1.2rem; text-align: center; margin: 1rem 0;">
            <strong>📱 WhatsApp:</strong> 8662580594
        </p>
        <p style="font-size: 1rem; text-align: center; margin-top: 1.5rem; color: #666;">
            ¿Tienes dudas sobre el programa? Contáctanos directamente y con gusto te atendemos.
        </p>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "body_and_energy":
    st.markdown("""
    <div class="section-header">
        <h2>BODY AND ENERGY</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Attractive centered button linking to MUPAI Digital Training Science
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0;">
        <a href="https://mupai-digital-training-science-fbeo.streamlit.app/" target="_blank" style="text-decoration: none;">
            <div class="attractive-button">
                <h2 style="margin: 0; color: #000; font-size: 1.8rem; font-weight: bold;">
                    ⚡ ACCEDER A BODY AND ENERGY
                </h2>
                <p style="margin: 0.5rem 0 0 0; color: #333; font-size: 1.1rem;">
                    Evaluación Avanzada de Balance Energético y Composición Corporal
                </p>
                <p style="margin: 0.5rem 0 0 0; color: #000; font-size: 1.2rem; font-weight: bold;">
                    👆 Da clic aquí para acceder
                </p>
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "food_preferences":
    st.markdown("""
    <div class="section-header">
        <h2>FOOD PREFERENCES</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Attractive centered button linking to Patrones Alimentarios
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0;">
        <a href="https://patronesalimentarios.streamlit.app/" target="_blank" style="text-decoration: none;">
            <div class="attractive-button">
                <h2 style="margin: 0; color: #000; font-size: 1.8rem; font-weight: bold;">
                    🍽️ ACCEDER A FOOD PREFERENCES
                </h2>
                <p style="margin: 0.5rem 0 0 0; color: #333; font-size: 1.1rem;">
                    Análisis Detallado de Patrones y Preferencias Alimentarias
                </p>
                <p style="margin: 0.5rem 0 0 0; color: #000; font-size: 1.2rem; font-weight: bold;">
                    👆 Da clic aquí para acceder
                </p>
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "designing_training":
    st.markdown("""
    <div class="section-header">
        <h2>DESIGNING YOUR TRAINING</h2>
        <p style="color: #ccc; margin-top: 0.5rem;">Cuestionario para Diseno de Programa de Entrenamiento Personalizado</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 1.5rem; border-radius: 12px;
                border-left: 5px solid #FFCC00; margin: 1rem 0; color: #fff;">
        <h4 style="color: #FFCC00; margin: 0 0 0.5rem 0;">Instrucciones</h4>
        <p style="margin: 0; color: #ccc;">Este cuestionario recopila la informacion necesaria para disenar tu programa de
        entrenamiento personalizado. Completa cada seccion con honestidad. <strong style="color: #FFCC00;">Tiempo estimado: 10-15 minutos.</strong></p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("designing_training_form"):

        # --- SECCION 1: DATOS PERSONALES ---
        st.markdown("""
        <div style="background: #1a1a2e; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #FFCC00; margin: 1rem 0;">
            <h3 style="color: #FFCC00;">Seccion 1: Datos Personales</h3>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            dt_nombre = st.text_input("Nombre completo*", placeholder="Tu nombre completo", key="dt_nombre")
            dt_email = st.text_input("Correo electronico*", placeholder="tu@email.com", key="dt_email")
            dt_edad = st.number_input("Edad*", min_value=16, max_value=80, value=25, key="dt_edad")
        with col2:
            dt_genero = st.selectbox("Sexo*", ["Masculino", "Femenino"], key="dt_genero")
            dt_peso = st.number_input("Peso (kg)*", min_value=40.0, max_value=200.0, value=70.0, step=0.1, key="dt_peso")
            dt_estatura = st.number_input("Estatura (cm)*", min_value=140, max_value=220, value=170, key="dt_estatura")

        # --- SECCION 2: EXPERIENCIA Y NIVEL ---
        st.markdown("""
        <div style="background: #1a1a2e; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #FFCC00; margin: 1rem 0;">
            <h3 style="color: #FFCC00;">Seccion 2: Experiencia y Nivel de Entrenamiento</h3>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            dt_experiencia = st.selectbox("Anos de experiencia en entrenamiento de fuerza*", [
                "Menos de 6 meses", "6 meses - 1 ano", "1-2 anos",
                "2-4 anos", "4-7 anos", "Mas de 7 anos"
            ], key="dt_exp")

            dt_nivel = st.selectbox("Nivel de entrenamiento*", [
                "Principiante", "Intermedio", "Avanzado"
            ], key="dt_nivel")

            st.markdown("""
            **Guia de niveles:**
            - **Principiante:** <1 ano, tecnica limitada en ejercicios basicos
            - **Intermedio:** 1-4 anos consistente, buena tecnica en compuestos
            - **Avanzado:** >4 anos, dominio tecnico completo
            """)

        with col2:
            dt_rutina_actual = st.selectbox("Rutina actual*", [
                "No, entreno sin plan fijo",
                "Si, rutina basica autodirigida",
                "Si, programa con periodizacion simple",
                "Si, programa avanzado con periodizacion"
            ], key="dt_rutina")

            dt_consistencia = st.selectbox("Consistencia ultimos 3 meses*", [
                "No he entrenado",
                "Esporadico (1-2 veces/semana inconsistente)",
                "Regular (3+ veces/semana, con algunas faltas)",
                "Muy consistente (entreno segun plan sin faltar)"
            ], key="dt_consist")

        # --- SECCION 3: OBJETIVO Y DISPONIBILIDAD ---
        st.markdown("""
        <div style="background: #1a1a2e; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #FFCC00; margin: 1rem 0;">
            <h3 style="color: #FFCC00;">Seccion 3: Objetivo y Disponibilidad</h3>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            dt_objetivo = st.selectbox("Objetivo principal de entrenamiento*", [
                "Hipertrofia", "Fuerza", "Recomposicion corporal", "Resistencia muscular"
            ], key="dt_obj")

            st.markdown("""
            - **Hipertrofia:** Maximo desarrollo de masa muscular
            - **Fuerza:** Maximo desarrollo de fuerza (1RM)
            - **Recomposicion:** Ganar musculo y perder grasa
            - **Resistencia muscular:** Capacidad de trabajo muscular sostenido
            """)

            dt_frecuencia = st.number_input("Dias disponibles para entrenar por semana*",
                                            min_value=2, max_value=6, value=4, key="dt_freq")

        with col2:
            dt_duracion = st.selectbox("Duracion disponible por sesion*", [
                "45 minutos", "60 minutos", "75 minutos", "90 minutos", "120 minutos"
            ], key="dt_dur")

            dt_horario = st.selectbox("Horario preferido", [
                "Manana (6-9 AM)", "Media manana (9-12 PM)",
                "Tarde (12-3 PM)", "Tarde-noche (3-6 PM)",
                "Noche (6-9 PM)", "Sin preferencia"
            ], key="dt_horario")

            dt_dias_especificos = st.multiselect(
                "Dias especificos disponibles (opcional)",
                ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"],
                key="dt_dias"
            )

        # --- SECCION 4: EQUIPO DISPONIBLE ---
        st.markdown("""
        <div style="background: #1a1a2e; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #FFCC00; margin: 1rem 0;">
            <h3 style="color: #FFCC00;">Seccion 4: Equipo Disponible</h3>
        </div>
        """, unsafe_allow_html=True)

        dt_ubicacion = st.selectbox("Donde entrenas?*", [
            "Gimnasio comercial completo",
            "Gimnasio basico (equipo limitado)",
            "Home gym / Gimnasio casero",
            "Al aire libre / Calistenia",
            "Muscle Up Gym"
        ], key="dt_ubic")

        equipo_default = OPCIONES_EQUIPO[:8] if dt_ubicacion in ["Gimnasio comercial completo", "Muscle Up Gym"] else []
        dt_equipo = st.multiselect(
            "Selecciona TODO el equipo disponible*",
            OPCIONES_EQUIPO,
            default=equipo_default,
            key="dt_equipo"
        )

        # --- SECCION 5: PRIORIDADES MUSCULARES ---
        st.markdown("""
        <div style="background: #1a1a2e; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #FFCC00; margin: 1rem 0;">
            <h3 style="color: #FFCC00;">Seccion 5: Prioridades Musculares</h3>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            dt_prioridades = st.multiselect(
                "Grupos musculares a PRIORIZAR (maximo 3)*",
                ["Pecho", "Espalda", "Hombros", "Cuadriceps",
                 "Isquiotibiales / Gluteos", "Biceps", "Triceps", "Core", "Pantorrillas"],
                max_selections=3,
                key="dt_prior"
            )
        with col2:
            dt_debiles = st.multiselect(
                "Puntos debiles percibidos (opcional)",
                ["Pecho", "Espalda", "Hombros", "Cuadriceps",
                 "Isquiotibiales / Gluteos", "Biceps", "Triceps", "Core", "Pantorrillas"],
                key="dt_debil"
            )

        # --- SECCION 6: SELECCION DE EJERCICIOS ---
        st.markdown("""
        <div style="background: #1a1a2e; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #FFCC00; margin: 1rem 0;">
            <h3 style="color: #FFCC00;">Seccion 6: Seleccion de Ejercicios</h3>
            <p style="color: #ccc; margin: 0.5rem 0 0 0;">Selecciona los ejercicios que conoces, dominas o deseas incluir.
            Se filtran por tu nivel y equipo disponible. Consulta la
            <strong style="color: #FFCC00;">Biblioteca de Ejercicios MUPAI (PDF)</strong> para detalles tecnicos.</p>
        </div>
        """, unsafe_allow_html=True)

        # Filtrar ejercicios
        ejercicios_disponibles = filtrar_ejercicios_por_nivel(dt_nivel)
        if dt_equipo:
            ejercicios_disponibles = filtrar_ejercicios_por_equipo(ejercicios_disponibles, dt_equipo)

        ejercicios_seleccionados = {}
        for patron, grupos in ejercicios_disponibles.items():
            with st.expander(f"{patron}", expanded=False):
                for grupo, ejercicios in grupos.items():
                    if ejercicios:
                        nombres = [ej["nombre"] for ej in ejercicios]
                        seleccion = st.multiselect(
                            f"{grupo}",
                            nombres,
                            key=f"ej_{patron}_{grupo}"
                        )
                        if seleccion:
                            if patron not in ejercicios_seleccionados:
                                ejercicios_seleccionados[patron] = []
                            ejercicios_seleccionados[patron].extend(seleccion)

        # --- SECCION 7: PRUEBAS FUNCIONALES ---
        st.markdown("""
        <div style="background: #1a1a2e; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #FFCC00; margin: 1rem 0;">
            <h3 style="color: #FFCC00;">Seccion 7: Pruebas Funcionales (AMRAP / 1RM)</h3>
            <p style="color: #ccc; margin: 0.5rem 0 0 0;">Si no puedes realizar el ejercicio o eres novato, coloca <strong style="color: #FFCC00;">0</strong>.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: #16213e; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; color: #ccc;">
            <strong style="color: #FFCC00;">Protocolo AMRAP:</strong> Calentamiento 5-10 min, luego maximas repeticiones con tecnica correcta. Detente cuando la tecnica se deteriore.
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            dt_lagartijas = st.number_input("Lagartijas maximas en 1 serie", min_value=0, max_value=200, value=0, key="dt_lag")
            dt_dominadas = st.number_input("Dominadas maximas en 1 serie", min_value=0, max_value=100, value=0, key="dt_dom")
            dt_sentadillas_bw = st.number_input("Sentadillas BW maximas en 1 serie", min_value=0, max_value=200, value=0, key="dt_sqbw")
        with col2:
            dt_plancha = st.number_input("Plancha frontal (segundos maximos)", min_value=0, max_value=600, value=0, key="dt_plank")
            dt_bench_1rm = st.number_input("Press banca 1RM estimado (kg) - Si lo conoces", min_value=0.0, max_value=300.0, value=0.0, step=2.5, key="dt_bench")
            dt_squat_1rm = st.number_input("Sentadilla 1RM estimado (kg) - Si lo conoces", min_value=0.0, max_value=400.0, value=0.0, step=2.5, key="dt_sq1rm")

        dt_dead_1rm = st.number_input("Peso muerto 1RM estimado (kg) - Si lo conoces", min_value=0.0, max_value=500.0, value=0.0, step=2.5, key="dt_dead")

        dt_conoce_rpe = st.selectbox("Conoces la escala RPE?", [
            "No, no la conozco", "La conozco pero no la uso", "Si, la uso regularmente"
        ], key="dt_rpe")

        # --- SECCION 8: LESIONES ---
        st.markdown("""
        <div style="background: #1a1a2e; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #FFCC00; margin: 1rem 0;">
            <h3 style="color: #FFCC00;">Seccion 8: Lesiones y Limitaciones</h3>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            dt_lesiones_actuales = st.text_area(
                "Lesiones actuales (o escribe 'Ninguna')*",
                placeholder="Ej: Dolor en hombro derecho, molestia en rodilla izquierda...",
                key="dt_les_act"
            )
        with col2:
            dt_lesiones_pasadas = st.text_area(
                "Lesiones pasadas relevantes (o escribe 'Ninguna')",
                placeholder="Ej: Operacion de menisco hace 2 anos...",
                key="dt_les_pas"
            )

        dt_limitaciones = st.multiselect(
            "Limitacion o dolor en alguno de estos movimientos?",
            [
                "Press por encima de la cabeza (overhead)",
                "Sentadilla profunda",
                "Peso muerto desde el suelo",
                "Rotacion de hombro",
                "Extension de rodilla completa",
                "Flexion de cadera profunda",
                "Dominadas / colgarse de barra",
                "Ninguna limitacion"
            ],
            key="dt_limit"
        )

        # --- SECCION 9: PREFERENCIAS ADICIONALES ---
        st.markdown("""
        <div style="background: #1a1a2e; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #FFCC00; margin: 1rem 0;">
            <h3 style="color: #FFCC00;">Seccion 9: Preferencias y Observaciones</h3>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            dt_cardio = st.selectbox("Realizas cardio adicional?", [
                "No", "Si, 1-2 veces/semana (ligero)",
                "Si, 3+ veces/semana",
                "Si, hago deporte adicional (futbol, natacion, etc.)"
            ], key="dt_cardio")

            dt_deload = st.selectbox("Sabes que es un deload (semana de descarga)?", [
                "No, no lo conozco", "Si, pero nunca los hago", "Si, los implemento regularmente"
            ], key="dt_deload")

        with col2:
            dt_suplementos = st.multiselect("Suplementos actuales (opcional)", [
                "Creatina", "Proteina en polvo (whey/caseina)",
                "Cafeina/Pre-workout", "BCAA/EAA", "Multivitaminico",
                "Omega-3", "Ninguno"
            ], key="dt_supps")

            dt_sueno = st.selectbox("Horas promedio de sueno por noche", [
                "Menos de 5h", "5-6h", "6-7h", "7-8h", "8-9h", "Mas de 9h"
            ], key="dt_sueno")

        dt_observaciones = st.text_area(
            "Observaciones adicionales para tu coach (opcional)",
            placeholder="Alergias, medicamentos, horarios especiales, motivaciones...",
            key="dt_obs"
        )

        dt_legal = st.checkbox(
            "Acepto los terminos y condiciones y autorizo el procesamiento de mis datos para fines de diseno de programa de entrenamiento personalizado*",
            key="dt_legal"
        )

        # --- SUBMIT ---
        dt_submitted = st.form_submit_button(
            "Generar Analisis y Diseno de Programa de Entrenamiento",
            type="primary", use_container_width=True
        )

        if dt_submitted:
            # Validaciones
            if not dt_nombre:
                st.error("El nombre completo es obligatorio")
            elif not dt_email:
                st.error("El correo electronico es obligatorio")
            elif not dt_legal:
                st.error("Debes aceptar los terminos y condiciones")
            elif not dt_equipo:
                st.error("Debes seleccionar al menos un tipo de equipo")
            else:
                # Calculos
                duracion_min = int(dt_duracion.split()[0])
                mapa_obj = {"Hipertrofia": "Hipertrofia", "Fuerza": "Fuerza",
                            "Recomposicion corporal": "Recomposicion", "Resistencia muscular": "Resistencia muscular"}
                objetivo_calc = mapa_obj.get(dt_objetivo, "Hipertrofia")

                freq = dt_frecuencia
                if freq in SPLITS_ENTRENAMIENTO:
                    split_info = SPLITS_ENTRENAMIENTO[freq]
                else:
                    split_info = SPLITS_ENTRENAMIENTO[min(SPLITS_ENTRENAMIENTO.keys(), key=lambda x: abs(x - freq))]

                distribucion_vol = calcular_distribucion_volumen(objetivo_calc, dt_nivel, dt_prioridades)
                esquema_reps = determinar_esquema_reps(objetivo_calc, dt_nivel)

                # Pruebas funcionales
                pruebas = {}
                if dt_lagartijas > 0: pruebas["Lagartijas maximas"] = dt_lagartijas
                if dt_dominadas > 0: pruebas["Dominadas maximas"] = dt_dominadas
                if dt_sentadillas_bw > 0: pruebas["Sentadillas BW maximas"] = dt_sentadillas_bw
                if dt_plancha > 0: pruebas["Plancha (segundos)"] = dt_plancha
                if dt_bench_1rm > 0: pruebas["Press banca 1RM (kg)"] = dt_bench_1rm
                if dt_squat_1rm > 0: pruebas["Sentadilla 1RM (kg)"] = dt_squat_1rm
                if dt_dead_1rm > 0: pruebas["Peso muerto 1RM (kg)"] = dt_dead_1rm

                # Lesiones
                lesiones_txt = ""
                if dt_lesiones_actuales and dt_lesiones_actuales.strip().lower() != "ninguna":
                    lesiones_txt += f"Actuales: {dt_lesiones_actuales}\n"
                if dt_lesiones_pasadas and dt_lesiones_pasadas.strip().lower() != "ninguna":
                    lesiones_txt += f"Pasadas: {dt_lesiones_pasadas}\n"
                if dt_limitaciones and "Ninguna limitacion" not in dt_limitaciones:
                    lesiones_txt += f"Limitaciones: {', '.join(dt_limitaciones)}"
                if not lesiones_txt:
                    lesiones_txt = "Sin lesiones o limitaciones reportadas"

                datos_reporte = {
                    "nombre": dt_nombre, "email": dt_email, "edad": dt_edad,
                    "genero": dt_genero, "peso": dt_peso, "estatura": dt_estatura,
                    "nivel": dt_nivel, "experiencia": dt_experiencia,
                    "objetivo": objetivo_calc, "frecuencia": freq,
                    "duracion_sesion": dt_duracion, "consistencia": dt_consistencia,
                    "rutina_actual": dt_rutina_actual, "ubicacion": dt_ubicacion,
                    "equipo": dt_equipo, "prioridades": dt_prioridades,
                    "puntos_debiles": dt_debiles, "split_nombre": split_info["nombre"],
                    "split_descripcion": split_info["descripcion"],
                    "distribucion_volumen": distribucion_vol,
                    "esquema_reps": esquema_reps,
                    "ejercicios_seleccionados": ejercicios_seleccionados,
                    "pruebas_funcionales": pruebas, "lesiones": lesiones_txt,
                    "cardio": dt_cardio, "deload": dt_deload,
                    "conoce_rpe": dt_conoce_rpe, "suplementos": dt_suplementos,
                    "sueno": dt_sueno, "observaciones": dt_observaciones if dt_observaciones else "Sin observaciones"
                }

                # --- MOSTRAR RESULTADOS ---
                st.markdown("---")
                st.markdown("""
                <div style="background: linear-gradient(135deg, #FFCC00 0%, #FFE066 50%, #FFA500 100%);
                            padding: 2rem; border-radius: 15px; text-align: center; margin: 1rem 0; color: #000;">
                    <h2>RESULTADOS - DESIGNING YOUR TRAINING</h2>
                    <p>Analisis para diseno de programa personalizado</p>
                </div>
                """, unsafe_allow_html=True)

                # Perfil
                st.markdown("### Perfil de Entrenamiento")
                col1, col2, col3, col4 = st.columns(4)
                with col1: st.metric("Nivel", dt_nivel)
                with col2: st.metric("Objetivo", objetivo_calc)
                with col3: st.metric("Frecuencia", f"{freq} dias/sem")
                with col4: st.metric("Sesion", dt_duracion)

                # Split
                st.markdown("### Split de Entrenamiento Recomendado")
                st.markdown(f"""
                <div style="background: #1a1a2e; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #FFCC00; margin: 1rem 0;">
                    <h4 style="color: #FFCC00;">{split_info['nombre']}</h4>
                    <p style="color: #ccc;">{split_info['descripcion']}</p>
                </div>
                """, unsafe_allow_html=True)

                for dia_nombre, patrones in split_info["dias"].items():
                    with st.expander(f"{dia_nombre}"):
                        for p in patrones:
                            st.write(f"- {p}")

                # Volumen
                st.markdown("### Volumen Semanal por Grupo Muscular")
                vol_df = pd.DataFrame({
                    "Patron de Movimiento": list(distribucion_vol.keys()),
                    "Series/Semana": list(distribucion_vol.values())
                })
                st.dataframe(vol_df, use_container_width=True, hide_index=True)

                # Esquema de reps
                st.markdown("### Esquema de Repeticiones y Descanso")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    <div style="background: #1a1a2e; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #FFCC00; margin: 0.5rem 0; color: #fff;">
                        <h4 style="color: #FFCC00;">Ejercicios Compuestos</h4>
                        <p><strong>Repeticiones:</strong> {esquema_reps['reps_compuesto']}</p>
                        <p><strong>Series:</strong> {esquema_reps['series_compuesto']}</p>
                        <p><strong>Descanso:</strong> {esquema_reps['descanso_compuesto']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div style="background: #1a1a2e; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #FFCC00; margin: 0.5rem 0; color: #fff;">
                        <h4 style="color: #FFCC00;">Ejercicios de Aislamiento</h4>
                        <p><strong>Repeticiones:</strong> {esquema_reps['reps_aislamiento']}</p>
                        <p><strong>Series:</strong> {esquema_reps['series_aislamiento']}</p>
                        <p><strong>Descanso:</strong> {esquema_reps['descanso_aislamiento']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.info(f"**RPE Objetivo:** {esquema_reps['rpe']} | **Tempo:** {esquema_reps['tempo']} (excentrica-pausa-concentrica-pausa)")

                # Ejercicios seleccionados
                if ejercicios_seleccionados:
                    st.markdown("### Ejercicios Seleccionados")
                    for patron, ejs in ejercicios_seleccionados.items():
                        if ejs:
                            st.markdown(f"**{patron}:**")
                            for ej in ejs:
                                st.write(f"  - {ej}")

                # Pruebas funcionales
                if pruebas:
                    st.markdown("### Resultados de Pruebas Funcionales")
                    cols_pruebas = st.columns(min(len(pruebas), 4))
                    for i, (nombre_prueba, valor) in enumerate(pruebas.items()):
                        with cols_pruebas[i % len(cols_pruebas)]:
                            st.metric(nombre_prueba, valor)

                # Advertencias
                advertencias = []
                if dt_nivel == "Principiante" and freq > 4:
                    advertencias.append("Frecuencia alta para principiante. Considerar 3-4 dias.")
                if dt_nivel == "Avanzado" and freq < 4:
                    advertencias.append("Frecuencia baja para avanzado. Podrias beneficiarte de mas dias.")
                if dt_limitaciones and "Ninguna limitacion" not in dt_limitaciones:
                    advertencias.append(f"Limitaciones reportadas: {', '.join(dt_limitaciones)}. El coach ajustara ejercicios.")
                if not pruebas:
                    advertencias.append("Sin pruebas funcionales. Se recomienda realizarlas para prescripcion mas precisa.")

                if advertencias:
                    st.markdown("### Advertencias y Notas")
                    for adv in advertencias:
                        st.warning(adv)

                # --- AREA DEL COACH ---
                st.markdown("---")
                st.markdown("### Area Exclusiva del Coach")
                dt_coach_pw = st.text_input("Contrasena del Coach:", type="password", key="dt_coach_pw")

                if dt_coach_pw == "MuPai2025":
                    st.success("Coach MUPAI verificado")
                    reporte = generar_reporte_entrenamiento(datos_reporte)
                    st.text_area("Reporte Completo:", reporte, height=500)

                    st.download_button(
                        label="Descargar Reporte de Entrenamiento (TXT)",
                        data=reporte,
                        file_name=f"designing_training_{dt_nombre.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )

                    json_data = json.dumps(datos_reporte, ensure_ascii=False, indent=2, default=str)
                    st.download_button(
                        label="Descargar Datos (JSON)",
                        data=json_data,
                        file_name=f"training_data_{dt_nombre.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                elif dt_coach_pw:
                    st.error("Acceso denegado.")

                # Confirmacion al cliente
                st.markdown("---")
                st.success(f"""
                **Cuestionario completado exitosamente!**

                Estimado/a {dt_nombre}: Tu evaluacion para diseno de programa de entrenamiento ha sido procesada.

                **Proximos pasos:**
                1. Tu coach MUPAI revisara tus respuestas y pruebas funcionales
                2. Se disenara un programa personalizado basado en tu nivel, objetivos y equipo
                3. Recibiras tu programa en formato profesional (PDF)

                **Tiempo de entrega:** 3-5 dias habiles
                """)

elif st.session_state.page == "about":
    st.markdown("""
    <div class="professional-header">
        <h2>SOBRE EL PROFESIONAL Y CONTACTO</h2>
        <p style="margin-top: 1rem; color: #666; font-size: 1rem;">👨‍⚕️ Acerca del Profesional</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main professional images - improved responsive styling
    st.markdown("""
    <div class='professional-images' style='text-align: center; margin: 2rem 0; display: flex; flex-direction: column; align-items: center; gap: 1.5rem;'>
    """, unsafe_allow_html=True)
    
    # First image - responsive with max width
    try:
        from PIL import Image
        main_image = Image.open("Copia de Anfitrión_20250809_125513_0000.png")
        st.image(main_image, caption="Coach Erick - Especialista MUPAI", use_container_width=True)
    except:
        st.info("🏢 Imagen Principal del Profesional")
    
    # Second image - responsive with max width
    try:
        secondary_image = Image.open("20250728_220454.jpg")
        st.image(secondary_image, caption="Imagen Secundaria Profesional", use_container_width=True)
    except:
        st.info("📸 Imagen Secundaria del Profesional")
    
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "contacto":
    st.markdown("""
    <div class="contact-section">
        <h2 class="contact-title">💬 CONTACTO</h2>
        <p class="contact-description">Da clic para comunicarte en el medio que necesites</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Contact icons using responsive layout
    st.markdown("""
    <div class="contact-icons">
        <div style="text-align: center;">
            <a href="https://wa.me/528662580594" target="_blank" style="text-decoration: none;">
                <div class="contact-icon whatsapp">
                    📱
                </div>
            </a>
            <p style="color: #333; font-size: 0.9rem; margin-top: 0.5rem; font-weight: bold;">WhatsApp</p>
        </div>
        <div style="text-align: center;">
            <a href="mailto:administracion@muscleupgym.fitness" style="text-decoration: none;">
                <div class="contact-icon email">
                    📧
                </div>
            </a>
            <p style="color: #333; font-size: 0.9rem; margin-top: 0.5rem; font-weight: bold;">Email</p>
        </div>
        <div style="text-align: center;">
            <a href="https://www.facebook.com/share/16WtR5TLw5/" target="_blank" style="text-decoration: none;">
                <div class="contact-icon facebook">
                    📘
                </div>
            </a>
            <p style="color: #333; font-size: 0.9rem; margin-top: 0.5rem; font-weight: bold;">Facebook</p>
        </div>
        <div style="text-align: center;">
            <a href="https://www.instagram.com/mup_lindavista" target="_blank" style="text-decoration: none;">
                <div class="contact-icon instagram">
                    📷
                </div>
            </a>
            <p style="color: #333; font-size: 0.9rem; margin-top: 0.5rem; font-weight: bold;">Instagram</p>
        </div>
        <div style="text-align: center;">
            <a href="https://muscleupgym.fitness/planes" target="_blank" style="text-decoration: none;">
                <div class="contact-icon website">
                    🌐
                </div>
            </a>
            <p style="color: #333; font-size: 0.9rem; margin-top: 0.5rem; font-weight: bold;">Página web matriz</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 1.5rem;">
        <p style="color: #333; font-size: 0.9rem; font-style: italic;">
            Respuesta garantizada en 24-48 horas
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Información de contacto detallada
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                padding: 2rem; border-radius: 15px; margin: 2rem 0; 
                border: 3px solid #FFCC00; box-shadow: 0 6px 20px rgba(255,204,0,0.3);">
        <h3 style="color: #FFCC00; text-align: center; margin-bottom: 1.5rem;">📞 Información de Contacto Muscle Up Gym</h3>
        <div style="color: #FFFFFF; font-size: 1.1rem; line-height: 1.8;">
            <p><strong style="color: #FFCC00;">📧 Correo:</strong> administracion@muscleupgym.fitness</p>
            <p><strong style="color: #FFCC00;">📱 WhatsApp:</strong> 8662580594</p>
            <p><strong style="color: #FFCC00;">📘 Facebook:</strong> Muscle Up Gym</p>
            <p><strong style="color: #FFCC00;">📷 Instagram:</strong> @mup_lindavista | @erickmuscleup</p>
            <p><strong style="color: #FFCC00;">🌐 Sitio Web:</strong> www.muscleupgym.fitness</p>
        </div>
        <div style="text-align: center; margin-top: 1.5rem; padding: 1rem; 
                    background: rgba(255,204,0,0.1); border-radius: 10px;">
            <p style="color: #FFCC00; font-weight: bold; margin: 0; font-size: 1.2rem;">
                ¡Agenda tu cita y recibe asesoría profesional!
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
logo_base64_footer = load_logo_image_base64()
if logo_base64_footer:
    footer_logo_html = f'<img src="{logo_base64_footer}" style=\'width: 120px; height: 120px; object-fit: contain;\'>'
else:
    footer_logo_html = '<div style="width: 120px; height: 120px; background-color: #ffcc00; display: flex; align-items: center; justify-content: center; color: #000; font-weight: bold; font-size: 2rem;">MUPAI</div>'

st.markdown(f"""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 10px; border: 1px solid #FFCC00;">
    <div style='margin-bottom: 1.5rem;'>
        {footer_logo_html}
    </div>
    <div style="display: flex; justify-content: center; gap: 1rem; margin: 1rem 0; flex-wrap: wrap;">
        <a href="https://www.facebook.com/share/16WtR5TLw5/" target="_blank" style="color: #4267B2; text-decoration: none;">📘 Facebook</a>
        <a href="https://www.instagram.com/mup_lindavista" target="_blank" style="color: #E4405F; text-decoration: none;">📷 Instagram</a>
        <a href="https://wa.me/528662580594" target="_blank" style="color: #25D366; text-decoration: none;">📱 WhatsApp</a>
        <a href="mailto:administracion@muscleupgym.fitness" style="color: #EA4335; text-decoration: none;">📧 Email</a>
        <a href="https://muscleupgym.fitness/planes" target="_blank" style="color: #FFCC00; text-decoration: none;">🌐 Planes Matriz</a>
    </div>
    <p style="color: #CCCCCC; font-size: 0.9rem;">© 2025 MUPAI - Muscle up GYM Digital Training Science Performance Assessment Intelligence</p>
</div>
""", unsafe_allow_html=True)
