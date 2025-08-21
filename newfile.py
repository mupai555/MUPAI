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
import re
# Temporarily comment out if the module doesn't exist yet
# from cuestionario_fbeo import mostrar_cuestionario_fbeo

# Configure Streamlit header for mobile visibility and sidebar access
mobile_header_style = """
    <style>
    /* Ensure Streamlit header is visible and accessible on mobile */
    [data-testid="stHeader"] {
        position: sticky !important;
        top: 0 !important;
        z-index: 1000 !important;
        background: white !important;
        visibility: visible !important;
        display: block !important;
    }
    
    /* Keep main menu (hamburger icon) visible */
    header, #MainMenu {
        visibility: visible !important;
        display: block !important;
    }
    
    /* Hide only non-essential elements but preserve header with hamburger menu */
    .stDeployButton {display: none !important;}
    
    /* Ensure hamburger menu is always clickeable on mobile */
    [data-testid="stSidebarNav"] {
        visibility: visible !important;
        display: block !important;
        z-index: 1001 !important;
    }
    </style>
"""
st.markdown(mobile_header_style, unsafe_allow_html=True)


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
    Loads the Muscle Up Gym logo image and returns it as base64 encoded string.
    Returns None if the image file is not found.
    """
    logo_image_path = 'LOGO MUP.png'
    
    try:
        with open(logo_image_path, 'rb') as f:
            image_data = f.read()
            encoded_image = base64.b64encode(image_data).decode()
            return f'data:image/png;base64,{encoded_image}'
    except FileNotFoundError:
        return None
    except Exception as e:
        return None

def load_mupai_logo_base64():
    """
    Loads the MUPAI logo image and returns it as base64 encoded string.
    Returns None if the image file is not found.
    """
    logo_image_path = 'LOGO MUPAI.png'
    
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

# Override CSS immediately after page config to ensure header visibility
st.markdown("""
<style>
/* CRITICAL OVERRIDE: Force Streamlit header visibility on all devices */
[data-testid="stHeader"] { 
    position: sticky !important; 
    top: 0 !important; 
    z-index: 1000 !important; 
    background: #fff !important; 
    visibility: visible !important; 
    display: block !important; 
}

header, #MainMenu { 
    visibility: visible !important; 
    display: block !important; 
}

.stAppHeader { 
    display: block !important; 
    visibility: visible !important; 
}

/* Ensure professional banner doesn't interfere with header */
.professional-banner { 
    position: relative !important; 
    z-index: 1 !important; 
    pointer-events: auto !important;
}

/* Decorative overlays should not block header interaction */
.overlay-decorative {
    pointer-events: none !important;
}
</style>

