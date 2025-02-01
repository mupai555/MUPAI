import streamlit as st
from datetime import time

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
    st.image("LOGO.png", use_container_width=True)
    st.title("Bienvenido a MUPAI")
    
    # [...] (Sección Inicio sin cambios)

elif menu == "Sobre Mí":
    st.title("Sobre Mí")
    # [...] (Sección Sobre Mí sin cambios)

elif menu == "Servicios":
    st.title("Servicios")
    # [...] (Sección Servicios sin cambios)

elif menu == "Perfil MUPAI/Salud y Rendimiento":
    submenu = st.sidebar.radio(
        "Selecciona una opción", 
        ["Entrenamiento", "Nutrición"],
        key="submenu_selector"
    )
    
    if submenu == "Entrenamiento":
        st.title("📋 Cuestionario Integral de Evaluación MUPAI")
        
        with st.form("cuestionario_mupai"):
            # Sección 1: Información Personal
            st.header("1. Información Personal")
            nombre = st.text_input("Nombre completo legal:")
            edad = st.number_input("Edad (años):", min_value=0, max_value=120, step=1)
            genero = st.radio("Género biológico:", ["Hombre", "Mujer"])
            
            # Sección 2: Cálculo FFMI
            st.header("2. Composición Corporal")
            col1, col2, col3 = st.columns(3)
            with col1:
                peso = st.number_input("Peso actual (kg):", min_value=30.0, max_value=300.0, step=0.1)
            with col2:
                altura = st.number_input("Altura (cm):", min_value=100, max_value=250, step=1)
            with col3:
                grasa = st.number_input("Porcentaje de grasa corporal:", min_value=5.0, max_value=50.0, step=0.1)
            
            # Sección 3: IPAQ
            st.header("3. Actividad Física (IPAQ)")
            with st.expander("Cuestionario de Actividad Física"):
                st.subheader("Actividades Vigorosas")
                vig_dias = st.number_input("Días con actividades vigorosas:", 0, 7)
                vig_horas = st.number_input("Horas por día:", 0, 24)
                vig_minutos = st.number_input("Minutos por día:", 0, 59)
                
                st.subheader("Actividades Moderadas")
                mod_dias = st.number_input("Días con actividades moderadas:", 0, 7)
                mod_horas = st.number_input("Horas por día:", 0, 24)
                mod_minutos = st.number_input("Minutos por día:", 0, 59)
                
                st.subheader("Caminata")
                cam_dias = st.number_input("Días caminando:", 0, 7)
                cam_horas = st.number_input("Horas por día:", 0, 24)
                cam_minutos = st.number_input("Minutos por día:", 0, 59)
                
                st.subheader("Tiempo Sentado")
                sent_horas = st.number_input("Horas sentado por día:", 0, 24)
                sent_minutos = st.number_input("Minutos sentado por día:", 0, 59)
            
            # Sección 4: PSQI (Sueño)
            st.header("4. Calidad del Sueño (PSQI)")
            with st.expander("Cuestionario de Sueño"):
                col1, col2 = st.columns(2)
                with col1:
                    dormir = st.time_input("Hora de acostarse:", value=time(22, 0))
                with col2:
                    despertar = st.time_input("Hora de despertarse:", value=time(7, 0))
                
                tiempo_dormir = st.selectbox("Tiempo en quedarse dormido:", 
                                           ["Menos de 15 minutos (0 puntos)",
                                            "Entre 16 y 30 minutos (1 punto)",
                                            "Entre 31 y 60 minutos (2 puntos)",
                                            "Más de 60 minutos (3 puntos)"])
                
                horas_sueño = st.selectbox("Horas de sueño reales:", 
                                         ["Más de 7 horas (0 puntos)",
                                          "Entre 6 y 7 horas (1 punto)",
                                          "Entre 5 y 6 horas (2 puntos)",
                                          "Menos de 5 horas (3 puntos)"])
                
                # Componente 5: Perturbaciones del Sueño
                st.subheader("Problemas durante el sueño (último mes)")
                problemas = [
                    "Despertar durante la noche",
                    "Ir al baño",
                    "Dificultad para respirar",
                    "Toser o roncar",
                    "Sentir frío",
                    "Sentir calor",
                    "Malos sueños",
                    "Dolor físico",
                    "Otros problemas"
                ]
                punt_problemas = []
                for problema in problemas:
                    punt = st.selectbox(f"{problema}:", 
                                      ["Ninguna vez (0)", 
                                       "Menos de 1 vez/sem (1)", 
                                       "1-2 veces/sem (2)", 
                                       "3+ veces/sem (3)"])
                    punt_problemas.append(int(punt.split("(")[1][0]))
                
                calidad_sueño = st.selectbox("Calidad general del sueño:", 
                                           ["Muy buena (0 puntos)",
                                            "Buena (1 punto)",
                                            "Regular (2 puntos)",
                                            "Mala (3 puntos)"])
            
            # Sección 5: PSS-10 (Estrés)
            st.header("5. Nivel de Estrés (PSS-10)")
            with st.expander("Escala de Estrés Percibido"):
                preguntas_estres = [
                    "¿Con qué frecuencia ha sentido que no podía controlar lo importante?",
                    "¿Ha sentido que no manejaba sus responsabilidades?",
                    "¿Se ha sentido nervioso o estresado?",
                    "¿Ha confiado en su capacidad para resolver problemas?",
                    "¿Ha sentido que las cosas iban bien?",
                    "¿No pudo cumplir con todas sus obligaciones?",
                    "¿Pudo controlar las irritaciones?",
                    "¿Sintió que controlaba la situación?",
                    "¿Se enojó por cosas fuera de su control?",
                    "¿Sintió que los problemas se acumulaban?"
                ]
                
                opciones_estres = ["Nunca", "Casi nunca", "Algunas veces", "A menudo", "Muy a menudo"]
                puntuaciones_estres = []
                
                for i, pregunta in enumerate(preguntas_estres):
                    respuesta = st.selectbox(f"{i+1}. {pregunta}", opciones_estres)
                    puntuacion = opciones_estres.index(respuesta)
                    
                    # Invertir puntuación para preguntas 4,5,7,8
                    if i in [3,4,6,7]:
                        puntuacion = 4 - puntuacion
                    puntuaciones_estres.append(puntuacion)
            
            # Botón de envío
            submitted = st.form_submit_button("Generar Perfil Completo")
            
            if submitted:
                # Cálculos FFMI
                mlg = peso * (1 - (grasa/100))
                ffmi = mlg / ((altura/100) ** 2)
                
                # Nivel de Entrenamiento
                if genero == "Hombre":
                    if ffmi <= 18: nivel = "Principiante"
                    elif 18.1 <= ffmi <= 20: nivel = "Intermedio"
                    elif 20.1 <= ffmi <= 22: nivel = "Avanzado"
                    elif 22.1 <= ffmi <= 25: nivel = "Élite"
                    else: nivel = "Nivel Físico-Culturismo"
                else:
                    if ffmi <= 16: nivel = "Principiante"
                    elif 16.1 <= ffmi <= 18: nivel = "Intermedio"
                    elif 18.1 <= ffmi <= 20: nivel = "Avanzado"
                    elif 20.1 <= ffmi <= 23: nivel = "Élite"
                    else: nivel = "Nivel Físico-Culturismo"
                
                # Cálculo PSQI
                puntos_sueño = sum([
                    int(tiempo_dormir.split("(")[1][0]),
                    int(horas_sueño.split("(")[1][0]),
                    sum(punt_problemas),
                    int(calidad_sueño.split("(")[1][0])
                ])
                
                # Cálculo PSS-10
                total_estres = sum(puntuaciones_estres)
                
                # Cálculo IPAQ
                met_vig = (vig_dias * ((vig_horas*60 + vig_minutos) * 8.0))
                met_mod = (mod_dias * ((mod_horas*60 + mod_minutos) * 4.0))
                met_cam = (cam_dias * ((cam_horas*60 + cam_minutos) * 3.3))
                met_total = met_vig + met_mod + met_cam
                
                # Resultados
                st.success("**Resultados Integrales**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("FFMI", f"{ffmi:.2f}")
                    st.metric("Nivel de Entrenamiento", nivel)
                    st.metric("Masa Libre Grasa", f"{mlg:.2f} kg")
                with col2:
                    st.metric("Calidad de Sueño", f"{puntos_sueño}/21", help="0-5: Buena, 6-10: Moderada, 11-21: Mala")
                    st.metric("Nivel de Estrés", f"{total_estres}/40", help="0-13: Bajo, 14-26: Moderado, 27-40: Alto")
                with col3:
                    st.metric("Actividad Física", f"{met_total:.0f} MET-min/sem", 
                            help="<600: Sedentario, 600-3000: Moderado, >3000: Activo")
                    st.metric("Tiempo Sentado", f"{(sent_horas*60 + sent_minutos)} min/día")
                
                # Recomendaciones
                with st.expander("🔍 Recomendaciones Personalizadas", expanded=True):
                    rec_ejercicio = "Entrenamiento de fuerza 4-5 días/semana" if met_total < 600 else "Mantener rutina actual"
                    rec_sueño = "Higiene del sueño prioritaria" if puntos_sueño > 10 else "Mantener hábitos actuales"
                    rec_estres = "Técnicas de relajación diarias" if total_estres > 26 else "Gestión preventiva del estrés"
                    
                    st.write(f"""
                    ### Plan de Acción:
                    - **Ejercicio:** {rec_ejercicio}
                    - **Sueño:** {rec_sueño}
                    - **Estrés:** {rec_estres}
                    - **Nutrición:** {"Déficit calórico" if grasa > 20 else "Mantenimiento"}
                    """)
                    
                    if nivel in ["Avanzado", "Élite"]:
                        st.write("### Categorías Competitivas Disponibles:")
                        st.write("- Classic Physique\n- Men’s Physique\n- Bodybuilding" if genero == "Hombre" else "- Wellness\n- Bikini\n- Bodybuilding")

    elif submenu == "Nutrición":
        st.title("Nutrición")
        # [...] (Sección Nutrición sin cambios)

elif menu == "Contacto":
    st.title("Contacto")
    # [...] (Sección Contacto sin cambios)
