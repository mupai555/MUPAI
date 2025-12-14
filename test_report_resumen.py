#!/usr/bin/env python3
"""
Test script for report summary generation (build_report_resumen)
Tests with Karina's case data
"""

import sys
import os

# Inline the build_report_resumen function to avoid streamlit import issues
def build_report_resumen(data):
    """
    Genera el reporte resumido para el usuario.
    
    Este reporte contiene ÚNICAMENTE los datos permitidos según la especificación:
    - Datos del cliente (sin teléfono ni email por defecto)
    - Antropometría y composición corporal básica
    - NO incluye FFMI ni detalles técnicos
    """
    # A) Datos del cliente
    reporte = "=" * 60 + "\n"
    reporte += "REPORTE RESUMIDO - EVALUACIÓN MUPAI\n"
    reporte += "=" * 60 + "\n\n"
    
    reporte += "DATOS DEL CLIENTE\n"
    reporte += "-" * 60 + "\n"
    reporte += f"Nombre completo: {data['nombre_completo']}\n"
    reporte += f"Edad: {data['edad']} años\n"
    reporte += f"Sexo: {data['sexo']}\n"
    reporte += f"Fecha de evaluación: {data['fecha_evaluacion']}\n"
    
    # Solo incluir contacto si está explícitamente activado
    if data.get('incluir_contacto', False):
        if 'telefono' in data and data['telefono']:
            reporte += f"Teléfono: {data['telefono']}\n"
        if 'email' in data and data['email']:
            reporte += f"Email: {data['email']}\n"
    
    # B) Antropometría, composición corporal e índices metabólicos
    reporte += "\n"
    reporte += "ANTROPOMETRÍA, COMPOSICIÓN CORPORAL E ÍNDICES METABÓLICOS\n"
    reporte += "-" * 60 + "\n"
    
    # Orden específico según requerimientos
    reporte += f"1. Peso: {data['peso']:.1f} kg\n"
    reporte += f"2. Estatura: {data['estatura']:.0f} cm\n"
    reporte += f"3. IMC: {data['imc']:.1f} kg/m²\n"
    reporte += f"4. % Grasa medido: {data['grasa_medida']:.1f}%\n"
    reporte += f"5. % Grasa corregido (DEXA/4C): {data['grasa_corregida']:.1f}%\n"
    
    # Grasa visceral (N/D si no disponible)
    grasa_visceral = data.get('grasa_visceral')
    if grasa_visceral is not None:
        reporte += f"6. Grasa visceral: {grasa_visceral:.1f}\n"
    else:
        reporte += "6. Grasa visceral: N/D\n"
    
    # % Masa muscular (N/D si no disponible)
    porcentaje_masa_muscular = data.get('porcentaje_masa_muscular')
    if porcentaje_masa_muscular is not None:
        reporte += f"7. % Masa muscular: {porcentaje_masa_muscular:.1f}%\n"
    else:
        reporte += "7. % Masa muscular: N/D\n"
    
    reporte += f"8. Masa libre de grasa: {data['mlg']:.1f} kg\n"
    reporte += f"9. Masa grasa: {data['masa_grasa']:.1f} kg\n"
    
    # Edad metabólica (N/D si no disponible)
    edad_metabolica = data.get('edad_metabolica')
    if edad_metabolica is not None:
        reporte += f"10. Edad metabólica: {edad_metabolica} años\n"
    else:
        reporte += "10. Edad metabólica: N/D\n"
    
    reporte += f"11. Categoría de grasa corporal: {data['nivel_grasa']}\n"
    
    reporte += "\n" + "=" * 60 + "\n"
    reporte += "NOTA: Este es un reporte resumido para el usuario.\n"
    reporte += "El análisis técnico detallado es de uso interno.\n"
    reporte += "=" * 60 + "\n"
    
    return reporte

