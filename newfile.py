import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="MUPAI - Entrenamiento Digital",
    page_icon="🤖",
    layout="wide",
)
# Definir la función para Calidad del Sueño
def cuestionario_calidad_sueno():
    st.title("Evaluación de la Calidad del Sueño - Índice de Pittsburgh")
    st.write("Responde las siguientes preguntas sobre tus hábitos de sueño durante el último mes:")

    # Bloque 1: Horarios de sueño
    hora_acostarse = st.text_input("1. ¿A qué hora te acuestas normalmente?")
    tiempo_dormirse = st.slider("2. ¿Cuánto tiempo tardas normalmente en dormirte (minutos)?", 0, 120, 15)
    hora_levantarse = st.text_input("3. ¿A qué hora te levantas normalmente?")
    horas_dormidas = st.slider("4. ¿Cuántas horas calculas que duermes habitualmente por noche?", 0, 12, 7)

    # Bloque 2: Problemas para dormir
    st.write("5. Durante el último mes, ¿con qué frecuencia has experimentado los siguientes problemas?")
    problemas_dormir = {
        "No poder conciliar el sueño en 30 minutos": st.radio(
            "a. No poder conciliar el sueño en los primeros 30 minutos:",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        ),
        "Despertarte durante la noche o muy temprano": st.radio(
            "b. Despertarte durante la noche o muy temprano:",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        ),
        "Ir al baño durante la noche": st.radio(
            "c. Tener que levantarte para ir al baño:",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        ),
        "No poder respirar bien": st.radio(
            "d. No poder respirar bien mientras duermes:",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        ),
        "Toser o roncar fuerte": st.radio(
            "e. Toser o roncar fuerte mientras duermes:",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        ),
        "Sentir frío": st.radio(
            "f. Sentir frío mientras duermes:",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        ),
        "Sentir calor": st.radio(
            "g. Sentir calor mientras duermes:",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        ),
        "Tener pesadillas": st.radio(
            "h. Tener pesadillas:",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        ),
        "Sentir dolor": st.radio(
            "i. Sentir dolor que dificulte tu sueño:",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        )
    }

    # Bloque 3: Uso de medicación
    uso_medicacion = st.radio(
        "6. ¿Cuántas veces tomaste medicamentos para dormir durante el último mes?",
        ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
    )

    # Bloque 4: Disfunción diurna
    st.write("7. Durante el último mes, ¿con qué frecuencia tuviste los siguientes problemas?")
    disfuncion_diurna_1 = st.radio(
        "a. Problemas para mantenerte despierto(a) mientras realizabas actividades sociales o tareas:",
        ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
    )
    disfuncion_diurna_2 = st.radio(
        "b. Dificultad para mantener el entusiasmo para hacer cosas:",
        ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
    )

    # Bloque 5: Calidad subjetiva del sueño
    calidad_sueno = st.radio(
        "8. ¿Cómo calificarías la calidad de tu sueño durante el último mes?",
        ["Muy buena", "Bastante buena", "Bastante mala", "Muy mala"]
    )

    # Botón para calcular la puntuación
    if st.button("Calcular Puntuación"):
        puntuacion = {"Ninguna vez": 0, "Menos de una vez a la semana": 1, "Una o dos veces a la semana": 2, "Tres o más veces a la semana": 3}
        calidad_puntuacion = {"Muy buena": 0, "Bastante buena": 1, "Bastante mala": 2, "Muy mala": 3}

        # Cálculo de los componentes
        componente_1 = calidad_puntuacion[calidad_sueno]
        componente_2 = 1 if tiempo_dormirse > 30 else 0  # Ejemplo de puntuación
        componente_3 = 0 if horas_dormidas >= 7 else (1 if horas_dormidas >= 6 else 2)
        componente_4 = sum(puntuacion[v] for v in problemas_dormir.values())
        componente_5 = puntuacion[uso_medicacion]
        componente_6 = puntuacion[disfuncion_diurna_1] + puntuacion[disfuncion_diurna_2]

        total_puntuacion = componente_1 + componente_2 + componente_3 + componente_4 + componente_5 + componente_6

        # Mostrar resultado
        st.write(f"### Tu puntuación total del PSQI es: {total_puntuacion}")
        if total_puntuacion <= 5:
            st.success("Buena calidad de sueño.")
        elif 6 <= total_puntuacion <= 10:
            st.warning("Calidad de sueño moderada.")
        else:
            st.error("Mala calidad de sueño. Considera consultar a un especialista.")

