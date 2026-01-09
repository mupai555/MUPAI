# Separación de Reportes: Resumen vs Completo

## Introducción

Este documento explica la implementación de la separación entre el **REPORTE RESUMIDO** (para el usuario) y el **REPORTE COMPLETO** (uso interno) en el sistema de evaluaciones MUPAI.

## Estructura de Reportes

### REPORTE RESUMIDO (Usuario)

**Propósito**: Proporcionar información clara y útil al usuario sin exponer detalles técnicos internos.

**Contenido incluido**:

#### A) Datos del Cliente
- Nombre completo
- Edad
- Sexo
- Fecha de evaluación
- ⚠️ Teléfono y email NO se incluyen por defecto (privacidad)

#### B) Antropometría y Composición Corporal
1. Peso (kg)
2. Estatura (cm)
3. IMC (kg/m²)
4. % Grasa medida (%)
5. % Grasa corregida (DEXA/4C) (%)
6. Grasa visceral (valor o N/D)
7. % Masa muscular (valor o N/D)
8. Masa libre de grasa (kg)
9. Masa grasa (kg)
10. Edad metabólica (valor o N/D)
11. Categoría de grasa corporal

**Contenido EXCLUIDO** (seguridad):
- ❌ FFMI actual
- ❌ Clasificación FFMI
- ❌ FFMI máximo
- ❌ Referencias a potencial alcanzado o margen de crecimiento
- ❌ Fórmulas, umbrales, multiplicadores
- ❌ Explicaciones técnicas detalladas

### REPORTE COMPLETO (Interno)

**Propósito**: Análisis técnico completo para uso del profesional.

**Contenido incluido**:
- ✓ Todos los datos del reporte resumido
- ✓ FFMI (Fat-Free Mass Index)
- ✓ Clasificación de nivel de entrenamiento (Novato/Intermedio/Avanzado/Elite)
- ✓ Tablas de referencia completas
- ✓ Datos técnicos y metodología

## Uso en el Código

### Función Principal: `build_report_resumen(data)`

```python
from MUPAI.FBEO import build_report_resumen

# Preparar datos
datos_resumen = {
    'nombre_completo': 'Nombre del Cliente',
    'edad': 30,
    'sexo': 'Hombre',  # o 'Mujer'
    'fecha_evaluacion': '2025-12-14',
    'peso': 75.0,  # kg
    'estatura': 175.0,  # cm
    'imc': 24.5,  # calculado
    'grasa_medida': 15.0,  # %
    'grasa_corregida': 16.0,  # %
    'mlg': 63.0,  # kg
    'masa_grasa': 12.0,  # kg
    'nivel_grasa': 'Normal saludable',
    
    # Opcionales (None si no disponibles)
    'grasa_visceral': 8.5,  # o None
    'porcentaje_masa_muscular': 42.0,  # % o None
    'edad_metabolica': 28,  # o None
    
    # Control de privacidad
    'incluir_contacto': False,  # True para incluir tel/email
    'telefono': '1234567890',
    'email': 'cliente@email.com'
}

# Generar reporte resumido
reporte_usuario = build_report_resumen(datos_resumen)
print(reporte_usuario)
```

### Flujo en la Aplicación

```python
# 1. Calcular métricas
imc = peso / (estatura_m ** 2)
mlg = peso * (1 - grasa_corregida / 100)
masa_grasa = peso * (grasa_corregida / 100)
ffmi = mlg / (estatura_m ** 2)

# 2. Generar REPORTE RESUMIDO (para mostrar al usuario)
datos_resumen = { ... }  # sin FFMI
reporte_resumido = build_report_resumen(datos_resumen)

# 3. Generar REPORTE COMPLETO (para PDF interno)
resumen_completo = {
    "Nivel de grasa corporal": nivel_grasa,
    "FFMI": f"{ffmi:.2f} — {nivel_ffmi}",
    "MLG": f"{mlg:.1f} kg",
}
pdf_bytes = generar_pdf(usuario, resumen_completo, tabla_bf_txt, tabla_ffmi_txt)
```

