# MUPAI - Sistema de Cuestionarios Nutricionales

Sistema completo de cuestionarios científicos para evaluación nutricional y composición corporal, diseñado para personalizar planes de nutrición de forma precisa y automatizada.

## 🚀 Características

- **Cuestionario de Balance Energético Avanzado**: Evaluación científica completa con cálculos automáticos de macronutrientes
- **Cuestionario de Preferencias Alimentarias**: Análisis detallado de gustos, antojos y restricciones
- **Interfaz Intuitiva**: Navegación por menú lateral con Streamlit
- **Envío Automático por Email**: Resultados enviados automáticamente al equipo de nutrición
- **Seguridad**: Credenciales manejadas via secrets/variables de entorno
- **Listo para Producción**: Configuración profesional y escalable

## 📋 Cuestionarios Incluidos

### 1. ⚡ Cuestionario de Balance Energético
- Evaluación de composición corporal con ajustes automáticos por método
- Cálculo de gasto energético total (GER, GEAF, GEE)
- Evaluación de calidad de sueño (Pittsburgh abreviado)
- Medición de estrés percibido (PSS-4)
- Factor de Recuperación Inteligente (FRI)
- Determinación automática de objetivos corporales
- Asignación inteligente de macronutrientes

### 2. 🍽️ Preferencias y Antojos Alimentarios
- Selección detallada de alimentos preferidos por grupos
- Análisis de antojos alimentarios y disparadores
- Identificación de restricciones y alergias
- Evaluación de preferencias dietéticas
- Personalización del plan nutricional

## 🛠️ Instalación y Configuración

### 1. Requisitos
```bash
pip install -r requirements.txt
```

### 2. Configuración de Email (IMPORTANTE)
Crea el archivo `.streamlit/secrets.toml` con tus credenciales SMTP:

```toml
# Configuración SMTP para Zoho Mail
smtp_server = "smtp.zoho.com"
smtp_port = 587

# Credenciales de email
email_usuario = "tu_email@tudominio.com"
email_password = "tu_contraseña_de_aplicación"

# Email de destino
email_destino = "administracion@muscleupgym.fitness"
```

### 3. Configuración de Seguridad
- Usa contraseñas de aplicación específicas (no tu contraseña principal)
- Habilita autenticación de dos factores en tu cuenta de email
- Asegúrate de que `.streamlit/secrets.toml` esté en tu `.gitignore`

### 4. Ejecutar la Aplicación
```bash
streamlit run app.py
```

## 🔧 Configuración para Producción

### Variables de Entorno
En producción, configura estas variables de entorno en lugar de usar secrets.toml:

```
SMTP_SERVER=smtp.zoho.com
SMTP_PORT=587
EMAIL_USUARIO=tu_email@tudominio.com
EMAIL_PASSWORD=tu_contraseña_de_aplicación
EMAIL_DESTINO=administracion@muscleupgym.fitness
```

### Deployment en Streamlit Cloud
1. Sube tu código a GitHub (sin secrets.toml)
2. En Streamlit Cloud, configura los secrets en la sección "Secrets"
3. Copia el contenido del archivo secrets_template.toml y personaliza

### Deployment en otras plataformas
- **Heroku**: Configura las variables en Config Vars
- **Google Cloud Run**: Usa Secret Manager
- **AWS**: Usa AWS Secrets Manager
- **Azure**: Usa Azure Key Vault

## 📊 Funcionalidades Científicas

### Cálculos de Balance Energético
- **GER**: Gasto Energético en Reposo (Mifflin-St Jeor & Katch-McArdle)
- **GEAF**: Gasto Energético por Actividad Física
- **GEE**: Gasto Energético por Ejercicio
- **FRI**: Factor de Recuperación Inteligente

### Evaluaciones Validadas
- **Composición Corporal**: Ajustes automáticos por método de medición
- **Calidad de Sueño**: Escala Pittsburgh abreviada
- **Estrés Percibido**: Escala PSS-4
- **FFMI**: Índice de Masa Libre de Grasa

### Asignación de Macronutrientes
- Proteína: 1.8-2.6 g/kg según objetivo
- Grasas: 0.8-1.2 g/kg según objetivo
- Carbohidratos: Por diferencia energética

## 🔒 Seguridad y Privacidad

- Datos encriptados en tránsito
- Credenciales nunca expuestas en código
- Información confidencial y no compartida
- Cumple con mejores prácticas de seguridad

## 📁 Estructura del Proyecto

```
MUPAI/
├── app.py                      # Aplicación principal con navegación
├── newfile.py                  # Cuestionario de balance energético
├── cuestionario_preferencias.py # Cuestionario de preferencias
├── cuestionario_fbeo.py        # [OBSOLETO] Cuestionario anterior
├── requirements.txt            # Dependencias
├── secrets_template.toml       # Plantilla de configuración
├── .gitignore                  # Archivos excluidos
├── README.md                   # Este archivo
└── .streamlit/
    └── secrets.toml           # Configuración de secrets (no commitear)
```

## 🚨 Notas Importantes

1. **NO** commits el archivo `.streamlit/secrets.toml` con credenciales reales
2. Usa contraseñas de aplicación específicas para email
3. El archivo `cuestionario_fbeo.py` es obsoleto y será removido
4. Todos los cuestionarios envían automáticamente por email
5. Los resultados se muestran al usuario tras completar

## 🆕 Cambios en Esta Versión

- ✅ Eliminado cuestionario antiguo de balance energético
- ✅ Conservado cuestionario de preferencias alimentarias
- ✅ Agregado nuevo cuestionario avanzado de balance energético
- ✅ Implementada navegación por menú lateral
- ✅ Agregado envío automático por email
- ✅ Configuración segura de credenciales
- ✅ Sistema listo para producción

## 📞 Soporte

Para soporte técnico contactar al equipo MUPAI:
- Email: administracion@muscleupgym.fitness
- Sistema: MUPAI Questionnaire System v3.0

## 📜 Licencia

Sistema propietario - MUPAI Team. Todos los derechos reservados.