<script>
// Mobile sidebar auto-open on first visit
(function() {
    function isMobile() {
        return window.innerWidth <= 768;
    }
    
    function openSidebarOnce() {
        // Check if we've already opened the sidebar
        if (localStorage.getItem('mupai_sidebar_opened_once')) {
            return;
        }
        
        if (!isMobile()) {
            return;
        }
        
        // Try multiple selectors for the hamburger menu
        const selectors = [
            '[data-testid="stSidebarNav"] button',
            '[data-testid="stSidebar"] button',
            '.css-1dp5vir button',
            '[aria-label="Open sidebar"]',
            'button[kind="header"]',
            '[data-testid="stHeader"] button'
        ];
        
        let sidebarButton = null;
        for (const selector of selectors) {
            sidebarButton = document.querySelector(selector);
            if (sidebarButton) break;
        }
        
        if (sidebarButton) {
            try {
                sidebarButton.click();
                // Mark that we've opened the sidebar once
                localStorage.setItem('mupai_sidebar_opened_once', 'true');
            } catch (error) {
                console.log('Could not auto-open sidebar:', error);
            }
        }
    }
    
    // Wait for DOM to be ready, then try multiple times as Streamlit loads dynamically
    setTimeout(openSidebarOnce, 1000);
    setTimeout(openSidebarOnce, 2000);
    setTimeout(openSidebarOnce, 3000);
})();
</script>
""", unsafe_allow_html=True)

# Initialize session state for page navigation if not already set
if 'page' not in st.session_state:
    st.session_state.page = 'inicio'

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
      
    /* ========================================================================== */
    /* MODULARIZED QUESTIONNAIRE CSS STYLES - SCOPED WITH 'cuest-' PREFIX */
    /* ========================================================================== */
    
    .cuest-section-header {  
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
      
    .cuest-container {  
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);  
        padding: 1.5rem;  
        border-radius: 12px;  
        border-left: 5px solid #FFCC00;  
        margin: 1rem 0;  
        box-shadow: 0 2px 8px rgba(255,204,0,0.1);  
        color: #FFFFFF;
    }  
      
    .cuest-results {  
        background: linear-gradient(135deg, #FFCC00 0%, #FFE066 50%, #FFF2A6 100%);  
        padding: 2rem;  
        border-radius: 15px;  
        color: #000;  
        margin: 1rem 0;  
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);  
    }  
      
    .cuest-metric-card {  
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);  
        padding: 1.5rem;  
        border-radius: 12px;  
        box-shadow: 0 3px 12px rgba(255,204,0,0.1);  
        border-left: 6px solid #FFCC00;  
        margin: 1rem 0;  
        transition: transform 0.2s ease;  
        color: #FFFFFF;
    }  
      
    .cuest-metric-card:hover {  
        transform: translateY(-2px);  
        box-shadow: 0 5px 20px rgba(255,204,0,0.2);  
    }

    .cuest-warning {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        border-left: 5px solid #ff3333;
    }

    .cuest-info {
        background: linear-gradient(135deg, #74b9ff 0%, #a29bfe 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        border-left: 5px solid #0984e3;
    }

    /* Mobile responsive styles for questionnaire components */
    @media (max-width: 768px) {
        .cuest-section-header {
            padding: 0.8rem;
            margin: 1rem 0;
            font-size: 0.9rem;
        }
        
        .cuest-container, .cuest-metric-card {
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 10px;
        }
        
        .cuest-results {
            padding: 1.5rem 1rem;
            margin: 1rem 0;
        }

        .cuest-warning, .cuest-info {
            padding: 1rem;
            margin: 0.5rem 0;
        }
    }

    @media (max-width: 480px) {
        .cuest-section-header {
            padding: 0.6rem;
            font-size: 0.8rem;
        }
        
        .cuest-container, .cuest-metric-card {
            padding: 0.8rem 0.6rem;
            margin: 0.3rem 0;
        }
        
        .cuest-results {
            padding: 1rem 0.8rem;
        }

        .cuest-warning, .cuest-info {
            padding: 0.8rem;
        }
    }
    
    /* ========================================================================== */
    /* END MODULARIZED QUESTIONNAIRE STYLES */
    /* ========================================================================== */
      
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
    
    .sidebar-icon-mobile {
        font-size: 1.6rem;
        font-weight: bold;
        color: #000;
        background: #FFCC00;
        padding: 0.3rem 0.6rem;
        border-radius: 10px;
        display: inline-block;
        margin: 0 0.3rem;
        box-shadow: 0 2px 8px rgba(255,204,0,0.4);
        animation: gentle-glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes gentle-glow {
        0% { box-shadow: 0 2px 8px rgba(255,204,0,0.4); }
        100% { box-shadow: 0 4px 12px rgba(255,204,0,0.6); }
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
    }
    
    /* ========================================================================== */
    /* MOBILE HEADER AND SIDEBAR ACCESSIBILITY IMPROVEMENTS */
    /* ========================================================================== */
    
    /* Ensure header stays visible and accessible on all devices */
    @media (max-width: 768px) {
        /* Force header to be visible and properly positioned */
        [data-testid="stHeader"] {
            position: sticky !important;
            top: 0 !important;
            z-index: 1000 !important;
            background: white !important;
            visibility: visible !important;
            display: block !important;
            height: auto !important;
            min-height: 45px !important;
        }
        
        /* Ensure professional banner doesn't overlap header */
        .professional-banner {
            margin-top: 1rem !important;
            position: relative !important;
            z-index: 100 !important;
        }
        
        /* Add small top margin to main content to account for sticky header */
        .stApp > div:first-child {
            padding-top: 0.5rem !important;
        }
    }
    
    /* Ultra-mobile devices - ensure hamburger menu is accessible */
    @media (max-width: 480px) {
        [data-testid="stHeader"] {
            min-height: 40px !important;
        }
        
        /* Slightly reduce banner margin on very small screens */
        .professional-banner {
            margin-top: 0.5rem !important;
        }
    }
    
    /* ========================================================================== */
    /* MODERN INSTITUTIONAL FOOTER STYLES - TECH GLASSMORPHISM DESIGN */
    /* ========================================================================== */
    
    .institutional-footer {
        background: linear-gradient(135deg, 
            rgba(0,0,0,0.95) 0%, 
            rgba(26,26,26,0.98) 25%, 
            rgba(45,45,45,0.95) 50%, 
            rgba(26,26,26,0.98) 75%, 
            rgba(0,0,0,0.95) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-top: 2px solid rgba(255,204,0,0.3);
        box-shadow: 0 -8px 32px rgba(255,204,0,0.1);
        position: relative;
        margin-top: 4rem;
        padding: 2.5rem 0;
        overflow: hidden;
    }
    
    .institutional-footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, 
            transparent 0%, 
            rgba(255,204,0,0.03) 25%, 
            transparent 50%, 
            rgba(255,204,0,0.03) 75%, 
            transparent 100%);
        animation: techShimmer 8s ease-in-out infinite;
        pointer-events: none;
    }
    
    @keyframes techShimmer {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.7; }
    }
    
    .footer-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        max-width: 1400px;
        margin: 0 auto;
        gap: 2rem;
        padding: 0 2rem;
        position: relative;
        z-index: 2;
    }
    
    .footer-logo-left, .footer-logo-right {
        flex: 0 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 160px;
        height: 120px;
        background: rgba(255,204,0,0.08);
        border-radius: 20px;
        border: 1px solid rgba(255,204,0,0.2);
        backdrop-filter: blur(10px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .footer-logo-left:hover, .footer-logo-right:hover {
        background: rgba(255,204,0,0.15);
        border-color: rgba(255,204,0,0.4);
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 10px 30px rgba(255,204,0,0.2);
    }
    
    .footer-logo-img {
        max-width: 130px;
        max-height: 90px;
        width: auto;
        height: auto;
        object-fit: contain;
        display: block;
        filter: drop-shadow(0 4px 8px rgba(255,204,0,0.3));
        transition: filter 0.3s ease;
    }
    
    .footer-logo-img:hover {
        filter: drop-shadow(0 6px 12px rgba(255,204,0,0.5));
    }
    
    .footer-logo-fallback {
        color: #FFCC00;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
    }
    
    .footer-center {
        flex: 1;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1.5rem;
    }
    
    .footer-contact-buttons {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .footer-contact-btn {
        background: linear-gradient(135deg, #FFCC00 0%, #FFD700 100%);
        color: #000;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        text-decoration: none;
        font-weight: bold;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(255,204,0,0.3);
        border: 2px solid transparent;
        position: relative;
        overflow: hidden;
    }
    
    .footer-contact-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .footer-contact-btn:hover::before {
        left: 100%;
    }
    
    .footer-contact-btn:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 8px 25px rgba(255,204,0,0.5);
        background: linear-gradient(135deg, #FFD700 0%, #FFCC00 100%);
    }
    
    .footer-social-icons {
        display: flex;
        gap: 1.2rem;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
    }
    
    .footer-social-link {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-decoration: none;
        padding: 0.8rem;
        border-radius: 15px;
        background: rgba(255,204,0,0.05);
        border: 1px solid rgba(255,204,0,0.1);
        backdrop-filter: blur(10px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        min-width: 80px;
        position: relative;
        overflow: hidden;
    }
    
    .footer-social-link::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at center, rgba(255,204,0,0.1) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .footer-social-link:hover::before {
        opacity: 1;
    }
    
    .footer-social-link:hover {
        background: rgba(255,204,0,0.12);
        border-color: rgba(255,204,0,0.3);
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 20px rgba(255,204,0,0.2);
    }
    
    .footer-icon {
        font-size: 1.8rem;
        margin-bottom: 0.3rem;
        transition: transform 0.3s ease;
    }
    
    .footer-social-link:hover .footer-icon {
        transform: scale(1.2) rotate(5deg);
    }
    
    .footer-icon-text {
        color: #FFFFFF;
        font-size: 0.85rem;
        font-weight: 500;
        text-shadow: 0 1px 2px rgba(0,0,0,0.5);
        transition: color 0.3s ease;
    }
    
    .footer-social-link:hover .footer-icon-text {
        color: #FFCC00;
    }
    
    .footer-copyright {
        color: #CCCCCC;
        font-size: 0.9rem;
        line-height: 1.5;
        text-align: center;
        max-width: 600px;
        padding: 1rem;
        background: rgba(0,0,0,0.3);
        border-radius: 15px;
        border: 1px solid rgba(255,204,0,0.1);
        backdrop-filter: blur(5px);
        text-shadow: 0 1px 2px rgba(0,0,0,0.5);
    }
    
    /* ========================================================================== */
    /* RESPONSIVE DESIGN FOR FOOTER */
    /* ========================================================================== */
    
    @media (max-width: 1024px) {
        .footer-content {
            flex-direction: column;
            gap: 2rem;
            padding: 0 1.5rem;
        }
        
        .footer-logo-left, .footer-logo-right {
            width: 140px;
            height: 100px;
        }
        
        .footer-center {
            order: 1;
            width: 100%;
        }
        
        .footer-logo-left {
            order: 2;
        }
        
        .footer-logo-right {
            order: 3;
        }
        
        .footer-contact-buttons {
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .footer-social-icons {
            gap: 1rem;
        }
    }
    
    @media (max-width: 768px) {
        .institutional-footer {
            padding: 2rem 0;
        }
        
        .footer-content {
            padding: 0 1rem;
            gap: 1.5rem;
        }
        
        .footer-logo-left, .footer-logo-right {
            width: 120px;
            height: 80px;
        }
        
        .footer-logo-img {
            max-width: 100px;
            max-height: 60px;
        }
        
        .footer-contact-btn {
            padding: 0.6rem 1.2rem;
            font-size: 0.9rem;
        }
        
        .footer-social-icons {
            gap: 0.8rem;
        }
        
        .footer-social-link {
            min-width: 70px;
            padding: 0.6rem;
        }
        
        .footer-icon {
            font-size: 1.5rem;
        }
        
        .footer-icon-text {
            font-size: 0.8rem;
        }
        
        .footer-copyright {
            font-size: 0.85rem;
            padding: 0.8rem;
        }
    }
    
    @media (max-width: 480px) {
        .institutional-footer {
            padding: 1.5rem 0;
        }
        
        .footer-content {
            padding: 0 0.8rem;
            gap: 1.2rem;
        }
        
        .footer-logo-left, .footer-logo-right {
            width: 100px;
            height: 70px;
        }
        
        .footer-logo-img {
            max-width: 80px;
            max-height: 50px;
        }
        
        .footer-contact-buttons {
            flex-direction: column;
            gap: 0.8rem;
            width: 100%;
        }
        
        .footer-contact-btn {
            width: 100%;
            max-width: 250px;
        }
        
        .footer-social-icons {
            gap: 0.6rem;
        }
        
        .footer-social-link {
            min-width: 60px;
            padding: 0.5rem;
        }
        
        .footer-icon {
            font-size: 1.3rem;
        }
        
        .footer-icon-text {
            font-size: 0.75rem;
        }
        
        .footer-copyright {
            font-size: 0.8rem;
            padding: 0.6rem;
            line-height: 1.3;
        }
    }
    
    .institutional-footer {
        background: linear-gradient(135deg, 
            rgba(0,0,0,0.95) 0%, 
            rgba(15,15,15,0.98) 35%, 
            rgba(25,25,25,0.95) 70%, 
            rgba(0,0,0,0.98) 100%) !important;
        backdrop-filter: blur(10px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(10px) saturate(180%) !important;
        border-top: 1px solid rgba(255,204,0,0.2) !important;
        box-shadow: 0 -8px 32px rgba(0,0,0,0.4), 
                    inset 0 1px 0 rgba(255,204,0,0.1) !important;
        width: 100vw !important;
        margin: 0 !important;
        margin-left: calc(-50vw + 50%) !important;
        padding: 3rem 0 !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .institutional-footer::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        background: radial-gradient(circle at 20% 50%, rgba(255,204,0,0.05) 0%, transparent 50%),
                    radial-gradient(circle at 80% 50%, rgba(255,215,0,0.03) 0%, transparent 50%) !important;
        pointer-events: none !important;
    }
    
    .footer-content {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        max-width: 1400px !important;
        margin: 0 auto !important;
        gap: 2.5rem !important;
        min-height: 120px !important;
        padding: 0 2rem !important;
        box-sizing: border-box !important;
        position: relative !important;
        z-index: 2 !important;
    }
    
    .footer-logo-left, .footer-logo-right {
        flex: 0 0 auto !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 160px !important;
        height: 120px !important;
        background: rgba(255,255,255,0.05) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255,204,0,0.15) !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .footer-logo-left:hover, .footer-logo-right:hover {
        transform: translateY(-4px) scale(1.02) !important;
        background: rgba(255,204,0,0.08) !important;
        border-color: rgba(255,204,0,0.3) !important;
        box-shadow: 0 12px 24px rgba(255,204,0,0.15) !important;
    }
    
    .footer-logo-img {
        max-width: 130px !important;
        max-height: 90px !important;
        width: auto !important;
        height: auto !important;
        object-fit: contain !important;
        display: block !important;
        filter: brightness(1.1) contrast(1.1) !important;
        transition: all 0.3s ease !important;
    }
    
    .footer-logo-img:hover {
        filter: brightness(1.3) contrast(1.2) !important;
        transform: scale(1.05) !important;
    }
    
    .footer-logo-fallback {
        color: #FFCC00 !important;
        text-align: center !important;
        font-weight: bold !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 1.2rem !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5) !important;
    }
    
    .footer-center {
        flex: 1 !important;
        text-align: center !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 1.5rem !important;
        max-width: 800px !important;
    }
    
    .footer-social-icons {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        gap: 1.5rem !important;
        flex-wrap: wrap !important;
        margin-bottom: 1rem !important;
    }
    
    .footer-social-link {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,204,0,0.2) !important;
        border-radius: 16px !important;
        padding: 1rem 1.2rem !important;
        text-decoration: none !important;
        color: #FFFFFF !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 0.5rem !important;
        min-width: 85px !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .footer-social-link::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255,204,0,0.1), transparent) !important;
        transition: left 0.6s ease !important;
    }
    
    .footer-social-link:hover::before {
        left: 100% !important;
    }
    
    .footer-social-link:hover {
        transform: translateY(-6px) scale(1.05) !important;
        background: rgba(255,204,0,0.12) !important;
        border-color: #FFCC00 !important;
        box-shadow: 0 12px 32px rgba(255,204,0,0.2), 
                    0 0 0 1px rgba(255,204,0,0.3) !important;
        color: #FFD700 !important;
    }
    
    .footer-icon {
        font-size: 2rem !important;
        margin-bottom: 0.3rem !important;
        transition: all 0.3s ease !important;
    }
    
    .footer-social-link:hover .footer-icon {
        transform: scale(1.2) rotate(5deg) !important;
        filter: drop-shadow(0 4px 8px rgba(255,204,0,0.4)) !important;
    }
    
    .footer-icon-text {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
    }
    
    .footer-contact-buttons {
        display: flex !important;
        gap: 1rem !important;
        justify-content: center !important;
        flex-wrap: wrap !important;
        margin: 1rem 0 !important;
    }
    
    .footer-contact-btn {
        background: linear-gradient(135deg, #FFCC00 0%, #FFD700 100%) !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.8rem 1.5rem !important;
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 0.9rem !important;
        text-decoration: none !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 0.5rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(255,204,0,0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .footer-contact-btn::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        background: linear-gradient(135deg, #FFD700 0%, #FFCC00 100%) !important;
        opacity: 0 !important;
        transition: opacity 0.3s ease !important;
    }
    
    .footer-contact-btn:hover::before {
        opacity: 1 !important;
    }
    
    .footer-contact-btn:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(255,204,0,0.4) !important;
    }
    
    .footer-contact-btn span {
        position: relative !important;
        z-index: 1 !important;
    }
    
    .footer-copyright {
        color: #FFFFFF !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        font-weight: 500 !important;
        max-width: 700px !important;
        margin: 0 auto !important;
        text-align: center !important;
        word-wrap: break-word !important;
        hyphens: auto !important;
        overflow-wrap: break-word !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.5) !important;
        background: rgba(255,255,255,0.03) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        border: 1px solid rgba(255,204,0,0.1) !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
    }
    
    /* Mobile footer responsiveness */
    @media (max-width: 768px) {
        .institutional-footer {
            padding: 2.5rem 0 !important;
        }
        
        .footer-content {
            flex-direction: column !important;
            text-align: center !important;
            gap: 2rem !important;
            min-height: auto !important;
            padding: 0 1rem !important;
        }
        
        .footer-logo-left, .footer-logo-right {
            width: 140px !important;
            height: 100px !important;
            order: 2 !important;
        }
        
        .footer-center {
            order: 1 !important;
            width: 100% !important;
        }
        
        .footer-social-icons {
            gap: 1.2rem !important;
        }
        
        .footer-social-link {
            min-width: 75px !important;
            padding: 0.8rem 1rem !important;
        }
        
        .footer-icon {
            font-size: 1.6rem !important;
        }
        
        .footer-icon-text {
            font-size: 0.8rem !important;
        }
        
        .footer-contact-buttons {
            flex-direction: column !important;
            align-items: center !important;
        }
        
        .footer-copyright {
            font-size: 0.9rem !important;
            padding: 1rem !important;
            max-width: 100% !important;
            line-height: 1.4 !important;
        }
        
        .footer-logo-img {
            max-width: 110px !important;
            max-height: 70px !important;
        }
        
        /* Mobile layout adjustments */
        .footer-logos-mobile {
            display: flex !important;
            justify-content: space-around !important;
            align-items: center !important;
            width: 100% !important;
            max-width: 350px !important;
            margin: 0 auto !important;
            order: 3 !important;
        }
    }
    
    @media (max-width: 480px) {
        .institutional-footer {
            padding: 2rem 0 !important;
        }
        
        .footer-content {
            padding: 0 0.5rem !important;
            gap: 1.5rem !important;
        }
        
        .footer-social-icons {
            gap: 1rem !important;
        }
        
        .footer-social-link {
            min-width: 65px !important;
            padding: 0.6rem 0.8rem !important;
        }
        
        .footer-icon {
            font-size: 1.4rem !important;
        }
        
        .footer-icon-text {
            font-size: 0.75rem !important;
        }
        
        .footer-contact-btn {
            padding: 0.7rem 1.2rem !important;
            font-size: 0.85rem !important;
        }
        
        .footer-copyright {
            font-size: 0.85rem !important;
            padding: 0.8rem !important;
            line-height: 1.3 !important;
        }
        
        .footer-logo-left, .footer-logo-right {
            width: 120px !important;
            height: 80px !important;
        }
        
        .footer-logo-img {
            max-width: 90px !important;
            max-height: 60px !important;
        }
    }
    
    /* ========================================================================== */
    /* WELCOME CONTAINER RESPONSIVE STYLES */
    /* ========================================================================== */
    
    .welcome-container {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    
    /* Mobile welcome container responsiveness */
    @media (max-width: 768px) {
        .welcome-container {
            padding: 2rem 1rem !important;
            margin: 1rem 0 !important;
            min-height: 250px !important;
        }
        
        .welcome-container h1 {
            font-size: 2.5rem !important;
            line-height: 1.2 !important;
            margin-bottom: 1rem !important;
        }
        
        .welcome-container h2 {
            font-size: 1.4rem !important;
            line-height: 1.3 !important;
            margin-bottom: 1.5rem !important;
        }
        
        .welcome-container p {
            font-size: 1.1rem !important;
            line-height: 1.5 !important;
            max-width: 100% !important;
            padding: 0 0.5rem !important;
        }
    }
    
    @media (max-width: 480px) {
        .welcome-container {
            padding: 1.5rem 0.8rem !important;
            min-height: 200px !important;
        }
        
        .welcome-container h1 {
            font-size: 2rem !important;
            margin-bottom: 0.8rem !important;
        }
        
        .welcome-container h2 {
            font-size: 1.2rem !important;
            margin-bottom: 1rem !important;
        }
        
        .welcome-container p {
            font-size: 1rem !important;
            padding: 0 0.3rem !important;
        }
    }
    
    /* ========================================================================== */
    /* END MOBILE RESPONSIVENESS BLOCK */
    /* ========================================================================== */
</style>  
""", unsafe_allow_html=True)

