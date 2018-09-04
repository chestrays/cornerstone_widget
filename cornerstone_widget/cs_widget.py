import ipywidgets as widgets
import traitlets as tr
import base64
import numpy as np


def encode_numpy_b64(in_img):
    # type: (np.ndarray) -> str
    """
    Encode numpy arrays as b64 strings
    :param in_img:
    :return:
    >>> encode_numpy_b64(np.eye(2))
    'AAAAAAAA8D8AAAAAAAAAAAAAAAAAAAAAAAAAAAAA8D8='
    """
    return base64.b64encode(in_img.tobytes()).decode()


@widgets.register
class CornerstoneWidget(widgets.DOMWidget):
    """A simple cornerstone widget"""
    _view_name = tr.Unicode('CornerstoneView').tag(sync=True)
    _view_module = tr.Unicode('cornerstone_widget').tag(sync=True)
    _model_module_version = tr.Unicode('0.1.0').tag(sync=True)

    _model_name = tr.Unicode('CornerstoneModel').tag(sync=True)
    _model_module = tr.Unicode('cornerstone_widget').tag(sync=True)
    _view_module_version = tr.Unicode('0.1.0').tag(sync=True)

    title_field = tr.Unicode('Awesome Widget').tag(sync=True)
    img_bytes = tr.Unicode('AQAAAAAAAAABAAAAAAAAAAEA').tag(sync=True)
    img_width = tr.Int(3).tag(sync=True)
    img_height = tr.Int(3).tag(sync=True)
    img_min = tr.Float(0).tag(sync=True)
    img_max = tr.Float(255).tag(sync=True)
    img_scale = tr.Float(1.0).tag(sync=True)

    def update_image(self, in_image):
        # type: (CornerstoneWidget, np.ndarray) -> None
        """
        Update the image loaded in the widget
        """
        (self.img_width, self.img_height) = in_image.shape
        self.img_min = float(in_image.min())
        self.img_max = float(in_image.max())
        self.img_bytes = encode_numpy_b64(in_image)
        self.img_scale = 1.0
