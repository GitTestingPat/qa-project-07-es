
<img width="1600" height="899" alt="selenium_python_logo" src="https://github.com/user-attachments/assets/9f34af9f-95a3-43b1-ac0c-f0bda77f2300" />


# **UI Selenium Automation Project** 

## **Test de pruebas automatizadas para comprobar la funcionalidad de una app de transporte llamada Urban Routes**

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

![Static Badge](https://img.shields.io/badge/:badgeContent)

# **Verificación e Instalación de Python y Pytest**

Este archivo detalla los pasos para verificar si Python está instalado en el entorno de desarrollo, cómo instalarlo si no lo está, y luego cómo verificar si pytest está instalado y cómo ejecutar pruebas utilizando pytest.

## **Verificar la Instalación de Python en Windows**

Para verificar si Python está instalado, abrir una terminal de Gitbash y ejecutar el siguiente comando:

    Ejecutar el comando 'python --version' o si esto no funciona pruebe 'python3 --version'

Si no tiene instalado Gitbash puede descargarlo para Windows desde [aquí](https://git-scm.com/download/win) <br>
Aunque no es necesario descargar Gitbash para macOS debido a que ya está instalada una versión por defecto llamada "Terminal zsh", puede descargar Gitbash [aquí](https://git-scm.com/downloads) 

Si Python está instalado en su sistema, este comando mostrará la versión instalada. Si no está instalado, se mostrará un mensaje de error indicando que 'python' no se reconoce como un comando.

**Instalación de Python**

Si Python no está instalado, siga estos pasos para instalarlo:

**Para Windows:**

Ir al sitio web oficial de Python [aquí](https://www.python.org/downloads/windows/) <br>
Descargar el instalador adecuado para su sistema operativo. <br>
Ejecutar el instalador y seguir las instrucciones en pantalla.

**Para macOS:**

Puede instalar Python usando Homebrew desde la terminal:

    brew install python o si esto no funciona intente brew install python3

o descargando el instalador desde el sitio web oficial de Python [aquí](https://www.python.org/downloads/).

**Para Linux:**

La mayoría de las distribuciones de Linux ya incluyen Python. Puede instalarlo a través del gestor de paquetes de distribución. Por ejemplo, en Ubuntu y Debian. <br>
Ejecute en la terminal:

    sudo apt-get update
    sudo apt-get install python3

**Verificar la Instalación de Pytest**

Para verificar si pytest está instalado, en la terminal, ejecutar:

    pytest --version

Si pytest está instalado, mostrará la versión instalada. Si no está instalado, se mostrará un mensaje de error indicando que 'pytest' no se reconoce como un comando.

Si pytest no está instalado, puede instalarlo usando pip, el gestor de paquetes de Python.

    pip install -U pytest

**Ejecutar Pruebas con Pytest**

Una vez que pytest esté instalado, puede ejecutar sus pruebas de la siguiente manera:

    En la terminal, asegúrese que está dentro del directorio donde se están sus pruebas.
    Ejecute el comando: pytest

Esto ejecutará todas las pruebas en el directorio actual y sus subdirectorios.

Recuerde que este es un ejemplo general. Los pasos pueden variar dependiendo de su sistema operativo y su configuración particular.

Esto debería proporcionar una guía clara para verificar la presencia de Python, instalarlo si es necesario, verificar la presencia de pytest y cómo ejecutar pruebas utilizando pytest una vez que esté instalado.




