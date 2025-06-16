import streamlit as st
import base64

# Configuración de la página
st.set_page_config(
    page_title="MUPAI - Entrenamiento Digital",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- CSS Personalizado ----
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        st.sidebar.warning("No se encontró el archivo CSS personalizado")

local_css("styles.css")

# ---- Funciones de cuestionarios (manteniendo tu contenido original) ----

# Calidad del Sueño (PSQI)
def cuestionario_calidad_sueno():
    with st.container():
        st.title("🌙 Evaluación de la Calidad del Sueño")
        st.subheader("Índice de Pittsburgh - PSQI")
        st.write("Responde las siguientes preguntas sobre tus hábitos de sueño durante el último mes:")
        
        with st.expander("📅 Horarios de sueño", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                hora_acostarse = st.text_input("1. ¿A qué hora te acuestas normalmente?")
            with col2:
                hora_levantarse = st.text_input("3. ¿A qué hora te levantas normalmente?")
            
            col3, col4 = st.columns(2)
            with col3:
                tiempo_dormirse = st.slider("2. ¿Cuánto tiempo tardas normalmente en dormirte (minutos)?", 0, 120, 15)
            with col4:
                horas_dormidas = st.slider("4. ¿Cuántas horas calculas que duermes habitualmente por noche?", 0, 12, 7)

        with st.expander("⚠️ Problemas para dormir", expanded=True):
            st.write("5. Durante el último mes, ¿con qué frecuencia has experimentado los siguientes problemas?")
            problemas_dormir = {
                "No poder conciliar el sueño en 30 minutos": st.radio(
                    "a. No poder conciliar el sueño en los primeros 30 minutos:",
                    ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                    horizontal=True
                ),
                "Despertarte durante la noche o muy temprano": st.radio(
                    "b. Despertarte durante la noche o muy temprano:",
                    ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                    horizontal=True
                ),
                "Ir al baño durante la noche": st.radio(
                    "c. Tener que levantarte para ir al baño:",
                    ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                    horizontal=True
                ),
                "No poder respirar bien": st.radio(
                    "d. No poder respirar bien mientras duermes:",
                    ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                    horizontal=True
                ),
                "Toser o roncar fuerte": st.radio(
                    "e. Toser o roncar fuerte mientras duermes:",
                    ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                    horizontal=True
                ),
                "Sentir frío": st.radio(
                    "f. Sentir frío mientras duermes:",
                    ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                    horizontal=True
                ),
                "Sentir calor": st.radio(
                    "g. Sentir calor mientras duermes:",
                    ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                    horizontal=True
                ),
                "Tener pesadillas": st.radio(
                    "h. Tener pesadillas:",
                    ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                    horizontal=True
                ),
                "Sentir dolor": st.radio(
                    "i. Sentir dolor que dificulte tu sueño:",
                    ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                    horizontal=True
                )
            }

        with st.expander("💊 Uso de medicación"):
            uso_medicacion = st.radio(
                "6. ¿Cuántas veces tomaste medicamentos para dormir durante el último mes?",
                ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                horizontal=True
            )

        with st.expander("😴 Disfunción diurna"):
            st.write("7. Durante el último mes, ¿con qué frecuencia tuviste los siguientes problemas?")
            disfuncion_diurna_1 = st.radio(
                "a. Problemas para mantenerte despierto(a) mientras realizabas actividades sociales o tareas:",
                ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                horizontal=True
            )
            disfuncion_diurna_2 = st.radio(
                "b. Dificultad para mantener el entusiasmo para hacer cosas:",
                ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"],
                horizontal=True
            )

        with st.expander("⭐ Calidad subjetiva"):
            calidad_sueno = st.radio(
                "8. ¿Cómo calificarías la calidad de tu sueño durante el último mes?",
                ["Muy buena", "Bastante buena", "Bastante mala", "Muy mala"],
                horizontal=True
            )

        if st.button("📊 Calcular Puntuación", use_container_width=True, type="primary"):
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

# Nivel de Actividad Física (IPAQ)
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
        if st.button("📊 Calcular Puntuación", key="calcular_puntuacion", use_container_width=True, type="primary"):
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
            st.metric(label="MET-minutos/semana", value=f"{total_met:.2f}")
            st.metric(label="Tiempo sedentario diario", value=f"{tiempo_sedentario_horas}h {tiempo_sedentario_minutos}min")

            # Clasificación de actividad
            st.subheader("Nivel de Actividad Física")
            if total_met >= 3000:
                st.success("Alta. ¡Excelente trabajo en mantenerte activo!")
                st.progress(0.9)
            elif 600 <= total_met < 3000:
                st.info("Moderada. Podrías incluir más actividad física para mejorar.")
                st.progress(0.6)
            else:
                st.warning("Baja. Considera realizar más actividades físicas para mejorar tu salud.")
                st.progress(0.3)

# Hábitos Alimenticios
def cuestionario_habitos_alimenticios():
    with st.container():
        st.title("🍎 Evaluación de Hábitos Alimenticios")
        st.write("Responde las siguientes preguntas para evaluar tus hábitos alimenticios y recibir recomendaciones personalizadas.")

        # Sección 1: Consumo de Alimentos Frescos
        with st.expander("🥦 Consumo de Alimentos Frescos", expanded=True):
            agua = st.radio("1. ¿Bebes al menos 1.5 litros de agua natural diariamente?", ["Nunca", "Algunas veces", "Casi siempre", "Siempre"], horizontal=True)
            verduras = st.radio("2. ¿Consumes al menos 200 g de verduras frescas diariamente?", ["Nunca", "Algunas veces", "Casi siempre", "Siempre"], horizontal=True)
            frutas = st.radio("3. ¿Consumes al menos 200 g de frutas diariamente?", ["Nunca", "Algunas veces", "Casi siempre", "Siempre"], horizontal=True)
            leguminosas = st.radio("4. ¿Consumes al menos 300 g de leguminosas semanalmente?", ["Nunca", "Algunas veces", "Casi siempre", "Siempre"], horizontal=True)
            frutos_secos = st.radio("5. ¿Consumes al menos 30 g de frutos secos o medio aguacate diariamente?", ["Nunca", "Algunas veces", "Casi siempre", "Siempre"], horizontal=True)

        # Sección 2: Carnes Frescas y Procesadas
        with st.expander("🍗 Carnes Frescas y Procesadas"):
            carne_fresca = st.radio(
                "6. ¿Qué tipo de carne fresca consumes con mayor frecuencia durante la semana?",
                ["Pescado fresco", "Pollo fresco", "Carne roja fresca", "No consumo carne fresca"],
                horizontal=True
            )
            carnes_procesadas = st.radio(
                "7. ¿Con qué frecuencia consumes carnes procesadas (embutidos, curadas, enlatadas o fritas)?",
                ["Nunca", "Algunas veces", "Casi siempre", "Siempre"],
                horizontal=True
            )

        # Sección 3: Hábitos Alimenticios Generales
        with st.expander("🍽️ Hábitos Alimenticios Generales", expanded=True):
            alimentos_fuera = st.radio("8. ¿Consumes alimentos no preparados en casa tres o más veces por semana?", ["Nunca", "Algunas veces", "Casi siempre", "Siempre"], horizontal=True)
            bebidas_azucaradas = st.radio("9. ¿Cuántas veces consumes bebidas azucaradas semanalmente?", ["Nunca", "1–3 veces", "4–6 veces", "Diario"], horizontal=True)
            postres_dulces = st.radio("10. ¿Consumes postres o dulces dos o más veces por semana?", ["Nunca", "Algunas veces", "Casi siempre", "Siempre"], horizontal=True)
            alimentos_procesados = st.radio("11. ¿Consumes alimentos procesados dos o más veces por semana?", ["Nunca", "Algunas veces", "Casi siempre", "Siempre"], horizontal=True)
            cereales = st.radio(
                "12. ¿Qué tipo de cereales consumes con mayor frecuencia?",
                ["Granos integrales", "Granos mínimamente procesados", "Granos procesados o ultraprocesados"],
                horizontal=True
            )

        # Sección 4: Consumo de Alcohol
        with st.expander("🍷 Consumo de Alcohol"):
            alcohol = st.radio(
                "13. Si eres hombre, ¿consumes más de 2 bebidas alcohólicas al día? Si eres mujer, ¿más de 1 bebida al día?",
                ["Nunca", "Algunas veces", "Casi siempre", "Siempre"],
                horizontal=True
            )

        # Botón para calcular la puntuación
        if st.button("📊 Calcular Puntuación", use_container_width=True, type="primary"):
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
                st.success("✅ Tus hábitos alimenticios son saludables.")
                st.progress(0.9)
                st.write("¡Felicidades! Tus elecciones alimenticias son excelentes. Sigue así para mantener una salud óptima.")
            elif 15 <= puntuacion_total < 30:
                st.warning("⚠️ Tus hábitos alimenticios son moderadamente saludables.")
                st.progress(0.6)
                st.write("Tienes hábitos buenos, pero hay áreas donde puedes mejorar. Considera reducir el consumo de alimentos procesados y aumentar tu ingesta de alimentos frescos.")
            else:
                st.error("❌ Tus hábitos alimenticios necesitan mejoras significativas.")
                st.progress(0.3)
                st.write("Es importante trabajar en tus hábitos alimenticios. Intenta incorporar más alimentos frescos y reducir el consumo de alimentos ultraprocesados. Podría ser útil consultar a un especialista.")

# ---- Barra lateral mejorada con tu logo ----
with st.sidebar:
    # Mostrar tu logo
    st.image("LOGO.png", use_container_width=True)
    st.divider()
    
    menu = st.selectbox(
        "Menú Principal",
        ["🏠 Inicio", "👤 Sobre Mí", "💼 Servicios", "📞 Contacto", "📊 Evaluación del Estilo de Vida"],
        index=0
    )
    
    st.divider()
    st.caption("MUPAI - Entrenamiento Digital Basado en Ciencia")
    st.caption("© 2023 Todos los derechos reservados")

# ---- Contenido principal respetando tu información original ----
if menu == "🏠 Inicio":
    # Mostrar el logo
    st.image("LOGO.png", use_container_width=True)

    # Título principal
    st.title("Bienvenido a MUPAI")

    # Misión
    st.header("Misión")
    st.write(
        """
        Hacer accesible el entrenamiento basado en ciencia, proporcionando planes completamente personalizados a través de herramientas digitales respaldadas por inteligencia artificial, datos precisos y la investigación más actualizada en ciencias del ejercicio. Nos enfocamos en promover el desarrollo integral de nuestros usuarios y su bienestar físico y mental.
        """
    )

    # Visión
    st.header("Visión")
    st.write(
        """
        Convertirnos en uno de los máximos referentes a nivel global en entrenamiento digital personalizado, aprovechando las nuevas tecnologías para hacer más accesible el fitness basado en ciencia. Aspiramos a transformar la experiencia del entrenamiento físico, integrando inteligencia artificial, investigación científica y herramientas digitales avanzadas que permitan a cualquier persona alcanzar su máximo potencial.
        """
    )

    # Política
    st.header("Política")
    st.write(
        """
        En **MUPAI**, nuestra política está fundamentada en el compromiso con la excelencia, la ética y el servicio centrado en el usuario. Actuamos con responsabilidad y transparencia para ofrecer soluciones tecnológicas que integren ciencia, personalización y accesibilidad, contribuyendo al bienestar integral de quienes confían en nosotros.
        """
    )

    # Política del Servicio
    st.header("Política del Servicio")
    st.write(
        """
        En **MUPAI**, guiamos nuestras acciones por los siguientes principios:
        - Diseñamos entrenamientos digitales que combinan personalización, datos confiables y ciencia del ejercicio.
        - Aprovechamos la tecnología para ofrecer un servicio accesible y adaptable a las necesidades de cada usuario.
        - Respetamos y protegemos la privacidad de los datos personales, garantizando su uso responsable.
        - Innovamos de forma continua para mejorar la experiencia y los resultados de nuestros usuarios.
        - Promovemos valores como el esfuerzo, la constancia y el respeto en cada interacción, fomentando un ambiente de crecimiento y bienestar.
        """
    )

elif menu == "👤 Sobre Mí":
    # Sección "Sobre Mí" con tu contenido original
    st.title("Sobre Mí")
    st.write("""
    Soy Erick Francisco De Luna Hernández, un profesional apasionado por el fitness y las ciencias del ejercicio, con una sólida formación académica y amplia experiencia en el diseño de metodologías de entrenamiento basadas en ciencia. Actualmente, me desempeño en **Muscle Up Gym**, donde estoy encargado del diseño y desarrollo de programas de entrenamiento fundamentados en evidencia científica. Mi labor se centra en crear metodologías personalizadas que optimicen el rendimiento físico y promuevan el bienestar integral de nuestros usuarios.

    Cuento con una Maestría en Fuerza y Acondicionamiento por el **Football Science Institute**, una Licenciatura en Ciencias del Ejercicio por la **Universidad Autónoma de Nuevo León (UANL)** y un intercambio académico internacional en la **Universidad de Sevilla**. Durante mi carrera, fui miembro del **Programa de Talento Universitario de la UANL**, una distinción que reconoce a estudiantes de excelencia académica y extracurricular. Además, adquirí experiencia clave en el **Laboratorio de Rendimiento Humano de la UANL**, colaborando en evaluaciones avanzadas de fuerza, biomecánica y acondicionamiento físico con tecnologías innovadoras.

    Mi trayectoria ha sido reconocida con distinciones como el **Premio al Mérito Académico de la UANL**, el **Primer Lugar de Generación** en la Facultad de Organización Deportiva y una **beca completa para un intercambio internacional** en la Universidad de Sevilla. Estos logros reflejan mi compromiso con la excelencia académica y profesional.

    Con una combinación de preparación académica, experiencia práctica y un enfoque basado en la evidencia, me dedico a diseñar soluciones que transformen el rendimiento físico y promuevan la salud integral, integrando ciencia, innovación y personalización.
    """)

    # Collage de imágenes (manteniendo tus imágenes originales)
    st.subheader("Galería de Imágenes")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("FB_IMG_1734820693317.jpg", use_container_width=True)
        st.image("FB_IMG_1734820729323.jpg", use_container_width=True)

    with col2:
        st.image("FB_IMG_1734820709707.jpg", use_container_width=True)
        st.image("FB_IMG_1734820808186.jpg", use_container_width=True)

    with col3:
        st.image("FB_IMG_1734820712642.jpg", use_container_width=True)

elif menu == "💼 Servicios":
    # Sección "Servicios" con tu contenido original
    st.title("Servicios")
    st.write("""
    **MUPAI** ofrece una amplia gama de servicios personalizados basados en ciencia del ejercicio:
    - Planes de entrenamiento individualizados.
    - Programas de mejora física y mental.
    - Asesoría en nutrición deportiva.
    - Consultoría en rendimiento deportivo.
    """)

elif menu == "📞 Contacto":
    # Sección "Contacto" con tu contenido original
    st.title("Contacto")
    st.write("""
    Para más información o consultas, contáctanos:
    - **Correo**: contacto@mupai.com
    - **Teléfono**: +52 866 258 05 94
    - **Ubicación**: Monterrey, Nuevo León
    """)

elif menu == "📊 Evaluación del Estilo de Vida":
    # Submenú para Evaluación del Estilo de Vida
    with st.sidebar:
        st.subheader("Áreas de Evaluación")
        submenu = st.radio(
            "Selecciona una evaluación",
            [
                "😰 Estrés Percibido", 
                "🌙 Calidad del Sueño", 
                "🏃 Nivel de Actividad Física", 
                "🍎 Hábitos Alimenticios", 
                "🧬 Potencial Genético Muscular"
            ]
        )
    
    if submenu == "😰 Estrés Percibido":
        st.title("Evaluación del Estrés Percibido")
        st.write("Responde las siguientes preguntas según cómo te has sentido durante el último mes:")

        # Preguntas del cuestionario
        options = ["Nunca", "Casi nunca", "A veces", "Bastante seguido", "Muy seguido"]
        q1 = st.radio("1. ¿Con qué frecuencia te has sentido molesto/a por algo que ocurrió inesperadamente?", options, horizontal=True)
        q2 = st.radio("2. ¿Con qué frecuencia has sentido que no puedes controlar las cosas importantes de tu vida?", options, horizontal=True)
        q3 = st.radio("3. ¿Con qué frecuencia has sentido nerviosismo o estrés?", options, horizontal=True)
        q4 = st.radio("4. ¿Con qué frecuencia has sentido confianza en tu capacidad para manejar tus problemas personales?", options, horizontal=True)
        q5 = st.radio("5. ¿Con qué frecuencia has sentido que las cosas estaban saliendo bien para ti?", options, horizontal=True)
        q6 = st.radio("6. ¿Con qué frecuencia has sentido que no podías lidiar con todas las cosas que tenías que hacer?", options, horizontal=True)
        q7 = st.radio("7. ¿Con qué frecuencia has sentido que podías controlar las irritaciones en tu vida?", options, horizontal=True)
        q8 = st.radio("8. ¿Con qué frecuencia has sentido que tenías el control sobre las cosas?", options, horizontal=True)
        q9 = st.radio("9. ¿Con qué frecuencia te has sentido enojado/a por cosas fuera de tu control?", options, horizontal=True)
        q10 = st.radio("10. ¿Con qué frecuencia has sentido que las dificultades se acumulaban tanto que no podías superarlas?", options, horizontal=True)

        # Botón para calcular el puntaje
        if st.button("📊 Calcular Puntuación", use_container_width=True, type="primary"):
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
            st.metric(label="Puntuación de Estrés", value=total_score)
            
            if total_score <= 13:
                st.success("Estrés bajo. ¡Excelente trabajo en mantener el equilibrio!")
                st.progress(0.2)
            elif 14 <= total_score <= 26:
                st.warning("Estrés moderado. Podrías beneficiarte de técnicas de manejo del estrés.")
                st.progress(0.5)
            else:
                st.error("Estrés alto. Considera buscar apoyo o implementar estrategias de relajación.")
                st.progress(0.8)
   
    elif submenu == "🌙 Calidad del Sueño":
        cuestionario_calidad_sueno()  # Llama la función de Calidad del Sueño mejorada
   
    elif submenu == "🏃 Nivel de Actividad Física":
        cuestionario_ipaq()  # Llama la función para Nivel de Actividad Física mejorada

    elif submenu == "🍎 Hábitos Alimenticios":
        cuestionario_habitos_alimenticios()  # Llama la función para Hábitos Alimenticios mejorada

    elif submenu == "🧬 Potencial Genético Muscular":
        st.title("Evaluación de Potencial Genético Muscular")
        st.write("Esta evaluación está en desarrollo. Próximamente podrás evaluar tu potencial genético para el desarrollo muscular.")
        st.image("dna.jpg", caption="Próximamente: Análisis de potencial genético", use_container_width=True)