# ==================== SIDEBAR NAVIGATION ====================
def crear_sidebar_navegacion():
    """
    Creates the sidebar navigation menu with all available pages.
    """
    with st.sidebar:
        # MUPAI Logo in sidebar
        logo_base64 = load_logo_image_base64()
        if logo_base64:
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 1rem;">
                <img src="{logo_base64}" style="max-width: 150px; height: auto;" alt="MUPAI Logo">
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 1rem; color: #FFCC00;">
                <h2>💪 MUPAI</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation buttons
        if st.button("🏠 Inicio", use_container_width=True):
            st.session_state.page = "inicio"
            st.rerun()
            
        if st.button("👥 ¿Quiénes Somos?", use_container_width=True):
            st.session_state.page = "quienes_somos"
            st.rerun()
            
        if st.button("💰 Planes y Costos", use_container_width=True):
            st.session_state.page = "planes_costos" 
            st.rerun()
            
        st.markdown("### 📋 Cuestionarios")
        
        if st.button("⚡ Balance Energético", use_container_width=True):
            st.session_state.page = "balance_energetico"
            st.rerun()
            
        if st.button("🍽️ Preferencias Alimentarias", use_container_width=True):
            st.session_state.page = "preferencias_alimentarias"
            st.rerun()
            
        if st.button("🍫 Antojos Alimentarios", use_container_width=True):
            st.session_state.page = "antojos_alimentarios"
            st.rerun()
            
        st.markdown("### 🧪 Test MUPAI")
        
        if st.button("🏋️‍♂️ Body and Energy", use_container_width=True):
            st.session_state.page = "body_and_energy"
            st.rerun()
            
        if st.button("🥗 Food Preferences", use_container_width=True):
            st.session_state.page = "food_preferences"
            st.rerun()
            
        if st.button("💪 Designing Training", use_container_width=True):
            st.session_state.page = "designing_training"
            st.rerun()
            
        st.markdown("---")
        
        if st.button("👨‍⚕️ Sobre el Profesional", use_container_width=True):
            st.session_state.page = "about"
            st.rerun()
            
        if st.button("📞 Contacto", use_container_width=True):
            st.session_state.page = "contacto"
            st.rerun()

