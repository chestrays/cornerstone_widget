var widgets = require('@jupyter-widgets/base');
var _ = require('lodash');
var cs = require('cornerstone-core');
var cm = require('cornerstone-math');
var ctools = require('cornerstone-tools');
var hammerjs = require('hammerjs');

ctools.external.cornerstone = cs;
ctools.external.cornerstoneMath = cm;
ctools.external.Hammer = hammerjs.Hammer;

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
        title_field: 'Cornerstone Widget',
        img_bytes: '',
        img_scale: 1,
        img_width: 0,
        img_height: 0,
        img_min: 0,
        img_max: 1
    })
});

var CornerstoneView = widgets.DOMWidgetView.extend({

    render: function () {
        this.message = document.createElement('div')
        this.viewer = document.createElement('div')
        var fv = $(this.viewer)
        fv.width('512px');
        fv.height('512px');
        // Enable our tools
        this.el.appendChild(this.message);
        this.el.appendChild(this.viewer);
        this.model.on('change:img_bytes', this.dicom_changed, this);
        this.model.on('change:img_scale', this.zoom_changed, this);
        this.model.on('change:title_field', this.message_changed, this);
    },

    parse_image: function (imageB64Data, width, height, min_val, max_val) {
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

        var imagePixelData = parsePixelData(imageB64Data);
        console.log('decoding: ' + width + 'x' + height + ' => ' + imagePixelData.length)

        function getPixelData() {
            return imagePixelData;
        }

        return {
            imageId: '',
            minPixelValue: 0,
            maxPixelValue: 65535,
            slope: (max_val-min_val)/65535.0,
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

    message_changed: function () {
        this.message.textContent = this.model.get('title_field');
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
        ctools.mouseInput.enable(this.viewer);
        ctools.mouseWheelInput.enable(this.viewer);
        ctools.wwwc.activate(this.viewer, 1); // Left Click
        ctools.pan.activate(this.viewer, 2); // Middle Click
        ctools.zoom.activate(this.viewer, 4); // Right Click
        ctools.zoomWheel.activate(this.viewer); // Mouse Wheel
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
