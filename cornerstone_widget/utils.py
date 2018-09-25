import base64
from functools import wraps
from typing import Callable

import ipywidgets as ipw
import numpy as np


def button_debounce(enable_if_failed=False):
    # type: (...) -> Callable[[Callable[[ipw.Button], None]], Callable[[ipw.Button], None]]
    """
    disable a button until the callback completes
    :param enable_if_failed: enable the button if the callback fails
    :return:
    """

    def decorator(callback):
        # type: (Callable[[ipw.Button], None]) -> Callable[[ipw.Button], None]
        """
        :param callback:
        :return:
        """

        @wraps(callback)
        def wrapped_callback(button):
            # type: (ipw.Button) -> None
            button.disabled = True
            try:
                callback(button)
            except Exception as e:
                if enable_if_failed:
                    button.disabled = False
                raise Exception from e
            button.disabled = False

        return wrapped_callback

    return decorator


def encode_numpy_b64(in_img, rgb=False):
    # type: (np.ndarray, bool) -> str
    """
    Encode numpy arrays as b64 strings
    :param in_img:
    :return:
    >>> encode_numpy_b64(np.eye(2).astype(np.float32))
    'AQAAAAAAAQA='
    >>> encode_numpy_b64(np.eye(2).astype(np.uint16))
    'AQAAAAAAAQA='
    >>> encode_numpy_b64(np.zeros((2, 2, 4)), True)
    'AAAAAAAAAAAAAAAAAAAAAA=='
    """
    if rgb:
        if len(in_img.shape) != 3:
            raise ValueError('Image is not a color image: {}'.format(
                in_img.shape))
        if in_img.shape[2] != 4:
            raise ValueError('Images must be RGBA images 4 channels')

        img_bytes = in_img.astype(np.uint8).tobytes()
    else:
        if len(in_img.shape) != 2:
            raise ValueError('Short encoding requires 2D grayscale images')

        img_bytes = in_img.astype(np.uint16).tobytes()
    return base64.b64encode(img_bytes).decode()


def get_nested(a_dict, *args, default_value=None):
    """
    Safely gets items buried in a nested dictionary
    :param a_dict: nested dictionary to check
    :param args: the keys to navigate down
    :param default_value: if the items are not found in nested dict
    :return: Item or none
    >>> test_dict = {'a': {'b': {'c': 5}}}
    >>> get_nested(test_dict, 'a', 'b', 'c')
    5
    >>> get_nested(test_dict, 'a', 'd', default_value=10)
    10
    >>> get_nested(test_dict, 'a', 'b', 'c', 'd')
    >>> list_dict = {'a': [{}, {'b': 2}]}
    >>> get_nested(list_dict, 'a', 1, 'b')
    2
    """

    value = a_dict
    for arg in args:
        if isinstance(value, dict):
            if arg in value:
                value = value[arg]
            else:
                return default_value
        elif isinstance(value, list):
            if isinstance(arg, int):
                value = value[arg]
            else:
                return default_value
        else:
            return default_value
    return value


def get_bbox_handles(in_view_dict):
    """
    the bounding box info is buried in a lot of dictionaries
    :param in_view_dict: a dictionary with the list inside of it
    :return: dict with x, y for start and stop coordinates
    Something like [{'x': [553, 835], 'y': [449, 705]}]
    >>> bbox = {'imageIdToolState': 0}
    >>> get_bbox_handles(bbox)
    []
    """
    if isinstance(in_view_dict, dict):
        bbox_list = get_nested(in_view_dict,
                               'imageIdToolState',
                               '',
                               'rectangleRoi',
                               'data',
                               default_value=[])
    else:
        bbox_list = []
    bbox_handles = [bbox['handles'] for bbox in bbox_list if 'handles' in bbox]
    return [{x_var: [x.get(key, {}).get(x_var) for key in ['start', 'end']] for
             x_var in ['x', 'y']}
            for x in bbox_handles]


def _virtual_click_button(btn):
    # type: (ipw.Button) -> None
    """
    A standardized function for clicking buttons programatically
    :param btn:
    :return:
    """
    for c_callback in btn._click_handlers.callbacks:
        c_callback(btn)
