import ipywidgets as ipw
import pytest

from cornerstone_widget.utils import button_debounce, _virtual_click_button


def test_debounce():
    d_button = ipw.Button()

    @button_debounce
    def simple_callback(btn):
        assert btn.disabled, 'Button should be disabled'

    d_button.on_click(simple_callback)
    assert not d_button.disabled
    _virtual_click_button(d_button)
    assert not d_button.disabled


def test_debounce_fail():
    d_button = ipw.Button()

    @button_debounce(enable_if_failed=False)
    def fail_and_block(btn):
        assert btn.disabled, 'Button should be disabled'
        raise ValueError('Problematic')

    d_button.on_click(fail_and_block)
    assert not d_button.disabled
    with pytest.raises(Exception):
        _virtual_click_button(d_button)
    assert d_button.disabled


def test_debounce_fail_enable():
    d_button = ipw.Button()

    @button_debounce(enable_if_failed=True)
    def fail_and_release(btn):
        assert btn.disabled, 'Button should be disabled'
        raise ValueError('Problematic')

    d_button.on_click(fail_and_release)
    assert not d_button.disabled
    with pytest.raises(Exception):
        _virtual_click_button(d_button)
    assert not d_button.disabled
