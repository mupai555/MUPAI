import streamlit as st
import sqlite3
import bcrypt
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Configuración inicial de la página
st.set_page_config(
    page_title="MUPAI - Entrenamiento Digital",
    page_icon="🤖",
    layout="wide",
)

# Configuración de la base de datos
def init_db():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                full_name TEXT,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                phone TEXT,
                birth_date TEXT,
                password TEXT,
                authorized INTEGER DEFAULT 0,
                role TEXT DEFAULT 'user',
                terms_accepted INTEGER DEFAULT 0,
                date_added TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_activity (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                action TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        conn.commit()

# Función para calcular el FFMI
def calcular_ffmi(peso, altura, porcentaje_grasa):
    masa_magra = peso * (1 - porcentaje_grasa / 100)
    return round(masa_magra / (altura ** 2), 2)

# Función para clasificar el FFMI
def clasificar_ffmi(ffmi):
    if ffmi < 18:
        return "Principiante"
    elif 18 <= ffmi < 20:
        return "Intermedio"
    elif 20 <= ffmi < 23.5:
        return "Avanzado"
    else:
        return "Élite"

# Función para calcular déficit óptimo
def calcular_deficit_optimo(porcentaje_grasa_actual, porcentaje_grasa_objetivo, semanas_restantes, peso):
    if porcentaje_grasa_actual <= porcentaje_grasa_objetivo:
        return 0  # Ya está en el objetivo
    deficit_calorico_semanal = ((porcentaje_grasa_actual - porcentaje_grasa_objetivo) * peso * 7700) / semanas_restantes
    deficit_diario = deficit_calorico_semanal / 7
    return round(deficit_diario, 2)

# Función para determinar balance energético
def calcular_balance_energetico(deficit_diario, calorias_mantenimiento):
    if deficit_diario == 0:
        return "Mantenimiento"
    elif deficit_diario > 0:
        return f"DÉFICIT: {calorias_mantenimiento - deficit_diario} kcal/día"
    else:
        return f"SUPERÁVIT: {calorias_mantenimiento + abs(deficit_diario)} kcal/día"

# Función para calcular volumen por grupo muscular
def calcular_volumen_por_categoria(categoria, nivel_entrenamiento):
    prioridades = {
        "Men’s Physique": {
            "Pectorales": "Alta",
            "Espalda": "Alta",
            "Bíceps": "Media",
            "Tríceps": "Media",
            "Cuádriceps": "Baja",
            "Pantorrillas": "Baja"
        },
        "Wellness": {
            "Cuádriceps": "Alta",
            "Glúteos": "Alta",
            "Isquiotibiales": "Media",
            "Pantorrillas": "Media",
            "Espalda": "Media",
            "Pectorales": "Baja"
        }
    }
    base_volumen = {"Alta": 18, "Media": 14, "Baja": 10}
    ajuste_nivel = 1.2 if nivel_entrenamiento == "Avanzado" else 1.0
    volumen_por_grupo = {grupo: round(base_volumen[prioridad] * ajuste_nivel, 1) for grupo, prioridad in prioridades[categoria].items()}
    return volumen_por_grupo

# Función para desplegar el cuestionario completo en Perfil MUPAI
def perfil_mupai():
    st.title("Perfil MUPAI - Fitness, Performance, and Health")
    st.write("""
    Este cuestionario está diseñado para personalizar tu entrenamiento, nutrición y progresión basándonos en tu estilo de vida, objetivos y estado físico actual. Por favor, completa las siguientes preguntas.
    """)

    # Sección 1: Datos Generales
    st.header("1. Datos Generales del Usuario")
    genero = st.selectbox("¿Cuál es tu género?", ["Masculino", "Femenino"])
    edad = st.number_input("¿Cuál es tu edad?", min_value=10, max_value=80, step=1)
    altura = st.number_input("¿Cuál es tu altura en metros?", min_value=1.0, max_value=2.5, step=0.01)
    peso = st.number_input("¿Cuál es tu peso actual en kilogramos?", min_value=30.0, max_value=200.0, step=0.1)
    porcentaje_grasa = st.number_input("Introduce tu porcentaje de grasa corporal (%)", min_value=5.0, max_value=50.0, step=0.1)

    # Cálculo del FFMI y clasificación
    if altura > 0 and peso > 0:
        ffmi = calcular_ffmi(peso, altura, porcentaje_grasa)
        clasificacion_ffmi = clasificar_ffmi(ffmi)
        st.subheader("Resultados del FFMI")
        st.write(f"Tu FFMI es: {ffmi}")
        st.write(f"Clasificación del Nivel de Entrenamiento (según FFMI): {clasificacion_ffmi}")

    # Sección 2: Objetivos
    st.header("2. Objetivos del Entrenamiento")
    objetivo_principal = st.selectbox("¿Cuál es tu objetivo principal de entrenamiento?", [
        "Hipertrofia General", "Salud General", "Competencia en Fisicoculturismo"
    ])
    categoria = st.selectbox("¿En qué categoría competirías?", ["Men’s Physique", "Wellness"])

    # Sección 3: Balance Energético
    st.header("3. Balance Energético")
    porcentaje_objetivo = st.number_input("Porcentaje de Grasa Objetivo (%)", min_value=3.0, max_value=50.0, step=0.1)
    semanas_restantes = st.number_input("Semanas Restantes para Competencia", min_value=1, max_value=52, step=1)
    calorias_mantenimiento = st.number_input("Calorías de Mantenimiento (kcal)", min_value=1000, max_value=5000, step=100)

    deficit_diario = calcular_deficit_optimo(porcentaje_grasa, porcentaje_objetivo, semanas_restantes, peso)
    balance_energetico = calcular_balance_energetico(deficit_diario, calorias_mantenimiento)
    st.write(f"Déficit Diario Recomendado: {deficit_diario} kcal/día")
    st.write(f"Recomendación: {balance_energetico}")

    # Sección 4: Volumen por Grupo Muscular
    st.header("4. Volumen Óptimo por Grupo Muscular")
    volumen_grupos = calcular_volumen_por_categoria(categoria, clasificacion_ffmi)
    for grupo, volumen in volumen_grupos.items():
        st.write(f"{grupo}: {volumen} series/semana")

    # Visualización de resultados con gráficos
    st.subheader("Visualización del Volumen por Grupo Muscular")
    fig, ax = plt.subplots()
    ax.bar(volumen_grupos.keys(), volumen_grupos.values(), color='skyblue')
    ax.set_ylabel("Series/Semana")
    ax.set_title("Distribución del Volumen por Grupo Muscular")
    st.pyplot(fig)

    st.success("Cuestionario completado. Revisa las recomendaciones finales.")

# Sección Registro
def registro():
    with st.expander("Registro de Usuario"):
        st.write("Por favor completa los siguientes campos para registrarte:")
        full_name = st.text_input("Nombre Completo")
        username = st.text_input("Usuario")
        email = st.text_input("Correo Electrónico")
        phone = st.text_input("Teléfono (opcional)")
        birth_date = st.date_input("Fecha de Nacimiento", min_value=datetime(1900, 1, 1), max_value=datetime.today())
        password = st.text_input("Contraseña", type="password")
        terms_accepted = st.checkbox("Acepto los Términos y Condiciones")
        if st.button("Registrar"):
            if not terms_accepted:
                st.error("Debes aceptar los Términos y Condiciones para registrarte.")
            elif register_user(full_name, username, email, phone, birth_date, password, terms_accepted):
                st.success("Usuario registrado con éxito. Espera autorización.")
            else:
                st.error("El usuario o correo ya existe.")

# Sección Inicio
def inicio():
    st.image("LOGO.png", use_container_width=True)
    st.title("Bienvenido a MUPAI")
    st.header("Misión")
    st.write("""
    Hacer accesible el entrenamiento basado en ciencia, proporcionando planes completamente personalizados a través de herramientas digitales respaldadas por inteligencia artificial, datos precisos y la investigación más actualizada en ciencias del ejercicio. Nos enfocamos en promover el desarrollo integral de nuestros usuarios y su bienestar físico y mental.
    """)

# Main function
def main():
    init_db()

    st.sidebar.title("Navegación")
    menu = ["Inicio", "Perfil MUPAI/Salud y Rendimiento", "Registro"]
    choice = st.sidebar.radio("Selecciona una opción:", menu)

    if choice == "Inicio":
        inicio()
    elif choice == "Perfil MUPAI/Salud y Rendimiento":
        perfil_mupai()
    elif choice == "Registro":
        registro()

if __name__ == "__main__":
    main()
