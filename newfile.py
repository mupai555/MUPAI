"""
MUPAI - Implementación Completa de Lógica Científica
Todas las funciones implementadas EXACTAMENTE según documentación
Sin simplificaciones, mantiene todos los rangos, clasificaciones y validaciones
"""

import numpy as np
from typing import Dict, Tuple, Union, Optional

# ==================== 1. AJUSTE DE GRASA CORPORAL - EXACTO ====================

def ajustar_grasa_corporal(porcentaje_grasa: float, metodo_medicion: str, pliegues: Optional[int] = None) -> float:
    """
    Implementa EXACTAMENTE los ajustes de grasa corporal según documentación
    
    BIA:
    - Si %BF < 18% → ajustar −2.5 puntos porcentuales
    - Si %BF > 25% → ajustar +3.5 puntos porcentuales
    - Si %BF entre 18–25% → sin ajuste
    
    Naval:
    - Si %BF < 15% → ajustar −2.5 puntos porcentuales
    - Si %BF > 25% → ajustar +3.0 puntos porcentuales
    - Si %BF entre 15–25% → sin ajuste
    
    Antropometría:
    - Si < 7 pliegues → ajustar +1.5 puntos porcentuales
    - Si ≥ 7 pliegues → sin ajuste
    
    DEXA: Sin ajuste
    """
    if metodo_medicion == "DEXA":
        return porcentaje_grasa
    
    elif metodo_medicion == "BIA":
        if porcentaje_grasa < 18:
            return porcentaje_grasa - 2.5
        elif porcentaje_grasa > 25:
            return porcentaje_grasa + 3.5
        else:  # 18-25%
            return porcentaje_grasa
    
    elif metodo_medicion == "Fórmula Naval":
        if porcentaje_grasa < 15:
            return porcentaje_grasa - 2.5
        elif porcentaje_grasa > 25:
            return porcentaje_grasa + 3.0
        else:  # 15-25%
            return porcentaje_grasa
    
    elif metodo_medicion == "Antropometría":
        if pliegues is None:
            raise ValueError("Número de pliegues requerido para método Antropometría")
        
        if pliegues < 7:
            return porcentaje_grasa + 1.5
        else:  # ≥ 7 pliegues
            return porcentaje_grasa
    
    else:
        raise ValueError(f"Método de medición no reconocido: {metodo_medicion}")


# ==================== 2. FACTORES DE ACTIVIDAD - EXACTOS ====================

def calcular_geaf(nivel_actividad: str, sexo: str) -> float:
    """
    Implementa EXACTAMENTE los factores GEAF según tabla por género
    """
    factores_geaf = {
        "Sedentario": {"Masculino": 1.00, "Femenino": 1.00},
        "Poco activo": {"Masculino": 1.11, "Femenino": 1.12},
        "Activo": {"Masculino": 1.25, "Femenino": 1.27},
        "Muy activo": {"Masculino": 1.48, "Femenino": 1.45}
    }
    
    try:
        return factores_geaf[nivel_actividad][sexo]
    except KeyError:
        raise ValueError(f"Nivel de actividad '{nivel_actividad}' o sexo '{sexo}' no válido")


# ==================== 3. EVALUACIÓN PITTSBURGH - EXACTA ====================

def evaluar_pittsburgh(dificultad_dormir: int, despertares: int, sensacion_descanso: int, calidad_percibida: int) -> Dict:
    """
    Implementa EXACTAMENTE la evaluación Pittsburgh 0-16 puntos
    
    Cada pregunta: 0-4 puntos
    Ítem 3 INVERTIDO: (4 - valor_ingresado)
    
    Fórmula: Q1 + Q2 + (4-Q3) + Q4
    Rango total: 0-16 puntos
    
    Clasificación:
    - 0–5 → Sueño bueno
    - 6–9 → Sueño moderadamente alterado
    - 10–16 → Sueño deficiente
    """
    # Validar rangos
    for valor in [dificultad_dormir, despertares, sensacion_descanso, calidad_percibida]:
        if not 0 <= valor <= 4:
            raise ValueError("Todos los valores deben estar entre 0 y 4")
    
    # Calcular score (item 3 invertido)
    score = dificultad_dormir + despertares + (4 - sensacion_descanso) + calidad_percibida
    
    # Validar rango final
    if not 0 <= score <= 16:
        raise ValueError(f"Score calculado fuera de rango: {score}")
    
    # Clasificación
    if score <= 5:
        clasificacion = "Sueño bueno"
    elif score <= 9:
        clasificacion = "Sueño moderadamente alterado"
    else:  # 10-16
        clasificacion = "Sueño deficiente"
    
    return {
        "score": score,
        "clasificacion": clasificacion,
        "rango": "0-16"
    }


