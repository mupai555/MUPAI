#!/usr/bin/env python3
"""
MUPAI - Advanced Energy Balance and Macronutrient Allocation Questionnaire
==========================================================================

A comprehensive scientific questionnaire system for optimal energy balance calculation
and intelligent macronutrient distribution based on individual characteristics,
activity levels, sleep quality, stress levels, and recovery factors.

Author: MUPAI Team
Version: 2.0
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime
from typing import Dict, Tuple, Any
import math
import base64
import os


# =============================================================================
# CONFIGURATION AND CONSTANTS
# =============================================================================

# Configure Streamlit page
st.set_page_config(
    page_title="MUPAI - Cuestionario Avanzado de Balance Energético",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Coach credentials
COACH_PASSWORD = "MuPai2025"
COACH_EMAIL = "mupaitraining@outlook.com"

# Scientific constants
PROTEIN_KCAL_PER_G = 4
FAT_KCAL_PER_G = 9
CARB_KCAL_PER_G = 4
ETA_FACTOR = 1.15  # Thermic Effect of Activity

# =============================================================================
# STYLING
# =============================================================================

st.markdown("""
<style>
    /* Navigation Banner */
    .navigation-banner {
        background: linear-gradient(135deg, #FFCC00 0%, #FFD700 50%, #FFA500 100%);
        padding: 1rem 2rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        color: #000;
        position: relative;
        z-index: 100;
    }
    
    .navigation-banner h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
        font-weight: bold;
        color: #000;
    }
    
    .navigation-banner p {
        margin: 0;
        font-size: 1rem;
        font-weight: 500;
        color: #333;
        line-height: 1.4;
    }
    
    .navigation-banner .emoji {
        font-size: 1.3rem;
        margin-right: 0.5rem;
    }
    
    /* Mobile responsiveness for banner */
    @media (max-width: 768px) {
        .navigation-banner {
            padding: 0.8rem 1rem;
            margin-bottom: 1rem;
        }
        
        .navigation-banner h3 {
            font-size: 1rem;
        }
        
        .navigation-banner p {
            font-size: 0.9rem;
        }
    }
    
    @media (max-width: 480px) {
        .navigation-banner {
            padding: 0.7rem 0.8rem;
        }
        
        .navigation-banner h3 {
            font-size: 0.95rem;
        }
        
        .navigation-banner p {
            font-size: 0.85rem;
        }
    }
    
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
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .section-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
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
    .warning-container {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        border-left: 5px solid #ff3333;
    }
    .info-container {
        background: linear-gradient(135deg, #74b9ff 0%, #a29bfe 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        border-left: 5px solid #0984e3;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #FFCC00;
        margin: 0.5rem 0;
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
    
    /* Professional Images Container - Always Stacked and Centered */
    .professional-images {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 2rem;
        margin: 2rem auto;
        text-align: center;
        max-width: 100%;
    }
    
    .professional-images img {
        max-width: 100% !important;
        height: auto !important;
        display: block !important;
        margin: 0 auto !important;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Ensure images are properly sized on different devices */
    .professional-images .main-image {
        max-width: 800px;
        width: 100%;
    }
    
    .professional-images .secondary-image {
        max-width: 600px;
        width: 100%;
    }
    
    /* Plans Information Banner */
    .plans-info-banner {
        background: linear-gradient(135deg, #74b9ff 0%, #a29bfe 50%, #6c5ce7 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        border-left: 5px solid #0984e3;
    }
    
    .plans-info-banner h3 {
        margin: 0 0 1rem 0;
        font-size: 1.4rem;
        font-weight: bold;
        color: white;
    }
    
    .plans-info-banner p {
        margin: 0;
        font-size: 1.1rem;
        font-weight: 500;
        line-height: 1.5;
        color: #f1f2f6;
    }
    
    .plans-info-banner .emoji {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    
    /* Mobile responsiveness for plans banner */
    @media (max-width: 768px) {
        .plans-info-banner {
            padding: 1.5rem;
            margin: 1.5rem 0;
        }
        
        .plans-info-banner h3 {
            font-size: 1.2rem;
        }
        
        .plans-info-banner p {
            font-size: 1rem;
        }
    }
    
    @media (max-width: 480px) {
        .plans-info-banner {
            padding: 1rem;
            margin: 1rem 0;
        }
        
        .plans-info-banner h3 {
            font-size: 1.1rem;
        }
        
        .plans-info-banner p {
            font-size: 0.9rem;
        }
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
        gap: 1.5rem;
        flex-wrap: wrap;
        margin: 1.5rem 0;
    }
    
    .contact-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        text-decoration: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        font-size: 2.5rem;
        color: white;
    }
    
    .contact-icon:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
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
    
    /* Mobile Responsive Styles */
    @media (max-width: 768px) {
        .professional-header {
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }
        
        .professional-header h2 {
            font-size: 1.5rem;
        }
        
        .professional-images {
            gap: 1.5rem;
            margin: 1.5rem auto;
        }
        
        .professional-images .main-image {
            max-width: 100%;
        }
        
        .professional-images .secondary-image {
            max-width: 100%;
        }
        
        .contact-section {
            padding: 1.5rem;
            margin: 1.5rem 0;
        }
        
        .contact-title {
            font-size: 1.5rem;
        }
        
        .contact-description {
            font-size: 1rem;
            margin-bottom: 1.5rem;
        }
        
        .contact-icons {
            gap: 1rem;
        }
        
        .contact-icon {
            width: 70px;
            height: 70px;
            font-size: 2rem;
        }
    }
    
    @media (max-width: 480px) {
        .professional-header {
            padding: 1rem;
        }
        
        .professional-header h2 {
            font-size: 1.3rem;
        }
        
        .professional-images {
            gap: 1rem;
            margin: 1rem auto;
        }
        
        .contact-section {
            padding: 1rem;
        }
        
        .contact-title {
            font-size: 1.3rem;
        }
        
        .contact-description {
            font-size: 0.9rem;
        }
        
        .contact-icon {
            width: 60px;
            height: 60px;
            font-size: 1.8rem;
        }
        
        .contact-icons {
            gap: 0.8rem;
        }
    }
    
    /* Sidebar Compact Spacing Optimization */
    /* Target main sidebar container */
    .css-1d391kg {
        padding-top: 1rem !important;
        padding-bottom: 0.5rem !important;
    }
    
    .css-1d391kg .stSelectbox {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .css-1d391kg h2 {
        margin-bottom: 0.5rem !important;
        margin-top: 0.5rem !important;
    }
    
    .css-1d391kg .stSelectbox > div {
        margin-bottom: 0.5rem !important;
    }
    
    .css-1d391kg hr {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* More specific sidebar selectors */
    .css-1cypcdb {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
    }
    
    .css-1cypcdb h2 {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
        line-height: 1.2 !important;
    }
    
    /* Selectbox specific spacing */
    .css-1cypcdb .stSelectbox {
        margin-top: 0.3rem !important;
        margin-bottom: 0.3rem !important;
    }
    
    .css-1cypcdb .stSelectbox > label {
        margin-bottom: 0.3rem !important;
    }
    
    /* Separator line spacing */
    .css-1cypcdb .element-container {
        margin-bottom: 0.5rem !important;
    }
    
    /* More robust sidebar targeting using multiple selectors */
    [data-testid="stSidebar"] {
        padding-top: 0.5rem !important;
    }
    
    [data-testid="stSidebar"] h2 {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
        padding-top: 0 !important;
        padding-bottom: 0.3rem !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox {
        margin-top: 0.3rem !important;
        margin-bottom: 0.3rem !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox > label {
        margin-bottom: 0.2rem !important;
        padding-bottom: 0.2rem !important;
    }
    
    [data-testid="stSidebar"] hr {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    [data-testid="stSidebar"] .element-container {
        margin-bottom: 0.3rem !important;
        padding-bottom: 0.3rem !important;
    }
    
    /* Additional universal sidebar spacing reduction */
    .css-1lcbmhc, .css-1siy2j7, .css-12ttj6m {
        padding-top: 0.5rem !important;
        padding-bottom: 0.3rem !important;
        margin-top: 0.3rem !important;
        margin-bottom: 0.3rem !important;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def display_navigation_banner():
    """Display the navigation banner that promotes sidebar usage."""
    st.markdown("""
    <div class="navigation-banner">
        <h3><span class="emoji">👉</span>¡Descubre todos los menús y detalles de MUPAI!</h3>
        <p>Haz clic en el ícono <strong>☰</strong> (esquina superior izquierda) para desplegar el menú lateral y acceder a todos los menús y la información detallada de MUPAI.</p>
    </div>
    """, unsafe_allow_html=True)


def display_plans_info_banner():
    """Display the plans information banner on the home page."""
    st.markdown("""
    <div class="plans-info-banner">
        <h3><span class="emoji">📋</span>¿Quieres conocer todos los detalles y el proceso para adquirir un plan?</h3>
        <p>Consulta el menú lateral <strong>"Planes y Costos"</strong> para ver información detallada de cada plan y la mecánica de adquisición paso a paso.</p>
    </div>
    """, unsafe_allow_html=True)


def get_base64_of_image(image_path: str) -> str:
    """
    Convert image file to base64 string for embedding in HTML.
    
    Args:
        image_path: Path to the image file
    
    Returns:
        Base64 encoded string of the image
    """
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Error loading image {image_path}: {e}")
        return ""

def create_image_html(image_path: str, alt_text: str, max_width: int = 400) -> str:
    """
    Create HTML img tag with base64 encoded image.
    
    Args:
        image_path: Path to the image file
        alt_text: Alt text for the image
        max_width: Maximum width in pixels
    
    Returns:
        HTML img tag string
    """
    base64_image = get_base64_of_image(image_path)
    if base64_image:
        file_extension = os.path.splitext(image_path)[1].lower()
        mime_type = "image/jpeg" if file_extension in ['.jpg', '.jpeg'] else "image/png"
        return f'<img src="data:{mime_type};base64,{base64_image}" alt="{alt_text}" style="max-width: {max_width}px; height: auto; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">'
    return f'<p>❌ Error loading {alt_text}</p>'

# =============================================================================
# CORE SCIENTIFIC CALCULATIONS
# =============================================================================

def adjust_body_fat_percentage(bf_original: float, method: str, gender: str, num_folds: int = None) -> float:
    """
    Adjusts body fat percentage based on measurement method and gender.
    
    Args:
        bf_original: Original body fat percentage
        method: Measurement method (DEXA, BIA, Fórmula Naval, Antropometría)
        gender: Masculino or Femenino
        num_folds: Number of skinfolds (for Antropometría method)
    
    Returns:
        Adjusted body fat percentage
    """
    if method == "DEXA":
        return bf_original  # Gold standard, no adjustment needed
    
    elif method == "BIA":
        if gender == "Masculino":
            if bf_original < 15:
                return bf_original + 2.5
            elif bf_original < 25:
                return bf_original + 1.8
            else:
                return bf_original + 1.2
        else:  # Femenino
            if bf_original < 20:
                return bf_original + 3.0
            elif bf_original < 30:
                return bf_original + 2.2
            else:
                return bf_original + 1.5
    
    elif method == "Fórmula Naval":
        if gender == "Masculino":
            if bf_original < 15:
                return bf_original + 1.5
            elif bf_original < 25:
                return bf_original + 1.0
            else:
                return bf_original + 0.5
        else:  # Femenino
            if bf_original < 20:
                return bf_original + 2.0
            elif bf_original < 30:
                return bf_original + 1.5
            else:
                return bf_original + 1.0
    
    elif method == "Antropometría":
        if num_folds == 3:
            return bf_original + 2.0
        elif num_folds == 4:
            return bf_original + 1.5
        elif num_folds == 7:
            return bf_original + 1.0
        else:
            return bf_original + 1.8
    
    return bf_original


def calculate_ffmi(weight: float, height: float, body_fat: float) -> float:
    """
    Calculates Fat-Free Mass Index (FFMI).
    
    Args:
        weight: Weight in kg
        height: Height in meters
        body_fat: Body fat percentage
    
    Returns:
        FFMI value
    """
    lean_mass = weight * (1 - body_fat / 100)
    ffmi = lean_mass / (height ** 2)
    return ffmi


def calculate_mifflin_st_jeor(weight: float, height: float, age: int, gender: str) -> float:
    """
    Calculates Resting Energy Expenditure using Mifflin-St Jeor equation.
    
    Args:
        weight: Weight in kg
        height: Height in cm
        age: Age in years
        gender: Masculino or Femenino
    
    Returns:
        REE in kcal/day
    """
    if gender == "Masculino":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161


def calculate_katch_mcardle(lean_mass: float) -> float:
    """
    Calculates Resting Energy Expenditure using Katch-McArdle equation.
    
    Args:
        lean_mass: Lean mass in kg
    
    Returns:
        REE in kcal/day
    """
    return 370 + (21.6 * lean_mass)


def calculate_geaf_factor(activity_level: str, gender: str) -> float:
    """
    Calculates Physical Activity Factor (GEAF) based on activity level and gender.
    
    Args:
        activity_level: Activity level category
        gender: Masculino or Femenino
    
    Returns:
        GEAF multiplier
    """
    factors = {
        "Sedentario": {"Masculino": 1.40, "Femenino": 1.35},
        "Ligeramente activo": {"Masculino": 1.55, "Femenino": 1.50},
        "Moderadamente activo": {"Masculino": 1.70, "Femenino": 1.65},
        "Muy activo": {"Masculino": 1.85, "Femenino": 1.80},
        "Extremadamente activo": {"Masculino": 2.00, "Femenino": 1.95}
    }
    return factors.get(activity_level, {}).get(gender, 1.40)


def calculate_gee(weight: float, training_minutes: int, training_days: int) -> float:
    """
    Calculates Exercise Energy Expenditure (GEE) using protocol formula.
    
    Args:
        weight: Body weight in kg
        training_minutes: Minutes per training session
        training_days: Training days per week
    
    Returns:
        Weekly GEE in kcal
    """
    # GEE = 0.1 × peso × minutos efectivos × días/semana
    return 0.1 * weight * training_minutes * training_days


def evaluate_pittsburgh_sleep(hours: str, time_to_sleep: str, awakenings: str, quality: str) -> int:
    """
    Evaluates sleep quality using abbreviated Pittsburgh Sleep Quality Index.
    
    Args:
        hours: Sleep duration category
        time_to_sleep: Time to fall asleep category
        awakenings: Number of awakenings category
        quality: Perceived sleep quality
    
    Returns:
        Pittsburgh score (0-16)
    """
    hours_map = {
        "Más de 9h": 0, "8-9h": 1, "7-8h": 2, "6-7h": 3, "5-6h": 4, "Menos de 5h": 5
    }
    
    time_map = {
        "Menos de 15 min": 0, "15-30 min": 1, "30-45 min": 2, "45-60 min": 3, "Más de 60 min": 4
    }
    
    awakenings_map = {
        "Nunca": 0, "1 vez": 1, "2 veces": 2, "3 veces": 3, "Más de 3 veces": 4
    }
    
    quality_map = {
        "Excelente": 0, "Buena": 1, "Regular": 2, "Mala": 3, "Muy mala": 4
    }
    
    return (hours_map.get(hours, 3) + 
            time_map.get(time_to_sleep, 2) + 
            awakenings_map.get(awakenings, 1) + 
            quality_map.get(quality, 2))


def evaluate_pss4_stress(q1: str, q2: str, q3: str, q4: str) -> int:
    """
    Evaluates perceived stress using PSS-4 scale.
    
    Args:
        q1-q4: Responses to PSS-4 questions
    
    Returns:
        PSS-4 score (0-16)
    """
    normal_map = {
        "Nunca": 0, "Casi nunca": 1, "A veces": 2, "Frecuentemente": 3, "Muy frecuentemente": 4
    }
    
    inverted_map = {
        "Nunca": 4, "Casi nunca": 3, "A veces": 2, "Frecuentemente": 1, "Muy frecuentemente": 0
    }
    
    return (normal_map.get(q1, 2) + 
            inverted_map.get(q2, 2) + 
            inverted_map.get(q3, 2) + 
            normal_map.get(q4, 2))


def calculate_fri(sleep_score: int, stress_score: int) -> Dict[str, Any]:
    """
    Calculates Intelligent Recovery Factor (FRI).
    
    Args:
        sleep_score: Pittsburgh sleep score
        stress_score: PSS-4 stress score
    
    Returns:
        Dictionary with FRI level, factor, and description
    """
    total_score = sleep_score + stress_score
    
    if total_score <= 6:
        return {"level": "Excelente", "factor": 1.0, "description": "Recuperación óptima"}
    elif total_score <= 12:
        return {"level": "Bueno", "factor": 0.95, "description": "Recuperación adecuada"}
    elif total_score <= 18:
        return {"level": "Regular", "factor": 0.90, "description": "Recuperación comprometida"}
    elif total_score <= 24:
        return {"level": "Deficiente", "factor": 0.85, "description": "Recuperación muy comprometida"}
    else:
        return {"level": "Crítico", "factor": 0.80, "description": "Recuperación crítica"}


def determine_automatic_goal(body_fat: float, gender: str, training_level: int) -> Dict[str, Any]:
    """
    Automatically determines body composition goal based on scientific criteria.
    
    Args:
        body_fat: Adjusted body fat percentage
        gender: Masculino or Femenino
        training_level: Training days per week
    
    Returns:
        Dictionary with goal, adjustment factor, and description
    """
    if gender == "Masculino":
        if body_fat > 25:
            return {"goal": "Definición", "adjustment": -0.125, "description": "Pérdida de grasa prioritaria"}
        elif 18 <= body_fat <= 25:
            return {"goal": "Definición", "adjustment": -0.075, "description": "Pérdida de grasa moderada"}
        elif 12 <= body_fat < 18:
            return {"goal": "Recomposición", "adjustment": -0.025, "description": "Recomposición corporal"}
        else:  # < 12%
            return {"goal": "Volumen", "adjustment": 0.125, "description": "Ganancia muscular"}
    else:  # Femenino
        if body_fat > 32:
            return {"goal": "Definición", "adjustment": -0.125, "description": "Pérdida de grasa prioritaria"}
        elif 25 <= body_fat <= 32:
            return {"goal": "Definición", "adjustment": -0.075, "description": "Pérdida de grasa moderada"}
        elif 20 <= body_fat < 25:
            return {"goal": "Recomposición", "adjustment": -0.025, "description": "Recomposición corporal"}
        else:  # < 20%
            return {"goal": "Volumen", "adjustment": 0.125, "description": "Ganancia muscular"}


def obtener_porcentaje_grasa_tmb_tradicional() -> float:
    """
    Retorna el porcentaje fijo de grasa basado en TMB/BMR tradicional.
    
    Fija la ingesta de grasa en 40% del TMB/BMR para todos los usuarios,
    independientemente del porcentaje de grasa corporal o el objetivo.
    
    Justificación científica y práctica:
    - Optimización hormonal: Prevención del descenso de testosterona y alteraciones endocrinas
      que ocurren con ingestas de grasa menores al 30-35% de las calorías totales
    - Mejor adherencia dietaria: Las grasas proporcionan mayor saciedad y palatabilidad,
      reduciendo la sensación de restricción y mejorando el cumplimiento a largo plazo
    - Estabilización metabólica: Mantiene niveles óptimos de hormonas esteroideas y 
      función tiroidea, especialmente importante en fases de restricción calórica
    
    Referencias científicas:
    - Volek et al., 1997: Testosterone and cortisol in relationship to dietary nutrients and resistance exercise
    - Smith et al., 2011: Changes in intake of protein foods, carbohydrate amount and quality, and long-term weight change
    - Riechman et al., 2007: Statins and dietary and serum cholesterol are associated with increased lean mass following resistance training
    - Burke et al., 2011: Carbohydrates for training and competition
    
    Returns:
        float: 0.40 (40% del TMB/BMR)
    """
    return 0.40


def calculate_macronutrients(total_calories: float, weight: float, goal: str, gender: str, tmb_bmr: float = None) -> Dict[str, float]:
    """
    Calculates intelligent macronutrient distribution based on goal.
    
    Args:
        total_calories: Total daily calories
        weight: Body weight in kg
        goal: Body composition goal
        gender: Masculino or Femenino
        tmb_bmr: TMB/BMR in kcal (optional, for fat calculation)
    
    Returns:
        Dictionary with macronutrient amounts in grams and calories
    """
    # Protein factor based on goal
    if goal == "Definición":
        protein_factor = 2.6
    elif goal == "Recomposición":
        protein_factor = 2.2
    else:  # Volumen
        protein_factor = 1.8
    
    protein_g = weight * protein_factor
    protein_kcal = protein_g * PROTEIN_KCAL_PER_G
    
    # Fat calculation using traditional TMB/BMR percentage
    if tmb_bmr is not None:
        # Use 40% of TMB/BMR for fat intake (fixed percentage)
        fat_percentage_tmb = obtener_porcentaje_grasa_tmb_tradicional()
        fat_kcal = tmb_bmr * fat_percentage_tmb
        fat_g = fat_kcal / FAT_KCAL_PER_G
    else:
        # Fallback to original logic if TMB/BMR not available
        if goal == "Definición":
            fat_factor = 0.8
        elif goal == "Recomposición":
            fat_factor = 1.0
        else:  # Volumen
            fat_factor = 1.2
        
        fat_g = weight * fat_factor
        fat_kcal = fat_g * FAT_KCAL_PER_G
    
    # Apply limits: ensure fat doesn't exceed 35% or fall below 20% of total calories
    max_fat_kcal = total_calories * 0.35
    min_fat_kcal = total_calories * 0.20
    
    if fat_kcal > max_fat_kcal:
        fat_kcal = max_fat_kcal
        fat_g = fat_kcal / FAT_KCAL_PER_G
    elif fat_kcal < min_fat_kcal:
        fat_kcal = min_fat_kcal
        fat_g = fat_kcal / FAT_KCAL_PER_G
    
    # Carbohydrates by difference
    carbs_kcal = total_calories - protein_kcal - fat_kcal
    carbs_g = carbs_kcal / CARB_KCAL_PER_G
    
    return {
        "protein_g": protein_g,
        "protein_kcal": protein_kcal,
        "fat_g": fat_g,
        "fat_kcal": fat_kcal,
        "carbs_g": carbs_g,
        "carbs_kcal": carbs_kcal
    }


def generate_warnings(fri: Dict[str, Any], goal: Dict[str, Any], body_fat: float, gender: str) -> list:
    """
    Generates automatic warnings based on assessment results.
    
    Args:
        fri: FRI assessment results
        goal: Automatic goal determination
        body_fat: Body fat percentage
        gender: Masculino or Femenino
    
    Returns:
        List of warning messages
    """
    warnings = []
    
    # FRI-based warnings
    if fri["level"] == "Crítico":
        warnings.append("⚠️ ALERTA CRÍTICA: Recuperación extremadamente comprometida. Considera consultar un profesional de la salud.")
    elif fri["level"] == "Deficiente":
        warnings.append("⚠️ ADVERTENCIA: Recuperación muy comprometida. Prioriza mejorar calidad de sueño y manejo del estrés.")
    elif fri["level"] == "Regular":
        warnings.append("💡 NOTA: Recuperación comprometida. Considera ajustar rutinas de sueño y técnicas de manejo del estrés.")
    
    # Body fat warnings
    if gender == "Masculino":
        if body_fat > 30:
            warnings.append("🚨 PRIORIDAD ALTA: Porcentaje de grasa corporal muy elevado. Déficit calórico agresivo recomendado.")
        elif body_fat < 8:
            warnings.append("⚠️ PRECAUCIÓN: Porcentaje de grasa corporal muy bajo. Monitorear salud hormonal.")
    else:  # Femenino
        if body_fat > 35:
            warnings.append("🚨 PRIORIDAD ALTA: Porcentaje de grasa corporal muy elevado. Déficit calórico agresivo recomendado.")
        elif body_fat < 16:
            warnings.append("⚠️ PRECAUCIÓN: Porcentaje de grasa corporal muy bajo. Monitorear salud hormonal.")
    
    # Goal-based warnings
    if goal["goal"] == "Definición" and goal["adjustment"] == -0.125:
        warnings.append("📊 ESTRATEGIA: Déficit calórico agresivo indicado. Monitorear masa muscular.")
    elif goal["goal"] == "Volumen":
        warnings.append("💪 ESTRATEGIA: Superávit calórico indicado. Monitorear ganancia de grasa.")
    
    return warnings


def generate_complete_report(full_name, email, age, gender, weight, height, bf_method, bf_original, 
                           bf_adjusted, lean_mass, ffmi, activity_level, occupation, training_minutes, 
                           training_days, daily_steps, ger_final, ger_method, geaf, gee_daily, 
                           get_total, sleep_score, stress_score, fri, goal, final_calories, 
                           macros, warnings):
    """Generate complete report for coach."""
    
    report = f"""
========================================
📊 ANÁLISIS AVANZADO DE BALANCE ENERGÉTICO
========================================

Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Cliente: {full_name}
Email: {email}

========================================
🆔 DATOS PERSONALES
========================================
Edad: {age} años
Sexo: {gender}

========================================
🧍‍♂️ COMPOSICIÓN CORPORAL
========================================
Peso: {weight} kg
Estatura: {height} cm
IMC: {weight / ((height/100) ** 2):.1f}
Método BF: {bf_method}
BF Original: {bf_original}%
BF Ajustado: {bf_adjusted:.1f}%
Ajuste aplicado: {bf_adjusted - bf_original:+.1f}%
Masa Magra: {lean_mass:.1f} kg
FFMI: {ffmi:.1f}

========================================
🏃‍♂️ ACTIVIDAD FÍSICA
========================================
Nivel de actividad: {activity_level}
Ocupación: {occupation}
Entrenamiento: {training_minutes} min × {training_days} días/semana
Pasos diarios: {daily_steps}

========================================
⚡ CÁLCULOS ENERGÉTICOS
========================================
GER: {ger_final:.0f} kcal (Método: {ger_method})
GEAF: {geaf:.2f}
GEE: {gee_daily:.0f} kcal/día
GET: {get_total:.0f} kcal/día

========================================
💤 EVALUACIÓN DEL SUEÑO
========================================
Puntuación Pittsburgh: {sleep_score}/16
Clasificación: {"Deficiente" if sleep_score >= 10 else "Adecuada"}

========================================
😖 EVALUACIÓN DEL ESTRÉS
========================================
Puntuación PSS-4: {stress_score}/16
Clasificación: {"Elevado" if stress_score >= 10 else "Manejable"}

========================================
🧠 FACTOR DE RECUPERACIÓN INTELIGENTE
========================================
Nivel FRI: {fri["level"]}
Factor: {fri["factor"]:.2f}
Descripción: {fri["description"]}

========================================
🎯 OBJETIVO AUTOMÁTICO
========================================
Objetivo: {goal["goal"]}
Ajuste: {goal["adjustment"]*100:+.1f}%
Justificación: {goal["description"]}

========================================
🍽️ ASIGNACIÓN DE MACRONUTRIENTES
========================================
Calorías Totales: {final_calories:.0f} kcal

Proteína: {macros["protein_g"]:.0f}g ({macros["protein_g"]/weight:.1f} g/kg)
         {macros["protein_kcal"]:.0f} kcal ({macros["protein_kcal"]/final_calories*100:.1f}%)

Grasas: {macros["fat_g"]:.0f}g ({macros["fat_g"]/weight:.1f} g/kg)
        {macros["fat_kcal"]:.0f} kcal ({macros["fat_kcal"]/final_calories*100:.1f}%)

Carbohidratos: {macros["carbs_g"]:.0f}g ({macros["carbs_g"]/weight:.1f} g/kg)
               {macros["carbs_kcal"]:.0f} kcal ({macros["carbs_kcal"]/final_calories*100:.1f}%)

========================================
⚠️ ADVERTENCIAS Y RECOMENDACIONES
========================================
"""
    
    if warnings:
        for warning in warnings:
            report += f"• {warning}\n"
    else:
        report += "• Sin advertencias específicas\n"
    
    report += f"""
========================================
📝 NOTAS PARA EL COACH
========================================
Prioridad: {"Alta" if fri["level"] in ["Deficiente", "Crítico"] or len(warnings) > 2 else "Media" if fri["level"] == "Regular" else "Estándar"}
Seguimiento: {"Semanal" if fri["level"] in ["Deficiente", "Crítico"] else "Quincenal" if fri["level"] == "Regular" else "Mensual"}
Contactar en: 24-48 horas

ALERTAS ESPECIALES:
{"• Recuperación comprometida - revisar hábitos de sueño y estrés" if fri["level"] in ["Regular", "Deficiente", "Crítico"] else "• Sin alertas especiales"}
{"• Composición corporal requiere atención prioritaria" if (gender == "Masculino" and (bf_adjusted > 25 or bf_adjusted < 10)) or (gender == "Femenino" and (bf_adjusted > 32 or bf_adjusted < 16)) else ""}

========================================
"""
    
    return report


# =============================================================================
# MAIN QUESTIONNAIRE INTERFACE
# =============================================================================

def main():
    """Main application interface with page navigation."""
    
    # =============================================================================
    # SIDEBAR NAVIGATION
    # =============================================================================
    
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2>🏠 Navegación</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Page navigation
        page = st.selectbox(
            "Selecciona una sección:",
            ["🏠 Cuestionario Principal", "💰 Planes y Tarifas"],
            index=0
        )
        
        st.markdown("---")
    
    # =============================================================================
    # PAGE ROUTING
    # =============================================================================
    
    if page == "💰 Planes y Tarifas":
        show_plans_page()
    else:
        show_main_questionnaire()


def show_plans_page():
    """Display the plans and pricing page."""
    
    # Navigation banner
    display_navigation_banner()
    
    # Main Logo
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            from PIL import Image
            logo = Image.open("LOGO.png")
            st.image(logo, width=400)
        except:
            st.info("🏢 Logo MUPAI")
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>💰 PLANES Y TARIFAS</h1>
        <p>Servicios Profesionales de Nutrición y Entrenamiento Personalizado</p>
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
        try:
            from PIL import Image
            bank_card_image = Image.open("Copia de Copia de Copia de Copia de Copia de Tarjeta GYM_20250715_074925_0000.png")
            st.image(bank_card_image, caption="Tarjeta Bancaria para Transferencias", width=500)
        except:
            st.info("💳 Imagen de tarjeta bancaria disponible para transferencias")


def show_main_questionnaire():
    """Display the main questionnaire interface."""
    
    # Navigation banner
    display_navigation_banner()
    
    # =============================================================================
    # ABOUT ME SECTION
    # =============================================================================
    
    st.markdown("""
    <div class="professional-header">
        <h2>SOBRE EL PROFESIONAL Y CONTACTO</h2>
        <p style="margin-top: 1rem; color: #666; font-size: 1rem;">👨‍⚕️ Acerca de mí</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional images - stacked, centered, and responsive
    st.markdown("<div class='professional-images'>", unsafe_allow_html=True)
    
    # Main professional image - large and centered
    main_image_html = create_image_html(
        "Copia de Anfitrión_20250809_125513_0000.png", 
        "Imagen Principal Profesional", 
        800  # Large width for main focal image
    )
    st.markdown(f"<div class='main-image'>{main_image_html}</div>", unsafe_allow_html=True)
    
    # Secondary image - centered below the main one
    secondary_image_html = create_image_html(
        "20250728_220454.jpg", 
        "Imagen Secundaria Profesional", 
        600  # Slightly smaller but still prominent
    )
    st.markdown(f"<div class='secondary-image'>{secondary_image_html}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # =============================================================================
    # CONTACT SECTION
    # =============================================================================
    
    st.markdown("""
    <div class="contact-section">
        <h2 class="contact-title">💬 CONTACTO</h2>
        <p class="contact-description">Da clic para comunicarte en el medio que necesites</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Contact icons using columns for better control
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <a href="https://wa.me/message/YOUR_WHATSAPP_NUMBER" target="_blank" style="text-decoration: none;">
                <div class="contact-icon whatsapp" style="margin: 0 auto;">
                    📱
                </div>
                <p style="color: #25D366; font-weight: bold; margin-top: 0.5rem; font-size: 0.9rem;">WhatsApp</p>
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center;">
            <a href="mailto:mupaitraining@outlook.com" style="text-decoration: none;">
                <div class="contact-icon email" style="margin: 0 auto;">
                    📧
                </div>
                <p style="color: #EA4335; font-weight: bold; margin-top: 0.5rem; font-size: 0.9rem;">Email</p>
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center;">
            <a href="https://facebook.com/YOUR_FACEBOOK_PAGE" target="_blank" style="text-decoration: none;">
                <div class="contact-icon facebook" style="margin: 0 auto;">
                    📘
                </div>
                <p style="color: #1877F2; font-weight: bold; margin-top: 0.5rem; font-size: 0.9rem;">Facebook</p>
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 1.5rem;">
        <p style="color: #333; font-size: 0.9rem; font-style: italic;">
            Respuesta garantizada en 24-48 horas
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Logo
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            from PIL import Image
            logo = Image.open("LOGO.png")
            st.image(logo, width=400)
        except:
            st.info("🏢 Logo MUPAI")
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>⚡ CUESTIONARIO AVANZADO DE BALANCE ENERGÉTICO ÓPTIMO</h1>
        <p>Sistema Científico Inteligente para Asignación de Macronutrientes</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Plans information banner
    display_plans_info_banner()
    
    # Main questionnaire form
    with st.form("advanced_energy_balance_form"):
        
        # =============================================================================
        # SECTION 1: PERSONAL DATA
        # =============================================================================
        
        st.markdown("""
        <div class="section-container">
            <h2>🆔 Sección 1: Datos Personales</h2>
            <p>Información básica necesaria para los cálculos personalizados.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Nombre completo*", placeholder="Tu nombre completo")
            email = st.text_input("Correo electrónico*", placeholder="tu@email.com")
            age = st.number_input("Edad*", min_value=16, max_value=80, value=25)
            
        with col2:
            gender = st.selectbox("Sexo*", ["Masculino", "Femenino"])
            st.markdown("")
            st.markdown("")
            legal_acceptance = st.checkbox("Acepto los términos y condiciones y autorizo el procesamiento de mis datos para fines científicos y de entrenamiento*")
        
        # =============================================================================
        # SECTION 2: BODY COMPOSITION
        # =============================================================================
        
        st.markdown("""
        <div class="section-container">
            <h2>🧍‍♂️ Sección 2: Composición Corporal</h2>
            <p>Evaluación detallada de tu composición corporal con ajustes automáticos por método de medición.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            height = st.number_input("Estatura (cm)*", min_value=140, max_value=220, value=170)
            weight = st.number_input("Peso (kg)*", min_value=40.0, max_value=200.0, value=70.0, step=0.1)
            bf_method = st.selectbox("Método de medición de grasa corporal*", [
                "DEXA", "BIA", "Fórmula Naval", "Antropometría"
            ])
            
        with col2:
            bf_original = st.number_input("Porcentaje de grasa corporal original (%)*", 
                                         min_value=5.0, max_value=50.0, value=20.0, step=0.1)
            
            num_folds = None
            if bf_method == "Antropometría":
                num_folds = st.selectbox("Número de pliegues cutáneos", [3, 4, 7])
            
            # Automatic adjustment
            bf_adjusted = adjust_body_fat_percentage(bf_original, bf_method, gender, num_folds)
            
            if bf_adjusted != bf_original:
                st.info(f"💡 **Ajuste automático aplicado:** {bf_original}% → {bf_adjusted:.1f}%")
                st.caption(f"Corrección científica por método {bf_method}")
            
            # Automatic calculations
            lean_mass = weight * (1 - bf_adjusted/100)
            ffmi = calculate_ffmi(weight, height/100, bf_adjusted)
            
            st.metric("Masa Magra", f"{lean_mass:.1f} kg")
            st.metric("FFMI", f"{ffmi:.1f}")
            
            # FFMI interpretation
            if gender == "Masculino":
                if ffmi > 25:
                    st.success("🏆 FFMI Excelente")
                elif ffmi > 22:
                    st.info("💪 FFMI Muy bueno")
                elif ffmi > 20:
                    st.warning("📈 FFMI Bueno")
                else:
                    st.error("📉 FFMI Bajo")
            else:  # Femenino
                if ffmi > 22:
                    st.success("🏆 FFMI Excelente")
                elif ffmi > 19:
                    st.info("💪 FFMI Muy bueno")
                elif ffmi > 17:
                    st.warning("📈 FFMI Bueno")
                else:
                    st.error("📉 FFMI Bajo")
        
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
            gee_weekly = calculate_gee(weight, training_minutes, training_days)
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
            st.markdown(f"""
            <div class="warning-container">
                <h4>⚠️ Impacto del FRI</h4>
                <p>Tu Factor de Recuperación Inteligente indica que tus objetivos energéticos serán ajustados 
                automáticamente en un <strong>{(1-fri['factor'])*100:.0f}%</strong> para optimizar tu recuperación.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # =============================================================================
        # FORM SUBMISSION AND CALCULATIONS
        # =============================================================================
        
        submitted = st.form_submit_button("🚀 Generar Análisis Completo y Asignación de Macronutrientes", 
                                         type="primary", use_container_width=True)
        
        if submitted:
            # Validation
            if not full_name:
                st.error("❌ **Error:** El nombre completo es obligatorio")
                return
            
            if not email:
                st.error("❌ **Error:** El correo electrónico es obligatorio")
                return
            
            if not legal_acceptance:
                st.error("❌ **Error:** Debes aceptar los términos y condiciones")
                return
            
            # =============================================================================
            # AUTOMATIC GOAL DETERMINATION
            # =============================================================================
            
            goal = determine_automatic_goal(bf_adjusted, gender, training_days)
            
            # Apply FRI and goal adjustment to calculate final calories
            if goal["adjustment"] < 0:  # Deficit
                final_calories = get_total * (1 + goal["adjustment"]) * fri["factor"]
            else:  # Surplus
                final_calories = get_total * (1 + goal["adjustment"]) * fri["factor"]
            
            # =============================================================================
            # MACRONUTRIENT ALLOCATION
            # =============================================================================
            
            macros = calculate_macronutrients(final_calories, weight, goal["goal"], gender, ger_final)
            
            # =============================================================================
            # GENERATE WARNINGS
            # =============================================================================
            
            warnings = generate_warnings(fri, goal, bf_adjusted, gender)
            
            # =============================================================================
            # RESULTS DISPLAY
            # =============================================================================
            
            st.markdown("---")
            st.markdown("""
            <div class="results-container">
                <h2>📊 RESULTADOS DEL ANÁLISIS COMPLETO</h2>
                <p>Evaluación científica personalizada con asignación inteligente de macronutrientes</p>
            </div>
            """, unsafe_allow_html=True)
            
            # User summary
            st.markdown("### 👤 Resumen de Datos Procesados")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Composición Corporal", f"{bf_adjusted:.1f}% GC")
                st.caption(f"Ajustado por método {bf_method}")
            
            with col2:
                st.metric("FFMI", f"{ffmi:.1f}")
                st.caption("Índice de masa libre de grasa")
            
            with col3:
                st.metric("GET", f"{get_total:.0f} kcal")
                st.caption("Gasto energético total")
            
            with col4:
                st.metric("Nivel FRI", fri["level"])
                st.caption(f"Factor: {fri['factor']:.2f}")
            
            # Automatic goal determination
            st.markdown("### 🎯 Objetivo Corporal Automático")
            
            st.markdown(f"""
            <div class="metric-card">
                <h3>🏆 Objetivo Determinado: {goal["goal"]}</h3>
                <p><strong>Justificación Científica:</strong> {goal["description"]}</p>
                <p><strong>Ajuste Calórico:</strong> {goal["adjustment"]*100:+.1f}%</p>
                <p><strong>Metodología:</strong> Basado en porcentaje de grasa corporal ({bf_adjusted:.1f}%), 
                género ({gender}), y nivel de entrenamiento ({training_days} días/semana)</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Final caloric target
            st.markdown("### ⚡ Objetivo Energético Final")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Calorías Objetivo", f"{final_calories:.0f} kcal/día")
                st.caption(f"Incluye ajuste por FRI ({fri['factor']:.2f})")
            
            with col2:
                adjustment_total = goal["adjustment"] * fri["factor"]
                if adjustment_total < 0:
                    st.metric("Tipo de Ajuste", "Déficit Calórico")
                    st.caption(f"Reducción: {abs(adjustment_total)*100:.1f}%")
                elif adjustment_total > 0:
                    st.metric("Tipo de Ajuste", "Superávit Calórico")
                    st.caption(f"Aumento: {adjustment_total*100:.1f}%")
                else:
                    st.metric("Tipo de Ajuste", "Mantenimiento")
                    st.caption("Sin ajuste calórico")
            
            # Macronutrient allocation
            st.markdown("### 🍽️ Asignación Inteligente de Macronutrientes")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>🥩 Proteína</h4>
                    <h3>{macros["protein_g"]:.0f}g</h3>
                    <p>{macros["protein_kcal"]:.0f} kcal ({macros["protein_kcal"]/final_calories*100:.1f}%)</p>
                    <p><strong>{macros["protein_g"]/weight:.1f} g/kg</strong></p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>🥑 Grasas</h4>
                    <h3>{macros["fat_g"]:.0f}g</h3>
                    <p>{macros["fat_kcal"]:.0f} kcal ({macros["fat_kcal"]/final_calories*100:.1f}%)</p>
                    <p><strong>{macros["fat_g"]/weight:.1f} g/kg</strong></p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>🍞 Carbohidratos</h4>
                    <h3>{macros["carbs_g"]:.0f}g</h3>
                    <p>{macros["carbs_kcal"]:.0f} kcal ({macros["carbs_kcal"]/final_calories*100:.1f}%)</p>
                    <p><strong>{macros["carbs_g"]/weight:.1f} g/kg</strong></p>
                </div>
                """, unsafe_allow_html=True)
            
            # Scientific rationale
            st.markdown("### 🔬 Justificación Científica de Macronutrientes")
            
            st.markdown(f"""
            **Proteína ({macros["protein_g"]/weight:.1f} g/kg):**
            - Objetivo {goal["goal"]}: Factor {macros["protein_g"]/weight:.1f} g/kg aplicado
            - Optimizado para {goal["description"].lower()}
            - Rango científico: {"2.2-2.6 g/kg" if goal["goal"] == "Definición" else "2.0-2.4 g/kg" if goal["goal"] == "Recomposición" else "1.8-2.0 g/kg"}
            
            **Grasas ({macros["fat_g"]/weight:.1f} g/kg):**
            - Ajuste por objetivo: {goal["goal"]}
            - Optimizado para salud hormonal y saciedad
            - Rango científico: {"0.8-1.0 g/kg" if goal["goal"] == "Definición" else "0.9-1.2 g/kg" if goal["goal"] == "Recomposición" else "1.0-1.2 g/kg"}
            
            **Carbohidratos ({macros["carbs_g"]/weight:.1f} g/kg):**
            - Calculado por diferencia energética
            - Optimizado para rendimiento en entrenamiento
            - Ajustado según demanda energética y objetivo corporal
            """)
            
            # Warnings and recommendations
            if warnings:
                st.markdown("### ⚠️ Advertencias y Recomendaciones Automáticas")
                
                for warning in warnings:
                    st.markdown(f"""
                    <div class="warning-container">
                        <p>{warning}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # =============================================================================
            # COACH AREA
            # =============================================================================
            
            st.markdown("---")
            st.markdown("### 🔐 Área Exclusiva del Coach")
            
            coach_password = st.text_input("Contraseña del Coach:", type="password")
            
            if coach_password == COACH_PASSWORD:
                st.success("✅ Coach MUPAI verificado")
                
                # Generate complete report
                report = generate_complete_report(
                    full_name, email, age, gender, weight, height, bf_method, bf_original, 
                    bf_adjusted, lean_mass, ffmi, activity_level, occupation, training_minutes, 
                    training_days, daily_steps, ger_final, ger_method, geaf, gee_daily, 
                    get_total, sleep_score, stress_score, fri, goal, final_calories, 
                    macros, warnings
                )
                
                st.text_area("Análisis Completo del Cliente:", report, height=400)
                
                # Download button
                st.download_button(
                    label="📥 Descargar Análisis Completo",
                    data=report,
                    file_name=f"analisis_completo_{full_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
                
            elif coach_password:
                st.error("❌ Acceso denegado. Solo el coach autorizado puede ver los resultados.")
            
            # User confirmation
            st.markdown("---")
            st.markdown("### ✅ Confirmación para el Cliente")
            
            st.success("🎉 **¡Análisis completado exitosamente!**")
            
            st.info(f"""
            **Estimado/a {full_name}:**
            
            Tu evaluación avanzada de balance energético ha sido procesada con éxito utilizando las metodologías científicas más actualizadas.
            
            **Próximos pasos:**
            1. Tu coach MUPAI revisará estos resultados detalladamente
            2. Recibirás un plan nutricional personalizado basado en este análisis
            3. Se programará seguimiento según tus necesidades específicas
            
            **Tiempo estimado de contacto:** 24-48 horas
            
            **Recordatorio:** Mantén tu rutina actual hasta recibir las indicaciones personalizadas del coach.
            """)


# =============================================================================
# MAIN APPLICATION ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
