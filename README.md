cornerstone_widget [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/chestrays/cornerstone_widget/master)
===============================

A Jupyter Widget for the Cornerstone Medical Image Viewing Library

Notebooks
----

The notebooks directory contains demo and tutorial
- https://mybinder.org/v2/gh/chestrays/cornerstone_widget/master?filepath=notebooks%2Fdemo.ipynb

Installation
------------

To install use pip:

    $ pip install cornerstone_widget
    $ jupyter nbextension enable --py --sys-prefix cornerstone_widget


For a development installation (requires npm),

    $ git clone https://github.com//cornerstone_widget.git
    $ cd cornerstone_widget
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix cornerstone_widget
    $ jupyter nbextension enable --py --sys-prefix cornerstone_widget
