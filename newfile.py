import streamlit as st
import base64
import os

# Configuración de la página
st.set_page_config(
    page_title="MUPAI - Entrenamiento Digital",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- CSS Personalizado (Mejorado) ----
def local_css(file_name):
    try:
        if os.path.exists(file_name):
            with open(file_name) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        else:
            # CSS básico por defecto si no existe el archivo
            st.markdown("""
            <style>
            .main {
                padding-top: 2rem;
            }
            .stButton > button {
                width: 100%;
                border-radius: 10px;
                border: none;
                background: linear-gradient(90deg, #4CAF50, #45a049);
                color: white;
                font-weight: bold;
            }
            .stSelectbox > div > div {
                border-radius: 10px;
            }
            .metric-container {
                background-color: #f0f2f6;
                padding: 1rem;
                border-radius: 10px;
                margin: 0.5rem 0;
            }
            </style>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.sidebar.info("Usando estilos por defecto")

local_css("styles.css")

# ---- Función para verificar si una imagen existe ----
def image_exists(image_path):
    return os.path.exists(image_path)

def safe_image(image_path, caption="", use_container_width=True, fallback_text="Imagen no disponible"):
    if image_exists(image_path):
        st.image(image_path, caption=caption, use_container_width=use_container_width)
    else:
        st.info(f"📷 {fallback_text}: {image_path}")

# ---- Funciones de cuestionarios (COMPLETAS Y CORREGIDAS) ----

# Calidad del Sueño (PSQI) - YA CORREGIDA ANTERIORMENTE
def cuestionario_calidad_sueno():
    with st.container():
        st.title("🌙 Evaluación de la Calidad del Sueño")
        st.subheader("Índice de Pittsburgh - PSQI")
        st.write("Responde las siguientes preguntas sobre tus hábitos de sueño durante el último mes:")
        
        with st.expander("📅 Horarios de sueño", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                hora_acostarse = st.text_input("1. ¿A qué hora te acuestas normalmente?", key="hora_acostarse")
            with col2:
                hora_levantarse = st.text_input("3. ¿A qué hora te levantas normalmente?", key="hora_levantarse")
            
            col3, col4 = st.columns(2)
            with col3:
                tiempo_dormirse = st.slider("2. ¿Cuánto tiempo tardas normalmente en dormirte (minutos)?", 0, 120, 15, key="tiempo_dormirse")
            with col4:
                horas_dormidas = st.slider("4. ¿Cuántas horas calculas que duermes habitualmente por noche?", 0, 12, 7, key="horas_dormidas")

        with st.expander("⚠️ Problemas para dormir", expanded=True):
            st.write("5. Durante el último mes, ¿con qué frecuencia has experimentado los siguientes problemas?")
            problemas_dormir = {
                "No poder conciliar el sueño en 30 minutos": st.radio(
                    "a. No poder conciliar el sueño en los primeros 30 minutos:",
                    ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                    horizontal=True,
                    key="problema_conciliar"
                ),
                "Despertarte durante la noche o muy temprano": st.radio(
                    "b. Despertarte durante la noche o muy temprano:",
                    ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                    horizontal=True,
                    key="problema_despertar"
                ),
                "Ir al baño durante la noche": st.radio(
                    "c. Tener que levantarte para ir al baño:",
                    ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                    horizontal=True,
                    key="problema_baño"
                ),
                "No poder respirar bien": st.radio(
                    "d. No poder respirar bien mientras duermes:",
                    ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                    horizontal=True,
                    key="problema_respirar"
                ),
                "Toser o roncar fuerte": st.radio(
                    "e. Toser o roncar fuerte mientras duermes:",
                    ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                    horizontal=True,
                    key="problema_roncar"
                ),
                "Sentir frío": st.radio(
                    "f. Sentir frío mientras duermes:",
                    ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                    horizontal=True,
                    key="problema_frio"
                ),
                "Sentir calor": st.radio(
                    "g. Sentir calor mientras duermes:",
                    ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                    horizontal=True,
                    key="problema_calor"
                ),
                "Tener pesadillas": st.radio(
                    "h. Tener pesadillas:",
                    ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                    horizontal=True,
                    key="problema_pesadillas"
                ),
                "Sentir dolor": st.radio(
                    "i. Sentir dolor que dificulte tu sueño:",
                    ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                    horizontal=True,
                    key="problema_dolor"
                )
            }

        with st.expander("💊 Uso de medicación"):
            uso_medicacion = st.radio(
                "6. ¿Cuántas veces tomaste medicamentos para dormir durante el último mes?",
                ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                horizontal=True,
                key="uso_medicacion"
            )

        with st.expander("😴 Disfunción diurna"):
            st.write("7. Durante el último mes, ¿con qué frecuencia tuviste los siguientes problemas?")
            disfuncion_diurna_1 = st.radio(
                "a. Problemas para mantenerte despierto(a) mientras realizabas actividades sociales o tareas:",
                ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                horizontal=True,
                key="disfuncion_1"
            )
            disfuncion_diurna_2 = st.radio(
                "b. Dificultad para mantener el entusiasmo para hacer cosas:",
                ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                horizontal=True,
                key="disfuncion_2"
            )

        with st.expander("⭐ Calidad subjetiva"):
            calidad_sueno = st.radio(
                "8. ¿Cómo calificarías la calidad de tu sueño durante el último mes?",
                ["Muy buena", "Bastante buena", "Bastante mala", "Muy mala"],
                horizontal=True,
                key="calidad_sueno"
            )

        if st.button("📊 Calcular Puntuación PSQI", use_container_width=True, type="primary", key="calc_psqi"):
            try:
                puntuacion = {"Ninguna vez": 0, "Menos de una vez a la semana": 1, "Una o dos veces a la semana": 2, "Tres o más veces a la semana": 3}
                calidad_puntuacion = {"Muy buena": 0, "Bastante buena": 1, "Bastante mala": 2, "Muy mala": 3}

                componente_1 = calidad_puntuacion[calidad_sueno]
                componente_2 = 1 if tiempo_dormirse > 30 else 0
                componente_3 = 0 if horas_dormidas >= 7 else (1 if horas_dormidas >= 6 else 2)
                componente_4 = sum(puntuacion[v] for v in problemas_dormir.values())
                componente_5 = puntuacion[uso_medicacion]
                componente_6 = puntuacion[disfuncion_diurna_1] + puntuacion[disfuncion_diurna_2]

                total_puntuacion = componente_1 + componente_2 + componente_3 + componente_4 + componente_5 + componente_6

                st.divider()
                st.subheader("Resultados de la Evaluación")
                st.metric(label="Puntuación Total PSQI", value=total_puntuacion)
                
                if total_puntuacion <= 5:
                    st.success("✅ Buena calidad de sueño")
                    st.progress(0.2)
                    st.write("Tu calidad de sueño es buena. Continúa con tus hábitos saludables.")
                elif 6 <= total_puntuacion <= 10:
                    st.warning("⚠️ Calidad de sueño moderada")
                    st.progress(0.5)
                    st.write("Tu sueño podría mejorar. Considera establecer rutinas más consistentes y crear un ambiente propicio para dormir.")
                else:
                    st.error("❌ Mala calidad de sueño")
                    st.progress(0.8)
                    st.write("Tu calidad de sueño necesita atención. Te recomendamos consultar con un especialista y revisar tus hábitos de sueño.")
            except Exception as e:
                st.error(f"Error al calcular la puntuación: {e}")

# Nivel de Actividad Física (IPAQ) - CORREGIDA
def cuestionario_ipaq():
    with st.container():
        st.title("🏃 Cuestionario de Actividad Física - IPAQ")
        st.write("Responde las siguientes preguntas sobre tu actividad física durante los últimos 7 días.")

        # Actividades físicas vigorosas
        with st.expander("💪 Actividades Físicas Vigorosas", expanded=True):
            dias_vigorosa = st.number_input(
                "1. Durante los últimos 7 días, ¿en cuántos días realizaste actividades físicas vigorosas como levantar objetos pesados, cavar, aeróbicos o andar en bicicleta rápido? (Días por semana)", 
                min_value=0, max_value=7, step=1, key="dias_vigorosa"
            )
            if dias_vigorosa > 0:
                col1, col2 = st.columns(2)
                with col1:
                    tiempo_vigorosa_horas = st.number_input(
                        "2. ¿Cuántas horas por día dedicaste generalmente a esas actividades vigorosas?", 
                        min_value=0, step=1, key="horas_vigorosa"
                    )
                with col2:
                    tiempo_vigorosa_minutos = st.number_input(
                        "¿Y cuántos minutos por día (además de las horas)?", 
                        min_value=0, max_value=59, step=1, key="minutos_vigorosa"
                    )
            else:
                tiempo_vigorosa_horas = 0
                tiempo_vigorosa_minutos = 0

        # Actividades físicas moderadas
        with st.expander("🚴 Actividades Físicas Moderadas", expanded=True):
            dias_moderada = st.number_input(
                "3. Durante los últimos 7 días, ¿en cuántos días realizaste actividades físicas moderadas como llevar cargas ligeras o andar en bicicleta a un ritmo normal? (Días por semana)", 
                min_value=0, max_value=7, step=1, key="dias_moderada"
            )
            if dias_moderada > 0:
                col1, col2 = st.columns(2)
                with col1:
                    tiempo_moderada_horas = st.number_input(
                        "4. ¿Cuántas horas por día dedicaste generalmente a esas actividades moderadas?", 
                        min_value=0, step=1, key="horas_moderada"
                    )
                with col2:
                    tiempo_moderada_minutos = st.number_input(
                        "¿Y cuántos minutos por día (además de las horas)?", 
                        min_value=0, max_value=59, step=1, key="minutos_moderada"
                    )
            else:
                tiempo_moderada_horas = 0
                tiempo_moderada_minutos = 0

        # Caminata
        with st.expander("🚶 Tiempo Dedicado a Caminar", expanded=True):
            dias_caminata = st.number_input(
                "5. Durante los últimos 7 días, ¿en cuántos días caminaste al menos 10 minutos seguidos? (Días por semana)", 
                min_value=0, max_value=7, step=1, key="dias_caminata"
            )
            if dias_caminata > 0:
                col1, col2 = st.columns(2)
                with col1:
                    tiempo_caminata_horas = st.number_input(
                        "6. ¿Cuántas horas por día dedicaste generalmente a caminar?", 
                        min_value=0, step=1, key="horas_caminata"
                    )
                with col2:
                    tiempo_caminata_minutos = st.number_input(
                        "¿Y cuántos minutos por día (además de las horas)?", 
                        min_value=0, max_value=59, step=1, key="minutos_caminata"
                    )
            else:
                tiempo_caminata_horas = 0
                tiempo_caminata_minutos = 0

        # Tiempo sedentario
        with st.expander("🪑 Tiempo de Sedentarismo"):
            col1, col2 = st.columns(2)
            with col1:
                tiempo_sedentario_horas = st.number_input(
                    "7. Durante los últimos 7 días, ¿cuántas horas por día dedicaste a estar sentado? (Promedio diario)", 
                    min_value=0, step=1, key="horas_sedentario"
                )
            with col2:
                tiempo_sedentario_minutos = st.number_input(
                    "¿Y cuántos minutos por día (además de las horas)?", 
                    min_value=0, max_value=59, step=1, key="minutos_sedentario"
                )

        # Calcular el scoring
        if st.button("📊 Calcular Puntuación IPAQ", key="calcular_puntuacion_ipaq", use_container_width=True, type="primary"):
            try:
                # Conversión de tiempo en minutos
                minutos_vigorosa = dias_vigorosa * ((tiempo_vigorosa_horas * 60) + tiempo_vigorosa_minutos)
                minutos_moderada = dias_moderada * ((tiempo_moderada_horas * 60) + tiempo_moderada_minutos)
                minutos_caminata = dias_caminata * ((tiempo_caminata_horas * 60) + tiempo_caminata_minutos)

                # Cálculo de METs
                met_vigorosa = minutos_vigorosa * 8.0  # METs para actividad vigorosa
                met_moderada = minutos_moderada * 4.0  # METs para actividad moderada
                met_caminata = minutos_caminata * 3.3  # METs para caminata

                # Total de METs
                total_met = met_vigorosa + met_moderada + met_caminata

                # Mostrar resultados
                st.divider()
                st.subheader("Resultados de la Evaluación")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="MET-minutos/semana", value=f"{total_met:.2f}")
                with col2:
                    st.metric(label="Tiempo sedentario diario", value=f"{tiempo_sedentario_horas}h {tiempo_sedentario_minutos}min")

                # Clasificación de actividad
                st.subheader("Nivel de Actividad Física")
                if total_met >= 3000:
                    st.success("🏆 Alta. ¡Excelente trabajo en mantenerte activo!")
                    st.progress(0.9)
                elif 600 <= total_met < 3000:
                    st.info("📈 Moderada. Podrías incluir más actividad física para mejorar.")
                    st.progress(0.6)
                else:
                    st.warning("📉 Baja. Considera realizar más actividades físicas para mejorar tu salud.")
                    st.progress(0.3)
                    
                # Recomendaciones adicionales
                st.subheader("Recomendaciones")
                if total_met < 600:
                    st.write("💡 **Sugerencias:**")
                    st.write("- Comienza con caminatas de 10-15 minutos diarios")
                    st.write("- Usa las escaleras en lugar del ascensor")
                    st.write("- Realiza pausas activas cada hora si trabajas sentado")
                elif 600 <= total_met < 3000:
                    st.write("💡 **Sugerencias para mejorar:**")
                    st.write("- Aumenta la intensidad de tus ejercicios gradualmente")
                    st.write("- Añade 1-2 días más de actividad vigorosa")
                    st.write("- Combina ejercicios de fuerza con cardio")
                else:
                    st.write("💡 **Mantén tu excelente nivel:**")
                    st.write("- Continúa con tu rutina actual")
                    st.write("- Varía los tipos de ejercicio para evitar el aburrimiento")
                    st.write("- Considera incluir ejercicios de flexibilidad")
                    
            except Exception as e:
                st.error(f"Error al calcular la puntuación: {e}")

# Hábitos Alimenticios - CORREGIDA
def cuestionario_habitos_alimenticios():
    with st.container():
        st.title("🍎 Evaluación de Hábitos Alimenticios")
        st.write("Responde las siguientes preguntas para evaluar tus hábitos alimenticios y recibir recomendaciones personalizadas.")

        # Sección 1: Consumo de Alimentos Frescos
        with st.expander("🥦 Consumo de Alimentos Frescos", expanded=True):
            agua = st.radio("1. ¿Bebes al menos 1.5 litros de agua natural diariamente?", 
                          ["Nunca", "Algunas veces", "Casi siempre", "Siempre"], 
                          horizontal=True, key="agua")
            verduras = st.radio("2. ¿Consumes al menos 200 g de verduras frescas diariamente?", 
                               ["Nunca", "Algunas veces", "Casi siempre", "Siempre"], 
                               horizontal=True, key="verduras")
            frutas = st.radio("3. ¿Consumes al menos 200 g de frutas diariamente?", 
                            ["Nunca", "Algunas veces", "Casi siempre", "Siempre"], 
                            horizontal=True, key="frutas")
            leguminosas = st.radio("4. ¿Consumes al menos 300 g de leguminosas semanalmente?", 
                                 ["Nunca", "Algunas veces", "Casi siempre", "Siempre"], 
                                 horizontal=True, key="leguminosas")
            frutos_secos = st.radio("5. ¿Consumes al menos 30 g de frutos secos o medio aguacate diariamente?", 
                                  ["Nunca", "Algunas veces", "Casi siempre", "Siempre"], 
                                  horizontal=True, key="frutos_secos")

        # Sección 2: Carnes Frescas y Procesadas
        with st.expander("🍗 Carnes Frescas y Procesadas"):
            carne_fresca = st.radio(
                "6. ¿Qué tipo de carne fresca consumes con mayor frecuencia durante la semana?",
                ["Pescado fresco", "Pollo fresco", "Carne roja fresca", "No consumo carne fresca"],
                horizontal=True, key="carne_fresca"
            )
            carnes_procesadas = st.radio(
                "7. ¿Con qué frecuencia consumes carnes procesadas (embutidos, curadas, enlatadas o fritas)?",
                ["Nunca", "Algunas veces", "Casi siempre", "Siempre"],
                horizontal=True, key="carnes_procesadas"
            )

        # Sección 3: Hábitos Alimenticios Generales
        with st.expander("🍽️ Hábitos Alimenticios Generales", expanded=True):
            alimentos_fuera = st.radio("8. ¿Consumes alimentos no preparados en casa tres o más veces por semana?", 
                                     ["Nunca", "Algunas veces", "Casi siempre", "Siempre"], 
                                     horizontal=True, key="alimentos_fuera")
            bebidas_azucaradas = st.radio("9. ¿Cuántas veces consumes bebidas azucaradas semanalmente?", 
                                        ["Nunca", "1–3 veces", "4–6 veces", "Diario"], 
                                        horizontal=True, key="bebidas_azucaradas")
            postres_dulces = st.radio("10. ¿Consumes postres o dulces dos o más veces por semana?", 
                                    ["Nunca", "Algunas veces", "Casi siempre", "Siempre"], 
                                    horizontal=True, key="postres_dulces")
            alimentos_procesados = st.radio("11. ¿Consumes alimentos procesados dos o más veces por semana?", 
                                          ["Nunca", "Algunas veces", "Casi siempre", "Siempre"], 
                                          horizontal=True, key="alimentos_procesados")
            cereales = st.radio(
                "12. ¿Qué tipo de cereales consumes con mayor frecuencia?",
                ["Granos integrales", "Granos mínimamente procesados", "Granos procesados o ultraprocesados"],
                horizontal=True, key="cereales"
            )

        # Sección 4: Consumo de Alcohol
        with st.expander("🍷 Consumo de Alcohol"):
            alcohol = st.radio(
                "13. Si eres hombre, ¿consumes más de 2 bebidas alcohólicas al día? Si eres mujer, ¿más de 1 bebida al día?",
                ["Nunca", "Algunas veces", "Casi siempre", "Siempre"],
                horizontal=True, key="alcohol"
            )

        # Botón para calcular la puntuación
        if st.button("📊 Calcular Puntuación Alimentaria", use_container_width=True, type="primary", key="calc_alimentacion"):
            try:
                puntuaciones = {"Nunca": 1, "Algunas veces": 2, "Casi siempre": 3, "Siempre": 4, "Diario": 4, "4–6 veces": 3, "1–3 veces": 2}
                carne_fresca_valores = {"Pescado fresco": 4, "Pollo fresco": 3, "Carne roja fresca": 2, "No consumo carne fresca": 0}
                carnes_procesadas_valores = {"Nunca": 0, "Algunas veces": -1, "Casi siempre": -2, "Siempre": -3}
                cereales_valores = {"Granos integrales": 4, "Granos mínimamente procesados": 3, "Granos procesados o ultraprocesados": -2}

                puntuacion_total = (
                    puntuaciones[agua] +
                    puntuaciones[verduras] +
                    puntuaciones[frutas] +
                    puntuaciones[leguminosas] +
                    puntuaciones[frutos_secos] +
                    carne_fresca_valores[carne_fresca] +
                    carnes_procesadas_valores[carnes_procesadas] +
                    puntuaciones[alimentos_fuera] +
                    puntuaciones[bebidas_azucaradas] +
                    puntuaciones[postres_dulces] +
                    puntuaciones[alimentos_procesados] +
                    cereales_valores[cereales] +
                    puntuaciones[alcohol]
                )

                st.divider()
                st.subheader("Resultados de la Evaluación")
                st.metric(label="Puntuación Total", value=puntuacion_total)

                # Feedback en función del puntaje
                if puntuacion_total >= 30:
                    st.success("✅ Tus hábitos alimenticios son excelentes.")
                    st.progress(0.9)
                    st.write("¡Felicidades! Tus elecciones alimenticias son excelentes. Sigue así para mantener una salud óptima.")
                elif 15 <= puntuacion_total < 30:
                    st.warning("⚠️ Tus hábitos alimenticios son moderadamente saludables.")
                    st.progress(0.6)
                    st.write("Tienes hábitos buenos, pero hay áreas donde puedes mejorar. Considera reducir el consumo de alimentos procesados y aumentar tu ingesta de alimentos frescos.")
                else:
                    st.error("❌ Tus hábitos alimenticios necesitan mejoras significativas.")
                    st.progress(0.3)
                    st.write("Es importante trabajar en tus hábitos alimenticios. Intenta incorporar más alimentos frescos y reducir el consumo de alimentos ultraprocesados. Podría ser útil consultar con un nutricionista.")

                # Recomendaciones específicas
                st.subheader("Recomendaciones Personalizadas")
                
                recomendaciones = []
                if puntuaciones[agua] < 3:
                    recomendaciones.append("💧 Aumenta tu consumo de agua. Lleva una botella contigo y establece recordatorios.")
                if puntuaciones[verduras] < 3:
                    recomendaciones.append("🥬 Incluye más verduras en tus comidas. Prueba ensaladas coloridas o verduras al vapor.")
                if puntuaciones[frutas] < 3:
                    recomendaciones.append("🍎 Consume más frutas frescas como snacks o en tus desayunos.")
                if carnes_procesadas_valores[carnes_procesadas] < -1:
                    recomendaciones.append("🚫 Reduce el consumo de carnes procesadas. Opta por carnes frescas y proteínas vegetales.")
                if cereales_valores[cereales] < 3:
                    recomendaciones.append("🌾 Elige granos integrales en lugar de productos refinados.")
                
                if recomendaciones:
                    for rec in recomendaciones:
                        st.write(f"- {rec}")
                else:
                    st.write("🎉 ¡Continúa con tus excelentes hábitos alimenticios!")
                    
            except Exception as e:
                st.error(f"Error al calcular la puntuación: {e}")

# ---- Barra lateral mejorada ----
with st.sidebar:
    # Mostrar logo si existe
    safe_image("LOGO.png", fallback_text="Logo MUPAI")
    st.divider()
    
    menu = st.selectbox(
        "Menú Principal",
        ["🏠 Inicio", "👤 Sobre Mí", "💼 Servicios", "📞 Contacto", "📊 Evaluación del Estilo de Vida"],
        index=0,
        key="menu_principal"
    )
    
    st.divider()
    st.caption("MUPAI - Entrenamiento Digital Basado en Ciencia")
    st.caption("© 2024 Todos los derechos reservados")

# ---- Contenido principal ----
if menu == "🏠 Inicio":
    # Mostrar el logo
    safe_image("LOGO.png", fallback_text="Logo MUPAI")

    # Título principal
    st.title("Bienvenido a MUPAI")
    st.markdown("---")

    # Misión
    st.header("🎯 Misión")
    st.write(
        """
        Hacer accesible el entrenamiento basado en ciencia, proporcionando planes completamente personalizados 
        a través de herramientas digitales respaldadas por inteligencia artificial, datos precisos y metodologías 
        validadas científicamente.
        """
    )

    # Visión
    st.header("🔮 Visión")
    st.write(
        """
        Convertirnos en uno de los máximos referentes a nivel global en entrenamiento digital personalizado, 
        aprovechando las nuevas tecnologías para hacer más accesible el fitness basado en ciencia para todas 
        las personas, sin importar su ubicación o nivel de experiencia.
        """
    )

    # Política
    st.header("📋 Política")
    st.write(
        """
        En **MUPAI**, nuestra política está fundamentada en el compromiso con la excelencia, la ética y el 
        servicio centrado en el usuario. Actuamos con responsabilidad y transparencia para ofrecer soluciones 
        de entrenamiento que transformen positivamente la vida de nuestros usuarios.
        """
    )

    # Política del Servicio
    st.header("🤝 Política del Servicio")
    st.write(
        """
        En **MUPAI**, guiamos nuestras acciones por los siguientes principios:
        
        - **Personalización Científica**: Diseñamos entrenamientos digitales que combinan personalización, datos confiables y ciencia del ejercicio.
        - **Tecnología Accesible**: Aprovechamos la tecnología para ofrecer un servicio accesible y adaptable a las necesidades de cada usuario.
        - **Privacidad y Seguridad**: Respetamos y protegemos la privacidad de los datos personales, garantizando su uso responsable.
        - **Innovación Continua**: Innovamos de forma continua para mejorar la experiencia y los resultados de nuestros usuarios.
        - **Valores Fundamentales**: Promovemos valores como el esfuerzo, la constancia y el respeto en cada interacción, fomentando un ambiente de crecimiento y bienestar.
        """
    )

elif menu == "👤 Sobre Mí":
    # Sección "Sobre Mí"
    st.title("👤 Sobre Mí")
    st.markdown("---")
    
    # Información profesional
    st.subheader("Erick Francisco De Luna Hernández")
    st.write("""
    Soy un profesional apasionado por el fitness y las ciencias del ejercicio, con una sólida formación académica 
    y amplia experiencia en el diseño de metodologías de entrenamiento personalizadas y basadas en evidencia científica.

    **Formación Académica:**
    - 🎓 **Maestría en Fuerza y Acondicionamiento** - Football Science Institute
    - 🎓 **Licenciatura en Ciencias del Ejercicio** - Universidad Autónoma de Nuevo León (UANL)
    - 📜 **Certificaciones especializadas** en metodologías avanzadas de entrenamiento

    **Reconocimientos:**
    - 🏆 **Premio al Mérito Académico de la UANL**
    - 🥇 **Primer Lugar de Generación** en la Facultad de Organización Deportiva
    - 🎖️ **Beca de excelencia académica** por desempeño sobresaliente

    **Filosofía Profesional:**
    
    Con una combinación de preparación académica rigurosa, experiencia práctica y un enfoque basado en la evidencia, 
    me dedico a diseñar soluciones que transformen el rendimiento físico y promuevan un estilo de vida saludable 
    y sostenible para cada individuo.
    """)

    # Collage de imágenes con manejo de errores
    st.subheader("📸 Galería Profesional")
    col1, col2, col3 = st.columns(3)

    with col1:
        safe_image("FB_IMG_1734820693317.jpg", "Entrenamiento funcional")
        safe_image("FB_IMG_1734820729323.jpg", "Sesión de coaching")

    with col2:
        safe_image("FB_IMG_1734820709707.jpg", "Evaluación biomecánica")
        safe_image("FB_IMG_1734820808186.jpg", "Conferencia científica")

    with col3:
        safe_image("FB_IMG_1734820712642.jpg", "Análisis de rendimiento")

elif menu == "💼 Servicios":
    # Sección "Servicios"
    st.title("💼 Servicios Profesionales")
    st.markdown("---")
    
    st.write("**MUPAI** ofrece una amplia gama de servicios personalizados basados en ciencia del ejercicio:")
    
    # Servicios en tarjetas
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏋️ Entrenamiento Personalizado")
        st.write("- Planes de entrenamiento individualizados")
        st.write("- Periodización científica")
        st.write("- Seguimiento de progreso")
        
        st.subheader("🧠 Consultoría en Rendimiento")
        st.write("- Análisis biomecánico")
        st.write("- Optimización del rendimiento deportivo")
        st.write("- Prevención de lesiones")
    
    with col2:
        st.subheader("💪 Programas de Mejora Física")
        st.write("- Desarrollo de fuerza y resistencia")
        st.write("- Composición corporal")
        st.write("- Rehabilitación funcional")
        
        st.subheader("🥗 Asesoría Nutricional")
        st.write("- Nutrición deportiva especializada")
        st.write("- Planes alimentarios personalizados")
        st.write("- Suplementación basada en evidencia")

elif menu == "📞 Contacto":
    # Sección "Contacto"
    st.title("📞 Información de Contacto")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📧 Contacto Directo")
        st.write("**Correo Electrónico:** contacto@mupai.com")
        st.write("**Teléfono:** +52 866 258 05 94")
        st.write("**Ubicación:** Monterrey, Nuevo León, México")
        
    with col2:
        st.subheader("🕒 Horarios de Atención")
        st.write("**Lunes a Viernes:** 8:00 AM - 6:00 PM")
        st.write("**Sábados:** 9:00 AM - 2:00 PM")
        st.write("**Domingos:** Citas especiales")
    
    st.markdown("---")
    st.info("💡 **Tip:** Para una consulta más eficiente, por favor completa primero nuestras evaluaciones del estilo de vida.")

elif menu == "📊 Evaluación del Estilo de Vida":
    # Submenú para Evaluación del Estilo de Vida
    with st.sidebar:
        st.subheader("🔍 Áreas de Evaluación")
        submenu = st.radio(
            "Selecciona una evaluación:",
            [
                "😰 Estrés Percibido", 
                "🌙 Calidad del Sueño", 
                "🏃 Nivel de Actividad Física", 
                "🍎 Hábitos Alimenticios", 
                "🧬 Potencial Genético Muscular"
            ],
            key="submenu_evaluacion"
        )
    
    if submenu == "😰 Estrés Percibido":
        st.title("😰 Evaluación del Estrés Percibido")
        st.write("Responde las siguientes preguntas según cómo te has sentido durante el último mes:")

        # Preguntas del cuestionario
        options = ["Nunca", "Casi nunca", "A veces", "Bastante seguido", "Muy seguido"]
        
        with st.expander("🧠 Cuestionario de Estrés Percibido (PSS-10)", expanded=True):
            q1 = st.radio("1. ¿Con qué frecuencia te has sentido molesto/a por algo que ocurrió inesperadamente?", 
                         options, horizontal=True, key="stress_q1")
            q2 = st.radio("2. ¿Con qué frecuencia has sentido que no puedes controlar las cosas importantes de tu vida?", 
                         options, horizontal=True, key="stress_q2")
            q3 = st.radio("3. ¿Con qué frecuencia has sentido nerviosismo o estrés?", 
                         options, horizontal=True, key="stress_q3")
            q4 = st.radio("4. ¿Con qué frecuencia has sentido confianza en tu capacidad para manejar tus problemas personales?", 
                         options, horizontal=True, key="stress_q4")
            q5 = st.radio("5. ¿Con qué frecuencia has sentido que las cosas estaban saliendo bien para ti?", 
                         options, horizontal=True, key="stress_q5")
            q6 = st.radio("6. ¿Con qué frecuencia has sentido que no podías lidiar con todas las cosas que tenías que hacer?", 
                         options, horizontal=True, key="stress_q6")
            q7 = st.radio("7. ¿Con qué frecuencia has sentido que podías controlar las irritaciones en tu vida?", 
                         options, horizontal=True, key="stress_q7")
            q8 = st.radio("8. ¿Con qué frecuencia has sentido que tenías el control sobre las cosas?", 
                         options, horizontal=True, key="stress_q8")
            q9 = st.radio("9. ¿Con qué frecuencia te has sentido enojado/a por cosas fuera de tu control?", 
                         options, horizontal=True, key="stress_q9")
            q10 = st.radio("10. ¿Con qué frecuencia has sentido que las dificultades se acumulaban tanto que no podías superarlas?", 
                          options, horizontal=True, key="stress_q10")

        # Botón para calcular el puntaje
        if st.button("📊 Calcular Puntuación de Estrés", use_container_width=True, type="primary", key="calc_stress"):
            try:
                scores = {"Nunca": 0, "Casi nunca": 1, "A veces": 2, "Bastante seguido": 3, "Muy seguido": 4}

                total_score = (
                    scores[q1] + scores[q2] + scores[q3] +
                    (4 - scores[q4]) +  # Pregunta inversa
                    (4 - scores[q5]) +  # Pregunta inversa
                    scores[q6] +
                    (4 - scores[q7]) +  # Pregunta inversa
                    (4 - scores[q8]) +  # Pregunta inversa
                    scores[q9] + scores[q10]
                )

                st.divider()
                st.subheader("Resultados de la Evaluación")
                st.metric(label="Puntuación de Estrés Percibido", value=f"{total_score}/40")
                
                if total_score <= 13:
                    st.success("✅ Estrés bajo. ¡Excelente trabajo en mantener el equilibrio!")
                    st.progress(0.2)
                    st.write("Tienes un buen manejo del estrés. Continúa con tus estrategias actuales de afrontamiento.")
                elif 14 <= total_score <= 26:
                    st.warning("⚠️ Estrés moderado. Podrías beneficiarte de técnicas de manejo del estrés.")
                    st.progress(0.5)
                    st.write("Considera incorporar técnicas de relajación, ejercicio regular y mejor organización del tiempo.")
                else:
                    st.error("❌ Estrés alto. Considera buscar apoyo profesional.")
                    st.progress(0.8)
                    st.write("Es recomendable buscar apoyo profesional y implementar estrategias de manejo del estrés de inmediato.")
                    
                # Recomendaciones específicas
                st.subheader("💡 Recomendaciones")
                if total_score <= 13:
                    st.write("- Mantén tus rutinas saludables actuales")
                    st.write("- Practica técnicas de mindfulness preventivas")
                elif 14 <= total_score <= 26:
                    st.write("- Implementa técnicas de respiración profunda")
                    st.write("- Establece límites claros en el trabajo")
                    st.write("- Dedica tiempo a actividades placenteras")
                else:
                    st.write("- Busca ayuda profesional (psicólogo o psiquiatra)")
                    st.write("- Considera técnicas de relajación progresiva")
                    st.write("- Evalúa cambios en tu estilo de vida")
                    
            except Exception as e:
                st.error(f"Error al calcular la puntuación: {e}")
   
    elif submenu == "🌙 Calidad del Sueño":
        cuestionario_calidad_sueno()
   
    elif submenu == "🏃 Nivel de Actividad Física":
        cuestionario_ipaq()

    elif submenu == "🍎 Hábitos Alimenticios":
        cuestionario_habitos_alimenticios()

    elif submenu == "🧬 Potencial Genético Muscular":
        st.title("🧬 Evaluación de Potencial Genético Muscular")
        st.info("📋 Esta evaluación está en desarrollo.")
        st.write("""
        Próximamente podrás evaluar tu potencial genético para el desarrollo muscular mediante:
        
        - 🧪 Análisis de polimorfismos genéticos
        - 💪 Evaluación de fibras musculares
        - 📊 Predicción de respuesta al entrenamiento
        - 🎯 Recomendaciones personalizadas de entrenamiento
        """)
        safe_image("dna.jpg", caption="Próximamente: Análisis de potencial genético", fallback_text="Imagen de ADN no disponible")
        
        st.markdown("---")
        st.write("**Mientras tanto, puedes completar las otras evaluaciones disponibles para obtener un perfil completo de tu estilo de vida.**")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666666;'>
        <p>© 2024 MUPAI - Entrenamiento Digital Basado en Ciencia</p>
        <p>Desarrollado con ❤️ por Erick Francisco De Luna Hernández</p>
    </div>
    """, 
    unsafe_allow_html=True
                )
