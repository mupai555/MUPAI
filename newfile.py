import streamlit as st
import pandas as pd
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import base64

# Configuración de la página
st.set_page_config(
    page_title="MUPAI - Fitness y Nutrición Personalizada",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mantener el branding MUPAI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FFCC00 0%, #FFD700 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        color: #000;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
    }
    
    .section-header {
        background-color: #000;
        color: #FFCC00;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    
    .questionnaire-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #FFCC00;
        margin: 1rem 0;
    }
    
    .results-container {
        background: linear-gradient(135deg, #FFCC00 0%, #FFE066 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: #000;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background-color: #f1f1f1;
    }
    
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #FFCC00;
        margin: 0.5rem 0;
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
        # Configurar aquí tu servidor SMTP
        # Esta es una función placeholder - necesitarás configurar tu servidor de email
        st.success(f"✅ Resultados enviados a {destinatario}")
        return True
    except Exception as e:
        st.error(f"❌ Error al enviar email: {str(e)}")
        return False

# Inicializar session state
if 'page' not in st.session_state:
    st.session_state.page = "inicio"

# Sidebar con navegación
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <h2 style='color: #FFCC00; background-color: #000; padding: 0.5rem; border-radius: 5px;'>
            💪 MUPAI
        </h2>
        <p style='color: #666; font-size: 0.9rem;'>Fitness y Nutrición Personalizada</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navegación principal
    if st.button("🏠 Inicio", use_container_width=True):
        st.session_state.page = "inicio"
    
    st.markdown("### 📋 Cuestionarios")
    
    if st.button("⚡ Cuestionario: Balance Energético Óptimo", use_container_width=True):
        st.session_state.page = "balance_energetico"
    
    if st.button("🍽️ Cuestionario: Patrones y Preferencias Alimenticias", use_container_width=True):
        st.session_state.page = "preferencias_alimentarias"
    
    if st.button("🧁 Cuestionario: Antojos Alimentarios", use_container_width=True):
        st.session_state.page = "antojos_alimentarios"
    
    st.markdown("---")
    
    if st.button("👨‍⚕️ Acerca de Mí", use_container_width=True):
        st.session_state.page = "about"
    
    if st.button("📞 Contacto", use_container_width=True):
        st.session_state.page = "contacto"

# Contenido principal según la página seleccionada
if st.session_state.page == "inicio":
    # Página de inicio
    st.markdown("""
    <div class="main-header">
        <h1>💪 MUPAI</h1>
        <p style="color: #000; font-size: 1.2rem; margin: 0;">Plataforma Digital Profesional para Fitness y Nutrición Personalizada</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Misión</h3>
            <p>Proporcionar orientación fitness y nutricional personalizada basada en evidencia científica para optimizar tu bienestar integral.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🔮 Visión</h3>
            <p>Ser la plataforma líder en transformación física personalizada, combinando tecnología avanzada con metodologías probadas.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>📋 Servicios</h3>
            <p>Evaluaciones personalizadas, planes nutricionales, seguimiento de progreso y coaching especializado.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-header">
        <h2>🚀 Comienza tu Transformación</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 📋 Cuestionarios Disponibles
    
    Utiliza nuestros cuestionarios especializados para obtener recomendaciones personalizadas:
    
    - **⚡ Balance Energético Óptimo**: Calcula tu ingesta calórica personalizada
    - **🍽️ Patrones y Preferencias Alimenticias**: Define tu perfil nutricional
    - **🧁 Antojos Alimentarios**: Identifica y maneja tus patrones de antojos
    """)

elif st.session_state.page == "balance_energetico":
    st.markdown("""
    <div class="section-header">
        <h2>⚡ Cuestionario: Balance Energético Óptimo</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("balance_energetico_form"):
        st.markdown("""
        <div class="questionnaire-container">
            <h3>🔹 SECCIÓN 1: Datos Personales y Composición Corporal</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            sexo = st.selectbox("1. Sexo:", ["Hombre", "Mujer", "Otro"])
            edad = st.number_input("2. Edad (años):", min_value=15, max_value=80, value=30)
            estatura = st.number_input("3. Estatura (cm):", min_value=140, max_value=220, value=170)
        
        with col2:
            peso = st.number_input("4. Peso actual (kg):", min_value=40.0, max_value=200.0, value=70.0, step=0.5)
            grasa_corporal = st.number_input("5. Porcentaje estimado de grasa corporal (%):", min_value=5.0, max_value=50.0, value=15.0, step=0.5)
            metodo_grasa = st.selectbox("6. ¿Qué método usaste para estimar tu grasa corporal?", 
                                      ["DEXA", "BIA", "Plicometría", "Visual", "Otro"])
        
        st.markdown("""
        <div class="questionnaire-container">
            <h3>🔹 SECCIÓN 2: Nivel de Actividad Diaria (NO deportiva)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        nivel_actividad = st.radio("7. ¿Cuál describe mejor tu nivel de actividad diaria?", [
            "🪑 Sedentario (<5000 pasos)",
            "🚶 Ligera (5000–7999 pasos)",
            "🚶‍♂️ Activo (8000–11999 pasos)",
            "🏃 Muy activo (≥12000 pasos)"
        ])
        
        # Limpiar el texto para el cálculo
        nivel_actividad_clean = nivel_actividad.split(" ")[1]
        
        st.markdown("""
        <div class="questionnaire-container">
            <h3>🔹 SECCIÓN 3: Entrenamiento</h3>
        </div>
        """, unsafe_allow_html=True)
        
        dias_entrenamiento = st.slider("8. Días por semana que entrenas:", 0, 7, 3)
        
        st.markdown("""
        <div class="questionnaire-container">
            <h3>🔹 SECCIÓN 4: Calidad del Sueño</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            horas_sueno = st.selectbox("9. Horas de sueño:", ["<5h", "5–6.5h", "6.5–8h", ">8h"])
            tiempo_dormir = st.radio("10. ¿Tardas >30 min en dormir?", ["Sí", "No"])
        
        with col2:
            despertares = st.radio("11. ¿Te despiertas más de 1 vez?", ["Sí", "No"])
            descansado = st.radio("12. ¿Te sientes descansado?", ["Sí", "No"])
        
        st.markdown("""
        <div class="questionnaire-container">
            <h3>🔹 SECCIÓN 5: Estrés Percibido</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Responde en una escala de 0 (nunca) a 4 (muy frecuentemente):**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            estres1 = st.slider("13. ¿Te has sentido alterado por algo inesperado?", 0, 4, 2)
            estres2 = st.slider("14. ¿Te has sentido incapaz de controlar cosas importantes?", 0, 4, 2)
        
        with col2:
            estres3 = st.slider("15. ¿Te has sentido nervioso o estresado?", 0, 4, 2)
            estres4 = st.slider("16. ¿Has sentido que las dificultades se acumulan?", 0, 4, 2)
        
        # Email opcional
        st.markdown("---")
        enviar_email = st.checkbox("📧 Enviar resultados por email")
        email_destinatario = ""
        if enviar_email:
            email_destinatario = st.text_input("Correo electrónico:", placeholder="tu@email.com")
        
        submitted = st.form_submit_button("🔥 Calcular Balance Energético", use_container_width=True)
        
        if submitted:
            # Realizar cálculos
            tmb = calcular_tmb_katch_mcardle(peso, grasa_corporal)
            geaf = calcular_geaf(sexo, nivel_actividad_clean)
            gee = calcular_gee(peso, dias_entrenamiento)
            eta = 1.25  # Efecto térmico fijo
            
            # Calcular gasto energético total
            ge = (tmb * geaf + gee) * eta
            
            # Evaluar penalizaciones
            penalizacion_sueno = evaluar_calidad_sueno(horas_sueno, tiempo_dormir, despertares, descansado)
            penalizacion_estres = evaluar_estres([estres1, estres2, estres3, estres4])
            
            # FBEO final
            fbeo_base = ge
            penalizacion_total = penalizacion_sueno + penalizacion_estres
            fbeo_ajustado = fbeo_base * (1 - penalizacion_total)
            
            # Mostrar resultados
            st.markdown("""
            <div class="results-container">
                <h2>📊 Resultados de tu Balance Energético Óptimo</h2>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("🔥 TMB (Katch-McArdle)", f"{tmb:.0f} kcal")
                st.metric("⚡ GEAF", f"{geaf:.2f}")
                st.metric("🏃 GEE", f"{gee:.0f} kcal")
            
            with col2:
                st.metric("🍽️ ETA", f"{eta:.2f}")
                st.metric("📈 Gasto Energético Total", f"{ge:.0f} kcal")
                st.metric("😴 Penalización Sueño", f"{penalizacion_sueno*100:.0f}%")
            
            with col3:
                st.metric("😰 Penalización Estrés", f"{penalizacion_estres*100:.0f}%")
                st.metric("🎯 FBEO Base", f"{fbeo_base:.0f} kcal")
                st.metric("✅ FBEO Ajustado", f"{fbeo_ajustado:.0f} kcal", delta=f"{fbeo_ajustado-fbeo_base:.0f}")
            
            st.markdown(f"""
            <div class="results-container">
                <h3>🏆 Recomendación Final</h3>
                <h2 style="text-align: center; font-size: 2.5rem;">
                    {fbeo_ajustado:.0f} kcal/día
                </h2>
                <p style="text-align: center; font-size: 1.2rem;">
                    Esta es tu ingesta calórica recomendada para mantener tu balance energético óptimo.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enviar email si se solicitó
            if enviar_email and email_destinatario:
                contenido_email = f"""
                RESULTADOS DEL BALANCE ENERGÉTICO ÓPTIMO - MUPAI
                
                Datos del usuario:
                - Sexo: {sexo}
                - Edad: {edad} años
                - Peso: {peso} kg
                - Estatura: {estatura} cm
                - Grasa corporal: {grasa_corporal}%
                
                Resultados:
                - TMB: {tmb:.0f} kcal
                - GEAF: {geaf:.2f}
                - GEE: {gee:.0f} kcal
                - Gasto Energético Total: {ge:.0f} kcal
                - FBEO Ajustado: {fbeo_ajustado:.0f} kcal/día
                
                Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}
                """
                enviar_email_resultados(email_destinatario, "Resultados MUPAI - Balance Energético", contenido_email)

elif st.session_state.page == "preferencias_alimentarias":
    st.markdown("""
    <div class="section-header">
        <h2>🍽️ Cuestionario: Patrones y Preferencias Alimenticias</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("preferencias_alimentarias_form"):
        st.markdown("""
        <div class="questionnaire-container">
            <h3>Selecciona tus alimentos preferidos por categoría (puedes elegir múltiples opciones):</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🥩 Proteínas Magras")
            proteinas_magras = st.multiselect("", [
                "Pollo (pechuga)", "Pavo", "Atún", "Claras de huevo", 
                "Pescado blanco", "Camarones", "Pulpo"
            ], key="proteinas_magras")
            
            st.markdown("### 🥓 Proteínas con Grasa")
            proteinas_grasa = st.multiselect("", [
                "Huevo entero", "Arrachera", "Salmón", "Carne molida", 
                "Sardinas", "Pollo con piel", "Cerdo"
            ], key="proteinas_grasa")
            
            st.markdown("### 🍌 Frutas")
            frutas = st.multiselect("", [
                "Manzana", "Plátano", "Mango", "Uvas", "Naranja", 
                "Fresas", "Piña", "Kiwi", "Pera"
            ], key="frutas")
            
            st.markdown("### 🥦 Vegetales")
            vegetales = st.multiselect("", [
                "Espinaca", "Brócoli", "Jitomate", "Lechuga", "Calabaza", 
                "Zanahoria", "Pepino", "Apio", "Coliflor"
            ], key="vegetales")
        
        with col2:
            st.markdown("### 🍠 Carbohidratos con Almidón")
            carbohidratos = st.multiselect("", [
                "Arroz integral", "Avena", "Papa", "Camote", "Quinoa", 
                "Pan integral", "Pasta integral", "Tortilla"
            ], key="carbohidratos")
            
            st.markdown("### 🧀 Lácteos Bajos en Grasa")
            lacteos_light = st.multiselect("", [
                "Yogur natural light", "Queso cottage", "Leche descremada", 
                "Queso panela", "Yogur griego 0%"
            ], key="lacteos_light")
            
            st.markdown("### 🧀 Lácteos Altos en Grasa")
            lacteos_grasa = st.multiselect("", [
                "Queso crema", "Mantequilla", "Queso cheddar", "Leche entera", 
                "Yogur griego completo", "Crema"
            ], key="lacteos_grasa")
            
            st.markdown("### 🥑 Grasas Saludables")
            grasas = st.multiselect("", [
                "Aguacate", "Nueces", "Almendras", "Aceite de oliva", 
                "Aceite de coco", "Semillas de chía", "Cacahuates"
            ], key="grasas")
        
        st.markdown("---")
        st.markdown("""
        <div class="questionnaire-container">
            <h3>🔸 Información Adicional</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            incluir_suplementos = st.radio("¿Deseas incluir suplementos?", ["Sí", "No"])
            marcas_preferidas = st.text_area("¿Tienes preferencias de marcas específicas?", 
                                           placeholder="Ej: Proteína X, Avena Y...")
        
        with col2:
            alimentos_adicionales = st.text_area("¿Otros alimentos que consumes frecuentemente?", 
                                                placeholder="Ej: Te verde, chocolate negro...")
            
            tiene_alergias = st.radio("¿Tienes alergias o intolerancias alimentarias?", ["No", "Sí"])
            alergias_detalle = ""
            if tiene_alergias == "Sí":
                alergias_detalle = st.text_area("Especifica cuáles:", 
                                               placeholder="Ej: Lactosa, gluten, nueces...")
        
        # Email opcional
        st.markdown("---")
        enviar_email = st.checkbox("📧 Enviar resultados por email")
        email_destinatario = ""
        if enviar_email:
            email_destinatario = st.text_input("Correo electrónico:", placeholder="tu@email.com")
        
        submitted = st.form_submit_button("🍽️ Generar Perfil Alimentario", use_container_width=True)
        
        if submitted:
            # Procesar resultados
            st.markdown("""
            <div class="results-container">
                <h2>📊 Tu Perfil de Preferencias Alimentarias</h2>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🥩 Proteínas Seleccionadas")
                if proteinas_magras:
                    st.write("**Magras:** " + ", ".join(proteinas_magras))
                if proteinas_grasa:
                    st.write("**Con grasa:** " + ", ".join(proteinas_grasa))
                
                st.markdown("### 🍌 Frutas y Vegetales")
                if frutas:
                    st.write("**Frutas:** " + ", ".join(frutas))
                if vegetales:
                    st.write("**Vegetales:** " + ", ".join(vegetales))
            
            with col2:
                st.markdown("### 🍠 Carbohidratos y Lácteos")
                if carbohidratos:
                    st.write("**Carbohidratos:** " + ", ".join(carbohidratos))
                if lacteos_light or lacteos_grasa:
                    lacteos_todos = lacteos_light + lacteos_grasa
                    st.write("**Lácteos:** " + ", ".join(lacteos_todos))
                
                st.markdown("### 🥑 Grasas Saludables")
                if grasas:
                    st.write("**Grasas:** " + ", ".join(grasas))
            
            # Información adicional
            if incluir_suplementos == "Sí" or marcas_preferidas or alimentos_adicionales or tiene_alergias == "Sí":
                st.markdown("### 🔸 Información Adicional")
                if incluir_suplementos == "Sí":
                    st.write("✅ Incluye suplementos en el plan")
                if marcas_preferidas:
                    st.write(f"**Marcas preferidas:** {marcas_preferidas}")
                if alimentos_adicionales:
                    st.write(f"**Alimentos adicionales:** {alimentos_adicionales}")
                if tiene_alergias == "Sí":
                    st.write(f"**Alergias/Intolerancias:** {alergias_detalle}")
            
            # Generar recomendaciones básicas
            total_categorias = len([x for x in [proteinas_magras, proteinas_grasa, frutas, vegetales, carbohidratos, lacteos_light, lacteos_grasa, grasas] if x])
            
            st.markdown(f"""
            <div class="results-container">
                <h3>🎯 Resumen de tu Perfil</h3>
                <p><strong>Categorías seleccionadas:</strong> {total_categorias}/8</p>
                <p><strong>Variedad alimentaria:</strong> {"Excelente" if total_categorias >= 6 else "Buena" if total_categorias >= 4 else "Limitada"}</p>
                <p>Este perfil será utilizado para personalizar tus recomendaciones nutricionales.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enviar email si se solicitó
            if enviar_email and email_destinatario:
                contenido_email = f"""
                PERFIL DE PREFERENCIAS ALIMENTARIAS - MUPAI
                
                Proteínas magras: {', '.join(proteinas_magras) if proteinas_magras else 'Ninguna'}
                Proteínas con grasa: {', '.join(proteinas_grasa) if proteinas_grasa else 'Ninguna'}
                Frutas: {', '.join(frutas) if frutas else 'Ninguna'}
                Vegetales: {', '.join(vegetales) if vegetales else 'Ninguna'}
                Carbohidratos: {', '.join(carbohidratos) if carbohidratos else 'Ninguna'}
                Lácteos bajos en grasa: {', '.join(lacteos_light) if lacteos_light else 'Ninguna'}
                Lácteos altos en grasa: {', '.join(lacteos_grasa) if lacteos_grasa else 'Ninguna'}
                Grasas saludables: {', '.join(grasas) if grasas else 'Ninguna'}
                
                Suplementos: {incluir_suplementos}
                Marcas preferidas: {marcas_preferidas}
                Alimentos adicionales: {alimentos_adicionales}
                Alergias: {alergias_detalle if tiene_alergias == "Sí" else "Ninguna"}
                
                Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}
                """
                enviar_email_resultados(email_destinatario, "Resultados MUPAI - Preferencias Alimentarias", contenido_email)

elif st.session_state.page == "antojos_alimentarios":
    st.markdown("""
    <div class="section-header">
        <h2>🧁 Cuestionario: Antojos Alimentarios</h2>
    </div>
    """, unsafe_allow_html=True)
    
    categorias_antojos = [
        ("🧁", "Panes dulces"),
        ("🍟", "Frituras"),
        ("🍫", "Chocolates"),
        ("🌮", "Antojitos mexicanos"),
        ("🍔", "Fast food"),
        ("🍕", "Pizza"),
        ("🍰", "Postres"),
        ("🥤", "Bebidas azucaradas"),
        ("🍪", "Galletas"),
        ("🍦", "Helados")
    ]
    
    with st.form("antojos_alimentarios_form"):
        st.markdown("""
        <div class="questionnaire-container">
            <h3>Para cada categoría de alimento, evalúa tu relación con los antojos:</h3>
        </div>
        """, unsafe_allow_html=True)
        
        resultados_antojos = {}
        
        for i, (emoji, categoria) in enumerate(categorias_antojos):
            st.markdown(f"""
            <div class="questionnaire-container">
                <h4>{emoji} {categoria}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                frecuencia = st.selectbox(
                    "Frecuencia:",
                    ["Nunca", "Rara vez", "Algunas veces", "Frecuente", "Casi diario"],
                    key=f"freq_{i}"
                )
                
                momento = st.selectbox(
                    "Momento del día:",
                    ["Mañana", "Tarde", "Noche", "Madrugada", "Variable"],
                    key=f"momento_{i}"
                )
            
            with col2:
                intensidad = st.selectbox(
                    "Intensidad del antojo:",
                    ["Leve", "Moderada", "Fuerte", "Muy fuerte"],
                    key=f"intensidad_{i}"
                )
                
                control = st.selectbox(
                    "Nivel de control:",
                    ["Siempre", "Casi siempre", "A veces", "Rara vez", "Nunca"],
                    key=f"control_{i}"
                )
            
            with col3:
                respuesta = st.selectbox(
                    "¿Cómo respondes?:",
                    ["Ignoro", "Alterno por algo sano", "Lo como", "Me arrepiento", "Otro"],
                    key=f"respuesta_{i}"
                )
                
                emocion = st.selectbox(
                    "Emoción asociada:",
                    ["Estrés", "Ansiedad", "Tristeza", "Aburrimiento", "Alegría", "Hambre real", "No lo sé"],
                    key=f"emocion_{i}"
                )
            
            resultados_antojos[categoria] = {
                "frecuencia": frecuencia,
                "momento": momento,
                "intensidad": intensidad,
                "control": control,
                "respuesta": respuesta,
                "emocion": emocion,
                "emoji": emoji
            }
            
            st.markdown("---")
        
        # Email opcional
        enviar_email = st.checkbox("📧 Enviar resultados por email")
        email_destinatario = ""
        if enviar_email:
            email_destinatario = st.text_input("Correo electrónico:", placeholder="tu@email.com")
        
        submitted = st.form_submit_button("🧁 Analizar Patrones de Antojos", use_container_width=True)
        
        if submitted:
            # Analizar resultados
            st.markdown("""
            <div class="results-container">
                <h2>📊 Análisis de tus Patrones de Antojos</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Calcular estadísticas
            frecuencias_altas = []
            momentos = []
            emociones = []
            control_bajo = []
            
            for categoria, datos in resultados_antojos.items():
                if datos["frecuencia"] in ["Frecuente", "Casi diario"]:
                    frecuencias_altas.append(f"{datos['emoji']} {categoria}")
                
                momentos.append(datos["momento"])
                emociones.append(datos["emocion"])
                
                if datos["control"] in ["Rara vez", "Nunca"]:
                    control_bajo.append(f"{datos['emoji']} {categoria}")
            
            # Encontrar patrones
            from collections import Counter
            
            momento_comun = Counter(momentos).most_common(1)[0][0] if momentos else "No definido"
            emocion_comun = Counter(emociones).most_common(1)[0][0] if emociones else "No definida"
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🔥 Categorías Más Frecuentes")
                if frecuencias_altas:
                    for categoria in frecuencias_altas[:3]:
                        st.write(f"• {categoria}")
                else:
                    st.write("No se identificaron antojos frecuentes")
                
                st.markdown("### ⏰ Momento Crítico")
                st.write(f"**{momento_comun}**")
                
                st.markdown("### 🎭 Emoción Detonante Principal")
                st.write(f"**{emocion_comun}**")
            
            with col2:
                st.markdown("### ⚠️ Áreas de Menor Control")
                if control_bajo:
                    for categoria in control_bajo[:3]:
                        st.write(f"• {categoria}")
                else:
                    st.write("Buen control general identificado")
                
                # Nivel de autocontrol general
                total_control = sum(1 for datos in resultados_antojos.values() 
                                  if datos["control"] in ["Siempre", "Casi siempre"])
                porcentaje_control = (total_control / len(resultados_antojos)) * 100
                
                st.markdown("### 🎯 Nivel de Autocontrol General")
                st.metric("", f"{porcentaje_control:.0f}%")
                
                if porcentaje_control >= 70:
                    st.success("🟢 Excelente autocontrol")
                elif porcentaje_control >= 50:
                    st.warning("🟡 Autocontrol moderado")
                else:
                    st.error("🔴 Autocontrol bajo - requiere atención")
            
            # Recomendaciones personalizadas
            st.markdown("""
            <div class="results-container">
                <h3>💡 Recomendaciones Personalizadas</h3>
            </div>
            """, unsafe_allow_html=True)
            
            recomendaciones = []
            
            if momento_comun == "Noche":
                recomendaciones.append("🌙 Planifica snacks saludables para la noche")
            elif momento_comun == "Tarde":
                recomendaciones.append("🌅 Asegúrate de tener un almuerzo completo y satisfactorio")
            
            if emocion_comun == "Estrés":
                recomendaciones.append("🧘‍♀️ Considera técnicas de manejo del estrés como meditación")
            elif emocion_comun == "Aburrimiento":
                recomendaciones.append("🎯 Busca actividades alternativas para ocupar el tiempo libre")
            
            if porcentaje_control < 50:
                recomendaciones.append("📝 Considera llevar un diario alimentario para mayor consciencia")
            
            for rec in recomendaciones:
                st.write(f"• {rec}")
            
            # Enviar email si se solicitó
            if enviar_email and email_destinatario:
                contenido_email = f"""
                ANÁLISIS DE ANTOJOS ALIMENTARIOS - MUPAI
                
                PATRONES IDENTIFICADOS:
                
                Categorías más frecuentes:
                {chr(10).join(frecuencias_altas) if frecuencias_altas else "Ninguna identificada"}
                
                Momento crítico: {momento_comun}
                Emoción detonante principal: {emocion_comun}
                Nivel de autocontrol general: {porcentaje_control:.0f}%
                
                Áreas de menor control:
                {chr(10).join(control_bajo) if control_bajo else "Buen control general"}
                
                RECOMENDACIONES:
                {chr(10).join(recomendaciones)}
                
                Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}
                """
                enviar_email_resultados(email_destinatario, "Resultados MUPAI - Antojos Alimentarios", contenido_email)

elif st.session_state.page == "about":
    st.markdown("""
    <div class="section-header">
        <h2>👨‍⚕️ Acerca de Mí</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Aquí puedes agregar tu foto de perfil
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <div style="width: 200px; height: 200px; background-color: #FFCC00; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-size: 4rem;">
                👨‍⚕️
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        ### 🎓 Perfil Profesional
        
        **Especialista en Fitness y Nutrición Personalizada**
        
        Con años de experiencia en el desarrollo de programas de transformación física basados en evidencia científica, me especializo en:
        
        - 🔬 Evaluación de composición corporal
        - 📊 Cálculos metabólicos personalizados  
        - 🍽️ Planificación nutricional individualizada
        - 🏋️‍♂️ Diseño de programas de entrenamiento
        - 🧠 Coaching en cambio de hábitos
        
        ### 📜 Certificaciones
        - Nutrición Deportiva Avanzada
        - Evaluación de Composición Corporal
        - Metabolismo y Balance Energético
        - Psicología del Comportamiento Alimentario
        """)
    
    st.markdown("""
    ### 🎯 Mi Filosofía
    
    Creo firmemente que cada persona es única y merece un enfoque personalizado para alcanzar sus objetivos de salud y fitness. 
    Mi metodología combina:
    
    - **Ciencia**: Bases sólidas en fisiología y nutrición
    - **Personalización**: Planes adaptados a tu estilo de vida
    - **Sostenibilidad**: Cambios que puedas mantener a largo plazo
    - **Apoyo**: Acompañamiento constante en tu proceso
    
    ### 🏆 Resultados que Lograrás
    
    - ✅ Mayor claridad sobre tus necesidades nutricionales
    - ✅ Mejor relación con la comida
    - ✅ Incremento en tu nivel de energía
    - ✅ Composición corporal optimizada
    - ✅ Hábitos saludables duraderos
    """)

elif st.session_state.page == "contacto":
    st.markdown("""
    <div class="section-header">
        <h2>📞 Contacto</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📱 Información de Contacto
        
        **📧 Email:** contacto@mupai.com
        
        **📱 WhatsApp:** +52 123 456 7890
        
        **📍 Ubicación:** Ciudad de México, México
        
        **🕒 Horarios de Atención:**
        - Lunes a Viernes: 9:00 AM - 7:00 PM
        - Sábados: 10:00 AM - 4:00 PM
        - Domingos: Solo emergencias
        
        ### 🌐 Redes Sociales
        
        - **Instagram:** @mupai_fitness
        - **Facebook:** MUPAI Fitness
        - **YouTube:** MUPAI Nutrition
        """)
    
    with col2:
        st.markdown("""
        ### 💬 Envía un Mensaje
        """)
        
        with st.form("contacto_form"):
            nombre = st.text_input("Nombre completo:")
            email = st.text_input("Email:")
            telefono = st.text_input("Teléfono (opcional):")
            asunto = st.selectbox("Asunto:", [
                "Consulta general",
                "Solicitar asesoría personalizada", 
                "Dudas sobre cuestionarios",
                "Colaboración profesional",
                "Otro"
            ])
            mensaje = st.text_area("Mensaje:", height=150)
            
            submitted = st.form_submit_button("📤 Enviar Mensaje", use_container_width=True)
            
            if submitted:
                if nombre and email and mensaje:
                    st.success("✅ ¡Mensaje enviado exitosamente! Te contactaré pronto.")
                    # Aquí puedes agregar la lógica para enviar el email
                else:
                    st.error("❌ Por favor completa todos los campos obligatorios.")
    
    st.markdown("---")
    st.markdown("""
    ### 🤝 Servicios Disponibles
    
    - **🔍 Evaluación Inicial Completa** - Análisis detallado de tu estado actual
    - **📋 Plan Nutricional Personalizado** - Diseñado específicamente para tus objetivos
    - **🏋️‍♂️ Programa de Entrenamiento** - Adaptado a tu nivel y disponibilidad
    - **📞 Seguimiento Mensual** - Monitoreo y ajustes continuos
    - **🎯 Coaching Grupal** - Sesiones de grupo para motivación adicional
    
    ### 💰 Inversión en tu Salud
    
    Contacta para conocer nuestros paquetes y opciones de pago flexibles. 
    ¡Tu transformación comienza con el primer paso!
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    <p>💪 <strong>MUPAI</strong> - Plataforma Digital Profesional para Fitness y Nutrición Personalizada</p>
    <p>© 2025 MUPAI. Todos los derechos reservados.</p>
</div>
""", unsafe_allow_html=True)
