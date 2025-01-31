import streamlit as st

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
    
    st.header("Misión")
    st.write("""
    Hacer accesible el entrenamiento basado en ciencia, proporcionando planes completamente personalizados a través de herramientas digitales respaldadas por inteligencia artificial, datos precisos y la investigación más actualizada en ciencias del ejercicio. Nos enfocamos en promover el desarrollo integral de nuestros usuarios y su bienestar físico y mental.
    """)

    st.header("Visión")
    st.write("""
    Convertirnos en uno de los máximos referentes a nivel global en entrenamiento digital personalizado, aprovechando las nuevas tecnologías para hacer más accesible el fitness basado en ciencia. Aspiramos a transformar la experiencia del entrenamiento físico, integrando inteligencia artificial, investigación científica y herramientas digitales avanzadas que permitan a cualquier persona alcanzar su máximo potencial.
    """)

    st.header("Política")
    st.write("""
    En **MUPAI**, nuestra política está fundamentada en el compromiso con la excelencia, la ética y el servicio centrado en el usuario. Actuamos con responsabilidad y transparencia para ofrecer soluciones tecnológicas que integren ciencia, personalización y accesibilidad, contribuyendo al bienestar integral de quienes confían en nosotros.
    """)

    st.header("Política del Servicio")
    st.write("""
    En **MUPAI**, guiamos nuestras acciones por los siguientes principios:
    - Diseñamos entrenamientos digitales que combinan personalización, datos confiables y ciencia del ejercicio.
    - Aprovechamos la tecnología para ofrecer un servicio accesible y adaptable a las necesidades de cada usuario.
    - Respetamos y protegemos la privacidad de los datos personales, garantizando su uso responsable.
    - Innovamos de forma continua para mejorar la experiencia y los resultados de nuestros usuarios.
    - Promovemos valores como el esfuerzo, la constancia y el respeto en cada interacción, fomentando un ambiente de crecimiento y bienestar.
    """)

elif menu == "Sobre Mí":
    st.title("Sobre Mí")
    st.write("""
    Soy Erick Francisco De Luna Hernández, un profesional apasionado por el fitness y las ciencias del ejercicio, con una sólida formación académica y amplia experiencia en el diseño de metodologías de entrenamiento basadas en ciencia. Actualmente, me desempeño en **Muscle Up Gym**, donde estoy encargado del diseño y desarrollo de programas de entrenamiento fundamentados en evidencia científica. Mi labor se centra en crear metodologías personalizadas que optimicen el rendimiento físico y promuevan el bienestar integral de nuestros usuarios.

    Cuento con una Maestría en Fuerza y Acondicionamiento por el **Football Science Institute**, una Licenciatura en Ciencias del Ejercicio por la **Universidad Autónoma de Nuevo León (UANL)** y un intercambio académico internacional en la **Universidad de Sevilla**. Durante mi carrera, fui miembro del **Programa de Talento Universitario de la UANL**, una distinción que reconoce a estudiantes de excelencia académica y extracurricular. Además, adquirí experiencia clave en el **Laboratorio de Rendimiento Humano de la UANL**, colaborando en evaluaciones avanzadas de fuerza, biomecánica y acondicionamiento físico con tecnologías innovadoras.

    Mi trayectoria ha sido reconocida con distinciones como el **Premio al Mérito Académico de la UANL**, el **Primer Lugar de Generación** en la Facultad de Organización Deportiva y una **beca completa para un intercambio internacional** en la Universidad de Sevilla. Estos logros reflejan mi compromiso con la excelencia académica y profesional.

    Con una combinación de preparación académica, experiencia práctica y un enfoque basado en la evidencia, me dedico a diseñar soluciones que transformen el rendimiento físico y promuevan la salud integral, integrando ciencia, innovación y personalización.
    """)

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

elif menu == "Servicios":
    st.title("Servicios")
    st.write("""
    **MUPAI** ofrece una amplia gama de servicios personalizados basados en ciencia del ejercicio:
    - Planes de entrenamiento individualizados.
    - Programas de mejora física y mental.
    - Asesoría en nutrición deportiva.
    - Consultoría en rendimiento deportivo.
    """)

