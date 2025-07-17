"""
MUPAI - Sistema de Cuestionarios Nutricionales
==============================================

Sistema completo de cuestionarios para evaluación nutricional y composición corporal.
Incluye cuestionarios de balance energético avanzado y preferencias alimentarias.

Autor: MUPAI Team
Versión: 3.0
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Añadir el directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Imports de los módulos de cuestionarios
from cuestionario_preferencias import mostrar_cuestionario_preferencias
from newfile import main as mostrar_cuestionario_balance_energetico

# Configuración de la página
st.set_page_config(
    page_title="MUPAI - Sistema de Cuestionarios Nutricionales",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Global
st.markdown("""
<style>
    .main-title {
        background: linear-gradient(135deg, #FFCC00 0%, #FFD700 50%, #FFA500 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .main-title h1 {
        color: #000;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sidebar-info {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #FFCC00;
    }
    .warning-box {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        border-left: 5px solid #ff3333;
    }
    .success-box {
        background: linear-gradient(135deg, #51cf66 0%, #69db7c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        border-left: 5px solid #37b24d;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Función principal de la aplicación"""
    
    # Título principal
    st.markdown("""
    <div class="main-title">
        <h1>💪 MUPAI - Sistema de Cuestionarios Nutricionales</h1>
        <p style="font-size: 1.2rem; margin: 0; color: #000;">Evaluación Científica Personalizada</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar con navegación
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-info">
            <h3>📋 Cuestionarios Disponibles</h3>
            <p>Selecciona el cuestionario que deseas completar:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Selector de cuestionario
        cuestionario_seleccionado = st.selectbox(
            "Elige un cuestionario:",
            [
                "🏠 Inicio",
                "⚡ Cuestionario de Balance Energético",
                "🍽️ Preferencias y Antojos Alimentarios"
            ]
        )
        
        # Información adicional en la sidebar
        st.markdown("---")
        st.markdown("""
        <div class="sidebar-info">
            <h4>ℹ️ Información Importante</h4>
            <ul>
                <li>Completa todos los campos obligatorios</li>
                <li>Los datos se envían automáticamente al equipo de nutrición</li>
                <li>Recibirás respuesta en 24-48 horas</li>
                <li>Todos los datos son confidenciales</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Contacto
        st.markdown("---")
        st.markdown("""
        <div class="sidebar-info">
            <h4>📞 Contacto</h4>
            <p><strong>Email:</strong> administracion@muscleupgym.fitness</p>
            <p><strong>Soporte:</strong> MUPAI Team</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Versión
        st.markdown("---")
        st.markdown(f"**Versión:** 3.0")
        st.markdown(f"**Actualizado:** {datetime.now().strftime('%Y-%m-%d')}")
    
    # Contenido principal según selección
    if cuestionario_seleccionado == "🏠 Inicio":
        mostrar_inicio()
    elif cuestionario_seleccionado == "⚡ Cuestionario de Balance Energético":
        mostrar_cuestionario_balance_energetico()
    elif cuestionario_seleccionado == "🍽️ Preferencias y Antojos Alimentarios":
        mostrar_cuestionario_preferencias()


def mostrar_inicio():
    """Muestra la página de inicio con información general"""
    
    st.markdown("""
    ## 🎯 Bienvenido al Sistema MUPAI
    
    Este sistema de cuestionarios científicos está diseñado para evaluar de manera integral 
    tu perfil nutricional y de composición corporal, permitiendo una personalización 
    óptima de tu plan de nutrición.
    """)
    
    # Cuestionarios disponibles
    st.markdown("### 📋 Cuestionarios Disponibles")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="success-box">
            <h4>⚡ Cuestionario de Balance Energético</h4>
            <p><strong>Duración:</strong> 15-20 minutos</p>
            <p><strong>Propósito:</strong> Evaluación completa del gasto energético, 
            composición corporal, actividad física, calidad de sueño y estrés para 
            calcular objetivos calóricos y distribución de macronutrientes.</p>
            <p><strong>Incluye:</strong></p>
            <ul>
                <li>Análisis de composición corporal</li>
                <li>Cálculo de gasto energético total</li>
                <li>Evaluación de calidad de sueño</li>
                <li>Medición de estrés percibido</li>
                <li>Asignación automática de macronutrientes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="success-box">
            <h4>🍽️ Preferencias y Antojos Alimentarios</h4>
            <p><strong>Duración:</strong> 10-15 minutos</p>
            <p><strong>Propósito:</strong> Identificar preferencias alimentarias, 
            antojos y restricciones para personalizar el plan nutricional.</p>
            <p><strong>Incluye:</strong></p>
            <ul>
                <li>Selección de alimentos preferidos</li>
                <li>Análisis de antojos alimentarios</li>
                <li>Identificación de disparadores</li>
                <li>Restricciones y alergias</li>
                <li>Preferencias dietéticas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Instrucciones
    st.markdown("### 📝 Instrucciones de Uso")
    
    st.markdown("""
    1. **Selecciona un cuestionario** en el menú lateral
    2. **Completa todos los campos** marcados como obligatorios (*)
    3. **Revisa tus respuestas** antes de enviar
    4. **Envía el cuestionario** usando el botón al final
    5. **Espera la respuesta** del equipo de nutrición (24-48 horas)
    """)
    
    # Advertencias importantes
    st.markdown("### ⚠️ Advertencias Importantes")
    
    st.markdown("""
    <div class="warning-box">
        <h4>🔒 Privacidad y Seguridad</h4>
        <ul>
            <li>Todos los datos se envían de forma segura y encriptada</li>
            <li>La información es confidencial y solo accesible al equipo de nutrición</li>
            <li>No compartimos datos con terceros</li>
            <li>Puedes solicitar eliminación de datos en cualquier momento</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="warning-box">
        <h4>💡 Recomendaciones</h4>
        <ul>
            <li>Completa los cuestionarios en un momento tranquilo</li>
            <li>Sé honesto en tus respuestas para obtener mejores resultados</li>
            <li>Ten a mano datos de composición corporal si los tienes</li>
            <li>No completes los cuestionarios si estás enfermo o en condiciones especiales</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Estadísticas (opcional)
    st.markdown("### 📊 Estadísticas del Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Cuestionarios Disponibles", "2")
    
    with col2:
        st.metric("Tiempo Promedio", "12-18 min")
    
    with col3:
        st.metric("Tiempo de Respuesta", "24-48 hrs")


if __name__ == "__main__":
    main()
