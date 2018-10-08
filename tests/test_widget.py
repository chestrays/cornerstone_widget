import numpy as np
import pytest
from ipywidgets.embed import embed_snippet

from cornerstone_widget import CornerstoneWidget, CornerstoneToolbarWidget
from cornerstone_widget.cs_widget import encode_numpy_b64
from cornerstone_widget.utils import _virtual_click_button


def test_encoding():
    with pytest.raises(ValueError):
        encode_numpy_b64(np.ones((4, 4, 2)))
    with pytest.raises(ValueError):
        encode_numpy_b64(np.ones((2, 3, 3)), rgb=True)
    with pytest.raises(ValueError):
        encode_numpy_b64(np.ones((2, 3)), rgb=True)


def test_ipy():
    c = CornerstoneWidget()
    c.update_image(np.ones((2, 1)))
    widget_state = c.get_state()
    assert widget_state['img_bytes'] == 'AAAAAA=='
    assert widget_state['img_width'] == 1
    assert widget_state['img_height'] == 2
    widget_html = embed_snippet(c)
    assert 'CornerstoneModel' in widget_html, 'Should contain widget code'
    assert 'cornerstone_widget' in widget_html, 'Should contain widget code'
    c.set_tool_state({'dog': 1})
    widget_state = c.get_state()
    assert widget_state['_tool_state_in'] == '{"dog": 1}'


def test_tools():
    c = CornerstoneWidget()
    c.select_tool('pan')
    widget_state = c.get_state()
    assert widget_state['_selected_tool'] == 'pan', 'Should be pan'
    with pytest.raises(NotImplementedError):
        c.select_tool('pane')
    with pytest.raises(NotImplementedError):
        c.update_image(np.zeros((3, 3, 3)))


def test_toolbar_tool():
    c = CornerstoneToolbarWidget()
    c.select_tool('pan')
    widget_state = c.cur_image_view.get_state()
    assert widget_state['_selected_tool'] == 'pan', 'Should be pan'

    # check toolbar
    for i in c._toolbar:
        cw = i.tooltip
        c.select_tool(cw)
        widget_state = c.cur_image_view.get_state()
        assert widget_state['_selected_tool'] == cw, 'Should be {}'.format(cw)

    with pytest.raises(NotImplementedError):
        c.select_tool('pane')
    with pytest.raises(NotImplementedError):
        c.update_image(np.zeros((3, 3, 3)))


def test_notoolbar():
    c = CornerstoneToolbarWidget(tools=[])
    assert len(c._toolbar) == 1
    start_but = c._toolbar[0]
    assert start_but.comm is not None, 'Should have something here'
    # click button
    _virtual_click_button(start_but)
    assert start_but.comm is None, 'Should be a dead button'


def test_toolbar_w_reset():
    cs_view = CornerstoneToolbarWidget(tools=['zoom',
                                              'probe', 'bbox', 'reset'])
    assert len(cs_view._toolbar) == 4


def test_invalid_toolbar():
    with pytest.raises(NotImplementedError):
        CornerstoneToolbarWidget(tools=['Magic_Lasso'])
