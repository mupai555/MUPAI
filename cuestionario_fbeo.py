# cuestionario_fbeo.py
import streamlit as st
import numpy as np
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# CONFIGURACIÓN DEL NUTRIÓLOGO
CORREO_NUTRIOLOGO = "erick@mupai.com"  # CAMBIA ESTO A TU CORREO REAL

def mostrar_cuestionario_fbeo():
    """Función principal del cuestionario FBEO"""
    
    # CSS específico para FBEO
    st.markdown("""
    <style>
        .fbeo-header {
            background: linear-gradient(135deg, #FFCC00 0%, #FFD700 50%, #FFA500 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .fbeo-section {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 5px solid #FFCC00;
            margin: 1rem 0;
        }
        .fbeo-results {
            background: linear-gradient(135deg, #FFCC00 0%, #FFE066 50%, #FFF2A6 100%);
            padding: 2rem;
            border-radius: 15px;
            color: #000;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="fbeo-header">
        <h2>🌱 Cuestionario MUPAI/Factores de Estilo de Vida</h2>
        <p style="font-size: 1.2rem; margin: 0;">Factor de Balance Energético Óptimo (FBEO)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar estado
    if 'fbeo_seccion' not in st.session_state:
        st.session_state.fbeo_seccion = 0
    if 'fbeo_datos' not in st.session_state:
        st.session_state.fbeo_datos = {}
    if 'fbeo_completado' not in st.session_state:
        st.session_state.fbeo_completado = False
          
    # Lista de secciones
    secciones = [
        "Datos Personales y Composición Corporal",
        "Selección Alimentaria",
        "Antojos Alimentarios", 
        "Comer Emocional",
        "Estrés Percibido",
        "Calidad de Sueño",
        "Actividad Física",
        "Resumen y Cálculo FBEO"
    ]
    
    # Si está completado, mostrar resultados
    if st.session_state.fbeo_completado:
        mostrar_resultados_fbeo()
        return
    
    # Barra de progreso
    progreso = st.session_state.fbeo_seccion / (len(secciones) - 1)
    st.progress(progreso)
    st.write(f"**Sección {st.session_state.fbeo_seccion + 1} de {len(secciones)}:** {secciones[st.session_state.fbeo_seccion]}")
    
    # Formulario principal
    with st.form("fbeo_form"):
        
        # SECCIÓN 0: DATOS PERSONALES
        if st.session_state.fbeo_seccion == 0:
            st.markdown('<div class="fbeo-section">', unsafe_allow_html=True)
            st.header("📋 Datos Personales y Composición Corporal")
            
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre completo*")
                edad = st.number_input("Edad*", min_value=18, max_value=100, value=25)
                genero = st.radio("Género*", ["Masculino", "Femenino"])
            
            with col2:
                email = st.text_input("Correo electrónico*")
                ocupacion = st.text_input("Ocupación")
            
            st.subheader("📊 Datos de Bioimpedancia Eléctrica")
            st.info("💡 Ingresa los datos obtenidos de tu medición con bioimpedancia")
            
            col3, col4, col5 = st.columns(3)
            with col3:
                peso = st.number_input("Peso (kg)*", min_value=30.0, max_value=200.0, step=0.1)
            with col4:
                estatura = st.number_input("Estatura (m)*", min_value=1.0, max_value=2.5, step=0.01)
            with col5:
                porcentaje_grasa = st.number_input("% Grasa Corporal*", min_value=5.0, max_value=50.0, step=0.1)
            
            dias_entrenamiento = st.slider("Días de entrenamiento de fuerza por semana", 0, 7, 0)
            st.markdown('</div>', unsafe_allow_html=True)
                  
        # SECCIÓN 1: SELECCIÓN ALIMENTARIA
        elif st.session_state.fbeo_seccion == 1:
            st.markdown('<div class="fbeo-section">', unsafe_allow_html=True)
            st.header("🍽️ Selección Alimentaria Personalizada")
            st.write("Marca todos los alimentos que consumes con facilidad o disfrutas")
            
            # Grupo 1: Proteína animal con grasa
            with st.expander("🥩 GRUPO 1: Proteína Animal con Más Contenido Graso", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    huevos_embutidos = st.multiselect(
                        "🍳 Huevos y embutidos",
                        ["Huevo entero", "Chorizo", "Salchicha", "Longaniza", "Tocino", "Jamón serrano"]
                    )
                    carnes_grasas = st.multiselect(
                        "🥩 Carnes grasas",
                        ["Costilla de res", "Costilla de cerdo", "Ribeye", "T-bone", "Arrachera", "Molida 80/20"]
                    )
                with col2:
                    quesos_grasos = st.multiselect(
                        "🧀 Quesos grasos",
                        ["Manchego", "Doble crema", "Oaxaca", "Gouda", "Cheddar"]
                    )
                    lacteos_enteros = st.multiselect(
                        "🥛 Lácteos enteros",
                        ["Leche entera", "Yogur entero", "Crema", "Yogur griego entero"]
                    )
            
            # Grupo 2: Proteína magra
            with st.expander("🍗 GRUPO 2: Proteína Animal Magra"):
                col1, col2 = st.columns(2)
                with col1:
                    carnes_magras = st.multiselect(
                        "🍗 Carnes magras",
                        ["Pechuga de pollo", "Filete de res", "Lomo de cerdo", "Atún en agua"]
                    )
                with col2:
                    pescados_blancos = st.multiselect(
                        "🐟 Pescados blancos",
                        ["Tilapia", "Basa", "Huachinango", "Robalo"]
                    )
            
            # Grupo 3: Grasas saludables
            with st.expander("🥑 GRUPO 3: Grasas Saludables"):
                grasas_naturales = st.multiselect(
                    "🥑 Grasas naturales",
                    ["Aguacate", "Aceitunas", "Coco", "Mantequilla de almendra"]
                )
                frutos_secos = st.multiselect(
                    "🌰 Frutos secos",
                    ["Almendras", "Nueces", "Pistaches", "Cacahuates", "Semillas de chía"]
                )
            
            # Grupo 4: Carbohidratos
            with st.expander("🍞 GRUPO 4: Carbohidratos"):
                cereales = st.multiselect(
                    "🌾 Cereales",
                    ["Avena", "Arroz", "Quinoa", "Pan integral", "Pasta"]
                )
                tuberculos = st.multiselect(
                    "🥔 Tubérculos",
                    ["Papa", "Camote", "Yuca", "Plátano"]
                )
            
            # Grupo 5 y 6: Vegetales y Frutas
            with st.expander("🥬 GRUPO 5: Vegetales"):
                vegetales = st.multiselect(
                    "Selecciona los vegetales",
                    ["Espinaca", "Brócoli", "Lechuga", "Tomate", "Zanahoria", "Pepino"]
                )
            
            with st.expander("🍎 GRUPO 6: Frutas"):
                frutas = st.multiselect(
                    "Selecciona las frutas",
                    ["Manzana", "Plátano", "Naranja", "Fresas", "Mango", "Piña"]
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
                  
        # SECCIÓN 2: ANTOJOS Y COMER EMOCIONAL
        elif st.session_state.fbeo_seccion == 2:
            st.markdown('<div class="fbeo-section">', unsafe_allow_html=True)
            st.header("😋 Antojos Alimentarios")
            
            antojos_dulces = st.multiselect(
                "🍫 Dulces/postres",
                ["Chocolate", "Galletas", "Pastel", "Helado", "Pan dulce"]
            )
            antojos_salados = st.multiselect(
                "🧂 Salados/snacks",
                ["Papas fritas", "Palomitas", "Nachos", "Pretzels"]
            )
            
            st.subheader("📋 Cuestionario del Comer Emocional")
            st.write("Indica con qué frecuencia comes en respuesta a estas emociones (1=Nunca, 5=Siempre)")
            
            emociones = [
                "¿Comes cuando estás de mal humor?",
                "¿Comes cuando te sientes solo/a?",
                "¿Comes cuando estás aburrido/a?",
                "¿Comes cuando te sientes ansioso/a?",
                "¿Comes cuando estás triste?"
            ]
            
            respuestas_emocionales = []
            for i, emocion in enumerate(emociones):
                valor = st.slider(emocion, 1, 5, 1, key=f"emo_{i}")
                respuestas_emocionales.append(valor)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # SECCIÓN 3: ESTRÉS
        elif st.session_state.fbeo_seccion == 3:
            st.markdown('<div class="fbeo-section">', unsafe_allow_html=True)
            st.header("😰 Escala de Estrés Percibido (PSS-4)")
            st.write("Responde sobre tus sentimientos durante el último mes")
            
            preguntas_estres = [
                "¿Con qué frecuencia te has sentido incapaz de controlar las cosas importantes?",
                "¿Con qué frecuencia te has sentido confiado/a en tu capacidad? (invertida)",
                "¿Con qué frecuencia has sentido que las dificultades se acumulan?",
                "¿Con qué frecuencia has sentido que todo te salía bien? (invertida)"
            ]
            
            respuestas_estres = []
            for i, pregunta in enumerate(preguntas_estres):
                valor = st.slider(pregunta, 1, 5, 3, key=f"estres_{i}")
                respuestas_estres.append(valor)
            
            st.info("1=Nunca, 2=Casi nunca, 3=A veces, 4=Frecuentemente, 5=Muy frecuentemente")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # SECCIÓN 4: CALIDAD DE SUEÑO
        elif st.session_state.fbeo_seccion == 4:
            st.markdown('<div class="fbeo-section">', unsafe_allow_html=True)
            st.header("😴 Calidad de Sueño (Pittsburgh)")
            
            col1, col2 = st.columns(2)
            with col1:
                horas_sueno = st.selectbox(
                    "Horas de sueño por noche",
                    ["< 5 horas", "5-6 horas", "6-7 horas", "7-8 horas", "8-9 horas", "> 9 horas"]
                )
                tiempo_dormirse = st.selectbox(
                    "Tiempo para quedarse dormido",
                    ["< 15 min", "15-30 min", "30-45 min", "45-60 min", "> 60 min"]
                )
            
            with col2:
                despertares = st.selectbox(
                    "Despertares nocturnos",
                    ["Ninguno", "1-2 veces", "3-4 veces", "5-6 veces", "> 6 veces"]
                )
                calidad_sueno = st.selectbox(
                    "Calidad general del sueño",
                    ["Muy buena", "Buena", "Regular", "Mala", "Muy mala"]
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
                  
        # SECCIÓN 5: ACTIVIDAD FÍSICA
        elif st.session_state.fbeo_seccion == 5:
            st.markdown('<div class="fbeo-section">', unsafe_allow_html=True)
            st.header("🏃 Nivel de Actividad Física (GEAF)")
            
            nivel_actividad = st.radio(
                "Selecciona tu nivel de actividad:",
                [
                    "🪑 Sedentario - Trabajo sentado, <7,500 pasos",
                    "🚶 Moderadamente activo - 7,500-9,999 pasos",
                    "🧍 Activo - 10,000-12,500 pasos",
                    "🔨 Muy activo - >12,500 pasos"
                ]
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # SECCIÓN 6: RESUMEN
        elif st.session_state.fbeo_seccion == 6:
            st.markdown('<div class="fbeo-section">', unsafe_allow_html=True)
            st.header("📊 Resumen de tu Evaluación")
            st.success("✅ Todos los datos han sido recopilados")
            st.info("Al hacer clic en 'Completar', se calculará tu FBEO y se enviará al especialista")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Botones de navegación
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.session_state.fbeo_seccion > 0:
                if st.form_submit_button("⬅️ Anterior", use_container_width=True):
                    st.session_state.fbeo_seccion -= 1
                    st.rerun()
        
        with col3:
            if st.session_state.fbeo_seccion < len(secciones) - 1:
                if st.form_submit_button("Siguiente ➡️", use_container_width=True):
                    # Aquí guardarías los datos de cada sección
                    guardar_datos_seccion()
                    st.session_state.fbeo_seccion += 1
                    st.rerun()
            else:
                if st.form_submit_button("✅ Completar Evaluación", use_container_width=True):
                    st.session_state.fbeo_completado = True
                    # Procesar y enviar datos
                    procesar_fbeo()
                    st.rerun()

def guardar_datos_seccion():
    """Guarda los datos de la sección actual"""
    # Aquí implementarías la lógica para guardar los datos
    pass

def procesar_fbeo():
    """Procesa el cálculo FBEO y envía los resultados"""
    # Aquí implementarías el cálculo completo del FBEO
    pass

def mostrar_resultados_fbeo():
    """Muestra los resultados al usuario"""
    st.markdown("""
    <div class="fbeo-results">
        <h2>✅ Evaluación FBEO Completada</h2>
        <p>¡Gracias por completar el cuestionario!</p>
        <p>Los resultados han sido enviados al especialista y recibirás un plan personalizado pronto.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Realizar Nueva Evaluación"):
        st.session_state.fbeo_completado = False
        st.session_state.fbeo_seccion = 0
        st.session_state.fbeo_datos = {}
        st.rerun()