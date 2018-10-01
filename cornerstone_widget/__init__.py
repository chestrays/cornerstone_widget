from .cs_widget import CornerstoneWidget, CornerstoneToolbarWidget
from .utils import get_bbox_handles


def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'cornerstone_widget',
        'require': 'cornerstone_widget/extension'
    }]

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
