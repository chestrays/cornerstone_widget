var widgets = require('@jupyter-widgets/base');
var _ = require('lodash');
var cs = require('cornerstone-core');
var cm = require('cornerstone-math');
var ctools = require('cornerstone-tools');


ctools.external.cornerstone = cs;
ctools.external.cornerstoneMath = cm;

// When serialiazing the entire widget state for embedding, only values that
// differ from the defaults will be specified.
var CornerstoneModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
        _model_name: 'CornerstoneModel',
        _view_name: 'CornerstoneView',
        _model_module: 'cornerstone_widget',
        _view_module: 'cornerstone_widget',
        _model_module_version: '0.1.0',
        _view_module_version: '0.1.0',
        img_bytes: '',
        img_scale: 1,
        img_width: 0,
        img_height: 0,
        img_min: 0,
        img_max: 1,
        _selected_tool: '',
        _tool_state_counter: '',
        _tool_state: ''
    })
});

function str2ab(str) {
    var buf = new ArrayBuffer(str.length * 2); // 2 bytes for each char
    var bufView = new Uint16Array(buf);
    var index = 0;
    for (var i = 0, strLen = str.length; i < strLen; i += 2) {
        var lower = str.charCodeAt(i);
        var upper = str.charCodeAt(i + 1);
        bufView[index] = lower + (upper << 8);
        index++;
    }
    return bufView;
}

function parsePixelData(base64PixelData, width, height) {
    var pixelDataAsString = window.atob(base64PixelData);
    var pixelData = str2ab(pixelDataAsString);
    return pixelData;
}

function disableContextMenu(e) {
    $(e).on('contextmenu', function (e) {
        e.preventDefault();
    });
}

var CornerstoneView = widgets.DOMWidgetView.extend({

    initialize: function () {
        this.viewer = document.createElement('div');
        var fv = $(this.viewer);
        disableContextMenu(this.viewer);
        fv.width('512px');
        fv.height('512px');
    },
    render: function () {
        this.el.appendChild(this.viewer);
        this.dicom_changed();
        this.model.on('change:img_bytes', this.dicom_changed, this);
        this.model.on('change:img_scale', this.zoom_changed, this);
        this.model.on('change:_tool_state', this.update_cs_state, this);
        this.model.on('change:_tool_state_counter', this.save_cs_state, this);
        this.model.on('change:_selected_tool', this.activate_tool, this);
    },
    parse_image: function (imageB64Data, width, height, min_val, max_val) {
        var imagePixelData = parsePixelData(imageB64Data);
        console.log('decoding: ' + width + 'x' + height + ' => ' + imagePixelData.length)

        function getPixelData() {
            return imagePixelData;
        }

        return {
            imageId: '',
            minPixelValue: 0,
            maxPixelValue: 65535,
            slope: (max_val - min_val) / 65535.0,
            intercept: min_val,
            windowCenter: 0.5 * (max_val + min_val),
            windowWidth: 0.5 * (max_val - min_val),
            getPixelData: getPixelData,
            rows: width,
            columns: height,
            height: height,
            width: width,
            color: false,
            columnPixelSpacing: 1.0,
            rowPixelSpacing: 1.0,
            sizeInBytes: height * width * 2
        };
    },
    dicom_changed: function () {
        var img_bytes = this.model.get('img_bytes');
        var img_width = this.model.get('img_width');
        var img_height = this.model.get('img_height');
        var img_min = this.model.get('img_min');
        var img_max = this.model.get('img_max');
        var out_img = this.parse_image(img_bytes, img_width, img_height, img_min, img_max);
        cs.enable(this.viewer);
        this.viewport = cs.getDefaultViewportForImage(this.viewer, out_img);
        console.log(out_img);
        cs.displayImage(this.viewer, out_img, this.viewport);
        this._setup_tools();
    },
    _setup_tools: function () {
        ctools.mouseInput.enable(this.viewer);
        ctools.mouseWheelInput.enable(this.viewer);
        ctools.wwwc.activate(this.viewer, 1); // Left Click
        ctools.pan.activate(this.viewer, 2); // Middle Click
        ctools.zoom.activate(this.viewer, 4); // Right Click
        ctools.zoomWheel.activate(this.viewer); // Mouse Wheel
    },
    _disable_all_tools: function (element) {
        // helper function used by the tool button handlers to disable the active tool
        // before making a new tool active
        ctools.wwwc.deactivate(element, 1);
        ctools.pan.deactivate(element, 2); // 2 is middle mouse button
        ctools.zoom.deactivate(element, 4); // 4 is right mouse button
        ctools.length.deactivate(element, 1);
        ctools.ellipticalRoi.deactivate(element, 1);
        ctools.rectangleRoi.deactivate(element, 1);
        ctools.angle.deactivate(element, 1);
        ctools.highlight.deactivate(element, 1);
        ctools.freehand.deactivate(element, 1);
        ctools.probe.deactivate(element, 1);

    },
    activate_tool: function () {
        var tool_name = this.model.get('_selected_tool');
        console.log('switching to tool: ' + tool_name);
        if (tool_name == 'reset') {
            this._disable_all_tools(this.viewer);
            cs.reset(this.viewer);
            ctools.appState.restore({});
            this._setup_tools();
        } else {
            this._disable_all_tools(this.viewer);
            if (tool_name == 'zoom') {
                ctools.zoom.activate(this.viewer, 1);
            }
            if (tool_name == 'window') {
                ctools.wwwc.activate(this.viewer, 1);
            }
            if (tool_name == 'pan') {
                ctools.pan.activate(this.viewer, 1);
                ctools.zoom.activate(this.viewer, 2);
            }
            if (tool_name == 'bbox') {
                ctools.rectangleRoi.enable(this.viewer);
                ctools.rectangleRoi.activate(this.viewer, 1);
            }
            if (tool_name == 'probe') {
                ctools.probe.enable(this.viewer);
                ctools.probe.activate(this.viewer, 1);
            }
            if (tool_name == 'highlight') {
                ctools.highlight.enable(this.viewer);
                ctools.highlight.activate(this.viewer, 1);
            }
            if (tool_name == 'freehand') {
                ctools.freehand.enable(this.viewer);
                ctools.freehand.activate(this.viewer, 1);
            }
        }

    },
    save_cs_state: function () {
        var appState = ctools.appState.save([this.viewer]);
        var appStr = JSON.stringify(appState);
        console.log('State is:' + appStr);
        this.model.set('_tool_state', appStr);
        this.model.save_changes();
    },
    update_cs_state: function () {
        var new_state_json = this.model.get('_tool_state');
        if (new_state_json.length > 1) {
            var appState = JSON.parse(new_state_json);
            console.log('updating state:' + new_state_json + ', ' + new_state_json.length);
            ctools.appState.restore(appState);
        }
    },
    zoom_changed: function () {
        this.viewport.scale = this.model.get('img_scale');
        cs.setViewport(this.viewer, this.viewport);
    }
});

module.exports = {
    CornerstoneModel: CornerstoneModel,
    CornerstoneView: CornerstoneView
};