# Definir la función para Nivel de Actividad Física 
def cuestionario_ipaq():
    st.title("Cuestionario de Actividad Física - IPAQ (Versión Corta)")
    st.write("Responde las siguientes preguntas sobre tu actividad física durante los últimos 7 días.")

    # Actividades físicas vigorosas
    st.subheader("Actividades Físicas Vigorosas")
    dias_vigorosa = st.number_input(
        "1. Durante los últimos 7 días, ¿en cuántos días realizaste actividades físicas vigorosas como levantar objetos pesados, cavar, aeróbicos o andar en bicicleta rápido? (Días por semana)", 
        min_value=0, max_value=7, step=1, key="dias_vigorosa"
    )
    if dias_vigorosa > 0:
        tiempo_vigorosa_horas = st.number_input(
            "2. ¿Cuántas horas por día dedicaste generalmente a esas actividades vigorosas?", 
            min_value=0, step=1, key="horas_vigorosa"
        )
        tiempo_vigorosa_minutos = st.number_input(
            "¿Y cuántos minutos por día (además de las horas)?", 
            min_value=0, max_value=59, step=1, key="minutos_vigorosa"
        )
    else:
        tiempo_vigorosa_horas = 0
        tiempo_vigorosa_minutos = 0

    # Actividades físicas moderadas
    st.subheader("Actividades Físicas Moderadas")
    dias_moderada = st.number_input(
        "3. Durante los últimos 7 días, ¿en cuántos días realizaste actividades físicas moderadas como llevar cargas ligeras o andar en bicicleta a un ritmo normal? (Días por semana)", 
        min_value=0, max_value=7, step=1, key="dias_moderada"
    )
    if dias_moderada > 0:
        tiempo_moderada_horas = st.number_input(
            "4. ¿Cuántas horas por día dedicaste generalmente a esas actividades moderadas?", 
            min_value=0, step=1, key="horas_moderada"
        )
        tiempo_moderada_minutos = st.number_input(
            "¿Y cuántos minutos por día (además de las horas)?", 
            min_value=0, max_value=59, step=1, key="minutos_moderada"
        )
    else:
        tiempo_moderada_horas = 0
        tiempo_moderada_minutos = 0

    # Caminata
    st.subheader("Tiempo Dedicado a Caminar")
    dias_caminata = st.number_input(
        "5. Durante los últimos 7 días, ¿en cuántos días caminaste al menos 10 minutos seguidos? (Días por semana)", 
        min_value=0, max_value=7, step=1, key="dias_caminata"
    )
    if dias_caminata > 0:
        tiempo_caminata_horas = st.number_input(
            "6. ¿Cuántas horas por día dedicaste generalmente a caminar?", 
            min_value=0, step=1, key="horas_caminata"
        )
        tiempo_caminata_minutos = st.number_input(
            "¿Y cuántos minutos por día (además de las horas)?", 
            min_value=0, max_value=59, step=1, key="minutos_caminata"
        )
    else:
        tiempo_caminata_horas = 0
        tiempo_caminata_minutos = 0

    # Tiempo sedentario
    st.subheader("Tiempo de Sedentarismo")
    tiempo_sedentario_horas = st.number_input(
        "7. Durante los últimos 7 días, ¿cuántas horas por día dedicaste a estar sentado? (Promedio diario)", 
        min_value=0, step=1, key="horas_sedentario"
    )
    tiempo_sedentario_minutos = st.number_input(
        "¿Y cuántos minutos por día (además de las horas)?", 
        min_value=0, max_value=59, step=1, key="minutos_sedentario"
    )

    # Calcular el scoring
    if st.button("Calcular Puntuación", key="calcular_puntuacion"):
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
        st.write(f"### Tu puntuación total de MET-minutos/semana es: {total_met:.2f}")
        st.write(f"Tiempo sedentario promedio: {tiempo_sedentario_horas} horas y {tiempo_sedentario_minutos} minutos por día.")

        # Clasificación de actividad
        if total_met >= 3000:
            st.success("Nivel de actividad: Alta. Excelente trabajo en mantenerte activo.")
        elif 600 <= total_met < 3000:
            st.info("Nivel de actividad: Moderada. Podrías incluir más actividad física para mejorar.")
        else:
            st.warning("Nivel de actividad: Baja. Considera realizar más actividades físicas para mejorar tu salud.")
        

