cornerstone_widget  [![Build Status](https://travis-ci.org/chestrays/cornerstone_widget.svg?branch=master)](https://travis-ci.org/chestrays/cornerstone_widget)  [![codecov](https://codecov.io/gh/chestrays/cornerstone_widget/branch/master/graph/badge.svg)](https://codecov.io/gh/chestrays/cornerstone_widget) [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/chestrays/cornerstone_widget/master)
===============================

A Jupyter Widget for the Cornerstone Medical Image Viewing Library

![Preview](preview.gif)

Overview
----
The widget lets you easily look at medical and similar images in the browser using the [CornerstoneJS](https://www.cornerstonejs.org/) library. The library offers lots of fancy functionality like zoom, windowing, panning, regions of interest, painting, polygons and beyond. Currently only a few of these features are implemented but feel free to make pull-requests or issues with suggestions

Notebooks
----

The notebooks directory contains demo and tutorial, you can use mybinder to get a quick feeling for what works well.
- https://mybinder.org/v2/gh/chestrays/cornerstone_widget/master?urlpath=apps%2Fnotebooks%2Fdemo.ipynb

Installation
------------

To install use pip:

    $ pip install git+https://github.com/chestrays/cornerstone_widget
    $ jupyter nbextension enable --py --sys-prefix cornerstone_widget


For a development installation (requires npm),

    $ git clone https://github.com//cornerstone_widget.git
    $ cd cornerstone_widget
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix cornerstone_widget
    $ jupyter nbextension enable --py --sys-prefix cornerstone_widget
    $ jupyter labextension install js
