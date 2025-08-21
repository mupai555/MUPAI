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
        color: #000;
        background: rgba(0,0,0,0.1);
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
            Haz clic en el ícono <span class="sidebar-icon">☰</span> en la esquina superior izquierda 
            para desplegar el menú lateral y acceder a todo el contenido y menús detallados de MUPAI.
        </p>
    </div>
    """, unsafe_allow_html=True)


def mostrar_banner_informativo():
    """
    Displays an informative banner only on the home page with overview and sidebar instructions.
    """
    st.markdown("""
    <div class="informative-banner">
        <p>
            Esta página te muestra un overview general de MUPAI y nuestros servicios principales. 
            Si quieres conocer más detalles, despliega la barra lateral (haz clic en ☰ arriba a la izquierda) 
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
        
# Inicializar session state
if 'page' not in st.session_state:
    st.session_state.page = "inicio"

# Navegación principal - reorganizada según requerimientos
st.sidebar.markdown("### 📋 NAVEGACIÓN")

if st.sidebar.button("🏠 Inicio", use_container_width=True):
    st.session_state.page = "inicio"

if st.sidebar.button("💸 Planes y Costos", use_container_width=True):
    st.session_state.page = "planes_costos"

if st.sidebar.button("🏢 ¿Quiénes somos?", use_container_width=True):
    st.session_state.page = "quienes_somos"

st.sidebar.markdown("---")
st.sidebar.markdown("### 👨‍🎓 SOBRE EL PROFESIONAL Y CONTACTO")

if st.sidebar.button("👨‍🎓 Acerca del Profesional", use_container_width=True):
    st.session_state.page = "about"

if st.sidebar.button("📞 Contacto", use_container_width=True):
    st.session_state.page = "contacto"

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧪 TEST MUPAI")

if st.sidebar.button("BODY AND ENERGY", use_container_width=True):
    st.session_state.page = "body_and_energy"

if st.sidebar.button("FOOD PREFERENCES", use_container_width=True):
    st.session_state.page = "food_preferences"

