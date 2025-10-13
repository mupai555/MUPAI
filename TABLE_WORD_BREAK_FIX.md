# Fix para Palabras Cortadas en Tablas HTML

## Problema Identificado
Las palabras dentro de las celdas de tablas HTML se estaban cortando incorrectamente con guiones en medio de las palabras. Ejemplos específicos:
- "Internos" se mostraba como "inter-nos"
- "Externos" se mostraba como "exter-nos"  
- "semanas" se mostraba como "sema-nas"
- "Descuento" se mostraba como "descuen-to"

## Causa
El CSS global aplicaba reglas de ruptura de palabras (`hyphens: auto`) y permitía cortes de línea a todos los elementos, incluyendo las celdas de tablas. Esto causaba que palabras completas se partieran innecesariamente.

## Solución Implementada
Se agregó un bloque CSS específico para celdas de tabla (`<th>` y `<td>`) en el archivo `newfile.py`, líneas 754-759:

```css
/* Fix for broken words in HTML tables - prevent words from breaking with hyphens */
table th, table td {
    white-space: nowrap !important;
    word-break: keep-all !important;
    hyphens: none !important;
}
```

### Explicación de las Propiedades CSS

1. **`white-space: nowrap !important;`**
   - Previene que el texto se divida en múltiples líneas dentro de las celdas
   - Mantiene todo el contenido en una sola línea

2. **`word-break: keep-all !important;`**
   - Evita que las palabras se rompan en medio
   - Mantiene las palabras completas intactas

3. **`hyphens: none !important;`**
   - Desactiva la división automática con guiones
   - Elimina los guiones que aparecían en medio de las palabras

## Tablas Afectadas
Este fix se aplica a todas las tablas HTML en el archivo, específicamente:

1. **Tabla Resumen de Planes Continuos** (línea ~2400)
   - Headers: "Plan", "Duración", "Descuento", "Precio Internos", "Precio Externos", "Ahorro"

2. **Tabla de Nutrición Extendida** (línea ~3044)
   - Headers: "Duración", "Precio Base Internos", "Descuento", etc.
   - Celdas con "12 semanas", "18 semanas", "24 semanas"

3. **Tabla de Entrenamiento Extendido** (línea ~3122)
   - Headers: similares a la tabla de nutrición
   - Celdas con "16 semanas", "24 semanas", "32 semanas"

4. **Tabla de Plan Combinado Extendido** (línea ~3197)
   - Headers: incluye todos los campos de precios internos y externos
   - Celdas con duraciones combinadas

## Resultado Esperado
Después de este fix:
- ✅ Las palabras en las celdas de tabla se mostrarán completas, sin cortes
- ✅ "Precio Internos" se mostrará como "Precio Internos" (sin "inter-nos")
- ✅ "Precio Externos" se mostrará como "Precio Externos" (sin "exter-nos")
- ✅ "12 semanas" se mostrará como "12 semanas" (sin "sema-nas")
- ✅ "Descuento" se mostrará como "Descuento" (sin "descuen-to")

## Compatibilidad
- ✅ **Desktop**: Las tablas mantienen su diseño original
- ✅ **Mobile**: Las tablas utilizan scroll horizontal (`overflow-x: auto`) para mantener el contenido sin cortes
- ✅ **Responsive**: El contenedor de las tablas ya tiene `overflow-x: auto`, permitiendo desplazamiento horizontal en pantallas pequeñas

## Testing Recomendado
1. Verificar en desktop que las tablas se muestran correctamente sin cortes de palabras
2. Verificar en tablet/mobile que el scroll horizontal funciona correctamente
3. Comprobar que todas las palabras en headers y celdas se muestran completas

## Archivos Modificados
- `newfile.py`: Agregado bloque CSS en líneas 754-759

## Fecha de Implementación
2025-01-XX (fecha actual)

## Referencias
- Issue relacionado: Corregir problema de palabras cortadas en tablas HTML
- Archivo de mejoras visuales: `INICIO_PAGE_IMPROVEMENTS.md`
- Archivo de responsive: `MOBILE_RESPONSIVENESS_IMPROVEMENTS.md`
