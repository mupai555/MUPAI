import streamlit as st
import pandas as pd
import os
import uuid

# Ruta del archivo donde se guardarán las respuestas
archivo_csv = "respuestas.csv"

# Crear un identificador único para el usuario
if "user_id" not in st.session_state:
    st.session_state["user_id"] = str(uuid.uuid4())

# Guardar el estado del cuestionario actual
if "cuestionario_actual" not in st.session_state:
    st.session_state["cuestionario_actual"] = 1

# Función para guardar respuestas
def guardar_respuestas(datos):
    datos["UserID"] = st.session_state["user_id"]  # Añadir el identificador del usuario
    if os.path.exists(archivo_csv):
        df = pd.read_csv(archivo_csv)
        df = pd.concat([df, pd.DataFrame([datos])], ignore_index=True)
    else:
        df = pd.DataFrame([datos])
    df.to_csv(archivo_csv, index=False)

# Funciones de los cuestionarios
def cuestionario_calidad_sueno():
    st.title("Cuestionario 1: Calidad del Sueño")
    hora_acostarse = st.text_input("1. ¿A qué hora te acuestas normalmente?")
    tiempo_dormirse = st.slider("2. ¿Cuánto tiempo tardas normalmente en dormirte (minutos)?", 0, 120, 15)
    hora_levantarse = st.text_input("3. ¿A qué hora te levantas normalmente?")
    horas_dormidas = st.slider("4. ¿Cuántas horas calculas que duermes habitualmente por noche?", 0, 12, 7)

    calidad_sueno = st.radio(
        "5. ¿Cómo calificarías la calidad de tu sueño durante el último mes?",
        ["Muy buena", "Bastante buena", "Bastante mala", "Muy mala"]
    )

    if st.button("Enviar Respuestas"):
        respuestas = {
            "Cuestionario": "Calidad del Sueño",
            "Hora de Acostarse": hora_acostarse,
            "Tiempo para Dormirse": tiempo_dormirse,
            "Hora de Levantarse": hora_levantarse,
            "Horas Dormidas": horas_dormidas,
            "Calidad del Sueño": calidad_sueno,
        }
        guardar_respuestas(respuestas)
        st.success("¡Tus respuestas han sido guardadas!")
        avanzar_cuestionario()

def cuestionario_actividad_fisica():
    st.title("Cuestionario 2: Actividad Física")
    dias_vigorosa = st.number_input("1. Días de actividad física vigorosa (últimos 7 días)", 0, 7, 0)
    minutos_vigorosa = st.number_input("2. Minutos diarios promedio de actividad vigorosa", 0, 120, 0)

    dias_moderada = st.number_input("3. Días de actividad física moderada (últimos 7 días)", 0, 7, 0)
    minutos_moderada = st.number_input("4. Minutos diarios promedio de actividad moderada", 0, 120, 0)

    dias_caminata = st.number_input("5. Días en que caminaste al menos 10 minutos seguidos", 0, 7, 0)
    minutos_caminata = st.number_input("6. Minutos diarios promedio caminando", 0, 120, 0)

    if st.button("Enviar Respuestas"):
        respuestas = {
            "Cuestionario": "Actividad Física",
            "Días Vigorosa": dias_vigorosa,
            "Minutos Vigorosa": minutos_vigorosa,
            "Días Moderada": dias_moderada,
            "Minutos Moderada": minutos_moderada,
            "Días Caminata": dias_caminata,
            "Minutos Caminata": minutos_caminata,
        }
        guardar_respuestas(respuestas)
        st.success("¡Tus respuestas han sido guardadas!")
        avanzar_cuestionario()

def cuestionario_habitos_alimenticios():
    st.title("Cuestionario 3: Hábitos Alimenticios")
    agua = st.radio("1. ¿Bebes al menos 1.5 litros de agua al día?", ["Nunca", "A veces", "Casi siempre", "Siempre"])
    frutas = st.radio("2. ¿Consumes frutas diariamente?", ["Nunca", "A veces", "Casi siempre", "Siempre"])
    verduras = st.radio("3. ¿Consumes verduras diariamente?", ["Nunca", "A veces", "Casi siempre", "Siempre"])

    alimentos_procesados = st.radio("4. ¿Consumes alimentos procesados más de 3 veces por semana?", ["Nunca", "A veces", "Casi siempre", "Siempre"])
    bebidas_azucaradas = st.radio("5. ¿Consumes bebidas azucaradas frecuentemente?", ["Nunca", "A veces", "Casi siempre", "Siempre"])

    if st.button("Enviar Respuestas"):
        respuestas = {
            "Cuestionario": "Hábitos Alimenticios",
            "Agua": agua,
            "Frutas": frutas,
            "Verduras": verduras,
            "Alimentos Procesados": alimentos_procesados,
            "Bebidas Azucaradas": bebidas_azucaradas,
        }
        guardar_respuestas(respuestas)
        st.success("¡Tus respuestas han sido guardadas!")
        avanzar_cuestionario()

# Control del flujo de cuestionarios
def avanzar_cuestionario():
    st.session_state["cuestionario_actual"] += 1

def mostrar_cuestionarios():
    if st.session_state["cuestionario_actual"] == 1:
        cuestionario_calidad_sueno()
    elif st.session_state["cuestionario_actual"] == 2:
        cuestionario_actividad_fisica()
    elif st.session_state["cuestionario_actual"] == 3:
        cuestionario_habitos_alimenticios()
    else:
        st.title("Gracias por completar los cuestionarios")
        st.write("Tus respuestas han sido registradas correctamente.")

# Menú principal
menu = st.sidebar.selectbox(
    "Menú",
    ["Inicio", "Sobre Mí", "Servicios", "Contacto", "Cuestionarios"]
)

# Contenido según la selección del menú
if menu == "Inicio":
    st.title("Bienvenido a MUPAI")
    st.image("LOGO.png", use_container_width=True)
    st.header("Misión")
    st.write(
        """
        Hacer accesible el entrenamiento basado en ciencia, proporcionando planes completamente personalizados 
        a través de herramientas digitales respaldadas por inteligencia artificial, datos precisos y la investigación más actualizada.
        """
    )
    st.header("Visión")
    st.write(
        """
        Convertirnos en uno de los máximos referentes a nivel global en entrenamiento digital personalizado, 
        aprovechando las nuevas tecnologías para hacer más accesible el fitness basado en ciencia.
        """
    )
    st.header("Política")
    st.write(
        """
        En **MUPAI**, nuestra política está fundamentada en el compromiso con la excelencia, la ética y el servicio centrado en el usuario.
        """
    )

elif menu == "Sobre Mí":
    st.title("Sobre Mí")
    st.write("""
    Soy Erick Francisco De Luna Hernández, un profesional apasionado por el fitness y las ciencias del ejercicio... 
    """)

elif menu == "Servicios":
    st.title("Servicios")
    st.write("""
    **MUPAI** ofrece una amplia gama de servicios personalizados basados en ciencia del ejercicio:
    - Planes de entrenamiento individualizados.
    - Programas de mejora física y mental.
    - Asesoría en nutrición deportiva.
    """)

elif menu == "Contacto":
    st.title("Contacto")
    st.write("""
    Para más información:
    - **Correo**: contacto@mupai.com
    - **Teléfono**: +52 866 258 05 94
    """)

elif menu == "Cuestionarios":
    mostrar_cuestionarios()
