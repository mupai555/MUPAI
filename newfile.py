import streamlit as st
from datetime import time, datetime

# Configuración de la página
st.set_page_config(
    page_title="MUPAI - Entrenamiento Digital",
    page_icon="🤖",
    layout="wide",
)

# Barra lateral de navegación
menu = st.sidebar.selectbox(
    "Menú",
    ["Inicio", "Sobre Mí", "Servicios", "Perfil MUPAI/Salud y Rendimiento", "Contacto"]
)

# Contenido según la selección del menú
if menu == "Inicio":
    st.image("LOGO.png", use_column_width=True)
    st.title("Bienvenido a MUPAI")
    
    # ... (Mismo contenido original)

elif menu == "Sobre Mí":
    st.title("Sobre Mí")
    # ... (Mismo contenido original)

elif menu == "Servicios":
    st.title("Servicios")
    # ... (Mismo contenido original)

elif menu == "Perfil MUPAI/Salud y Rendimiento":
    submenu = st.sidebar.radio(
        "Selecciona una opción", 
        ["Entrenamiento", "Nutrición"],
        key="submenu_selector"
    )
    
    if submenu == "Entrenamiento":
        st.title("📋 Evaluación Integral MUPAI")
        
        with st.form("cuestionario_mupai"):
            # ===== SECCIÓN 1: DATOS PERSONALES =====
            st.header("1. Información Básica")
            nombre = st.text_input("Nombre completo:")
            edad = st.number_input("Edad (años):", 18, 100)
            genero = st.radio("Sexo biológico:", ["Hombre", "Mujer"])
            
            # ===== SECCIÓN 2: COMPOSICIÓN CORPORAL =====
            st.header("2. Medidas Corporales")
            col1, col2, col3 = st.columns(3)
            with col1:
                peso = st.number_input("Peso (kg):", 40.0, 200.0)
            with col2:
                altura = st.number_input("Altura (cm):", 140, 220)
            with col3:
                grasa = st.number_input("% Grasa corporal:", 5.0, 50.0)
            
            # ===== SECCIÓN 3: IPAQ =====
            st.header("3. Actividad Física (IPAQ)")
            with st.expander("Cuestionario IPAQ"):
                # Actividades vigorosas
                st.subheader("Actividades Vigorosas")
                vig_dias = st.slider("Días/semana con actividades intensas:", 0, 7)
                vig_tiempo = st.number_input("Minutos/día:", 0, 1440)
                
                # Actividades moderadas
                st.subheader("Actividades Moderadas")
                mod_dias = st.slider("Días/semana con actividades moderadas:", 0, 7)
                mod_tiempo = st.number_input("Minutos/día:", 0, 1440)
                
                # Caminata
                st.subheader("Caminatas")
                cam_dias = st.slider("Días/semana caminando:", 0, 7)
                cam_tiempo = st.number_input("Minutos/día:", 0, 1440)
                
                # Tiempo sentado
                st.subheader("Sedentarismo")
                sent_tiempo = st.number_input("Minutos/día sentado:", 0, 1440)
            
            # ===== SECCIÓN 4: PSQI =====
            st.header("4. Calidad del Sueño (PSQI)")
            with st.expander("Cuestionario de Sueño"):
                col1, col2 = st.columns(2)
                with col1:
                    hora_acostar = st.time_input("Hora de acostarse:")
                with col2:
                    hora_levantar = st.time_input("Hora de despertarse:")
                
                # Componente 2: Latencia
                latencia = st.selectbox("Tiempo en conciliar el sueño:", 
                    ["<15 min (0)", "16-30 min (1)", "31-60 min (2)", ">60 min (3)"])
                
                # Componente 3: Duración
                horas_sueño = st.selectbox("Horas de sueño real:", 
                    [">7h (0)", "6-7h (1)", "5-6h (2)", "<5h (3)"])
                
                # Componente 5: Perturbaciones
                st.subheader("Problemas durante el sueño (último mes)")
                perturbaciones = [
                    "Despertar por la noche", "Ir al baño", "Dificultad respirar",
                    "Ronquidos/toser", "Frío/calor", "Pesadillas", "Dolor físico"
                ]
                punt_perturbaciones = []
                for p in perturbaciones:
                    freq = st.selectbox(p, 
                        ["Ninguna (0)", "<1/sem (1)", "1-2/sem (2)", "≥3/sem (3)"])
                    punt_perturbaciones.append(int(freq[-2]))
                
                # Componente 6: Medicación
                medicacion = st.selectbox("Uso de pastillas para dormir:", 
                    ["Ninguna (0)", "<1/sem (1)", "1-2/sem (2)", "≥3/sem (3)"])
            
            # ===== SECCIÓN 5: PSS-10 =====
            st.header("5. Estrés Percibido (PSS-10)")
            with st.expander("Escala de Estrés"):
                preguntas = [
                    "Molesto por cosas inesperadas",
                    "Incapacidad de controlar cosas importantes",
                    "Sentirse nervioso/estresado",
                    "Confianza en resolver problemas (invertida)",
                    "Las cosas van bien (invertida)",
                    "No cumplir obligaciones",
                    "Controlar irritaciones (invertida)",
                    "Control de la situación (invertida)",
                    "Enojo por cosas fuera de control",
                    "Problemas acumulados"
                ]
                
                respuestas = []
                for i, pregunta in enumerate(preguntas):
                    opcion = st.radio(pregunta, 
                        ["Nunca (0)", "Casi nunca (1)", "A veces (2)", 
                         "A menudo (3)", "Muy a menudo (4)"],
                        horizontal=True)
                    punt = int(opcion[-2])
                    
                    # Invertir preguntas 4,5,7,8
                    if i in [3,4,6,7]:
                        punt = 4 - punt
                    respuestas.append(punt)
            
            # ===== ENVÍO =====
            submitted = st.form_submit_button("Generar Reporte")
            
            if submitted:
                # === CÁLCULOS ===
                # FFMI
                mlg = peso * (1 - (grasa/100))
                ffmi = mlg / ((altura/100)**2)
                
                # PSQI
                punt_sueño = (
                    int(latencia[-2]) + 
                    int(horas_sueño[-2]) + 
                    sum(punt_perturbaciones) + 
                    int(medicacion[-2])
                )
                
                # PSS-10
                estres_total = sum(respuestas)
                
                # IPAQ
                met_vig = vig_dias * (vig_tiempo * 8.0)
                met_mod = mod_dias * (mod_tiempo * 4.0)
                met_cam = cam_dias * (cam_tiempo * 3.3)
                met_total = met_vig + met_mod + met_cam
                
                # === RESULTADOS ===
                st.success("**Resultados de la Evaluación**")
                
                # Columnas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("FFMI", f"{ffmi:.1f}", help="Índice de Masa Libre de Grasa")
                    st.metric("Nivel Entrenamiento", 
                        "Principiante" if ffmi < 18 else "Avanzado" if ffmi < 22 else "Élite")
                
                with col2:
                    st.metric("Calidad de Sueño", 
                        f"{punt_sueño}/21", 
                        "Buena" if punt_sueño <6 else "Mala" if punt_sueño>10 else "Regular")
                    st.metric("Estrés Percibido", 
                        f"{estres_total}/40", 
                        "Bajo" if estres_total<14 else "Alto" if estres_total>26 else "Moderado")
                
                with col3:
                    st.metric("Actividad Física", 
                        f"{met_total:.0f} MET-min/sem", 
                        "Sedentario" if met_total<600 else "Activo")
                    st.metric("Tiempo Sentado", f"{sent_tiempo} min/día")
                
                # Recomendaciones
                with st.expander("🔍 Plan de Acción Personalizado"):
                    st.write("""
                    **Entrenamiento:** 
                    - Frecuencia: 4 días/semana 
                    - Enfoque: {'Fuerza' if ffmi <20 else 'Hipertrofia'}
                    
                    **Recuperación:**
                    - Técnicas de relajación diarias
                    - Higiene del sueño: Mantener horarios regulares
                    
                    **Nutrición:**
                    - {'Déficit calórico' if grasa >20 else 'Mantenimiento'}
                    - Suplementación: Proteína + Creatina
                    """)

    elif submenu == "Nutrición":
        st.title("Nutrición")
        # ... (Mismo contenido original)

elif menu == "Contacto":
    st.title("Contacto")
    # ... (Mismo contenido original)
