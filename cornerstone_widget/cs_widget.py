import base64

import ipywidgets as widgets
import numpy as np
import traitlets as tr


def encode_numpy_b64(in_img):
    # type: (np.ndarray) -> str
    """
    Encode numpy arrays as b64 strings
    :param in_img:
    :return:
    >>> encode_numpy_b64(np.eye(2).astype(np.float32))
    'AQAAAAAAAQA='
    >>> encode_numpy_b64(np.eye(2).astype(np.uint16))
    'AQAAAAAAAQA='
    """
    u16_img = in_img.astype(np.uint16).tobytes()
    return base64.b64encode(u16_img).decode()


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

        rs_image = (in_image - self.img_min)
        im_range = self.img_max - self.img_min
        MIN_RANGE = 1
        if im_range < MIN_RANGE:
            self.img_max = self.img_min + MIN_RANGE
            im_range = MIN_RANGE
        rs_image *= (2 ** 16 - 1) / im_range
        self.img_bytes = encode_numpy_b64(rs_image)
        self.img_scale = 1.0
