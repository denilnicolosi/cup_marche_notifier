"""
Tests for is_slots_available().

The bug this covers: the original code passed EC.text_to_be_present_in_element(...)
directly to an `if` statement. That function returns a *callable*, not a bool,
so the condition was always True — the monitor never detected available slots.
"""
from unittest.mock import MagicMock

import pytest

from prenotazione import is_slots_available

_RESULT_XPATH = "/html/body/div[3]/div[4]/div[1]/h3"


def _driver_with_text(text: str) -> MagicMock:
    driver = MagicMock()
    driver.find_element.return_value.text = text
    return driver


def test_no_slots_when_nessun_risultato_trovato():
    driver = _driver_with_text("Nessun risultato trovato")
    assert is_slots_available(driver) is False


def test_slots_available_when_different_heading():
    driver = _driver_with_text("Risultati trovati: 3 disponibilità")
    assert is_slots_available(driver) is True


def test_slots_available_when_heading_is_empty():
    driver = _driver_with_text("")
    assert is_slots_available(driver) is True


def test_reads_correct_xpath():
    driver = _driver_with_text("Nessun risultato trovato")
    is_slots_available(driver)
    driver.find_element.assert_called_once_with(
        pytest.importorskip("selenium.webdriver.common.by").By.XPATH,
        _RESULT_XPATH,
    )
