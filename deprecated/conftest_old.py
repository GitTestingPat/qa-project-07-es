"""
CÓDIGO OBSOLETO - NO USAR

Este archivo contiene código que fue removido de conftest.py
durante la refactorización del 2025-12-22.

Razón de remoción: Fixture nunca utilizada y código comentado innecesario.
"""

import pytest
from selenium import webdriver
from pages.urban_routes_page import UrbanRoutesPage
import data


# ============================================================================
# FIXTURE OBSOLETA: page_with_url_and_cdp
# ============================================================================
# Removida: 2025-12-22
# Razón: Ningún test la utiliza
# Líneas no cubiertas en coverage: 58-60 (0% coverage)
#
# CDP ya está habilitado por defecto en el fixture 'driver' principal,
# por lo que esta fixture duplica funcionalidad sin agregar valor.
#
# Alternativa: Usar la fixture 'page_with_url' existente
# ============================================================================

@pytest.fixture
def page_with_url_and_cdp(driver, data):
    """
    OBSOLETA: No usar
    
    Abre la URL base y retorna página con CDP habilitado.
    
    Problema:
    - CDP ya está habilitado en el driver base
    - Nunca fue utilizada por ningún test
    - Duplica funcionalidad de page_with_url
    
    Migración:
    --------
    # Antes:
    def test_ejemplo(page_with_url_and_cdp):
        # tu código aquí
    
    # Después:
    def test_ejemplo(page_with_url):
        # tu código aquí
        # CDP ya está habilitado por defecto
    """
    driver.get(data.BASE_URL)
    page = UrbanRoutesPage(driver)
    return page


# ============================================================================
# CÓDIGO COMENTADO REMOVIDO
# ============================================================================
# Las siguientes líneas estaban comentadas en el fixture 'driver'
# y fueron removidas porque no agregan valor:
#
# Línea 15-17 (comentado):
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
#
# Razón de remoción:
# - Código comentado por más de 1 mes
# - No se usa en producción
# - Genera confusión sobre si debe estar o no
# - Si se necesita en el futuro, puede obtenerse del historial de git
#
# Fecha de remoción: 2025-12-22
# ============================================================================


# ============================================================================
# NOTAS HISTÓRICAS
# ============================================================================
#
# Este archivo se mantiene solo para referencia. Si necesitas restaurar
# algún código, revisa primero si hay una alternativa mejor en utils/.
#
# Para configuraciones de Chrome: ver utils/browser_utils.py
# Para esperas: ver utils/wait_utils.py
# Para validaciones: ver utils/validation_utils.py
#
# ============================================================================
