#!/usr/bin/env bash
PATH=$PATH:phantomjs-2.1.1-linux-x86_64/bin 
jupyter notebook --NotebookApp.token='' --no-browser --port 8765
node_modules/casperjs/bin/casperjs test tests/test_basic.js