# ==================== 4. EVALUACIÓN PSS-4 - EXACTA ====================

def evaluar_pss4(control_vida: int, manejo_problemas: int, cosas_favor: int, dificultades: int) -> Dict:
    """
    Implementa EXACTAMENTE PSS-4 con ítems invertidos
    
    Ítems 2 y 3 INVERTIDOS: (4 - valor_ingresado)
    
    Fórmula: Q1 + (4-Q2) + (4-Q3) + Q4
    Rango: 0-16 puntos
    
    Clasificación PSS-4:
    - 0-4: Estrés bajo
    - 5-8: Estrés moderado  
    - 9-12: Estrés alto
    - 13-16: Estrés muy alto
    """
    # Validar rangos
    for valor in [control_vida, manejo_problemas, cosas_favor, dificultades]:
        if not 0 <= valor <= 4:
            raise ValueError("Todos los valores deben estar entre 0 y 4")
    
    # Calcular score (ítems 2 y 3 invertidos)
    score = control_vida + (4 - manejo_problemas) + (4 - cosas_favor) + dificultades
    
    # Validar rango final
    if not 0 <= score <= 16:
        raise ValueError(f"Score calculado fuera de rango: {score}")
    
    # Clasificación
    if score <= 4:
        clasificacion = "Estrés bajo"
    elif score <= 8:
        clasificacion = "Estrés moderado"
    elif score <= 12:
        clasificacion = "Estrés alto"
    else:  # 13-16
        clasificacion = "Estrés muy alto"
    
    return {
        "score": score,
        "clasificacion": clasificacion,
        "rango": "0-16"
    }


# ==================== 5. FACTOR DE RECUPERACIÓN INTELIGENTE - EXACTO ====================

def calcular_fri(score_pittsburgh: int, score_pss4: int) -> Dict:
    """
    Implementa EXACTAMENTE el cálculo FRI según tabla
    
    FRI = (20 - score_pittsburgh) + (20 - score_pss4)
    
    Clasificación:
    - ≥ 17: 🟢 Muy alto
    - 14–16: 🟢 Alto
    - 11–13: 🟡 Intermedio
    - 8–10: 🟠 Bajo
    - ≤ 7: 🔴 Muy bajo
    """
    # Validar rangos
    if not 0 <= score_pittsburgh <= 16:
        raise ValueError(f"Score Pittsburgh fuera de rango: {score_pittsburgh}")
    if not 0 <= score_pss4 <= 16:
        raise ValueError(f"Score PSS-4 fuera de rango: {score_pss4}")
    
    # Calcular FRI
    fri = (20 - score_pittsburgh) + (20 - score_pss4)
    
    # Clasificación
    if fri >= 17:
        nivel = "🟢 Muy alto"
    elif fri >= 14:
        nivel = "🟢 Alto"
    elif fri >= 11:
        nivel = "🟡 Intermedio"
    elif fri >= 8:
        nivel = "🟠 Bajo"
    else:  # ≤ 7
        nivel = "🔴 Muy bajo"
    
    return {
        "fri": fri,
        "nivel": nivel,
        "score_pittsburgh": score_pittsburgh,
        "score_pss4": score_pss4
    }


# ==================== 6. DETERMINACIÓN AUTOMÁTICA DE OBJETIVO - EXACTA ====================

