# Función principal corregida
def main():
    aplicar_estilos()
    menu = mostrar_menu()
    
    # Mostrar cabecera en todas las páginas
    mostrar_cabecera()
    
    # Manejar la navegación
    if menu == "🏠 Inicio":
        pagina_inicio()
    elif menu == "👤 Sobre Mí":
        pagina_sobre_mi()
    elif menu == "🔬 Evaluaciones":
        pagina_evaluaciones()
    elif menu == "💼 Servicios":
        pagina_servicios()  # Necesitarás implementar esta función
    elif menu == "📞 Contacto":
        pagina_contacto()   # Necesitarás implementar esta función
    elif menu == "📊 Resultados":
        st.write("Página de resultados en desarrollo")
    
    # Mostrar footer en todas las páginas
    mostrar_footer()

# Añade estas funciones vacías temporalmente
def pagina_servicios():
    st.header("Nuestros Servicios")
    st.write("Contenido de servicios en desarrollo...")

def pagina_contacto():
    st.header("Contacto")
    st.write("Contenido de contacto en desarrollo...")