elif menu == "Perfil MUPAI/Salud y Rendimiento":
    submenu = st.sidebar.radio(
        "Selecciona una opción", 
        ["Entrenamiento", "Nutrición"],
        key="submenu_selector"
    )
    
    if submenu == "Entrenamiento":
        st.title("📋 Cuestionario de Evaluación MUPAI")
        
        with st.form("cuestionario_mupai"):
            # Sección 1: Información Personal
            st.header("1. Información Personal")
            nombre = st.text_input("Nombre completo legal:")
            edad = st.number_input("Edad (años):", min_value=0, max_value=120, step=1)
            genero = st.radio("Género biológico:", ["Hombre", "Mujer"])
            
            # Sección 2: Cálculo FFMI
            st.header("2. Cálculo del Índice de Masa Libre de Grasa (FFMI)")
            peso = st.number_input("Peso actual (kg):", min_value=30.0, max_value=300.0, step=0.1)
            altura = st.number_input("Altura (cm):", min_value=100, max_value=250, step=1)
            grasa = st.number_input("Porcentaje de grasa corporal:", min_value=5.0, max_value=50.0, step=0.1)
            
            # Sección 3: Frecuencia de Entrenamiento
            st.header("3. Frecuencia Semanal de Entrenamiento")
            frecuencia = st.radio("¿Cuántas veces por semana puedes entrenar?", 
                                ["2 veces por semana", "3 veces por semana", 
                                 "4 veces por semana", "5 veces por semana", 
                                 "6 veces por semana"])
            
            # Sección 4: Factores de Recuperación
            st.header("4. Factores de Recuperación")
            
            # 4.1 Calidad del Sueño
            st.subheader("Calidad del Sueño")
            col1, col2 = st.columns(2)
            with col1:
                dormir = st.time_input("Hora de acostarse (formato 24h):")
            with col2:
                despertar = st.time_input("Hora de despertarse (formato 24h):")
                
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
            
            problemas_sueño = st.selectbox("Frecuencia de problemas de sueño:", 
                                         ["Nunca (0 puntos)",
                                          "Menos de una vez por semana (1 punto)",
                                          "Entre 1 y 2 veces por semana (2 puntos)",
                                          "Tres o más veces por semana (3 puntos)"])
            
            calidad_sueño = st.selectbox("Calidad general del sueño:", 
                                       ["Muy buena (0 puntos)",
                                        "Buena (1 punto)",
                                        "Regular (2 puntos)",
                                        "Mala (3 puntos)"])
            
            # 4.2 Estrés Percibido
            st.subheader("Escala de Estrés Percibido")
            preguntas_estres = [
                "En el último mes, ¿con qué frecuencia has sentido que no podías controlar lo que sucedía en tu vida?",
                "En el último mes, ¿con qué frecuencia has sentido que tenías demasiadas responsabilidades?",
                "En el último mes, ¿con qué frecuencia te has sentido abrumado por el estrés?",
                "En el último mes, ¿con qué frecuencia has sentido que no podías manejar todo lo que tenías que hacer?",
                "En el último mes, ¿con qué frecuencia has sentido que no tenías control sobre el estrés?",
                "En el último mes, ¿con qué frecuencia has sentido que todo iba bien? (pregunta invertida)",
                "En el último mes, ¿con qué frecuencia has sentido que podías manejar tus problemas? (pregunta invertida)",
                "En el último mes, ¿con qué frecuencia has sentido que tenías todo bajo control? (pregunta invertida)",
                "En el último mes, ¿con qué frecuencia has sentido que las dificultades eran demasiado grandes?",
                "En el último mes, ¿con qué frecuencia has sentido que estabas en control de tu tiempo? (pregunta invertida)"
            ]
            
            opciones_estres = ["Nunca", "Casi nunca", "Algunas veces", "A menudo", "Muy a menudo"]
            puntuaciones_estres = []
            
            for i, pregunta in enumerate(preguntas_estres):
                respuesta = st.selectbox(f"{i+1}. {pregunta}", opciones_estres)
                puntuacion = opciones_estres.index(respuesta)
                
                # Invertir puntuación para preguntas invertidas (6-8 y 10)
                if i in [5, 6, 7, 9]:  # Índices base 0
                    puntuacion = 4 - puntuacion
                puntuaciones_estres.append(puntuacion)
            
            # Sección 5: Objetivos de Entrenamiento
            st.header("5. Objetivos de Entrenamiento")
            tipo_programa = st.radio("Tipo de Programa:", 
                                   ["Hipertrofia General", "Competición en Fisicoculturismo"])
            
            grupos_musculares = [
                "Flexores de codo", "Triceps", "Dorsal ancho", "Trapecio",
                "Pectoral", "Deltoides", "Cuádriceps", "Isquitibiales",
                "Glúteos", "Pantorrillas"
            ]
            
            if tipo_programa == "Hipertrofia General":
                priorizar = st.multiselect("Priorizar grupos musculares:", grupos_musculares)
                no_enfatizar = st.multiselect("Grupos musculares a no enfatizar:", grupos_musculares)
            
            # Botón de envío
            submitted = st.form_submit_button("Calcular Perfil")
            
            if submitted:
                # Cálculos FFMI
                mlg = peso * (1 - (grasa/100))
                ffmi = mlg / ((altura/100) ** 2)
                
                # Determinar nivel de entrenamiento
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
                
                # Calcular puntuación sueño
                puntos_sueño = sum([
                    int(tiempo_dormir.split("(")[1][0]),
                    int(horas_sueño.split("(")[1][0]),
                    int(problemas_sueño.split("(")[1][0]),
                    int(calidad_sueño.split("(")[1][0])
                ])
                
                # Calcular estrés
                total_estres = sum(puntuaciones_estres)
                
                # Mostrar resultados
                st.success("**Resultados del Análisis**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("FFMI", f"{ffmi:.2f}")
                    st.metric("Nivel de Entrenamiento", nivel)
                    st.metric("Masa Libre de Grasa", f"{mlg:.2f} kg")
                with col2:
                    st.metric("Calidad de Sueño", f"{puntos_sueño}/12")
                    st.metric("Nivel de Estrés", f"{total_estres}/40")
                with col3:
                    st.metric("Frecuencia Recomendada", frecuencia)
                    st.metric("Tipo de Programa", tipo_programa)
                
                # Cálculos metabólicos
                tmb = 370 + (21.6 * mlg)
                st.subheader("Metabolismo")
                st.write(f"**Tasa Metabólica Basal (TMB):** {tmb:.2f} kcal")
                
                # Recomendaciones finales
                with st.expander("📌 Recomendaciones Personalizadas", expanded=True):
                    st.write(f"""
                    ### Plan de Acción:
                    - **Programa de entrenamiento:** {tipo_programa}
                    - **Frecuencia semanal:** {frecuencia}
                    - **Enfoque de recuperación:** {"Prioritario 🔴" if puntos_sueño > 5 or total_estres > 20 else "Moderado 🟢"}
                    - **Suplementación recomendada:** {"Básica (Proteína, Creatina)" if nivel in ["Principiante", "Intermedio"] else "Avanzada (BCAAs, Pre-entreno)"}
                    """)
                    
                    if tipo_programa == "Competición en Fisicoculturismo":
                        if "Avanzado" in nivel or "Élite" in nivel:
                            st.write("\n### Categorías disponibles:")
                            if genero == "Hombre":
                                st.write("- Classic Physique\n- Men’s Physique\n- BODYBUILDING")
                            else:
                                st.write("- Wellness\n- Bikini\n- Bodybuilding")
                        else:
                            st.warning("Se requiere nivel Avanzado o superior para categorías de competición")

    elif submenu == "Nutrición":
        st.title("Nutrición")
        st.write("""
        En esta sección exploraremos cómo optimizar la nutrición para mejorar el rendimiento deportivo, la salud y el bienestar.
        """)

elif menu == "Contacto":
    st.title("Contacto")
    st.write("""
    Para más información o consultas, contáctanos:
    - **Correo**: contacto@mupai.com
    - **Teléfono**: +52 123 456 7890
    - **Ubicación**: Monterrey, Nuevo León
    """)
