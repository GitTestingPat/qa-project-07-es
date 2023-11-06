# qa-project-07-es
# **UI Selenium automation project** 

Test de pruebas automatizadas para comprobar la funcionalidad de una app de transporte llamada Urban Routes. 

- Definición de localizadores y métodos utilizados en la clase UrbanRoutesPage
- Definición de las pruebas en la clase TestUrbanRoutes.
- Pruebas automatizadas que cubren el proceso completo de pedir un taxi:
- Configurar una dirección.
- Seleccionar una tarifa.
- Rellenar el campo número de teléfono con un número válido.
- Agregar una tarjeta de crédito válida.  
- Escribir un mensaje para el conductor.
- Realizar peticiones y servicios.
- Solicitar un taxi presionando el botón correspondiente.
- Esperar a que aparezca la información del conductor, matrícula y tiempo de espera en el modal.

# Verificación e Instalación de Python y Pytest

Este archivo detalla los pasos para verificar si Python está instalado en el entorno de desarrollo, cómo instalarlo si no lo está, y luego cómo verificar si pytest está instalado y cómo ejecutar pruebas utilizando pytest.

## Verificar la Instalación de Python

Para verificar si Python está instalado, abrir una terminal y ejecutar el siguiente comando:

* Abrir terminal en gitbash
Ejecutar el comando 'python --version'

Si Python está instalado, este comando mostrará la versión instalada. Si no está instalado, se mostrará un mensaje de error indicando que 'python' no se reconoce como un comando.

Instalación de Python

Si Python no está instalado, siga estos pasos para instalarlo:

Para Windows:

    Ir al sitio web oficial de Python: python.org.
    Descargar el instalador adecuado para su sistema operativo.
    Ejecutar el instalador y seguir las instrucciones en pantalla.

Para macOS:

Puede instalar Python usando Homebrew o descargando el instalador desde el sitio web oficial de Python.

brew install python

Para Linux:

La mayoría de las distribuciones de Linux ya incluyen Python. Puede instalarlo a través del gestor de paquetes de distribución. Por ejemplo, en Ubuntu y Debian:

sudo apt-get update
sudo apt-get install python3

Verificar la Instalación de Pytest

Para verificar si pytest está instalado, en la terminal, ejecutar:

pytest --version

Si pytest está instalado, mostrará la versión instalada. Si no está instalado, se mostrará un mensaje de error indicando que 'pytest' no se reconoce como un comando.

Si pytest no está instalado, puede instalarlo usando pip, el gestor de paquetes de Python.

pip install -U pytest

Ejecutar Pruebas con Pytest

Una vez que pytest esté instalado, puede ejecutar sus pruebas de la siguiente manera:

    Asegúrese de que está en el directorio donde se encuentran sus pruebas.
    Ejecutar el comando: pytest

Esto ejecutará todas las pruebas en el directorio actual y sus subdirectorios.

Recuerde que este es un ejemplo general. Los pasos pueden variar dependiendo de su sistema operativo y su configuración particular.


**
Esto debería proporcionar una guía clara para verificar la presencia de Python, instalarlo si es necesario, verificar la presencia de pytest y cómo ejecutar pruebas utilizando pytest una vez que esté instalado.