def mostrar_banner_profesional():
    """
    Displays a professional banner encouraging users to access the sidebar menu.
    Visible on all pages and devices with enhanced mobile instructions.
    """
    st.markdown("""
    <div class="professional-banner">
        <h4>👉 ¡Descubre Todo el Contenido de MUPAI!</h4>
        <p>
            <span class="desktop-instruction">Haz clic en el ícono <span class="sidebar-icon">☰</span> en la esquina superior izquierda 
            para desplegar el menú lateral y acceder a todo el contenido y menús detallados de MUPAI.</span>
            <span class="mobile-instruction">📱 <strong>En móvil:</strong> Toca el ícono <span class="sidebar-icon-mobile">☰</span> 
            arriba a la izquierda para abrir el menú completo con todos los cuestionarios y opciones de MUPAI.</span>
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

# Create sidebar navigation
crear_sidebar_navegacion()

# ==================== PÁGINA DE INICIO ====================
if st.session_state.page == "inicio":
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
    
    # Professional banner - visible on all pages
    mostrar_banner_profesional()
    
    # Título de bienvenida
    st.markdown("""
    <div class="welcome-container" style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                padding: 3rem 2rem; border-radius: 20px; text-align: center; 
                margin: 2rem 0; border: 2px solid #FFCC00; 
                box-shadow: 0 4px 15px rgba(255,204,0,0.3);
                display: flex; flex-direction: column; align-items: center; 
                justify-content: center; min-height: 300px;">
        <h1 style="color: #FFCC00; font-size: 3.5rem; font-weight: bold; 
                   margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(255,204,0,0.5);
                   text-align: center; width: 100%;">
            🎯 Bienvenido a MUPAI
        </h1>
        <h2 style="color: #FFFFFF; font-size: 1.8rem; margin-bottom: 2rem; font-weight: 500;
                   text-align: center; width: 100%;">
            Tu Transformación Física Basada en Ciencia e Inteligencia Artificial
        </h2>
        <p style="color: #FFFFFF; font-size: 1.3rem; line-height: 1.6; max-width: 900px; 
                  margin: 0 auto; text-align: center;">
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
    # Professional banner - visible on all pages
    mostrar_banner_profesional()
    
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
# ==================== CUESTIONARIO BALANCE ENERGÉTICO ====================
elif st.session_state.page == "balance_energetico":
    # Professional banner - visible on all pages
    mostrar_banner_profesional()
    
    st.markdown("""
    <div class="cuest-section-header">
        <h2>🧮 Cuestionario Científico Avanzado - Balance Energético Óptimo</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="cuest-container">
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
            <div class="cuest-warning">
                <h4>⚠️ Calidad de Sueño Deficiente</h4>
                <p><strong>Puntuación Pittsburgh: {sleep_score}/16</strong></p>
                <p>Tu calidad de sueño está comprometida, lo que puede afectar tu recuperación y objetivos nutricionales.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="cuest-info">
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
            <div class="cuest-warning">
                <h4>⚠️ Nivel de Estrés Elevado</h4>
                <p><strong>Puntuación PSS-4: {stress_score}/16</strong></p>
                <p>Tu nivel de estrés es alto, lo que puede impactar tu recuperación y objetivos nutricionales.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="cuest-info">
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
            <div class="cuest-warning">
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
    <div class="cuest-section-header">
        <h2>🍽️ Cuestionario: Patrones y Preferencias Alimenticias</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="cuest-container">
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
        <div class="cuest-container">
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
    <div class="cuest-section-header">
        <h2>🧁 Cuestionario de Antojos Alimentarios (Food Cravings)</h2>
        <h3>Versión Población Mexicana</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="cuest-container">
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
        <div class="cuest-container">
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
    # Professional banner - visible on all pages
    mostrar_banner_profesional()
    
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
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="corporate-section">
        <h4>💰 Precios:</h4>
        <ul>
            <li><strong>Usuarios Internos (miembros del gym):</strong> $550 MXN</li>
            <li><strong>Usuarios Externos:</strong> $700 MXN</li>
        </ul>
        <h4>✅ Beneficios Incluidos:</h4>
        <ul>
            <li>Evaluación inicial completa con bioimpedancia</li>
            <li>6 menús semanales adaptados (calorías, macros, micronutrientes)</li>
            <li>Personalización según preferencias alimentarias</li>
            <li>Evaluación final con medición corporal</li>
            <li>Menús extra desde $100 (internos) $150 (externos) MXN</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Plan 2: Entrenamiento Personalizado
    st.markdown("""
    <div class="corporate-section">
        <h3>💪 Plan de Entrenamiento Personalizado</h3>
        <p><strong>Duración:</strong> 8 semanas</p>
        <p><strong>Descripción:</strong> Programa de entrenamiento científicamente diseñado según tu nivel, objetivos, disponibilidad de tiempo y equipamiento.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="corporate-section">
        <h4>💰 Precios:</h4>
        <ul>
            <li><strong>Usuarios Internos (miembros del gym):</strong> $650 MXN</li>
            <li><strong>Usuarios Externos:</strong> $800 MXN</li>
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
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="corporate-section">
        <h4>💰 Precios:</h4>
        <ul>
            <li><strong>Usuarios Internos (miembros del gym):</strong> $1050 MXN</li>
            <li><strong>Usuarios Externos:</strong> $1350 MXN</li>
        </ul>
        <h4>✅ Beneficios Incluidos:</h4>
        <ul>
            <li>Ambos planes completos (nutrición + entrenamiento)</li>
            <li>Evaluación inicial y final con bioimpedancia</li>
            <li>Integración total entre dieta y entrenamiento</li>
            <li>Seguimiento coordinado de progreso</li>
            <li><strong>Ahorro de $150 MXN (internos) o $150 MXN (externos)</strong></li>
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
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="questionnaire-container">
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

# ==================== NUEVAS PÁGINAS TEST MUPAI ====================
elif st.session_state.page == "body_and_energy":
    # Professional banner - visible on all pages
    mostrar_banner_profesional()
    
    st.markdown("""
    <div class="cuest-section-header">
        <h2>BODY AND ENERGY</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Attractive centered button linking to Body And Energy Calculator
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0;">
        <a href="https://mupai-digital-training-science-fbeo.streamlit.app/" target="_blank" style="text-decoration: none;">
            <div class="attractive-button">
                <h2 style="margin: 0; color: #000; font-size: 1.8rem; font-weight: bold;">
                    🏋️‍♂️ ACCEDER A BODY AND ENERGY
                </h2>
                <p style="margin: 0.5rem 0 0 0; color: #333; font-size: 1.1rem;">
                    Herramienta profesional para cálculo exacto de gasto energético y composición corporal
                </p>
                <p style="margin: 0.5rem 0 0 0; color: #000; font-size: 1.2rem; font-weight: bold;">
                    👆 Da clic aquí para acceder
                </p>
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "food_preferences":
    # Professional banner - visible on all pages
    mostrar_banner_profesional()
    
    st.markdown("""
    <div class="cuest-section-header">
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
    <div class="cuest-section-header">
        <h2>DESIGNING YOUR TRAINING</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="cuest-container">
        <h3>Pronto disponible.</h3>
    </div>
    """, unsafe_allow_html=True)

# ==================== PÁGINAS ADICIONALES ====================
elif st.session_state.page == "about":
    # Professional banner - visible on all pages
    mostrar_banner_profesional()
    
    # Professional header with subtitle
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
        st.image(main_image, caption="Imagen Principal Profesional", use_container_width=True)
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
    # Professional banner - visible on all pages
    mostrar_banner_profesional()
    
    # Contact section with responsive styling
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

# ===========================================================================
# MODERN INSTITUTIONAL FOOTER
# ===========================================================================
# Footer institucional regenerado el 2025-01-23 con diseño moderno y tecnológico
# Características: Glassmorphism, gradientes dinámicos, hover animations, responsive design
# ===========================================================================

def mostrar_footer_institucional():
    """
    Displays the modern institutional footer with logos, social media links and copyright.
    Features glassmorphism design, dynamic gradients, hover animations and responsive layout.
    """
    # Load logos
    logo_mupai = load_mupai_logo_base64()
    logo_mup = load_muscle_up_logo_base64()
    
    # Prepare logo HTML for left logo
    left_logo_html = f'<img src="{logo_mupai}" alt="LOGO MUPAI" class="footer-logo-img">' if logo_mupai else '<div class="footer-logo-fallback"><h3>💪 MUPAI</h3></div>'
    
    # Prepare logo HTML for right logo  
    right_logo_html = f'<img src="{logo_mup}" alt="LOGO MUP" class="footer-logo-img">' if logo_mup else '<div class="footer-logo-fallback"><h3>🏋️ MUP</h3></div>'
    
    # Render complete footer in single markdown call
    st.markdown(f"""
    <div class="institutional-footer">
        <div class="footer-content">
            <!-- Left Logo -->
            <div class="footer-logo-left">
                {left_logo_html}
            </div>
            
            <!-- Center Content -->
            <div class="footer-center">
                <!-- Contact Buttons -->
                <div class="footer-contact-buttons">
                    <a href="https://wa.me/528662580594" target="_blank" class="footer-contact-btn">
                        <span>📱 WhatsApp</span>
                    </a>
                    <a href="mailto:administracion@muscleupgym.fitness" target="_blank" class="footer-contact-btn">
                        <span>📧 Contacto</span>
                    </a>
                </div>
                
                <!-- Social Media Icons -->
                <div class="footer-social-icons">
                    <a href="https://wa.me/528662580594" target="_blank" class="footer-social-link">
                        <div class="footer-icon">📱</div>
                        <div class="footer-icon-text">WhatsApp</div>
                    </a>
                    <a href="mailto:administracion@muscleupgym.fitness" target="_blank" class="footer-social-link">
                        <div class="footer-icon">📧</div>
                        <div class="footer-icon-text">Email</div>
                    </a>
                    <a href="https://www.facebook.com/share/16WtR5TLw5/" target="_blank" class="footer-social-link">
                        <div class="footer-icon">📘</div>
                        <div class="footer-icon-text">Facebook</div>
                    </a>
                    <a href="https://www.instagram.com/mup_lindavista" target="_blank" class="footer-social-link">
                        <div class="footer-icon">📷</div>
                        <div class="footer-icon-text">Instagram</div>
                    </a>
                    <a href="https://muscleupgym.fitness/planes" target="_blank" class="footer-social-link">
                        <div class="footer-icon">🌐</div>
                        <div class="footer-icon-text">Website</div>
                    </a>
                </div>
                
                <!-- Copyright -->
                <div class="footer-copyright">
                    © 2025 MUPAI - Muscle up GYM Digital Training Science Performance Assessment Intelligence<br>
                    © 2025 MUPAI - Muscle up GYM Digital Nutrition Science Alimentary Pattern Assessment Intelligence
                </div>
            </div>
            
            <!-- Right Logo -->
            <div class="footer-logo-right">
                {right_logo_html}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===========================================================================
# Display footer on all pages
# ===========================================================================
mostrar_footer_institucional()
