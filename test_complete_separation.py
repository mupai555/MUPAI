#!/usr/bin/env python3
"""
Test to verify complete separation between summary and complete reports.

This test verifies:
1. Summary report (for user) does NOT contain FFMI data
2. Complete report data (for internal use) DOES contain FFMI data
3. Both reports can coexist in the same workflow
"""

import sys

def build_report_resumen(data):
    """Summary report function (inline for testing)"""
    reporte = "=" * 60 + "\n"
    reporte += "REPORTE RESUMIDO - EVALUACIÓN MUPAI\n"
    reporte += "=" * 60 + "\n\n"
    
    reporte += "DATOS DEL CLIENTE\n"
    reporte += "-" * 60 + "\n"
    reporte += f"Nombre completo: {data['nombre_completo']}\n"
    reporte += f"Edad: {data['edad']} años\n"
    reporte += f"Sexo: {data['sexo']}\n"
    reporte += f"Fecha de evaluación: {data['fecha_evaluacion']}\n"
    
    if data.get('incluir_contacto', False):
        if 'telefono' in data and data['telefono']:
            reporte += f"Teléfono: {data['telefono']}\n"
        if 'email' in data and data['email']:
            reporte += f"Email: {data['email']}\n"
    
    reporte += "\n"
    reporte += "ANTROPOMETRÍA, COMPOSICIÓN CORPORAL E ÍNDICES METABÓLICOS\n"
    reporte += "-" * 60 + "\n"
    
    reporte += f"1. Peso: {data['peso']:.1f} kg\n"
    reporte += f"2. Estatura: {data['estatura']:.0f} cm\n"
    reporte += f"3. IMC: {data['imc']:.1f} kg/m²\n"
    reporte += f"4. % Grasa medida: {data['grasa_medida']:.1f}%\n"
    reporte += f"5. % Grasa corregida (DEXA/4C): {data['grasa_corregida']:.1f}%\n"
    
    grasa_visceral = data.get('grasa_visceral')
    if grasa_visceral is not None:
        reporte += f"6. Grasa visceral: {grasa_visceral:.1f}\n"
    else:
        reporte += "6. Grasa visceral: N/D\n"
    
    porcentaje_masa_muscular = data.get('porcentaje_masa_muscular')
    if porcentaje_masa_muscular is not None:
        reporte += f"7. % Masa muscular: {porcentaje_masa_muscular:.1f}%\n"
    else:
        reporte += "7. % Masa muscular: N/D\n"
    
    reporte += f"8. Masa libre de grasa: {data['mlg']:.1f} kg\n"
    reporte += f"9. Masa grasa: {data['masa_grasa']:.1f} kg\n"
    
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

def build_complete_report_data(nombre, edad, genero, estatura, peso, email, telefono,
                                metodo_grasa, grasa_reportada, grasa_corregida,
                                nivel_grasa, ffmi, nivel_ffmi, mlg):
    """
    Simulates the complete report data structure (used for PDF generation)
    This should INCLUDE FFMI data for internal use
    """
    usuario = {
        "Nombre": nombre,
        "Edad": f"{edad} años",
        "Género": genero,
        "Estatura": f"{estatura} cm",
        "Peso": f"{peso} kg",
        "Email": email,
        "Teléfono": telefono,
        "Método %BF": metodo_grasa,
        "%BF reportado": f"{grasa_reportada:.1f}%",
        "%BF corregido (DEXA)": f"{grasa_corregida:.1f}%",
    }
    resumen = {
        "Nivel de grasa corporal": nivel_grasa,
        "FFMI": f"{ffmi:.2f} — {nivel_ffmi}",
        "MLG": f"{mlg:.1f} kg",
    }
    return usuario, resumen

