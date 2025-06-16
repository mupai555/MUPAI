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
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Intenta cargar el CSS si existe
try:
    local_css("styles.css")
except:
    st.warning("No se encontró el archivo CSS personalizado")

# ---- Logo y Encabezado ----
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# ---- Definición de funciones mejoradas ----
def cuestionario_calidad_sueno():
    with st.container():
        st.title("🌙 Evaluación de la Calidad del Sueño")
        st.subheader("Índice de Pittsburgh - PSQI")
        st.write("Responde las siguientes preguntas sobre tus hábitos de sueño durante el último mes:")
        
        with st.expander("📅 Horarios de sueño", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                hora_acostarse = st.text_input("Hora de acostarse (ej: 22:30)", key="hora_acostar")
            with col2:
                hora_levantarse = st.text_input("Hora de levantarse (ej: 07:00)", key="hora_levantar")
            
            col3, col4 = st.columns(2)
            with col3:
                tiempo_dormirse = st.slider("Tiempo para dormirse (minutos)", 0, 120, 15, key="tiempo_dormir")
            with col4:
                horas_dormidas = st.slider("Horas de sueño por noche", 0.0, 12.0, 7.0, step=0.5, key="horas_dormir")

        with st.expander("⚠️ Problemas para dormir", expanded=True):
            problemas = [
                "No poder conciliar el sueño en 30 minutos",
                "Despertarte durante la noche o muy temprano",
                "Ir al baño durante la noche",
                "No poder respirar bien",
                "Toser o roncar fuerte",
                "Sentir frío",
                "Sentir calor",
                "Tener pesadillas",
                "Sentir dolor"
            ]
            
            opciones = ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
            
            problemas_respuestas = {}
            for i, problema in enumerate(problemas):
                problemas_respuestas[problema] = st.radio(
                    f"{i+1}. {problema}:",
                    opciones,
                    horizontal=True,
                    key=f"problema_{i}"
                )

        with st.expander("💊 Uso de medicación"):
            uso_medicacion = st.radio(
                "Frecuencia de uso de medicamentos para dormir:",
                opciones,
                horizontal=True,
                key="medicacion"
            )

        with st.expander("😴 Disfunción diurna"):
            disfuncion_diurna_1 = st.radio(
                "Problemas para mantenerse despierto durante actividades:",
                opciones,
                horizontal=True,
                key="disfuncion1"
            )
            disfuncion_diurna_2 = st.radio(
                "Dificultad para mantener el entusiasmo:",
                opciones,
                horizontal=True,
                key="disfuncion2"
            )

        with st.expander("⭐ Calidad subjetiva"):
            calidad_sueno = st.radio(
                "Calificación de la calidad de tu sueño:",
                ["Muy buena", "Bastante buena", "Bastante mala", "Muy mala"],
                horizontal=True,
                key="calidad"
            )

        if st.button("📊 Calcular Puntuación", use_container_width=True, type="primary"):
            puntuacion = {"Ninguna vez": 0, "Menos de una vez a la semana": 1, "Una o dos veces a la semana": 2, "Tres o más veces a la semana": 3}
            calidad_puntuacion = {"Muy buena": 0, "Bastante buena": 1, "Bastante mala": 2, "Muy mala": 3}

            componente_1 = calidad_puntuacion[calidad_sueno]
            componente_2 = 1 if tiempo_dormirse > 30 else 0
            componente_3 = 0 if horas_dormidas >= 7 else (1 if horas_dormidas >= 6 else 2)
            componente_4 = sum(puntuacion[v] for v in problemas_respuestas.values())
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

# Otras funciones (ipaq, habitos_alimenticios, etc) irían aquí...

# ---- Barra lateral mejorada ----
with st.sidebar:
    st.title("MUPAI")
    st.subheader("Entrenamiento Digital")
    st.divider()
    
    menu = st.selectbox(
        "Menú Principal",
        ["🏠 Inicio", "👤 Sobre Mí", "💼 Servicios", "📞 Contacto", "📊 Evaluación del Estilo de Vida"],
        index=0
    )
    
    st.divider()
    st.caption("MUPAI - Entrenamiento Digital Basado en Ciencia")
    st.caption("© 2023 Todos los derechos reservados")

# ---- Contenido principal ----
if menu == "🏠 Inicio":
    st.title("Bienvenido a MUPAI")
    st.subheader("Entrenamiento Digital Basado en Ciencia")
    
    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["Misión", "Visión", "Política"])
    
    with tab1:
        st.header("🚀 Misión")
        st.write("""
        Hacer accesible el entrenamiento basado en ciencia, proporcionando planes completamente personalizados a través de herramientas digitales respaldadas por inteligencia artificial, datos precisos y la investigación más actualizada en ciencias del ejercicio.
        """)
    
    with tab2:
        st.header("🔭 Visión")
        st.write("""
        Convertirnos en uno de los máximos referentes a nivel global en entrenamiento digital personalizado, aprovechando las nuevas tecnologías para hacer más accesible el fitness basado en ciencia.
        """)
    
    with tab3:
        st.header("📜 Política")
        st.write("""
        En **MUPAI**, nuestra política está fundamentada en el compromiso con la excelencia, la ética y el servicio centrado en el usuario.
        """)
    
    st.divider()
    
    st.header("Nuestros Valores Fundamentales")
    cols = st.columns(4)
    valores = [
        ("💡", "Innovación", "Aprovechamos la tecnología para crear soluciones avanzadas"),
        ("🎯", "Personalización", "Diseñamos planes únicos para cada individuo"),
        ("🔬", "Ciencia", "Basamos todo en evidencia científica sólida"),
        ("❤️", "Bienestar", "Buscamos tu desarrollo físico y mental integral")
    ]
    
    for i, (icono, titulo, desc) in enumerate(valores):
        with cols[i]:
            st.markdown(f"<h3 style='text-align:center;'>{icono} {titulo}</h3>", unsafe_allow_html=True)
            st.caption(desc)
    
    st.divider()