# Definir la función para el cuestionario Mini-ECCA v.2
def cuestionario_mini_ecca():
    st.title("Cuestionario Mini-ECCA v.2")
    st.write("Responde las siguientes preguntas sobre tus hábitos alimenticios y estilo de vida:")

    # Preguntas del cuestionario
    opciones = ["Nunca", "Algunas veces", "Casi siempre", "Siempre"]

    q1 = st.radio("1. ¿Bebe, por lo menos, 1.5 litros de agua natural todos los días (de lunes a domingo)?", opciones)
    q2 = st.radio("2. ¿Consume, por lo menos, 200 g de verduras cocidas o crudas todos los días (de lunes a domingo)?", opciones)
    q3 = st.radio("3. ¿Consume, al menos, 200 g de pescado fresco o congelado (no enlatado) a la semana?", opciones)
    q4 = st.radio("4. ¿Cuántas veces a la semana consume una o más latas (o vasos) de alguna bebida azucarada?", opciones)
    q5 = st.radio("5. ¿Consume, por lo menos, 200 g de frutas todos los días (de lunes a domingo)?", opciones)
    q6 = st.radio("6. ¿Consume, por lo menos, 30 g de oleaginosas o medio aguacate todos los días (de lunes a domingo)?", opciones)
    q7 = st.radio("7. ¿Consume alimentos no preparados en casa 3 o más veces por semana?", opciones)
    q8 = st.radio("8. ¿Consume alimentos procesados (frituras, embutidos, platillos empaquetados) 2 o más veces por semana?", opciones)
    q9 = st.radio("9. ¿Consume, por lo menos, 300 g de leguminosas a la semana?", opciones)
    q10 = st.radio("10. ¿Incluye algún tipo de lácteos o sus equivalentes en su dieta diaria?", opciones)
    q11 = st.radio("11. ¿Cuántas veces a la semana consume alimentos fritos?", opciones)
    q12 = st.radio("12. ¿Realiza al menos 30 minutos de actividad física 3 veces por semana o más?", opciones)
    q13 = st.radio("13. ¿Evita el consumo de alimentos con alto contenido de sodio (ejemplo: embutidos, sopas instantáneas)?", opciones)
    q14 = st.radio("14. ¿Consume productos integrales como pan integral, avena o arroz integral al menos 3 veces a la semana?", opciones)

    # Botón para calcular la puntuación
    if st.button("Calcular Puntuación"):
        # Asignar valores numéricos a las respuestas
        puntuacion = {"Nunca": 1, "Algunas veces": 2, "Casi siempre": 3, "Siempre": 4}
        total_puntuacion = (
            puntuacion[q1] + puntuacion[q2] + puntuacion[q3] + puntuacion[q4] +
            puntuacion[q5] + puntuacion[q6] + puntuacion[q7] + puntuacion[q8] +
            puntuacion[q9] + puntuacion[q10] + puntuacion[q11] + puntuacion[q12] +
            puntuacion[q13] + puntuacion[q14]
        )

        # Mostrar resultado
        st.write(f"### Tu puntuación total es: {total_puntuacion}")
        if total_puntuacion >= 50:
            st.success("¡Excelente! Tienes hábitos alimenticios muy saludables.")
        elif 35 <= total_puntuacion < 50:
            st.info("Tus hábitos alimenticios son buenos, pero pueden mejorar.")
        else:
            st.warning("Considera adoptar hábitos más saludables para mejorar tu calidad de vida.")

