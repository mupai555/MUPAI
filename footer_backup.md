# Footer Institucional - Backup Completo
**Fecha de extracción:** 2025-01-23  
**Archivo origen:** newfile.py  
**Propósito:** Respaldar toda la información del footer institucional para futura regeneración profesional

---

## 📋 Índice de Contenidos
1. [Función Principal del Footer](#función-principal-del-footer)
2. [CSS Completo del Footer](#css-completo-del-footer)
3. [Funciones de Carga de Logos](#funciones-de-carga-de-logos)
4. [Enlaces y Contenido](#enlaces-y-contenido)
5. [Estructura HTML](#estructura-html)
6. [Información para Regeneración](#información-para-regeneración)

---

## 🔧 Función Principal del Footer

```python
def mostrar_footer_institucional():
    """
    Displays the institutional footer with logos, social media links and copyright.
    Responsive design for all devices.
    """
    # Load logos
    logo_mupai = load_mupai_logo_base64()
    logo_mup = load_muscle_up_logo_base64()
    
    st.markdown("""
    <div class="institutional-footer">
        <div class="footer-content">
            <!-- Left Logo -->
            <div class="footer-logo-left">
    """, unsafe_allow_html=True)
    
    if logo_mupai:
        st.markdown(f"""
                <img src="{logo_mupai}" alt="LOGO MUPAI" class="footer-logo-img">
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
                <div class="footer-logo-fallback">
                    <h3>💪 MUPAI</h3>
                </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
            </div>
            
            <!-- Center Social Media Icons -->
            <div class="footer-center">
                <div class="footer-social-icons">
                    <a href="https://wa.me/528662580594" target="_blank" class="footer-social-link whatsapp">
                        <span class="footer-icon">📱</span>
                        <span class="footer-icon-text">WhatsApp</span>
                    </a>
                    <a href="mailto:administracion@muscleupgym.fitness" class="footer-social-link email">
                        <span class="footer-icon">📧</span>
                        <span class="footer-icon-text">Email</span>
                    </a>
                    <a href="https://www.facebook.com/share/16WtR5TLw5/" target="_blank" class="footer-social-link facebook">
                        <span class="footer-icon">📘</span>
                        <span class="footer-icon-text">Facebook</span>
                    </a>
                    <a href="https://www.instagram.com/mup_lindavista" target="_blank" class="footer-social-link instagram">
                        <span class="footer-icon">📷</span>
                        <span class="footer-icon-text">Instagram</span>
                    </a>
                    <a href="https://muscleupgym.fitness/planes" target="_blank" class="footer-social-link website">
                        <span class="footer-icon">🌐</span>
                        <span class="footer-icon-text">Web</span>
                    </a>
                </div>
                <div class="footer-copyright">
                    © 2025 MUPAI - Muscle up GYM Digital Training Science Performance Assessment Intelligence<br>
                    © 2025 MUPAI - Muscle up GYM Digital Nutrition Science Alimentary Pattern Assessment Intelligence
                </div>
            </div>
            
            <!-- Right Logo -->
            <div class="footer-logo-right">
    """, unsafe_allow_html=True)
    
    if logo_mup:
        st.markdown(f"""
                <img src="{logo_mup}" alt="LOGO MUP" class="footer-logo-img">
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
                <div class="footer-logo-fallback">
                    <h3>🏋️ MUP</h3>
                </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
```

**Líneas originales en newfile.py:** 1802-1889

---

## 🎨 CSS Completo del Footer

```css
/* ========================================================================== */
/* INSTITUTIONAL FOOTER STYLES */
/* ========================================================================== */

.institutional-footer {
    background: #000000 !important;
    border-top: 3px solid #FFCC00 !important;
    padding: 2.5rem 0 !important;
    margin-top: 4rem !important;
    box-shadow: 0 -5px 15px rgba(255,204,0,0.2) !important;
    width: 100vw !important;
    position: relative !important;
    left: 50% !important;
    right: 50% !important;
    margin-left: -50vw !important;
    margin-right: -50vw !important;
    box-sizing: border-box !important;
}

.footer-content {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    max-width: 1200px !important;
    margin: 0 auto !important;
    gap: 2rem !important;
    min-height: 100px !important;
    padding: 0 1rem !important;
    box-sizing: border-box !important;
}

.footer-logo-left, .footer-logo-right {
    flex: 0 0 auto;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 140px;
    height: 100px;
}

.footer-logo-img {
    max-width: 120px;
    max-height: 80px;
    width: auto;
    height: auto;
    object-fit: contain;
    display: block;
}

.footer-logo-fallback {
    color: #FFCC00;
    text-align: center;
    font-weight: bold;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.footer-center {
    flex: 1;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.footer-social-icons {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-bottom: 1rem;
    flex-wrap: wrap;
}

.footer-social-link {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    text-decoration: none !important;
    color: #FFCC00 !important;
    transition: all 0.3s ease !important;
    padding: 0.5rem !important;
    border-radius: 8px !important;
}

.footer-social-link:hover {
    background-color: rgba(255,204,0,0.1) !important;
    transform: translateY(-2px) !important;
    color: #FFD700 !important;
}

.footer-icon {
    font-size: 1.8rem;
    margin-bottom: 0.3rem;
}

.footer-icon-text {
    font-size: 0.9rem;
    font-weight: 500;
}

.footer-copyright {
    color: #FFFFFF !important;
    font-size: 0.95rem !important;
    line-height: 1.4 !important;
    font-weight: 500 !important;
    max-width: 600px !important;
    margin: 0 auto !important;
    text-align: center !important;
    word-wrap: break-word !important;
    hyphens: auto !important;
    overflow-wrap: break-word !important;
}

/* Mobile footer responsiveness */
@media (max-width: 768px) {
    .institutional-footer {
        padding: 2rem 0 !important;
    }
    
    .footer-content {
        flex-direction: column !important;
        text-align: center !important;
        gap: 1.5rem !important;
        min-height: auto !important;
        padding: 0 1rem !important;
    }
    
    .footer-logo-left, .footer-logo-right {
        width: 120px !important;
        height: 80px !important;
        order: 2 !important;
    }
    
    .footer-center {
        order: 1 !important;
        width: 100% !important;
    }
    
    .footer-social-icons {
        gap: 1rem !important;
    }
    
    .footer-social-link {
        min-width: 70px;
    }
    
    .footer-icon {
        font-size: 1.5rem;
    }
    
    .footer-icon-text {
        font-size: 0.8rem;
    }
    
    .footer-copyright {
        font-size: 0.85rem;
        padding: 0 1rem;
        max-width: 100%;
        line-height: 1.3;
    }
    
    .footer-logo-img {
        max-width: 100px;
        max-height: 60px;
    }
    
    /* Stack logos horizontally on mobile */
    .institutional-footer .footer-content {
        display: flex;
        flex-direction: column;
    }
    
    .footer-logos-mobile {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        max-width: 300px;
        margin: 0 auto;
        order: 3;
    }
}

@media (max-width: 480px) {
    .institutional-footer {
        padding: 1.5rem 0;
    }
    
    .footer-content {
        padding: 0 0.5rem;
    }
    
    .footer-social-icons {
        gap: 0.8rem;
    }
    
    .footer-social-link {
        min-width: 60px;
        padding: 0.3rem;
    }
    
    .footer-icon {
        font-size: 1.3rem;
    }
    
    .footer-icon-text {
        font-size: 0.75rem;
    }
    
    .footer-copyright {
        font-size: 0.8rem;
        padding: 0 0.5rem;
        line-height: 1.2;
    }
    
    .footer-logo-left, .footer-logo-right {
        width: 100px;
        height: 60px;
    }
    
    .footer-logo-img {
        max-width: 80px;
        max-height: 50px;
    }
    
    .footer-logo-img {
        max-width: 80px;
        max-height: 50px;
    }
}
```

**Líneas originales en newfile.py:** 1475-1695

---

## 🖼️ Funciones de Carga de Logos

### Función load_mupai_logo_base64()
```python
def load_mupai_logo_base64():
    """
    Loads the MUPAI logo image and returns it as base64 encoded string.
    Returns None if the image file is not found.
    """
    logo_image_path = 'LOGO MUPAI.png'
    
    try:
        with open(logo_image_path, 'rb') as f:
            image_data = f.read()
            encoded_image = base64.b64encode(image_data).decode()
            return f'data:image/png;base64,{encoded_image}'
    except FileNotFoundError:
        return None
    except Exception as e:
        return None
```

### Función load_muscle_up_logo_base64()
```python
def load_muscle_up_logo_base64():
    """
    Loads the Muscle Up Gym logo image and returns it as base64 encoded string.
    Returns None if the image file is not found.
    """
    logo_image_path = 'LOGO MUP.png'
    
    try:
        with open(logo_image_path, 'rb') as f:
            image_data = f.read()
            encoded_image = base64.b64encode(image_data).decode()
            return f'data:image/png;base64,{encoded_image}'
    except FileNotFoundError:
        return None
    except Exception as e:
        return None
```

**Líneas originales en newfile.py:** 118-133 y 101-116

---

## 🔗 Enlaces y Contenido

### Enlaces de Redes Sociales
- **WhatsApp:** https://wa.me/528662580594
- **Email:** mailto:administracion@muscleupgym.fitness
- **Facebook:** https://www.facebook.com/share/16WtR5TLw5/
- **Instagram:** https://www.instagram.com/mup_lindavista
- **Website:** https://muscleupgym.fitness/planes

### Iconos Utilizados
- **WhatsApp:** 📱
- **Email:** 📧
- **Facebook:** 📘
- **Instagram:** 📷
- **Website:** 🌐

### Texto de Copyright
```
© 2025 MUPAI - Muscle up GYM Digital Training Science Performance Assessment Intelligence
© 2025 MUPAI - Muscle up GYM Digital Nutrition Science Alimentary Pattern Assessment Intelligence
```

### Textos de Fallback para Logos
- **MUPAI:** 💪 MUPAI
- **MUP:** 🏋️ MUP

---

## 🏗️ Estructura HTML

### Layout Principal
```html
<div class="institutional-footer">
    <div class="footer-content">
        <!-- Left Logo Section -->
        <div class="footer-logo-left">
            <!-- MUPAI Logo or Fallback -->
        </div>
        
        <!-- Center Content Section -->
        <div class="footer-center">
            <!-- Social Media Icons -->
            <div class="footer-social-icons">
                <!-- 5 Social Links -->
            </div>
            <!-- Copyright Text -->
            <div class="footer-copyright">
                <!-- Company Copyright -->
            </div>
        </div>
        
        <!-- Right Logo Section -->
        <div class="footer-logo-right">
            <!-- MUP Logo or Fallback -->
        </div>
    </div>
</div>
```

### Llamada de la Función
**Línea original:** 3893
```python
# ==================== INSTITUTIONAL FOOTER ====================
# Display footer on all pages
mostrar_footer_institucional()
```

---

## 🔄 Información para Regeneración

### Dependencias Requeridas
- `streamlit` - Para st.markdown()
- `base64` - Para codificación de imágenes

### Archivos de Imágenes Necesarios
- `LOGO MUPAI.png` - Logo principal de MUPAI
- `LOGO MUP.png` - Logo de Muscle Up Gym

### Características del Diseño
1. **Responsive:** Diseño adaptable para móviles y escritorio
2. **Full Width:** Usa 100vw para expandirse a todo el ancho
3. **Three Column Layout:** Logo izquierdo, contenido central, logo derecho
4. **Hover Effects:** Efectos de hover en enlaces sociales
5. **Fallback Support:** Texto alternativo si no cargan las imágenes

### Colores del Tema
- **Background:** #000000 (Negro)
- **Primary Accent:** #FFCC00 (Amarillo mostaza)
- **Secondary Accent:** #FFD700 (Oro)
- **Text:** #FFFFFF (Blanco)

### Posicionamiento
- **Desktop:** Layout horizontal de 3 columnas
- **Tablet:** Layout vertical con logos ordenados
- **Mobile:** Layout vertical compacto

---

## 📝 Notas de Eliminación

**Fecha de eliminación:** 2025-01-23  
**Motivo:** Limpieza de interfaz visual antes de regeneración profesional  
**Componentes eliminados:**
1. Función `mostrar_footer_institucional()` (líneas 1802-1889)
2. CSS del footer institucional (líneas 1475-1695)
3. Llamada de la función (línea 3893)
4. Comentario asociado (líneas 3891-3892)

**Funciones de logos conservadas:** Las funciones `load_mupai_logo_base64()` y `load_muscle_up_logo_base64()` permanecen en el código ya que pueden ser utilizadas en otras partes de la aplicación.

---

## ⚠️ Advertencias para Regeneración

1. **Mantener responsive design** para garantizar funcionamiento en móviles
2. **Conservar estructura de 3 columnas** para mantener identidad visual
3. **Verificar existencia de archivos de logos** antes de implementar
4. **Probar en múltiples dispositivos** después de la regeneración
5. **Mantener accesibilidad** con alt tags apropiados
6. **Verificar todos los enlaces** antes de poner en producción

---

**Este backup contiene toda la información necesaria para regenerar profesionalmente el footer institucional de MUPAI.**