import json
from typing import Dict

import ipywidgets as widgets
import numpy as np
import traitlets as tr
from IPython.display import display

from .utils import encode_numpy_b64

MIN_RANGE = 1  # the minimum max-min value (prevent dividing by 0)


@widgets.register
class CornerstoneWidget(widgets.DOMWidget):
    """
    A widget for viewing 2D images with zoom and windowing support
    >>> cs = CornerstoneWidget()
    >>> cs.update_image(np.eye(3))
    >>> cs.get_state()['img_bytes']
    '//8AAAAAAAD//wAAAAAAAP//'
    >>> cs.select_tool('pan')
    >>> cs.get_tool_state()
    {}
    """

    _view_name = tr.Unicode('CornerstoneView').tag(sync=True)
    _view_module = tr.Unicode('cornerstone_widget').tag(sync=True)
    _model_module_version = tr.Unicode('0.1.0').tag(sync=True)

    _model_name = tr.Unicode('CornerstoneModel').tag(sync=True)
    _model_module = tr.Unicode('cornerstone_widget').tag(sync=True)
    _view_module_version = tr.Unicode('0.1.0').tag(sync=True)

    img_bytes = tr.Unicode('AQAAAAAAAAABAAAAAAAAAAEA').tag(sync=True)
    img_width = tr.Int(3).tag(sync=True)
    img_height = tr.Int(3).tag(sync=True)
    img_min = tr.Float(0).tag(sync=True)
    img_max = tr.Float(255).tag(sync=True)
    img_scale = tr.Float(1.0).tag(sync=True)
    img_color = tr.Bool(False).tag(sync=True)
    _tool_state_in = tr.Unicode('').tag(sync=True)
    _tool_state_out = tr.Unicode('').tag(sync=True)
    _selected_tool = tr.Unicode('').tag(sync=True)

    VALID_TOOLS = ['zoom',
                   'pan',
                   'freehand',
                   'bbox',
                   'probe',
                   'reset',
                   'window',
                   'highlight'
                   ]

    def update_image(self, in_image):
        # type: (CornerstoneWidget, np.ndarray) -> None
        """
        Update the image loaded in the widget
        """
        self.img_height = in_image.shape[0]
        self.img_width = in_image.shape[1]
        if len(in_image.shape) == 2:
            self.img_min = float(in_image.min())
            self.img_max = float(in_image.max())
            self.img_color = False
            rs_image = (in_image - self.img_min)
            im_range = self.img_max - self.img_min
            MIN_RANGE = 1
            if im_range < MIN_RANGE:
                self.img_max = self.img_min + MIN_RANGE
                im_range = MIN_RANGE
            rs_image *= (2 ** 16 - 1) / im_range
            self.img_bytes = encode_numpy_b64(rs_image)
        elif len(in_image.shape) == 3:
            if in_image.shape[2] != 4:
                raise NotImplementedError('Images must be RGBA')
            self.img_color = True
            self.img_min = 0
            self.img_max = 255
            self.img_bytes = encode_numpy_b64(
                in_image.clip(0, 255).astype(np.uint8), rgb=True)
        self.img_scale = 1.0

    def select_tool(self, tool_name):
        # type: (str) -> None
        """
        The tool to select in the cornerstone widget
        :param tool_name:  can be reset, zoom, window, pan, probe, bbox
        :return:
        >>> cs = CornerstoneWidget()
        >>> cs.select_tool('pan')
        >>> cs.get_state()['_selected_tool']
        'pan'
        """
        tool_name = tool_name.lower().strip()
        if tool_name not in self.VALID_TOOLS + ['', 'none']:
            raise NotImplementedError('{} tool is not available'.format(
                tool_name))
        self._selected_tool = tool_name

    def get_tool_state(self):
        # type: () -> Dict
        """Get the state of all the tools as a dictionary"""
        if len(self._tool_state_out) > 0:
            return json.loads(self._tool_state_out)
        else:
            return {}

    def set_tool_state(self, state):
        """A method for feeding data into the widget"""
        self._tool_state_in = json.dumps(state)


class WidgetObject:
    """class to make non-widgets seem more widgety"""

    def __init__(self, widget_obj):
        self._widget_obj = widget_obj

    def get_widget(self):
        return self._widget_obj

    def _ipython_display_(self):
        display(self.get_widget())


class CornerstoneToolbarWidget(WidgetObject):
    """
    A slightly more fancy version of cornerstone with a toolbar
    >>> cs = CornerstoneToolbarWidget()
    >>> cs.update_image(np.ones((3,2)))
    """
    # a dictionary of tool name to toolbar button properties
    TOOLS = {'pan': dict(icon='arrows', description='Pan'),
             'window': dict(icon='adjust', description='Window'),
             'zoom': dict(icon='search-plus', description='Zoom'),
             'probe': dict(icon='info-circle', description='Probe'),
             'bbox': dict(icon='edit', description='Bounding Box')
             }

    def __init__(self, buttons_per_row=3,
                 tools=['pan', 'window', 'zoom', 'probe']):
        self.cur_image_view = CornerstoneWidget()

        self._empty_data = np.zeros((3, 3))
        self._cur_image_data = np.ones((1, 1))
        
        refresh_but = widgets.Button(description="Start",
                                     icon="play",
                                     button_style="success"
                                     )
        # We use the refresh button as a "start" button to
        # show the first image and then replace the on_click
        # handler after the first click

        def _first_click(button):
            button.description = "Reset"
            button.icon = "refresh"
            button.button_style = ""
            self._refresh_image()
            button._click_handlers.callbacks.pop()
            button.on_click(
                lambda b: self._refresh_image()
            )
        refresh_but.on_click(_first_click)

        self._toolbar = [refresh_but]

        def _button_switch_callback(in_str):
            """we need an extra layer of separation so the callbacks work"""

            def _callback(*args, **kwargs):
                self.select_tool(in_str)

            return _callback

        for name in tools:
            c_but = widgets.Button(tooltip=name, **self.TOOLS[name])
            c_but.on_click(_button_switch_callback(name))
            self._toolbar += [c_but]

        c_toolbar = []
        c_row = []
        for i, c_but in enumerate(self._toolbar, 1):
            c_row += [c_but]
            if (i % buttons_per_row) == 0:
                c_toolbar += [widgets.HBox(c_row)]
                c_row = []
        if len(c_row) > 0:
            c_toolbar += [widgets.HBox(c_row)]

        panel = widgets.VBox(c_toolbar + [self.cur_image_view])

        super().__init__(panel)

    def update_image(self, in_image):
        self._cur_image_data = in_image
        self.cur_image_view.update_image(self._cur_image_data)
        self.select_tool('')
        self.select_tool('reset')

    def select_tool(self, tool_name):
        """
        Set the tool to use with the widget
        :param tool_name:
        :return:
        """
        self.cur_image_view.select_tool(tool_name)

    def _refresh_image(self):
        self.cur_image_view.update_image(self._empty_data)
        self.cur_image_view.update_image(self._cur_image_data)
        self.cur_image_view.select_tool('reset')

    def get_state(self):
        return self.cur_image_view.get_tool_state()