def determinar_objetivo_automatico(porcentaje_grasa: float, sexo: str, nivel_entrenamiento: str) -> Dict:
    """
    Implementa EXACTAMENTE la tabla de objetivos automáticos
    
    HOMBRES:
    - > 26% → Definición (cualquier nivel)
    - 21–26% → Definición (Principiante–Intermedio)
    - 15–21% → Recomposición (Principiante–Intermedio)
    - 8–15% → Volumen moderado (Intermedio–Avanzado)
    - ≤ 8% → Volumen agresivo (Avanzado/Experto)
    
    MUJERES:
    - > 39% → Definición (cualquier nivel)
    - 33–39% → Definición (Principiante–Intermedio)
    - 24–33% → Recomposición (Principiante–Intermedio)
    - 14–24% → Volumen moderado (Intermedio–Avanzado)
    - ≤ 14% → Volumen agresivo (Avanzado/Experto)
    """
    if sexo == "Masculino":
        if porcentaje_grasa > 26:
            return {
                "objetivo": "Definición",
                "nivel_requerido": "Cualquier nivel",
                "razon": "BF > 26%"
            }
        elif 21 <= porcentaje_grasa <= 26:
            if nivel_entrenamiento in ["Principiante", "Intermedio"]:
                return {
                    "objetivo": "Definición",
                    "nivel_requerido": "Principiante–Intermedio",
                    "razon": "BF 21-26%"
                }
            else:
                return {
                    "objetivo": "Recomposición",
                    "nivel_requerido": "Nivel avanzado detectado",
                    "razon": "BF 21-26% con nivel avanzado"
                }
        elif 15 <= porcentaje_grasa < 21:
            return {
                "objetivo": "Recomposición",
                "nivel_requerido": "Principiante–Intermedio",
                "razon": "BF 15-21%"
            }
        elif 8 < porcentaje_grasa < 15:
            return {
                "objetivo": "Volumen moderado",
                "nivel_requerido": "Intermedio–Avanzado",
                "razon": "BF 8-15%"
            }
        else:  # ≤ 8%
            return {
                "objetivo": "Volumen agresivo",
                "nivel_requerido": "Avanzado/Experto",
                "razon": "BF ≤ 8%"
            }
    
    else:  # Femenino
        if porcentaje_grasa > 39:
            return {
                "objetivo": "Definición",
                "nivel_requerido": "Cualquier nivel",
                "razon": "BF > 39%"
            }
        elif 33 <= porcentaje_grasa <= 39:
            if nivel_entrenamiento in ["Principiante", "Intermedio"]:
                return {
                    "objetivo": "Definición",
                    "nivel_requerido": "Principiante–Intermedio",
                    "razon": "BF 33-39%"
                }
            else:
                return {
                    "objetivo": "Recomposición",
                    "nivel_requerido": "Nivel avanzado detectado",
                    "razon": "BF 33-39% con nivel avanzado"
                }
        elif 24 <= porcentaje_grasa < 33:
            return {
                "objetivo": "Recomposición",
                "nivel_requerido": "Principiante–Intermedio",
                "razon": "BF 24-33%"
            }
        elif 14 < porcentaje_grasa < 24:
            return {
                "objetivo": "Volumen moderado",
                "nivel_requerido": "Intermedio–Avanzado",
                "razon": "BF 14-24%"
            }
        else:  # ≤ 14%
            return {
                "objetivo": "Volumen agresivo",
                "nivel_requerido": "Avanzado/Experto",
                "razon": "BF ≤ 14%"
            }


# ==================== 7. DÉFICITS Y SUPERÁVITS - EXACTOS ====================

def obtener_deficit_ranges() -> Dict:
    """
    Implementa EXACTAMENTE los rangos de déficit por categoría
    """
    return {
        "Preparación Concurso": {
            "rango": (0.025, 0.075),
            "perdida_max": 0.005,
            "descripcion": "Déficit muy conservador para mantener masa muscular"
        },
        "Atlético": {
            "rango": (0.05, 0.25),
            "perdida_max": 0.007,
            "descripcion": "Déficit moderado para atletas"
        },
        "Promedio": {
            "rango": (0.20, 0.40),
            "perdida_max": 0.010,
            "descripcion": "Déficit estándar para población general"
        },
        "Sobrepeso": {
            "rango": (0.30, 0.50),
            "perdida_max": 0.015,
            "descripcion": "Déficit agresivo para sobrepeso"
        },
        "Obeso": {
            "rango": "PSMF",
            "perdida_max": "N/A",
            "descripcion": "Protein-Sparing Modified Fast requerido"
        }
    }


