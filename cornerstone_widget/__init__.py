from ._version import version_info, __version__

from .cs_widget import CornerstoneWidget, CornerstoneToolbarWidget
from .utils import get_bbox_handles


def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'cornerstone_widget',
        'require': 'cornerstone_widget/extension'
    }]
