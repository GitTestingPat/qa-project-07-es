"""
Métodos auxiliares para debugging y troubleshooting.
No se usan en tests regulares pero son útiles para investigación.
"""

def debug_iframes(self):
    """Método temporal para detectar iframes en la página"""
    iframes = self.driver.find_elements(By.TAG_NAME, "iframe")  # noqa: F821
    print(f"\n🔍 Total de iframes encontrados: {len(iframes)}")
    
    for i, iframe in enumerate(iframes):
        print(f"\niframe {i+1}:")
        print(f"  - ID: {iframe.get_attribute('id')}")
        print(f"  - Name: {iframe.get_attribute('name')}")
        print(f"  - Class: {iframe.get_attribute('class')}")
        print(f"  - Src: {iframe.get_attribute('src')}")


def debug_modal_html(self):
    """Guarda el HTML completo del modal y muestra todos los botones"""
    print("\n🔍 === DEBUGGING MODAL ===")
    
    # Guardar HTML completo
    html_source = self.driver.page_source
    with open("debug_modal.html", "w", encoding="utf-8") as f:
        f.write(html_source)
    print("✅ HTML guardado en 'debug_modal.html'")
    
    # Buscar TODOS los botones
    buttons = self.driver.find_elements(By.TAG_NAME, "button")  # noqa: F821
    print(f"\n🔍 Total de botones encontrados: {len(buttons)}")
    
    for i, btn in enumerate(buttons):
        try:
            text = btn.text
            classes = btn.get_attribute("class")
            btn_type = btn.get_attribute("type")
            is_visible = btn.is_displayed()
            is_enabled = btn.is_enabled()
            disabled = btn.get_attribute("disabled")
            
            if is_visible or 'agregar' in text.lower() or 'add' in text.lower():
                print(f"\n📍 Botón {i+1}:")
                print(f"  Texto: '{text}'")
                print(f"  Clases: '{classes}'")
                print(f"  Type: '{btn_type}'")
                print(f"  Visible: {is_visible}")
                print(f"  Enabled: {is_enabled}")
                print(f"  Disabled attr: {disabled}")
        except Exception as e:
            print(f"  Error: {e}")
    
    # Buscar el modal específico
    try:
        modals = self.driver.find_elements(By.CLASS_NAME, "modal")  # noqa: F821
        print(f"\n🔍 Modales encontrados: {len(modals)}")
        for i, modal in enumerate(modals):
            if modal.is_displayed():
                print(f"\nModal {i+1} visible:")
                print(f"  Clases: {modal.get_attribute('class')}")
                # Buscar botones dentro del modal
                modal_buttons = modal.find_elements(By.TAG_NAME, "button")  # noqa: F821
                print(f"  Botones dentro: {len(modal_buttons)}")
                for j, mb in enumerate(modal_buttons):
                    print(f"    Botón {j+1}: '{mb.text}' - visible: {mb.is_displayed()}")
    except Exception as e:
        print(f"Error buscando modales: {e}")