def obtener_superavit_ranges() -> Dict:
    """
    Implementa EXACTAMENTE los rangos de superávit por porcentaje BF
    """
    return {
        "< 12%": {
            "nivel": "Avanzado/Experto",
            "rango": (0.15, 0.20),
            "descripcion": "Superávit alto para BF muy bajo"
        },
        "12-15%": {
            "nivel": "Intermedio/Avanzado",
            "rango": (0.10, 0.15),
            "descripcion": "Superávit moderado para BF bajo"
        },
        "> 18%": {
            "nivel": "No recomendado",
            "rango": "Recomposición",
            "descripcion": "Recomposición recomendada en lugar de volumen"
        }
    }


# ==================== 8. MODULACIÓN FRI - EXACTA ====================

def ajustar_por_fri(deficit_superavit_base: float, fri_nivel: str, objetivo: str) -> Dict:
    """
    Implementa EXACTAMENTE la modulación por FRI
    
    - 🔴 Muy bajo: -50% del déficit/superávit
    - 🟠 Bajo: -30%
    - 🟡 Intermedio: -10%
    - 🟢 Alto: 0% (sin ajuste)
    - 🟢 Muy alto: +5% (solo volumen agresivo)
    """
    # Determinar factor de ajuste
    if "🔴 Muy bajo" in fri_nivel:
        factor_ajuste = -0.50
    elif "🟠 Bajo" in fri_nivel:
        factor_ajuste = -0.30
    elif "🟡 Intermedio" in fri_nivel:
        factor_ajuste = -0.10
    elif "🟢 Alto" in fri_nivel:
        factor_ajuste = 0.0
    elif "🟢 Muy alto" in fri_nivel:
        # Solo +5% para volumen agresivo
        factor_ajuste = 0.05 if "agresivo" in objetivo.lower() else 0.0
    else:
        factor_ajuste = 0.0
    
    # Aplicar ajuste
    ajuste_absoluto = deficit_superavit_base * factor_ajuste
    valor_ajustado = deficit_superavit_base + ajuste_absoluto
    
    return {
        "valor_original": deficit_superavit_base,
        "factor_ajuste": factor_ajuste,
        "ajuste_absoluto": ajuste_absoluto,
        "valor_ajustado": valor_ajustado,
        "fri_nivel": fri_nivel
    }


# ==================== 9. CÁLCULOS ENERGÉTICOS - EXACTOS ====================

def calcular_gasto_energetico_total(peso: float, estatura: float, porcentaje_grasa: float, 
                                   sexo: str, nivel_actividad: str, minutos_entrenamiento: int, 
                                   dias_entrenamiento: int) -> Dict:
    """
    Implementa EXACTAMENTE los cálculos energéticos
    
    1. TMB (Katch-McArdle): TMB = 370 + (21.6 × Masa_Magra_kg)
    2. Masa_Magra = peso × (1 - porcentaje_grasa_corregido)
    3. GEAF según tabla exacta por género
    4. GEE = 0.1 × peso × minutos_efectivos × días_semana
    5. GEE_diario = GEE_semanal ÷ 7
    6. GET = (TMB × GEAF + GEE_diario) × ETA(1.15)
    """
    # 1. Calcular masa magra
    masa_magra = peso * (1 - porcentaje_grasa / 100)
    
    # 2. TMB usando Katch-McArdle EXACTA
    tmb = 370 + (21.6 * masa_magra)
    
    # 3. GEAF según tabla exacta
    geaf = calcular_geaf(nivel_actividad, sexo)
    
    # 4. GEE cálculo exacto
    gee_semanal = 0.1 * peso * minutos_entrenamiento * dias_entrenamiento
    gee_diario = gee_semanal / 7
    
    # 5. GET final con ETA exacto
    eta = 1.15
    get = (tmb * geaf + gee_diario) * eta
    
    return {
        "masa_magra": masa_magra,
        "tmb": tmb,
        "geaf": geaf,
        "gee_semanal": gee_semanal,
        "gee_diario": gee_diario,
        "eta": eta,
        "get": get,
        "detalles": {
            "formula_tmb": "370 + (21.6 × Masa_Magra_kg)",
            "formula_gee": "0.1 × peso × minutos × días",
            "formula_get": "(TMB × GEAF + GEE_diario) × ETA(1.15)"
        }
    }


