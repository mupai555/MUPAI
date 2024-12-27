import streamlit as st

import matplotlib.pyplot as plt

import pandas as pd

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

# Función del Cuestionario de Hábitos Alimenticios
def cuestionario_habitos_alimenticios():
    st.title("Evaluación General de Hábitos Alimenticios")
    st.write("Responde las siguientes preguntas para evaluar tus hábitos alimenticios y recibir recomendaciones personalizadas.")

    # Sección 1: Consumo de Alimentos Frescos
    st.header("Sección 1: Consumo de Alimentos Frescos")
    agua = st.radio("1. ¿Bebes al menos 1.5 litros de agua natural diariamente?", ["Nunca", "Algunas veces", "Casi siempre", "Siempre"])
    verduras = st.radio("2. ¿Consumes al menos 200 g de verduras frescas diariamente?", ["Nunca", "Algunas veces", "Casi siempre", "Siempre"])
    frutas = st.radio("3. ¿Consumes al menos 200 g de frutas diariamente?", ["Nunca", "Algunas veces", "Casi siempre", "Siempre"])
    leguminosas = st.radio("4. ¿Consumes al menos 300 g de leguminosas semanalmente?", ["Nunca", "Algunas veces", "Casi siempre", "Siempre"])
    frutos_secos = st.radio("5. ¿Consumes al menos 30 g de frutos secos o medio aguacate diariamente?", ["Nunca", "Algunas veces", "Casi siempre", "Siempre"])

    # Sección 2: Carnes Frescas y Procesadas
    st.header("Sección 2: Carnes Frescas y Procesadas")
    carne_fresca = st.radio(
        "6. ¿Qué tipo de carne fresca consumes con mayor frecuencia durante la semana?",
        ["Pescado fresco", "Pollo fresco", "Carne roja fresca", "No consumo carne fresca"]
    )
    carnes_procesadas = st.radio(
        "7. ¿Con qué frecuencia consumes carnes procesadas (embutidos, curadas, enlatadas o fritas)?",
        ["Nunca", "Algunas veces", "Casi siempre", "Siempre"]
    )

    # Sección 3: Hábitos Alimenticios Generales
    st.header("Sección 3: Hábitos Alimenticios Generales")
    alimentos_fuera = st.radio("8. ¿Consumes alimentos no preparados en casa tres o más veces por semana?", ["Nunca", "Algunas veces", "Casi siempre", "Siempre"])
    bebidas_azucaradas = st.radio("9. ¿Cuántas veces consumes bebidas azucaradas semanalmente?", ["Nunca", "1–3 veces", "4–6 veces", "Diario"])
    postres_dulces = st.radio("10. ¿Consumes postres o dulces dos o más veces por semana?", ["Nunca", "Algunas veces", "Casi siempre", "Siempre"])
    alimentos_procesados = st.radio("11. ¿Consumes alimentos procesados dos o más veces por semana?", ["Nunca", "Algunas veces", "Casi siempre", "Siempre"])
    cereales = st.radio(
        "12. ¿Qué tipo de cereales consumes con mayor frecuencia?",
        ["Granos integrales", "Granos mínimamente procesados", "Granos procesados o ultraprocesados"]
    )

    # Sección 4: Consumo de Alcohol
    st.header("Sección 4: Consumo de Alcohol")
    alcohol = st.radio(
        "13. Si eres hombre, ¿consumes más de 2 bebidas alcohólicas al día? Si eres mujer, ¿más de 1 bebida al día?",
        ["Nunca", "Algunas veces", "Casi siempre", "Siempre"]
    )

    # Botón para calcular la puntuación
    if st.button("Calcular Puntuación"):
        puntuaciones = {"Nunca": 1, "Algunas veces": 2, "Casi siempre": 3, "Siempre": 4}
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

        st.write(f"### Tu puntuación total es: {puntuacion_total}")

        # Feedback en función del puntaje
        if puntuacion_total >= 30:
            st.success("✅ Tus hábitos alimenticios son saludables.")
            st.write("¡Felicidades! Tus elecciones alimenticias son excelentes. Sigue así para mantener una salud óptima.")
        elif 15 <= puntuacion_total < 30:
            st.warning("⚠️ Tus hábitos alimenticios son moderadamente saludables.")
            st.write("Tienes hábitos buenos, pero hay áreas donde puedes mejorar. Considera reducir el consumo de alimentos procesados y aumentar tu ingesta de alimentos frescos.")
        else:
            st.error("❌ Tus hábitos alimenticios necesitan mejoras significativas.")
            st.write("Es importante trabajar en tus hábitos alimenticios. Intenta incorporar más alimentos frescos y reducir el consumo de alimentos ultraprocesados. Podría ser útil consultar a un especialista.")
     

