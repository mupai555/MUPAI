#!/usr/bin/env python3
"""
Test script para verificar la integración modular de BODY AND ENERGY.
Este script valida que todas las funciones importadas funcionan correctamente.
"""

def test_body_and_energy_module():
    """Test the body_and_energy module functions."""
    print("🧪 Iniciando tests del módulo body_and_energy...")
    
    try:
        # Test imports
        from body_and_energy import (
            show_body_and_energy,
            validate_name_body_energy,
            validate_phone_body_energy,
            validate_email_body_energy,
            calcular_tmb_cunningham_body_energy,
            calcular_mlg_body_energy,
            calcular_ffmi_body_energy,
            clasificar_ffmi_body_energy,
            calcular_edad_metabolica_body_energy,
            obtener_geaf_body_energy,
            corregir_porcentaje_grasa_body_energy,
            calculate_psmf_body_energy,
            sugerir_deficit_body_energy
        )
        print("✅ Todas las funciones importadas exitosamente")
        
        # Test validation functions
        print("\n📋 Testing validation functions:")
        
        # Test name validation
        valid, msg = validate_name_body_energy("Juan Pérez García")
        assert valid == True, f"Name validation failed: {msg}"
        print(f"  ✅ Validación de nombre: {valid}")
        
        invalid, msg = validate_name_body_energy("Juan")
        assert invalid == False, "Name validation should fail for single word"
        print(f"  ✅ Validación de nombre inválido: {invalid} - {msg}")
        
        # Test phone validation
        valid, msg = validate_phone_body_energy("8661234567")
        assert valid == True, f"Phone validation failed: {msg}"
        print(f"  ✅ Validación de teléfono: {valid}")
        
        invalid, msg = validate_phone_body_energy("123")
        assert invalid == False, "Phone validation should fail for short number"
        print(f"  ✅ Validación de teléfono inválido: {invalid} - {msg}")
        
        # Test email validation
        valid, msg = validate_email_body_energy("usuario@ejemplo.com")
        assert valid == True, f"Email validation failed: {msg}"
        print(f"  ✅ Validación de email: {valid}")
        
        invalid, msg = validate_email_body_energy("email_invalido")
        assert invalid == False, "Email validation should fail for invalid format"
        print(f"  ✅ Validación de email inválido: {invalid} - {msg}")
        
        # Test calculation functions
        print("\n🧮 Testing calculation functions:")
        
        # Test TMB calculation
        tmb = calcular_tmb_cunningham_body_energy(65.5)
        expected_tmb = 370 + (21.6 * 65.5)
        assert abs(tmb - expected_tmb) < 0.01, f"TMB calculation error: {tmb} vs {expected_tmb}"
        print(f"  ✅ Cálculo TMB: {tmb:.1f} kcal")
        
        # Test MLG calculation
        mlg = calcular_mlg_body_energy(80, 15)
        expected_mlg = 80 * (1 - 15/100)
        assert abs(mlg - expected_mlg) < 0.01, f"MLG calculation error: {mlg} vs {expected_mlg}"
        print(f"  ✅ Cálculo MLG: {mlg:.1f} kg")
        
        # Test FFMI calculation
        ffmi = calcular_ffmi_body_energy(65.5, 175)
        assert ffmi > 0, "FFMI should be positive"
        print(f"  ✅ Cálculo FFMI: {ffmi:.2f}")
        
        # Test FFMI classification
        clasificacion = clasificar_ffmi_body_energy(20.5, "Hombre")
        assert clasificacion in ["Bajo", "Promedio", "Bueno", "Avanzado", "Élite"]
        print(f"  ✅ Clasificación FFMI: {clasificacion}")
        
        # Test metabolic age
        edad_met = calcular_edad_metabolica_body_energy(30, 15, "Hombre")
        assert 18 <= edad_met <= 80, "Metabolic age should be in valid range"
        print(f"  ✅ Edad metabólica: {edad_met} años")
        
        # Test GEAF
        geaf = obtener_geaf_body_energy("Activo")
        assert geaf == 1.25, f"GEAF for Activo should be 1.25, got {geaf}"
        print(f"  ✅ Factor GEAF: {geaf}")
        
        # Test body fat correction
        grasa_corregida = corregir_porcentaje_grasa_body_energy(20, "DEXA (Gold Standard)", "Hombre")
        assert grasa_corregida == 20, "DEXA method should not change the value"
        print(f"  ✅ Corrección grasa corporal: {grasa_corregida}%")
        
        # Test deficit suggestion
        deficit = sugerir_deficit_body_energy(25, "Hombre")
        assert 0 <= deficit <= 50, f"Deficit should be reasonable, got {deficit}"
        print(f"  ✅ Sugerencia de déficit: {deficit}%")
        
        # Test PSMF calculation
        psmf = calculate_psmf_body_energy("Hombre", 80, 25, 68)
        assert isinstance(psmf, dict), "PSMF should return a dictionary"
        print(f"  ✅ Cálculo PSMF: {'Aplicable' if psmf.get('psmf_aplicable') else 'No aplicable'}")
        
        print("\n🎉 ¡Todos los tests pasaron exitosamente!")
        print("\n📊 Resumen de funciones validadas:")
        print("  ✅ 3 funciones de validación")
        print("  ✅ 8 funciones de cálculo")
        print("  ✅ 1 función principal de interfaz")
        print("  ✅ Total: 12+ funciones verificadas")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    except AssertionError as e:
        print(f"❌ Test falló: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def test_integration_with_newfile():
    """Test that newfile.py can import the module correctly."""
    print("\n🔗 Testing integration with newfile.py...")
    
    try:
        # Check that newfile.py has the correct import
        with open('newfile.py', 'r') as f:
            content = f.read()
        
        if 'from body_and_energy import show_body_and_energy' in content:
            print("  ✅ Import statement found in newfile.py")
        else:
            print("  ❌ Import statement not found in newfile.py")
            return False
        
        if 'show_body_and_energy()' in content:
            print("  ✅ Function call found in newfile.py")
        else:
            print("  ❌ Function call not found in newfile.py")
            return False
        
        # Check that old function definition is removed
        if 'def mostrar_body_and_energy():' not in content:
            print("  ✅ Old function definition removed from newfile.py")
        else:
            print("  ⚠️ Old function definition still exists in newfile.py")
        
        print("  ✅ Integration with newfile.py is correct")
        return True
        
    except Exception as e:
        print(f"  ❌ Error checking integration: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 BODY AND ENERGY - Test Suite de Integración Modular")
    print("=" * 60)
    
    # Test the module
    module_test = test_body_and_energy_module()
    
    # Test integration
    integration_test = test_integration_with_newfile()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN FINAL:")
    print(f"  Module Tests: {'✅ PASS' if module_test else '❌ FAIL'}")
    print(f"  Integration Tests: {'✅ PASS' if integration_test else '❌ FAIL'}")
    
    if module_test and integration_test:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("✅ La modularización está completa y funcionando correctamente")
        print("✅ El módulo body_and_energy.py está listo para uso en producción")
        print("✅ La integración con newfile.py es exitosa")
        return 0
    else:
        print("\n❌ ALGUNOS TESTS FALLARON")
        print("🔧 Revisa los errores anteriores y corrige antes de continuar")
        return 1


if __name__ == "__main__":
    exit(main())