# ==================== 10. MACRONUTRIENTES - EXACTOS ====================

def calcular_macronutrientes_avanzados(calorias_totales: float, peso: float, objetivo_automatico: str) -> Dict:
    """
    Implementa EXACTAMENTE los rangos de macronutrientes
    
    PROTEÍNA (g/kg):
    - Déficit: 2.2 – 2.6 g/kg
    - Recomposición: 2.0 – 2.3 g/kg
    - Superávit: 1.8 – 2.0 g/kg
    
    GRASA (g/kg):
    - Déficit: 0.8 – 1.0 g/kg
    - Recomposición: 0.9 – 1.1 g/kg
    - Superávit: 1.0 – 1.2 g/kg
    
    CARBOHIDRATOS: Por diferencia calórica
    """
    # Determinar rangos según objetivo
    if "Definición" in objetivo_automatico:
        proteina_min, proteina_max = 2.2, 2.6
        grasa_min, grasa_max = 0.8, 1.0
    elif "Recomposición" in objetivo_automatico:
        proteina_min, proteina_max = 2.0, 2.3
        grasa_min, grasa_max = 0.9, 1.1
    else:  # Volumen
        proteina_min, proteina_max = 1.8, 2.0
        grasa_min, grasa_max = 1.0, 1.2
    
    # Calcular valores medios
    proteina_gkg = (proteina_min + proteina_max) / 2
    grasa_gkg = (grasa_min + grasa_max) / 2
    
    # Calcular gramos totales
    proteina_g = peso * proteina_gkg
    grasa_g = peso * grasa_gkg
    
    # Calcular calorías de proteína y grasa
    proteina_kcal = proteina_g * 4
    grasa_kcal = grasa_g * 9
    
    # Carbohidratos por diferencia
    carbs_kcal = calorias_totales - proteina_kcal - grasa_kcal
    carbs_g = carbs_kcal / 4
    
    return {
        "proteina": {
            "gramos": proteina_g,
            "kcal": proteina_kcal,
            "gkg": proteina_gkg,
            "rango_gkg": (proteina_min, proteina_max),
            "porcentaje": (proteina_kcal / calorias_totales) * 100
        },
        "grasa": {
            "gramos": grasa_g,
            "kcal": grasa_kcal,
            "gkg": grasa_gkg,
            "rango_gkg": (grasa_min, grasa_max),
            "porcentaje": (grasa_kcal / calorias_totales) * 100
        },
        "carbohidratos": {
            "gramos": carbs_g,
            "kcal": carbs_kcal,
            "gkg": carbs_g / peso,
            "porcentaje": (carbs_kcal / calorias_totales) * 100
        },
        "total_kcal": calorias_totales,
        "objetivo": objetivo_automatico
    }


# ==================== 11. VALIDACIONES CRUZADAS - TODAS ====================

def validar_actividad_ocupacion(nivel_actividad: str, ocupacion: str) -> Dict:
    """
    Implementa validación cruzada exacta:
    
    Si ocupacion == "Oficina/estudiante" y actividad == "Muy activo":
        → Ajustar a "Activo"
    """
    nivel_original = nivel_actividad
    nivel_ajustado = nivel_actividad
    ajuste_realizado = False
    razon = ""
    
    if ocupacion in ["Oficina/estudiante", "Oficina/Escritorio"] and nivel_actividad == "Muy activo":
        nivel_ajustado = "Activo"
        ajuste_realizado = True
        razon = "Ocupación sedentaria incompatible con 'Muy activo'"
    
    return {
        "nivel_original": nivel_original,
        "nivel_ajustado": nivel_ajustado,
        "ajuste_realizado": ajuste_realizado,
        "razon": razon,
        "ocupacion": ocupacion
    }


