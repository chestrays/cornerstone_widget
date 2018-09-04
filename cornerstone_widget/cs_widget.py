import ipywidgets as widgets
import traitlets as tr

@widgets.register
class CornerstoneWidget(widgets.DOMWidget):
    """A simple cornerstone widget"""
    view_name = tr.Unicode('CornerstoneWidget').tag(sync=True)
    _view_module = tr.Unicode('cs_widget').tag(sync=True)
    _view_module_version = tr.Unicode('0.1.0').tag(sync=True)
    title_field = tr.Unicode('Awesome Widget').tag(sync=True)
    img_bytes = tr.Unicode('AQAAAAAAAAABAAAAAAAAAAEA').tag(sync=True)
    img_width = tr.Int(3).tag(sync=True)
    img_height= tr.Int(3).tag(sync=True)
    img_min = tr.Float(0).tag(sync=True)
    img_max = tr.Float(255).tag(sync=True)
    img_scale = tr.Float(1.0).tag(sync=True)

    def update_image(self, in_image):
        (self.img_width, self.img_height) = in_image.shape
        self.img_min = in_image.min()
        self.img_max = in_image.max()
        self.img_bytes = ja.cornerstone.encode_numpy_b64(in_image)
        self.img_scale=1.0
