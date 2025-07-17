"""
Cuestionario de Preferencias y Antojos Alimentarios
====================================================

Sistema de evaluación de preferencias alimentarias y antojos para personalización nutricional.
"""

import streamlit as st
import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def mostrar_cuestionario_preferencias():
    """Función principal del cuestionario de preferencias y antojos alimentarios"""
    
    # CSS específico para el cuestionario
    st.markdown("""
    <style>
        .pref-header {
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 50%, #FFB5B5 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .pref-section {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 5px solid #FF6B6B;
            margin: 1rem 0;
        }
        .pref-results {
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 50%, #FFB5B5 100%);
            padding: 2rem;
            border-radius: 15px;
            color: #fff;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="pref-header">
        <h2>🍽️ Cuestionario de Preferencias y Antojos Alimentarios</h2>
        <p style="font-size: 1.2rem; margin: 0; color: #fff;">Personalización de tu plan nutricional</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Formulario principal
    with st.form("preferencias_form"):
        
        # Datos personales básicos
        st.markdown('<div class="pref-section">', unsafe_allow_html=True)
        st.header("📋 Datos Personales")
        
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre completo*")
            edad = st.number_input("Edad*", min_value=18, max_value=100, value=25)
        with col2:
            email = st.text_input("Correo electrónico*")
            telefono = st.text_input("Teléfono")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Selección alimentaria
        st.markdown('<div class="pref-section">', unsafe_allow_html=True)
        st.header("🍽️ Selección Alimentaria Personalizada")
        st.write("Marca todos los alimentos que consumes con facilidad o disfrutas")
        
        # Grupo 1: Proteína animal con grasa
        with st.expander("🥩 GRUPO 1: Proteína Animal con Más Contenido Graso", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                huevos_embutidos = st.multiselect(
                    "🍳 Huevos y embutidos",
                    ["Huevo entero", "Chorizo", "Salchicha", "Longaniza", "Tocino", "Jamón serrano"]
                )
                carnes_grasas = st.multiselect(
                    "🥩 Carnes grasas",
                    ["Costilla de res", "Costilla de cerdo", "Ribeye", "T-bone", "Arrachera", "Molida 80/20"]
                )
            with col2:
                quesos_grasos = st.multiselect(
                    "🧀 Quesos grasos",
                    ["Manchego", "Doble crema", "Oaxaca", "Gouda", "Cheddar"]
                )
                lacteos_enteros = st.multiselect(
                    "🥛 Lácteos enteros",
                    ["Leche entera", "Yogur entero", "Crema", "Yogur griego entero"]
                )
        
        # Grupo 2: Proteína magra
        with st.expander("🍗 GRUPO 2: Proteína Animal Magra"):
            col1, col2 = st.columns(2)
            with col1:
                carnes_magras = st.multiselect(
                    "🍗 Carnes magras",
                    ["Pechuga de pollo", "Filete de res", "Lomo de cerdo", "Atún en agua"]
                )
            with col2:
                pescados_blancos = st.multiselect(
                    "🐟 Pescados blancos",
                    ["Tilapia", "Basa", "Huachinango", "Robalo"]
                )
        
        # Grupo 3: Grasas saludables
        with st.expander("🥑 GRUPO 3: Grasas Saludables"):
            grasas_naturales = st.multiselect(
                "🥑 Grasas naturales",
                ["Aguacate", "Aceitunas", "Coco", "Mantequilla de almendra"]
            )
            frutos_secos = st.multiselect(
                "🌰 Frutos secos",
                ["Almendras", "Nueces", "Pistaches", "Cacahuates", "Semillas de chía"]
            )
        
        # Grupo 4: Carbohidratos
        with st.expander("🍞 GRUPO 4: Carbohidratos"):
            cereales = st.multiselect(
                "🌾 Cereales",
                ["Avena", "Arroz", "Quinoa", "Pan integral", "Pasta"]
            )
            tuberculos = st.multiselect(
                "🥔 Tubérculos",
                ["Papa", "Camote", "Yuca", "Plátano"]
            )
        
        # Grupo 5 y 6: Vegetales y Frutas
        with st.expander("🥬 GRUPO 5: Vegetales"):
            vegetales = st.multiselect(
                "Selecciona los vegetales",
                ["Espinaca", "Brócoli", "Lechuga", "Tomate", "Zanahoria", "Pepino", "Apio", "Pimientos", "Cebolla", "Calabacín"]
            )
        
        with st.expander("🍎 GRUPO 6: Frutas"):
            frutas = st.multiselect(
                "Selecciona las frutas",
                ["Manzana", "Plátano", "Naranja", "Fresas", "Mango", "Piña", "Uvas", "Melón", "Sandía", "Kiwi"]
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Antojos alimentarios
        st.markdown('<div class="pref-section">', unsafe_allow_html=True)
        st.header("😋 Antojos Alimentarios")
        
        col1, col2 = st.columns(2)
        with col1:
            antojos_dulces = st.multiselect(
                "🍫 Dulces/postres que más antojas",
                ["Chocolate", "Galletas", "Pastel", "Helado", "Pan dulce", "Caramelos", "Flan", "Gelatina"]
            )
        with col2:
            antojos_salados = st.multiselect(
                "🧂 Salados/snacks que más antojas",
                ["Papas fritas", "Palomitas", "Nachos", "Pretzels", "Chicharrones", "Doritos", "Cheetos"]
            )
        
        # Frecuencia de antojos
        st.subheader("📈 Frecuencia de Antojos")
        frecuencia_antojos = st.select_slider(
            "¿Con qué frecuencia tienes antojos?",
            options=["Nunca", "Raramente", "Ocasionalmente", "Frecuentemente", "Muy frecuentemente"],
            value="Ocasionalmente"
        )
        
        # Momento del día de antojos
        momento_antojos = st.multiselect(
            "¿En qué momento del día tienes más antojos?",
            ["Mañana", "Media mañana", "Tarde", "Noche", "Madrugada", "Después de comer"]
        )
        
        # Disparadores de antojos
        disparadores = st.multiselect(
            "¿Qué situaciones disparan tus antojos?",
            ["Estrés", "Aburrimiento", "Tristeza", "Ansiedad", "Celebraciones", "Ver comida", "Olores", "Hambre física"]
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Restricciones alimentarias
        st.markdown('<div class="pref-section">', unsafe_allow_html=True)
        st.header("🚫 Restricciones Alimentarias")
        
        col1, col2 = st.columns(2)
        with col1:
            alergias = st.multiselect(
                "Alergias alimentarias",
                ["Nueces", "Gluten", "Lactosa", "Mariscos", "Huevos", "Soja", "Pescado", "Ninguna"]
            )
        with col2:
            intolerancias = st.multiselect(
                "Intolerancias alimentarias",
                ["Lactosa", "Gluten", "Fructosa", "Histamina", "Ninguna"]
            )
        
        # Preferencias dietéticas
        tipo_dieta = st.selectbox(
            "¿Sigues algún tipo de dieta específica?",
            ["Ninguna", "Vegetariana", "Vegana", "Keto", "Paleo", "Mediterránea", "Baja en carbohidratos", "Otra"]
        )
        
        if tipo_dieta == "Otra":
            dieta_especifica = st.text_input("Especifica tu dieta:")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Comentarios adicionales
        st.markdown('<div class="pref-section">', unsafe_allow_html=True)
        st.header("💭 Comentarios Adicionales")
        comentarios = st.text_area(
            "¿Hay algo más que quieras compartir sobre tus preferencias alimentarias?",
            placeholder="Escribe aquí cualquier información adicional que consideres importante..."
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Botón de envío
        submitted = st.form_submit_button("📨 Enviar Cuestionario de Preferencias", type="primary", use_container_width=True)
        
        if submitted:
            # Validación
            if not nombre or not email:
                st.error("❌ Por favor, completa todos los campos obligatorios (nombre y email)")
                return
            
            # Recopilar todos los datos
            datos_preferencias = {
                "timestamp": datetime.now().isoformat(),
                "datos_personales": {
                    "nombre": nombre,
                    "edad": edad,
                    "email": email,
                    "telefono": telefono
                },
                "seleccion_alimentaria": {
                    "huevos_embutidos": huevos_embutidos,
                    "carnes_grasas": carnes_grasas,
                    "quesos_grasos": quesos_grasos,
                    "lacteos_enteros": lacteos_enteros,
                    "carnes_magras": carnes_magras,
                    "pescados_blancos": pescados_blancos,
                    "grasas_naturales": grasas_naturales,
                    "frutos_secos": frutos_secos,
                    "cereales": cereales,
                    "tuberculos": tuberculos,
                    "vegetales": vegetales,
                    "frutas": frutas
                },
                "antojos": {
                    "antojos_dulces": antojos_dulces,
                    "antojos_salados": antojos_salados,
                    "frecuencia_antojos": frecuencia_antojos,
                    "momento_antojos": momento_antojos,
                    "disparadores": disparadores
                },
                "restricciones": {
                    "alergias": alergias,
                    "intolerancias": intolerancias,
                    "tipo_dieta": tipo_dieta,
                    "dieta_especifica": dieta_especifica if tipo_dieta == "Otra" else None
                },
                "comentarios": comentarios
            }
            
            # Enviar por email
            if enviar_email_preferencias(datos_preferencias):
                st.success("✅ ¡Cuestionario enviado exitosamente!")
                st.markdown(f"""
                <div class="pref-results">
                    <h3>📧 Cuestionario Enviado</h3>
                    <p><strong>Nombre:</strong> {nombre}</p>
                    <p><strong>Email:</strong> {email}</p>
                    <p><strong>Fecha:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>Tu cuestionario de preferencias alimentarias ha sido enviado al equipo de nutrición. 
                    Recibirás una respuesta personalizada en las próximas 24-48 horas.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("❌ Error al enviar el cuestionario. Por favor, intenta de nuevo.")


def enviar_email_preferencias(datos):
    """Envía el cuestionario de preferencias por email"""
    try:
        # Configuración SMTP desde secrets
        smtp_server = st.secrets.get("smtp_server", "smtp.zoho.com")
        smtp_port = st.secrets.get("smtp_port", 587)
        email_usuario = st.secrets.get("email_usuario", "")
        email_password = st.secrets.get("email_password", "")
        email_destino = st.secrets.get("email_destino", "administracion@muscleupgym.fitness")
        
        if not email_usuario or not email_password:
            st.error("❌ Configuración de email no disponible")
            return False
        
        # Crear mensaje
        mensaje = MIMEMultipart()
        mensaje["From"] = email_usuario
        mensaje["To"] = email_destino
        mensaje["Subject"] = f"MUPAI - Cuestionario de Preferencias Alimentarias - {datos['datos_personales']['nombre']}"
        
        # Cuerpo del mensaje
        cuerpo = f"""
CUESTIONARIO DE PREFERENCIAS Y ANTOJOS ALIMENTARIOS
================================================

📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

👤 DATOS PERSONALES:
- Nombre: {datos['datos_personales']['nombre']}
- Edad: {datos['datos_personales']['edad']} años
- Email: {datos['datos_personales']['email']}
- Teléfono: {datos['datos_personales']['telefono']}

🍽️ SELECCIÓN ALIMENTARIA:

🥩 Proteína Animal con Grasa:
- Huevos y embutidos: {', '.join(datos['seleccion_alimentaria']['huevos_embutidos']) if datos['seleccion_alimentaria']['huevos_embutidos'] else 'Ninguno'}
- Carnes grasas: {', '.join(datos['seleccion_alimentaria']['carnes_grasas']) if datos['seleccion_alimentaria']['carnes_grasas'] else 'Ninguno'}
- Quesos grasos: {', '.join(datos['seleccion_alimentaria']['quesos_grasos']) if datos['seleccion_alimentaria']['quesos_grasos'] else 'Ninguno'}
- Lácteos enteros: {', '.join(datos['seleccion_alimentaria']['lacteos_enteros']) if datos['seleccion_alimentaria']['lacteos_enteros'] else 'Ninguno'}

🍗 Proteína Animal Magra:
- Carnes magras: {', '.join(datos['seleccion_alimentaria']['carnes_magras']) if datos['seleccion_alimentaria']['carnes_magras'] else 'Ninguno'}
- Pescados blancos: {', '.join(datos['seleccion_alimentaria']['pescados_blancos']) if datos['seleccion_alimentaria']['pescados_blancos'] else 'Ninguno'}

🥑 Grasas Saludables:
- Grasas naturales: {', '.join(datos['seleccion_alimentaria']['grasas_naturales']) if datos['seleccion_alimentaria']['grasas_naturales'] else 'Ninguno'}
- Frutos secos: {', '.join(datos['seleccion_alimentaria']['frutos_secos']) if datos['seleccion_alimentaria']['frutos_secos'] else 'Ninguno'}

🍞 Carbohidratos:
- Cereales: {', '.join(datos['seleccion_alimentaria']['cereales']) if datos['seleccion_alimentaria']['cereales'] else 'Ninguno'}
- Tubérculos: {', '.join(datos['seleccion_alimentaria']['tuberculos']) if datos['seleccion_alimentaria']['tuberculos'] else 'Ninguno'}

🥬 Vegetales: {', '.join(datos['seleccion_alimentaria']['vegetales']) if datos['seleccion_alimentaria']['vegetales'] else 'Ninguno'}

🍎 Frutas: {', '.join(datos['seleccion_alimentaria']['frutas']) if datos['seleccion_alimentaria']['frutas'] else 'Ninguno'}

😋 ANTOJOS ALIMENTARIOS:
- Antojos dulces: {', '.join(datos['antojos']['antojos_dulces']) if datos['antojos']['antojos_dulces'] else 'Ninguno'}
- Antojos salados: {', '.join(datos['antojos']['antojos_salados']) if datos['antojos']['antojos_salados'] else 'Ninguno'}
- Frecuencia: {datos['antojos']['frecuencia_antojos']}
- Momento del día: {', '.join(datos['antojos']['momento_antojos']) if datos['antojos']['momento_antojos'] else 'No especificado'}
- Disparadores: {', '.join(datos['antojos']['disparadores']) if datos['antojos']['disparadores'] else 'No especificado'}

🚫 RESTRICCIONES ALIMENTARIAS:
- Alergias: {', '.join(datos['restricciones']['alergias']) if datos['restricciones']['alergias'] else 'Ninguna'}
- Intolerancias: {', '.join(datos['restricciones']['intolerancias']) if datos['restricciones']['intolerancias'] else 'Ninguna'}
- Tipo de dieta: {datos['restricciones']['tipo_dieta']}
{f"- Dieta específica: {datos['restricciones']['dieta_especifica']}" if datos['restricciones']['dieta_especifica'] else ''}

💭 COMENTARIOS ADICIONALES:
{datos['comentarios'] if datos['comentarios'] else 'Sin comentarios adicionales'}

---
Este cuestionario fue enviado automáticamente desde el sistema MUPAI.
"""
        
        mensaje.attach(MIMEText(cuerpo, "plain"))
        
        # Enviar email
        with smtplib.SMTP(smtp_server, smtp_port) as servidor:
            servidor.starttls()
            servidor.login(email_usuario, email_password)
            servidor.send_message(mensaje)
        
        return True
        
    except Exception as e:
        st.error(f"Error al enviar email: {str(e)}")
        return False