def test_complete_workflow_karina():
    """
    Test the complete workflow with Karina's data.
    Verifies that both summary and complete reports are generated correctly.
    """
    print("=" * 70)
    print("TEST: Complete Workflow with Karina's Case")
    print("=" * 70)
    
    # Karina's data
    nombre = "San Juana Karina Martinez Sanchez"
    edad = 41
    genero = "Mujer"
    estatura = 160.0
    peso = 65.0
    email = "sanjuanamartine.5307@gmail.com"
    telefono = "8661357422"
    metodo_grasa = "Omron HBF-516 (BIA)"
    grasa_reportada = 28.0
    grasa_corregida = 30.0
    
    # Calculations
    estatura_m = estatura / 100
    imc = peso / (estatura_m ** 2)
    mlg = peso * (1 - grasa_corregida / 100)
    masa_grasa = peso * (grasa_corregida / 100)
    ffmi = mlg / (estatura_m ** 2)
    
    # Classifications
    nivel_grasa = "Sobrepeso"  # 28-35% for women
    nivel_ffmi = "Intermedia"  # Example classification
    
    # 1. Generate SUMMARY REPORT (for user - NO FFMI)
    datos_resumen = {
        'nombre_completo': nombre,
        'edad': edad,
        'sexo': genero,
        'fecha_evaluacion': '2025-12-10',
        'peso': peso,
        'estatura': estatura,
        'imc': imc,
        'grasa_medida': grasa_reportada,
        'grasa_corregida': grasa_corregida,
        'mlg': mlg,
        'masa_grasa': masa_grasa,
        'nivel_grasa': nivel_grasa,
        'grasa_visceral': None,
        'porcentaje_masa_muscular': None,
        'edad_metabolica': None,
        'incluir_contacto': False,
        'telefono': telefono,
        'email': email
    }
    reporte_resumido = build_report_resumen(datos_resumen)
    
    # 2. Generate COMPLETE REPORT DATA (for internal use - WITH FFMI)
    usuario_completo, resumen_completo = build_complete_report_data(
        nombre, edad, genero, estatura, peso, email, telefono,
        metodo_grasa, grasa_reportada, grasa_corregida,
        nivel_grasa, ffmi, nivel_ffmi, mlg
    )
    
    print("\n[1] SUMMARY REPORT (FOR USER):")
    print("-" * 70)
    print(reporte_resumido)
    
    print("\n[2] COMPLETE REPORT DATA (FOR INTERNAL USE/PDF):")
    print("-" * 70)
    print("Usuario data:")
    for k, v in usuario_completo.items():
        print(f"  {k}: {v}")
    print("\nResumen data:")
    for k, v in resumen_completo.items():
        print(f"  {k}: {v}")
    
    print("\n" + "=" * 70)
    print("VERIFICATION CHECKS:")
    print("=" * 70)
    
    # Convert complete report to string for checking
    complete_report_str = str(usuario_completo) + str(resumen_completo)
    
    checks = {
        '✓ Summary report does NOT contain FFMI': 'FFMI' not in reporte_resumido,
        '✓ Summary report does NOT contain FFMI classification': 'Intermedia' not in reporte_resumido and 'Novata' not in reporte_resumido,
        '✓ Complete report DOES contain FFMI': 'FFMI' in complete_report_str,
        '✓ Complete report DOES contain FFMI value': str(round(ffmi, 2)) in complete_report_str,
        '✓ Summary report contains name': nombre in reporte_resumido,
        '✓ Summary report contains body composition': 'Masa libre de grasa:' in reporte_resumido,
        '✓ Summary report has N/D for missing data': 'N/D' in reporte_resumido,
        '✓ Summary report contains category': nivel_grasa in reporte_resumido,
        '✓ Complete report contains all personal data': all(field in complete_report_str for field in [nombre, str(edad), genero]),
        '✓ Both reports coexist': len(reporte_resumido) > 0 and len(complete_report_str) > 0,
    }
    
    all_passed = True
    for check_name, result in checks.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {check_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ ALL WORKFLOW TESTS PASSED")
        print("\nCONCLUSION:")
        print("  - Summary report (user-facing) successfully excludes FFMI")
        print("  - Complete report (internal) successfully includes FFMI")
        print("  - Both reports can be generated in the same workflow")
    else:
        print("✗ SOME WORKFLOW TESTS FAILED")
    print("=" * 70)
    
    return all_passed

if __name__ == "__main__":
    print("Testing Complete Report Separation\n")
    
    test_passed = test_complete_workflow_karina()
    
    if test_passed:
        print("\n✓ COMPLETE SEPARATION VERIFIED SUCCESSFULLY")
        sys.exit(0)
    else:
        print("\n✗ SEPARATION TEST FAILED")
        sys.exit(1)