## Manejo de Datos Faltantes

Campos que pueden no estar disponibles se muestran como "N/D":

```python
datos_resumen = {
    # ...
    'grasa_visceral': None,  # → "Grasa visceral: N/D"
    'porcentaje_masa_muscular': None,  # → "% Masa muscular: N/D"
    'edad_metabolica': None,  # → "Edad metabólica: N/D"
}
```

## Control de Privacidad

Por defecto, el teléfono y email NO se incluyen en el reporte resumido:

```python
# Por defecto (sin contacto)
datos_resumen = {
    'incluir_contacto': False,  # o simplemente omitir
    'telefono': '1234567890',
    'email': 'cliente@email.com'
}
# → Teléfono y email NO aparecen en el reporte

# Activar inclusión de contacto
datos_resumen = {
    'incluir_contacto': True,  # Activar explícitamente
    'telefono': '1234567890',
    'email': 'cliente@email.com'
}
# → Teléfono y email SÍ aparecen en el reporte
```

## Pruebas

### Ejecutar Tests

```bash
# Test básico con caso de Karina
python test_report_resumen.py

# Test de separación completa
python test_complete_separation.py
```

### Verificaciones Clave

✓ Reporte resumido NO contiene FFMI  
✓ Reporte resumido NO contiene clasificaciones técnicas  
✓ Reporte completo SÍ contiene FFMI  
✓ Ambos reportes coexisten correctamente  
✓ Datos faltantes se muestran como "N/D"  
✓ Contacto no se incluye por defecto  

## Ejemplo de Salida

### Reporte Resumido (Usuario)

```
============================================================
REPORTE RESUMIDO - EVALUACIÓN MUPAI
============================================================

DATOS DEL CLIENTE
------------------------------------------------------------
Nombre completo: San Juana Karina Martinez Sanchez
Edad: 41 años
Sexo: Mujer
Fecha de evaluación: 2025-12-10

ANTROPOMETRÍA, COMPOSICIÓN CORPORAL E ÍNDICES METABÓLICOS
------------------------------------------------------------
1. Peso: 65.0 kg
2. Estatura: 160 cm
3. IMC: 25.4 kg/m²
4. % Grasa medida: 28.0%
5. % Grasa corregida (DEXA/4C): 30.0%
6. Grasa visceral: N/D
7. % Masa muscular: N/D
8. Masa libre de grasa: 45.5 kg
9. Masa grasa: 19.5 kg
10. Edad metabólica: N/D
11. Categoría de grasa corporal: Sobrepeso

============================================================
NOTA: Este es un reporte resumido para el usuario.
El análisis técnico detallado es de uso interno.
============================================================
```

### Reporte Completo (Interno - PDF)

```
Datos personales:
  Nombre: San Juana Karina Martinez Sanchez
  Edad: 41 años
  Género: Mujer
  ...

Resumen de composición corporal:
  Nivel de grasa corporal: Sobrepeso
  FFMI: 17.77 — Intermedia
  MLG: 45.5 kg

Tabla de %BF:
  ...

Tabla de FFMI:
  <14      | Novata
  14-16    | Intermedia
  16-18    | Avanzada
  18-20    | Elite (Natty max)
  >20      | Posible uso de anabólicos
```

## Seguridad

✓ No se expone FFMI al usuario (información técnica interna)  
✓ No se exponen fórmulas ni umbrales  
✓ Contacto protegido por defecto  
✓ Separación clara entre información pública e interna  

## Mantenimiento

- La función `build_report_resumen()` está en `MUPAI/FBEO.py`
- Los tests están en `test_report_resumen.py` y `test_complete_separation.py`
- El reporte completo permanece sin cambios en `generar_pdf()`

---

**Versión**: 1.0  
**Fecha**: Diciembre 2025  
**Autor**: MUPAI Team