elif menu == "👤 Sobre Mí":
    st.title("Sobre Mí")
    st.write("""
    Soy Erick Francisco De Luna Hernández, un profesional apasionado por el fitness y las ciencias del ejercicio, con una sólida formación académica y amplia experiencia en el diseño de metodologías de entrenamiento basadas en ciencia.
    """)
    
    st.subheader("Formación Académica")
    st.write("""
    - Maestría en Fuerza y Acondicionamiento por el Football Science Institute
    - Licenciatura en Ciencias del Ejercicio por la UANL
    - Intercambio académico en la Universidad de Sevilla
    """)
    
    st.subheader("Experiencia Profesional")
    st.write("""
    Actualmente me desempeño en Muscle Up Gym, donde estoy encargado del diseño y desarrollo de programas de entrenamiento fundamentados en evidencia científica.
    """)
    
    st.subheader("Logros y Reconocimientos")
    st.write("""
    - Premio al Mérito Académico de la UANL
    - Primer Lugar de Generación en la Facultad de Organización Deportiva
    - Beca completa para intercambio internacional
    """)

elif menu == "💼 Servicios":
    st.title("Nuestros Servicios")
    st.write("Ofrecemos soluciones personalizadas basadas en ciencia para optimizar tu rendimiento físico y bienestar integral.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🎯 Entrenamiento Personalizado")
        st.write("Planes individualizados basados en tu perfil físico, objetivos y disponibilidad.")
        st.button("Más información", key="btn_entrenamiento")
    
    with col2:
        st.subheader("📊 Evaluación Integral")
        st.write("Análisis completo de tu condición física, hábitos y potencial de mejora.")
        st.button("Más información", key="btn_evaluacion")
    
    with col3:
        st.subheader("🍎 Nutrición Deportiva")
        st.write("Asesoría nutricional personalizada para potenciar tu rendimiento y salud.")
        st.button("Más información", key="btn_nutricion")
    
    st.divider()
    
    st.subheader("Nuestro Enfoque")
    st.write("""
    Combinamos ciencia del ejercicio, tecnología de vanguardia y metodologías probadas para ofrecer:
    - Programas 100% personalizados
    - Seguimiento constante
    - Ajustes basados en datos
    - Soporte profesional continuo
    """)

elif menu == "📞 Contacto":
    st.title("Contacto")
    st.write("Estamos aquí para ayudarte en tu camino hacia un mejor bienestar físico.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Información de Contacto")
        st.write("📧 contacto@mupai.com")
        st.write("📱 +52 866 258 05 94")
        st.write("🏢 Monterrey, Nuevo León, México")
        
        st.subheader("Horario de Atención")
        st.write("Lunes a Viernes: 9:00 AM - 6:00 PM")
        st.write("Sábados: 10:00 AM - 2:00 PM")
    
    with col2:
        st.subheader("Envíanos un Mensaje")
        nombre = st.text_input("Nombre completo")
        email = st.text_input("Correo electrónico")
        mensaje = st.text_area("Mensaje", height=150)
        if st.button("Enviar mensaje", type="primary"):
            st.success("¡Mensaje enviado con éxito! Te contactaremos pronto.")

elif menu == "📊 Evaluación del Estilo de Vida":
    st.title("Evaluación de Estilo de Vida")
    st.write("Completa nuestras evaluaciones para recibir recomendaciones personalizadas.")
    
    # Submenú para Evaluación del Estilo de Vida
    submenu = st.selectbox(
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
        st.header("Evaluación del Estrés Percibido")
        st.write("Responde las siguientes preguntas según cómo te has sentido durante el último mes:")
        
        # (Contenido del cuestionario de estrés iría aquí)

    elif submenu == "🌙 Calidad del Sueño":
        cuestionario_calidad_sueno()
    
    elif submenu == "🏃 Nivel de Actividad Física":
        st.header("Cuestionario de Actividad Física - IPAQ")
        st.write("Responde las siguientes preguntas sobre tu actividad física durante los últimos 7 días.")
        # (Contenido del cuestionario IPAQ iría aquí)
    
    elif submenu == "🍎 Hábitos Alimenticios":
        st.header("Evaluación de Hábitos Alimenticios")
        st.write("Responde las siguientes preguntas para evaluar tus hábitos alimenticios.")
        # (Contenido del cuestionario de hábitos alimenticios iría aquí)
    
    elif submenu == "🧬 Potencial Genético Muscular":
        st.header("Evaluación de Potencial Genético Muscular")
        st.write("Completa este cuestionario para evaluar tu potencial genético para el desarrollo muscular.")
        # (Contenido del cuestionario genético iría aquí)