def test_karina_case():
    """
    Test with Karina's case data from the problem statement
    San Juana Karina Martinez Sanchez, 41 years old
    """
    # Sample data for Karina
    # Using reasonable estimates for body composition
    peso = 65.0  # kg
    estatura = 160.0  # cm
    grasa_medida = 28.0  # %
    grasa_corregida = 30.0  # % DEXA corrected
    
    # Calculations
    estatura_m = estatura / 100
    imc = peso / (estatura_m ** 2)
    mlg = peso * (1 - grasa_corregida / 100)
    masa_grasa = peso * (grasa_corregida / 100)
    
    # Classification for woman with 30% body fat
    nivel_grasa = "Sobrepeso"  # Between 28-35% for women
    
    datos_resumen = {
        'nombre_completo': 'San Juana Karina Martinez Sanchez',
        'edad': 41,
        'sexo': 'Mujer',
        'fecha_evaluacion': '2025-12-10',
        'peso': peso,
        'estatura': estatura,
        'imc': imc,
        'grasa_medida': grasa_medida,
        'grasa_corregida': grasa_corregida,
        'mlg': mlg,
        'masa_grasa': masa_grasa,
        'nivel_grasa': nivel_grasa,
        'grasa_visceral': None,  # N/D
        'porcentaje_masa_muscular': None,  # N/D
        'edad_metabolica': None,  # N/D
        'incluir_contacto': False,
        'telefono': '8661357422',
        'email': 'sanjuanamartine.5307@gmail.com'
    }
    
    print("=" * 70)
    print("TEST: Karina's Case - Summary Report")
    print("=" * 70)
    
    reporte = build_report_resumen(datos_resumen)
    print(reporte)
    
    print("\n" + "=" * 70)
    print("VERIFICATION CHECKS:")
    print("=" * 70)
    
    # Verify that FFMI is NOT in the summary
    checks = {
        'FFMI not in report': 'FFMI' not in reporte,
        'Clasificación FFMI not in report': 'Clasificación FFMI' not in reporte,
        'Novato/Intermedio/Avanzado not in report': all(term not in reporte for term in ['Novato', 'Novata', 'Intermedio', 'Intermedia', 'Avanzado', 'Avanzada', 'Elite']),
        'Contains name': 'San Juana Karina Martinez Sanchez' in reporte,
        'Contains age': '41 años' in reporte,
        'Contains sex': 'Mujer' in reporte,
        'Contains peso': str(peso) in reporte,
        'Contains estatura': '160 cm' in reporte,
        'Contains IMC': 'IMC:' in reporte,
        'Contains grasa medida': 'Grasa medido:' in reporte,
        'Contains grasa corregida': 'Grasa corregido (DEXA/4C):' in reporte,
        'Contains MLG': 'Masa libre de grasa:' in reporte,
        'Contains masa grasa': 'Masa grasa:' in reporte,
        'Contains categoría': 'Categoría de grasa corporal:' in reporte,
        'Grasa visceral N/D': 'Grasa visceral: N/D' in reporte,
        'Masa muscular N/D': 'Masa muscular: N/D' in reporte,
        'Edad metabólica N/D': 'Edad metabólica: N/D' in reporte,
        'No phone in report (default)': '8661357422' not in reporte,
        'No email in report (default)': 'sanjuanamartine.5307@gmail.com' not in reporte,
    }
    
    all_passed = True
    for check_name, result in checks.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {check_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 70)
    
    return all_passed

def test_with_optional_data():
    """
    Test with optional data present (grasa visceral, masa muscular, edad metabólica)
    """
    peso = 75.0
    estatura = 175.0
    grasa_medida = 15.0
    grasa_corregida = 16.0
    
    estatura_m = estatura / 100
    imc = peso / (estatura_m ** 2)
    mlg = peso * (1 - grasa_corregida / 100)
    masa_grasa = peso * (grasa_corregida / 100)
    
    datos_resumen = {
        'nombre_completo': 'Test User',
        'edad': 30,
        'sexo': 'Hombre',
        'fecha_evaluacion': '2025-12-14',
        'peso': peso,
        'estatura': estatura,
        'imc': imc,
        'grasa_medida': grasa_medida,
        'grasa_corregida': grasa_corregida,
        'mlg': mlg,
        'masa_grasa': masa_grasa,
        'nivel_grasa': 'Normal saludable',
        'grasa_visceral': 8.5,  # Present
        'porcentaje_masa_muscular': 42.0,  # Present
        'edad_metabolica': 28,  # Present
        'incluir_contacto': True,  # Include contact
        'telefono': '1234567890',
        'email': 'test@example.com'
    }
    
    print("\n" + "=" * 70)
    print("TEST: With Optional Data Present")
    print("=" * 70)
    
    reporte = build_report_resumen(datos_resumen)
    print(reporte)
    
    print("\n" + "=" * 70)
    print("VERIFICATION CHECKS:")
    print("=" * 70)
    
    checks = {
        'Grasa visceral has value': 'Grasa visceral: 8.5' in reporte,
        'Masa muscular has value': 'Masa muscular: 42.0' in reporte,
        'Edad metabólica has value': 'Edad metabólica: 28' in reporte,
        'Phone included (activated)': '1234567890' in reporte,
        'Email included (activated)': 'test@example.com' in reporte,
        'FFMI not in report': 'FFMI' not in reporte,
    }
    
    all_passed = True
    for check_name, result in checks.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {check_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 70)
    
    return all_passed

if __name__ == "__main__":
    print("Running Report Summary Tests\n")
    
    test1_passed = test_karina_case()
    test2_passed = test_with_optional_data()
    
    print("\n" + "=" * 70)
    print("FINAL RESULTS:")
    print("=" * 70)
    print(f"Karina's case test: {'✓ PASSED' if test1_passed else '✗ FAILED'}")
    print(f"Optional data test: {'✓ PASSED' if test2_passed else '✗ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n✓ ALL TESTS PASSED SUCCESSFULLY")
        sys.exit(0)
    else:
        print("\n✗ SOME TESTS FAILED")
        sys.exit(1)
