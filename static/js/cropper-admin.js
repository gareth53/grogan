window.$ = django.jQuery;

$(function() {
    'use strict';
    window.gusto = window.gusto || {};
    gusto.cropper = {
        $container: $('#image_container'),
        $asset: $('#displayed_image'),
        $cropper: null,
        orig_width: null,
        orig_height: null,
        zoom: {
            min: 0,
            max: 0,
            value: 0
        },
        crop: {
            width: 0,
            height: 0,
            max_x: 0,
            max_y: 0
        },

        init: function () {
            this.orig_width = this.$asset.width();
            this.orig_height = this.$asset.height();

            this.$cropper = $('<div id="cropper" style="background-image:url(' + this.$asset.attr("src") + ');left:0;top:0;"></div>');

            this.$container.append('<div class="image_mask"></div>').append(this.$cropper);

            this.set_image_dimensions();
            this.init_crop();
            this.init_zoomer();
        },

        set_image_dimensions: function () {
            var zoom = $('#id_zoom_ratio').val(),
                width = Math.round(this.orig_width * zoom),
                height = Math.round(this.orig_height * zoom);

            this.$asset.css({
                'width': width,
                'height': height
            });

        },

        init_crop: function () {
            var that = this,
                asset_type = $('#id_asset_type option:selected').text(),
                regExp = /\[([^)]+)\]/,
                matches = regExp.exec(asset_type),
                crop_dimensions = matches[1].split(' x ');

            this.crop.width = crop_dimensions[0];
            this.crop.height = crop_dimensions[1];
            this.crop.max_x = this.orig_width - this.crop.width;
            this.crop.max_y = this.orig_height - this.crop.height;

            this.$cropper.css({
                width: this.crop.width,
                height: this.crop.height
            });

            this.dragging = false;

            this.$cropper.on('mousedown', function(e) {
                var pos =  that.get_mouse_pos_in_img(e),
                    now_left = parseInt(that.$cropper.css('left'), 10),
                    now_top = parseInt(that.$cropper.css('top'), 10);

                that.$cropper.css('border-color', '#ff0');
                that.dragging = true;

                that.drag_offset = {
                    'x': pos.x - now_left,
                    'y': pos.y - now_top
                };
            });

            $(document).on('mouseup', function () {
                that.dragging = false;
                that.$cropper.css('border-color', '#fff');
            });

            $(document).on('mousemove', function (e) {
                // TODO: throttle
                if (that.dragging) {
                    var coords = that.get_mouse_pos_in_img(e);
                    that.move_cropper(coords.x - that.drag_offset.x, coords.y - that.drag_offset.y);
                }
            });
        },

        get_mouse_pos_in_img: function (e) {
            var posX = e.pageX,
                posY = e.pageY,
                img_coods = this.$asset[0].getBoundingClientRect();

            // TODO respect scroll position
            return {
                'x': posX - img_coods.left,
                'y': posY - img_coods.top
            };
        },

        move_cropper: function (left, top, zoom_w, zoom_h) {
            // move the cropper to a given co-ordinate and zoom
            left = left || parseInt(this.$cropper.css('left'), 10);
            top = top || parseInt(this.$cropper.css('top'), 10);

            // respect bounding box
            left = Math.min(left, this.crop.max_x);
            top = Math.min(top, this.crop.max_y);
            left = Math.max(0, left);
            top = Math.max(0, top);

            this.$cropper.css('left', left);
            this.$cropper.css('top', top);

            // update form values
            $('#id_crop_left').val(left);
            $('#id_crop_top').val(top);

            this.$cropper.css('background-position', -left + 'px ' + -top + 'px');

            if (zoom_w && zoom_h) {
                this.$cropper.css('background-size', zoom_w + 'px ' + zoom_h + 'px');
            }
        },

        init_zoomer: function () {
            this.zoom.min = this.get_min_zoom_width();
            this.zoom.max = this.$asset.width() * 1.5;
            this.zoom.value = this.$asset.width();
        },

        get_min_zoom_width: function () {
            var min_zoom =  Math.min((this.$asset.width() / this.crop.width), (this.$asset.height() / this.crop.height));

            return this.$asset.width() / min_zoom;
        }
    };

    gusto.cropper.init();
});