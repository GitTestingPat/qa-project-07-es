"""
Métodos deprecados - mantener solo temporalmente.
TODO: Revisar para eliminar después de refactorizaciones.
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 

def click_add_card_confirm_button(self):
        """Hace clic en el botón 'Agregar' para confirmar la tarjeta"""
        
        # Activar el modal haciendo clic en el campo número de tarjeta
        try:
            card_number_field = self.driver.find_element(*self.CARD_NUMBER_INPUT)
            card_number_field.click()
            time.sleep(0.3)
            print("✅ Modal activado con clic en número de tarjeta.")
        except Exception as e:
            print(f"⚠️ No se pudo hacer clic en número de tarjeta: {e}")
        
        # Verificar si necesitamos cambiar a un iframe
        try:
            # Intentar encontrar el botón en el contexto actual
            button = self.driver.find_element(*self.ADD_CARD_CONFIRM_BUTTON)
            print("✅ Botón encontrado en contexto principal.")
        except Exception as e:
            # Si no se encuentra, buscar en iframes
            print(f"⚠️ Botón no encontrado en contexto principal, buscando en iframes...: {e}")
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")  
            print(f"🔍 Encontrados {len(iframes)} iframes")
            
            button_found = False
            for i, iframe in enumerate(iframes):
                try:
                    print(f"  Cambiando a iframe {i+1}...")
                    self.driver.switch_to.frame(iframe)
                    
                    # Intentar encontrar el botón dentro del iframe
                    button = self.driver.find_element(*self.ADD_CARD_CONFIRM_BUTTON)
                    print(f"✅ Botón encontrado en iframe {i+1}")
                    button_found = True
                    break
                except Exception as e:
                    # Volver al contexto principal y probar el siguiente iframe
                    self.driver.switch_to.default_content()
                    print(f"⚠️ No se encontró el botón en iframe {i+1}: {e}")
                    continue
            
            if not button_found:
                # Volver al contexto principal antes de lanzar error
                self.driver.switch_to.default_content()
                raise Exception("❌ No se pudo encontrar el botón 'Agregar' en ningún contexto")
        
        # Hacer clic en el botón
        try:
            # Esperar a que sea clickeable
            button = WebDriverWait(self.driver, 10).until( 
                EC.element_to_be_clickable(self.ADD_CARD_CONFIRM_BUTTON)  
            )
            
            # Scroll al botón (por si está fuera de vista)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(0.2)  
            
            button.click()
            print("✅ Botón 'Agregar' clickeado.")
            
        except Exception as e:
            print(f"⚠️ Error al hacer clic normal: {e}, intentando con JavaScript...")
            button = self.driver.find_element(*self.ADD_CARD_CONFIRM_BUTTON)
            self.driver.execute_script("arguments[0].click();", button)
            print("✅ Botón 'Agregar' clickeado con JavaScript.")
        
        finally:
            # IMPORTANTE: Volver al contexto principal
            self.driver.switch_to.default_content()
            print("✅ Vuelto al contexto principal.")