# Barra lateral de navegación
menu = st.sidebar.selectbox(
    "Menú",
    ["Inicio", "Sobre Mí", "Servicios", "Contacto", "Evaluación del Estilo de Vida"]
)

# Contenido del menú principal
if menu == "Inicio":
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

elif menu == "Sobre Mí":
    # Sección "Sobre Mí"
    st.title("Sobre Mí")
    st.write("""
    Soy Erick Francisco De Luna Hernández, un profesional apasionado por el fitness y las ciencias del ejercicio, con una sólida formación académica y amplia experiencia en el diseño de metodologías de entrenamiento basadas en ciencia. Actualmente, me desempeño en **Muscle Up Gym**, donde estoy encargado del diseño y desarrollo de programas de entrenamiento fundamentados en evidencia científica. Mi labor se centra en crear metodologías personalizadas que optimicen el rendimiento físico y promuevan el bienestar integral de nuestros usuarios.

    Cuento con una Maestría en Fuerza y Acondicionamiento por el **Football Science Institute**, una Licenciatura en Ciencias del Ejercicio por la **Universidad Autónoma de Nuevo León (UANL)** y un intercambio académico internacional en la **Universidad de Sevilla**. Durante mi carrera, fui miembro del **Programa de Talento Universitario de la UANL**, una distinción que reconoce a estudiantes de excelencia académica y extracurricular. Además, adquirí experiencia clave en el **Laboratorio de Rendimiento Humano de la UANL**, colaborando en evaluaciones avanzadas de fuerza, biomecánica y acondicionamiento físico con tecnologías innovadoras.

    Mi trayectoria ha sido reconocida con distinciones como el **Premio al Mérito Académico de la UANL**, el **Primer Lugar de Generación** en la Facultad de Organización Deportiva y una **beca completa para un intercambio internacional** en la Universidad de Sevilla. Estos logros reflejan mi compromiso con la excelencia académica y profesional.

    Con una combinación de preparación académica, experiencia práctica y un enfoque basado en la evidencia, me dedico a diseñar soluciones que transformen el rendimiento físico y promuevan la salud integral, integrando ciencia, innovación y personalización.
    """)

    # Collage de imágenes
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
    # Sección "Servicios"
    st.title("Servicios")
    st.write("""
    **MUPAI** ofrece una amplia gama de servicios personalizados basados en ciencia del ejercicio:
    - Planes de entrenamiento individualizados.
    - Programas de mejora física y mental.
    - Asesoría en nutrición deportiva.
    - Consultoría en rendimiento deportivo.
    """)

elif menu == "Contacto":
    # Sección "Contacto"
    st.title("Contacto")
    st.write("""
    Para más información o consultas, contáctanos:
    - **Correo**: contacto@mupai.com
    - **Teléfono**: +52 866 258 05 94
    - **Ubicación**: Monterrey, Nuevo León
    """)

