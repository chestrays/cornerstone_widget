var cornerstone_widget = require('./index');
var base = require('@jupyter-widgets/base');

module.exports = {
  id: 'cornerstone_widget',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'cornerstone_widget',
          version: cornerstone_widget.version,
          exports: cornerstone_widget
      });
  },
  autoStart: true
};