def validar_entrenamiento_nivel(nivel_entrenamiento: str, minutos_entrenamiento: int) -> Dict:
    """
    Implementa límites exactos:
    
    - Principiante: máximo 45 minutos efectivos
    - Intermedio: máximo 60 minutos
    - Avanzado: hasta 75 minutos
    """
    limites = {
        "Principiante": 45,
        "Intermedio": 60,
        "Avanzado": 75
    }
    
    limite_max = limites.get(nivel_entrenamiento, 60)
    minutos_originales = minutos_entrenamiento
    minutos_ajustados = min(minutos_entrenamiento, limite_max)
    ajuste_realizado = minutos_ajustados != minutos_originales
    
    return {
        "minutos_originales": minutos_originales,
        "minutos_ajustados": minutos_ajustados,
        "limite_max": limite_max,
        "ajuste_realizado": ajuste_realizado,
        "nivel_entrenamiento": nivel_entrenamiento
    }


def validar_pasos_actividad(pasos_diarios: str, nivel_actividad_declarado: str) -> Dict:
    """
    Implementa validación cruzada:
    
    - < 7,500 pasos → validar "Sedentario"
    - 7,500-9,999 → validar "Poco activo"
    - 10,000-12,500 → validar "Activo"
    - > 12,500 → validar "Muy activo"
    """
    # Convertir pasos a valor numérico para validación
    pasos_num = 0
    if "< 5,000" in pasos_diarios:
        pasos_num = 4000
    elif "5,000-7,500" in pasos_diarios:
        pasos_num = 6250
    elif "7,500-10,000" in pasos_diarios:
        pasos_num = 8750
    elif "10,000-12,500" in pasos_diarios:
        pasos_num = 11250
    elif "> 12,500" in pasos_diarios:
        pasos_num = 15000
    
    # Determinar nivel esperado según pasos
    if pasos_num < 7500:
        nivel_esperado = "Sedentario"
    elif pasos_num < 10000:
        nivel_esperado = "Poco activo"
    elif pasos_num <= 12500:
        nivel_esperado = "Activo"
    else:
        nivel_esperado = "Muy activo"
    
    # Validar concordancia
    concordancia = nivel_actividad_declarado == nivel_esperado
    
    return {
        "pasos_diarios": pasos_diarios,
        "pasos_estimados": pasos_num,
        "nivel_declarado": nivel_actividad_declarado,
        "nivel_esperado": nivel_esperado,
        "concordancia": concordancia,
        "recomendacion": nivel_esperado if not concordancia else nivel_actividad_declarado
    }


# ==================== 12. CASOS DE PRUEBA OBLIGATORIOS ====================

def ejecutar_casos_prueba_obligatorios():
    """
    Implementa TODOS los casos de prueba obligatorios de la documentación
    """
    print("=== CASOS DE PRUEBA OBLIGATORIOS ===")
    
    # Ejemplo BIA
    print("\n1. Ejemplo BIA:")
    print("Input: 16% BIA →", ajustar_grasa_corporal(16, "BIA"))
    print("Input: 28% BIA →", ajustar_grasa_corporal(28, "BIA"))
    
    # Ejemplo Pittsburgh
    print("\n2. Ejemplo Pittsburgh:")
    print("Q1=2, Q2=3, Q3=1, Q4=2 →", evaluar_pittsburgh(2, 3, 1, 2))
    
    # Ejemplo Objetivo
    print("\n3. Ejemplo Objetivo:")
    print("Hombre, 23% BF, Principiante →", determinar_objetivo_automatico(23, "Masculino", "Principiante"))
    
    # Ejemplo PSS-4
    print("\n4. Ejemplo PSS-4:")
    print("Q1=1, Q2=2, Q3=3, Q4=1 →", evaluar_pss4(1, 2, 3, 1))
    
    # Ejemplo FRI
    print("\n5. Ejemplo FRI:")
    pittsburgh_result = evaluar_pittsburgh(2, 3, 1, 2)
    pss4_result = evaluar_pss4(1, 2, 3, 1)
    print("Score Pittsburgh=10, PSS-4=6 →", calcular_fri(pittsburgh_result["score"], pss4_result["score"]))


if __name__ == "__main__":
    ejecutar_casos_prueba_obligatorios()