# Función principal: Evaluación del Potencial Genético Muscular
def evaluacion_potencial_genetico():
    st.title("Evaluación del Potencial Genético Muscular")
    st.write("Completa los siguientes campos para calcular tu índice de masa libre de grasa (FFMI) y evaluar tu nivel de desarrollo muscular.")

    # Entradas del usuario
    genero = st.radio("Género:", ["Hombre", "Mujer"])
    altura_m = st.number_input("Altura (en metros):", min_value=1.0, max_value=2.5, step=0.01)
    peso_kg = st.number_input("Peso (en kilogramos):", min_value=30.0, max_value=200.0, step=0.1)
    grasa_corporal = st.slider("Porcentaje de grasa corporal actual (%):", 5, 50, step=1)
    grasa_deseada = st.slider("Porcentaje de grasa corporal deseado (%):", 5, 50, step=1)

    # Circunferencias corporales
    st.subheader("Circunferencias Corporales (en cm)")
    brazo_cm = st.number_input("Brazo (flexionado):", min_value=20.0, max_value=60.0, step=0.1)
    pecho_cm = st.number_input("Pecho:", min_value=50.0, max_value=150.0, step=0.1)
    cintura_cm = st.number_input("Cintura:", min_value=40.0, max_value=150.0, step=0.1)
    cadera_cm = st.number_input("Cadera:", min_value=50.0, max_value=150.0, step=0.1)

    # Validación
    if grasa_deseada > grasa_corporal:
        st.error("El porcentaje de grasa corporal deseado no puede ser mayor al actual.")
        return

    # Botón para calcular
    if st.button("Calcular Potencial"):
        # Cálculo de masa magra actual
        masa_magra_actual = peso_kg * (1 - grasa_corporal / 100)

        # Cálculo de peso proyectado
        peso_proyectado = masa_magra_actual / (1 - grasa_deseada / 100)

        # FFMI actual y proyectado
        ffmi_actual = masa_magra_actual / (altura_m ** 2)
        ffmi_proyectado = peso_proyectado * (1 - grasa_deseada / 100) / (altura_m ** 2)

        # Proporciones corporales
        brazo_cintura = brazo_cm / cintura_cm
        pecho_cintura = pecho_cm / cintura_cm
        cintura_cadera = cintura_cm / cadera_cm

        # Clasificación por métricas individuales
        def clasificar_metricas(metric, genero, tipo):
            rangos = {
                "Hombre": {
                    "FFMI": [(0, 18, "Principiante"), (18, 21, "Intermedio"), (21, 25, "Avanzado"), (25, float('inf'), "Élite")],
                    "Brazo-Cintura": [(0, 0.35, "Principiante"), (0.35, 0.4, "Intermedio"), (0.4, 0.45, "Avanzado"), (0.45, float('inf'), "Élite")],
                    "Pecho-Cintura": [(0, 1.2, "Principiante"), (1.2, 1.4, "Intermedio"), (1.4, 1.6, "Avanzado"), (1.6, float('inf'), "Élite")],
                    "Cintura-Cadera": [(0.9, float('inf'), "Principiante"), (0.85, 0.9, "Intermedio"), (0.8, 0.85, "Avanzado"), (0, 0.8, "Élite")]
                },
                "Mujer": {
                    "FFMI": [(0, 15, "Principiante"), (15, 18, "Intermedio"), (18, 20, "Avanzado"), (20, float('inf'), "Élite")],
                    "Brazo-Cintura": [(0, 0.3, "Principiante"), (0.3, 0.35, "Intermedio"), (0.35, 0.4, "Avanzado"), (0.4, float('inf'), "Élite")],
                    "Pecho-Cintura": [(0, 1.0, "Principiante"), (1.0, 1.2, "Intermedio"), (1.2, 1.4, "Avanzado"), (1.4, float('inf'), "Élite")],
                    "Cintura-Cadera": [(0.85, float('inf'), "Principiante"), (0.8, 0.85, "Intermedio"), (0.75, 0.8, "Avanzado"), (0, 0.75, "Élite")]
                }
            }
            for rango in rangos[genero][tipo]:
                if rango[0] <= metric < rango[1]:
                    return rango[2]

        # Feedback de niveles
        nivel_ffmi_actual = clasificar_metricas(ffmi_actual, genero, "FFMI")
        nivel_brazo_cintura = clasificar_metricas(brazo_cintura, genero, "Brazo-Cintura")
        nivel_pecho_cintura = clasificar_metricas(pecho_cintura, genero, "Pecho-Cintura")
        nivel_cintura_cadera = clasificar_metricas(cintura_cadera, genero, "Cintura-Cadera")
        nivel_ffmi_proyectado = clasificar_metricas(ffmi_proyectado, genero, "FFMI")

        # Mostrar resultados
        st.write("### Resultados Actuales")
        st.write(f"- **Masa Magra Actual:** {masa_magra_actual:.2f} kg")
        st.write(f"- **FFMI Actual:** {ffmi_actual:.2f} ({nivel_ffmi_actual})")
        st.write(f"- **Relación Brazo/Cintura:** {brazo_cintura:.2f} ({nivel_brazo_cintura})")
        st.write(f"- **Relación Pecho/Cintura:** {pecho_cintura:.2f} ({nivel_pecho_cintura})")
        st.write(f"- **Relación Cintura/Cadera:** {cintura_cadera:.2f} ({nivel_cintura_cadera})")

        st.write("### Resultados Proyectados")
        st.write(f"- **Peso Proyectado:** {peso_proyectado:.2f} kg")
        st.write(f"- **FFMI Proyectado:** {ffmi_proyectado:.2f} ({nivel_ffmi_proyectado})")

        # Tablas de referencia
        st.write("### Tablas de Referencia")
        tabla_ffmi = pd.DataFrame({
            "Nivel de Entrenamiento": ["Principiante", "Intermedio", "Avanzado", "Élite"],
            "FFMI Hombres": ["<18", "18-21", "21-25", ">25"],
            "FFMI Mujeres": ["<15", "15-18", "18-20", ">20"]
        })
        st.table(tabla_ffmi)

        tabla_proporciones = pd.DataFrame({
            "Nivel de Entrenamiento": ["Principiante", "Intermedio", "Avanzado", "Élite"],
            "Brazo/Cintura Hombres": ["<0.35", "0.35-0.4", "0.4-0.45", ">0.45"],
            "Pecho/Cintura Hombres": ["<1.2", "1.2-1.4", "1.4-1.6", ">1.6"],
            "Cintura/Cadera Hombres": [">=0.9", "0.85-0.9", "0.8-0.85", "<0.8"],
            "Brazo/Cintura Mujeres": ["<0.3", "0.3-0.35", "0.35-0.4", ">0.4"],
            "Pecho/Cintura Mujeres": ["<1.0", "1.0-1.2", "1.2-1.4", ">1.4"],
            "Cintura/Cadera Mujeres": [">=0.85", "0.8-0.85", "0.75-0.8", "<0.75"]
        })
        st.table(tabla_proporciones)

        # Gráfica de comparación de FFMI
        fig, ax = plt.subplots()
        categorias = ["Actual", "Proyectado"]
        valores = [ffmi_actual, ffmi_proyectado]
        ax.bar(categorias, valores, color=['blue', 'green'])
        ax.set_ylabel("FFMI")
        ax.set_title("Comparación de FFMI Actual vs Proyectado")
        st.pyplot(fig)



        
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

    elif submenu == "Hábitos Alimenticios":
      cuestionario_habitos_alimenticios()  # Llama la función para Hábitos Alimenticios 

    elif submenu == "Potencial Genético Muscular":
        evaluacion_potencial_genetico() # Llama la función para Potencial Genético Muscular
        


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
