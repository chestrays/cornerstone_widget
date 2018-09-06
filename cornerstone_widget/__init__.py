from ._version import version_info, __version__

from .cs_widget import CornerstoneWidget, CornerstoneToolbarWidget


def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'cornerstone_widget',
        'require': 'cornerstone_widget/extension'
    }]