if st.sidebar.button("DESIGNING YOUR TRAINING", use_container_width=True):
    st.session_state.page = "designing_training"

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

    # Servicios principales con precios destacados
    st.markdown("""
    <div class="section-header">
        <h2>🚀 Nuestros Servicios Especializados</h2>
        <p style="font-size: 1.3rem; color: #FFFFFF; text-align: center; margin-top: 1rem;">
            Planes diseñados científicamente para maximizar tus resultados
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                    padding: 2.5rem 2rem; border-radius: 20px; margin: 1rem 0; 
                    border: 3px solid #FFCC00; box-shadow: 0 6px 20px rgba(255,204,0,0.3);
                    text-align: center; min-height: 450px; display: flex; flex-direction: column;">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">🍽️</div>
            <h3 style="color: #FFCC00; font-size: 1.8rem; margin-bottom: 1rem; font-weight: bold;">
                Nutrición Personalizada
            </h3>
            <div style="background: #FFCC00; color: #000; padding: 1rem; border-radius: 10px; 
                        margin-bottom: 1.5rem; font-weight: bold; font-size: 1.4rem;">
                💰 $550 - $700 MXN
            </div>
            <p style="color: #FFFFFF; font-size: 1.1rem; line-height: 1.6; margin-bottom: 1.5rem; flex-grow: 1;">
                <strong>Duración:</strong> 6 semanas<br><br>
                • Evaluación inicial con bioimpedancia<br>
                • 6 menús semanales adaptados<br>
                • Personalización por preferencias<br>
                • Macronutrientes científicos<br>
                • Evaluación final completa<br>
                • Menús extra disponibles
            </p>
            <div style="background: rgba(255,204,0,0.2); padding: 1rem; border-radius: 10px;">
                <p style="color: #FFCC00; font-weight: bold; margin: 0;">
                    ✨ Perfecto para optimizar tu alimentación
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                    padding: 2.5rem 2rem; border-radius: 20px; margin: 1rem 0; 
                    border: 3px solid #FFCC00; box-shadow: 0 6px 20px rgba(255,204,0,0.3);
                    text-align: center; min-height: 450px; display: flex; flex-direction: column;">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">💪</div>
            <h3 style="color: #FFCC00; font-size: 1.8rem; margin-bottom: 1rem; font-weight: bold;">
                Entrenamiento Personalizado
            </h3>
            <div style="background: #FFCC00; color: #000; padding: 1rem; border-radius: 10px; 
                        margin-bottom: 1.5rem; font-weight: bold; font-size: 1.4rem;">
                💰 $650 - $800 MXN
            </div>
            <p style="color: #FFFFFF; font-size: 1.1rem; line-height: 1.6; margin-bottom: 1.5rem; flex-grow: 1;">
                <strong>Duración:</strong> 8 semanas<br><br>
                • Evaluación "Designing Your Training"<br>
                • Plan personalizado volumen/intensidad<br>
                • Adaptación a tu horario y nivel<br>
                • Entrega profesional en PDF<br>
                • Progresiones incluidas<br>
                • Evaluación final de progresos
            </p>
            <div style="background: rgba(255,204,0,0.2); padding: 1rem; border-radius: 10px;">
                <p style="color: #FFCC00; font-weight: bold; margin: 0;">
                    🔥 Ideal para maximizar tu rendimiento
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                    padding: 2.5rem 2rem; border-radius: 20px; margin: 1rem 0; 
                    border: 3px solid #FFD700; box-shadow: 0 6px 20px rgba(255,215,0,0.4);
                    text-align: center; min-height: 450px; display: flex; flex-direction: column;
                    position: relative; overflow: hidden;">
            <div style="position: absolute; top: 0; right: 0; background: #FFD700; 
                        color: #000; padding: 0.5rem 1rem; font-weight: bold; 
                        transform: rotate(45deg); transform-origin: 100% 0%;">
                🌟 POPULAR
            </div>
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">🔥</div>
            <h3 style="color: #FFD700; font-size: 1.8rem; margin-bottom: 1rem; font-weight: bold;">
                Plan Combinado
            </h3>
            <div style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); 
                        color: #000; padding: 1rem; border-radius: 10px; 
                        margin-bottom: 1.5rem; font-weight: bold; font-size: 1.4rem;">
                💰 $1,050 - $1,350 MXN
                <div style="font-size: 1rem; margin-top: 0.5rem;">💸 Ahorra $150 MXN</div>
            </div>
            <p style="color: #FFFFFF; font-size: 1.1rem; line-height: 1.6; margin-bottom: 1.5rem; flex-grow: 1;">
                <strong>Lo mejor de ambos mundos</strong><br><br>
                • Nutrición + Entrenamiento integrados<br>
                • Evaluación inicial y final completa<br>
                • Sinergia total entre dieta y ejercicio<br>
                • Seguimiento coordinado<br>
                • Resultados optimizados<br>
                • Máximo ahorro económico
            </p>
            <div style="background: rgba(255,215,0,0.2); padding: 1rem; border-radius: 10px;">
                <p style="color: #FFD700; font-weight: bold; margin: 0;">
                    ⭐ La solución completa más efectiva
                </p>
            </div>
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

    # Rest of quienes_somos content would go here
    st.markdown("""
    <div class="section-header">
        <h2>🏢 ¿Quiénes Somos?</h2>
    </div>
    """, unsafe_allow_html=True)

# Continue with other pages...
elif st.session_state.page == "planes_costos":
    st.markdown("""
    <div class="section-header">
        <h2>💸 Planes y Costos</h2>
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
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "about":
    st.markdown("""
    <div class="professional-header">
        <h2>SOBRE EL PROFESIONAL Y CONTACTO</h2>
        <p style="margin-top: 1rem; color: #666; font-size: 1rem;">👨‍⚕️ Acerca del Profesional</p>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "contacto":
    st.markdown("""
    <div class="contact-section">
        <h2 class="contact-title">💬 CONTACTO</h2>
        <p class="contact-description">Da clic para comunicarte en el medio que necesites</p>
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