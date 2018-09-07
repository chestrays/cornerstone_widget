#!/usr/bin/env bash
jupyter notebook --NotebookApp.token='' --no-browser --port 8765
casperjs tests/test_basic.js