elif menu == "Evaluación del Estilo de Vida":
    # Submenú para Evaluación del Estilo de Vida
    submenu = st.sidebar.radio(
        "Áreas de Evaluación",
        [
            "Estrés Percibido", 
            "Calidad del Sueño", 
            "Nivel de Actividad Física", 
            "Hábitos Alimenticios", 
            "Potencial Genético Muscular"
        ]
    )

    if submenu == "Estrés Percibido":
        st.title("Evaluación del Estrés Percibido")
        st.write("Responde las siguientes preguntas según cómo te has sentido durante el último mes:")

        # Preguntas del cuestionario
        options = ["Nunca", "Casi nunca", "A veces", "Bastante seguido", "Muy seguido"]
        q1 = st.radio("1. ¿Con qué frecuencia te has sentido molesto/a por algo que ocurrió inesperadamente?", options)
        q2 = st.radio("2. ¿Con qué frecuencia has sentido que no puedes controlar las cosas importantes de tu vida?", options)
        q3 = st.radio("3. ¿Con qué frecuencia has sentido nerviosismo o estrés?", options)
        q4 = st.radio("4. ¿Con qué frecuencia has sentido confianza en tu capacidad para manejar tus problemas personales?", options)
        q5 = st.radio("5. ¿Con qué frecuencia has sentido que las cosas estaban saliendo bien para ti?", options)
        q6 = st.radio("6. ¿Con qué frecuencia has sentido que no podías lidiar con todas las cosas que tenías que hacer?", options)
        q7 = st.radio("7. ¿Con qué frecuencia has sentido que podías controlar las irritaciones en tu vida?", options)
        q8 = st.radio("8. ¿Con qué frecuencia has sentido que tenías el control sobre las cosas?", options)
        q9 = st.radio("9. ¿Con qué frecuencia te has sentido enojado/a por cosas fuera de tu control?", options)
        q10 = st.radio("10. ¿Con qué frecuencia has sentido que las dificultades se acumulaban tanto que no podías superarlas?", options)

        # Botón para calcular el puntaje
        if st.button("Calcular Puntuación"):
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

            st.write("### Tu puntuación total es:", total_score)
            if total_score <= 13:
                st.success("Estrés bajo. ¡Excelente trabajo en mantener el equilibrio!")
            elif 14 <= total_score <= 26:
                st.warning("Estrés moderado. Podrías beneficiarte de técnicas de manejo del estrés.")
            else:
                st.error("Estrés alto. Considera buscar apoyo o implementar estrategias de relajación.")

    elif submenu == "Calidad del Sueño":
        cuestionario_calidad_sueno()  # Llama la función de Calidad del Sueño
   
    elif submenu == "Nivel de Actividad Física":
      cuestionario_ipaq()  # Llama la función para Nivel de Actividad Física


# Función para el cuestionario de Calidad del Sueño
def cuestionario_calidad_sueno():
    st.title("Evaluación de la Calidad del Sueño - Índice de Pittsburgh")
    st.write("Responde las siguientes preguntas sobre tus hábitos de sueño durante el último mes:")

    hora_acostarse = st.text_input("1. ¿A qué hora te acuestas normalmente?")
    tiempo_dormirse = st.selectbox(
        "2. ¿Cuánto tiempo tardas normalmente en dormirte?",
        ["Menos de 15 minutos", "16-30 minutos", "31-60 minutos", "Más de 60 minutos"]
    )
    hora_levantarse = st.text_input("3. ¿A qué hora te levantas normalmente?")
    horas_dormidas = st.slider("4. ¿Cuántas horas calculas que duermes habitualmente por noche?", 0, 12, 7)

    st.write("5. Durante el último mes, ¿con qué frecuencia has experimentado los siguientes problemas?")
    problemas_dormir = {
        "No poder conciliar el sueño en 30 minutos": st.radio(
            "a. No poder conciliar el sueño en los primeros 30 minutos:",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        ),
        "Despertarte durante la noche o muy temprano": st.radio(
            "b. Despertarte durante la noche o muy temprano:",
            ["Ninguna vez", "Menos de una vez a la semana", "Una o dos veces a la semana", "Tres o más veces a la semana"]
        )
    }

    calidad_sueno = st.radio(
        "6. ¿Cómo calificarías la calidad de tu sueño?",
        ["Muy buena", "Bastante buena", "Bastante mala", "Muy mala"]
    )

    if st.button("Calcular Puntuación"):
        puntuacion = {"Ninguna vez": 0, "Menos de una vez a la semana": 1, "Una o dos veces a la semana": 2, "Tres o más veces a la semana": 3}
        calidad_puntuacion = {"Muy buena": 0, "Bastante buena": 1, "Bastante mala": 2, "Muy mala": 3}

        total_puntuacion = sum(puntuacion[respuesta] for respuesta in problemas_dormir.values())
        total_puntuacion += calidad_puntuacion[calidad_sueno]

        st.write(f"### Tu puntuación total es: {total_puntuacion}")
        if total_puntuacion <= 5:
            st.success("Buena calidad de sueño.")
        elif 6 <= total_puntuacion <= 10:
            st.warning("Calidad de sueño moderada.")
        else:
            st.error("Mala calidad de sueño. Considera consultar a un especialista.")
   
elif submenu == "Mini-ECCA v.2":
        cuestionario_mini_ecca()  # Llama a la función Mini-ECCA v.2
        
