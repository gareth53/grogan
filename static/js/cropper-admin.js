window.$ = django.jQuery;

/*
    TODO:
    - Handle if the specified crop is larger than the asset we're working with
 */


$(function () {
    'use strict';
    window.gusto = window.gusto || {};
    gusto.cropper = {
        $container: $('#image_container'),
        $asset: $('#displayed_image'),
        $zoomer: $('#zoomer'),
        $cropper: null,
        orig_ratio: 1,
        orig_width: 0,
        orig_height: 0,
        disp_width: 0,
        disp_height: 0,
        zoomer: {
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

        areas: {},

        init: function () {
            this.orig_width = this.$asset.width();
            this.orig_height = this.$asset.height();
            this.orig_ratio = $('#id_zoom_ratio').val();

            this.disp_width = this.orig_width * this.orig_ratio;
            this.disp_height = this.orig_height * this.orig_ratio;

            this.$cropper = $('<div id="cropper" style="background-image:url(' + this.$asset.attr("src") + ');left:0;top:0;"></div>');

            // this.$container.append('<div class="image_mask"></div>').append(this.$cropper);

            this.set_image_dimensions();
            this.init_crop();
            this.init_zoomer();

            this.init_hack();
        },

        init_hack: function () {
            var that = this;
            this.drag = false;
            this.on_focus = false;
            this.current_focus = {};

            this.$container.on('mousedown', function (e) {
                if (that.is_left_button(e)) {
                    that.on_focus = that.is_on_focus_area(e);
                    that.drag = true;
                    if (!that.on_focus) {
                        that.create_focus_area(that.get_mouse_pos_in_img(e));
                    }
                }
            });

            this.$container.on('mousemove', function (e) {
                if (that.drag) {
                    var pos = that.get_mouse_pos_in_img(e);
                    if (that.on_focus) {
                        that.move_focus_area(pos)
                    } else {
                        that.update_focus_area_dims(pos);
                    }                    
                }
            });

            this.$container.on('mouseup', function (e) {
                that.drag = false;
                that.on_focus = false;
                that.current_focus = '';
                console.log(that.areas);
            });
        },

        move_focus_area: function (pos) {
            console.log('move', pos);
        },



        is_on_focus_area: function (e) {
            var that = this;
            var on_focus = false;
            var pos = this.get_mouse_pos_in_img(e);
            for (var key in this.areas) {
                if ((pos.x >= that.areas[key].x) && (pos.x <= (that.areas[key].x + that.areas[key].width)) && (pos.y >= that.areas[key].y) && (pos.y <= (that.areas[key].y + that.areas[key].height))) {
                    that.current_focus = that.areas[key];
                    return true;
                }
            }
            this.current_focus = {};
            return on_focus
        },

        is_left_button: function (e) {
            return e.which === 1;
        },

        get_random_colour: function (format) {
            var color = "";
            if (format === 'hex') {
                var letters = '0123456789ABCDEF';
                color = '#';
                for (var i = 0; i < 6; i++) {
                    color += letters[Math.floor(Math.random() * 16)];
                }
            } else {
                color = "";
                var max = 255;
                var min = 0;
                for (var i = 0; i < 3; i++) {
                    if (i != 0) color += ",";
                    color += (Math.floor(Math.random() * (max - min) + min));
                }
            }
            return color;
        },

        create_focus_area: function (pos) {
            var that = this;
            var next_focus = $('.focus_area').length + 1;
            var class_name = 'focus_' + next_focus;
            this.$container.append('<div class="focus_area ' + class_name + '"></div>');
            var $focus = $('.focus_' + next_focus, this.$container);
            var colour = this.get_random_colour();
            var focus_obj = {};
            $focus.css({
                'left': pos.x,
                'top': pos.y,
                'border-color': 'rgb(' + colour + ')',
                'background-color': 'rgba(' + colour + ', 0.2)'
            });
            console.log(pos.y)
            focus_obj['x'] = pos.x;
            focus_obj['y'] = pos.y;
            focus_obj['colour'] = colour;
            
            this.areas[class_name] = focus_obj;
            this.current_focus = class_name;
            // console.log("created ", focus_obj, this.areas);
        },

        update_focus_area_dims: function (pos) {
            var data = this.areas[this.current_focus];
            // console.log(data)
            var $focus = $("." + this.current_focus, this.$container);
            var new_width = pos.x - data['x'];
            var new_height = pos.y - data['y'];
            $focus.css({
                'width': new_width,
                'height': new_height
            });
            this.areas[this.current_focus]['width'] = new_width;
            this.areas[this.current_focus]['height'] = new_height;
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
                $asset_type = $('#id_crop_spec');

            if ($asset_type.val().length === 0) {
                return;
            }
            var asset_dims = $asset_type.find('option:selected').text(),
                regExp = /\[([^)]+)\]/,
                matches = regExp.exec(asset_dims),
                crop_dimensions = matches[1].split(' x ');

            this.crop.width = crop_dimensions[0];
            this.crop.height = crop_dimensions[1];
            this.crop.max_x = this.disp_width - this.crop.width;
            this.crop.max_y = this.disp_height - this.crop.height;

            this.$cropper.css({
                width: this.crop.width,
                height: this.crop.height
            });

            this.dragging = false;

            this.$cropper.on('mousedown', function (e) {
                var pos = that.get_mouse_pos_in_img(e),
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

            $asset_type.on('change', function () {
                that.init_crop();
            });

            this.move_cropper($('#id_crop_left').val(), $('#id_crop_top').val(), this.orig_width * $('#id_zoom_ratio').val(), this.orig_height * $('#id_zoom_ratio').val());
        },

        get_mouse_pos_in_img: function (e) {
            var posX = e.clientX,
                posY = e.clientY,
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

            this.$cropper.css('background-position', ((-left) - 1) + 'px ' + ((-top) - 1) + 'px');

            if (zoom_w && zoom_h) {
                this.$cropper.css('background-size', zoom_w + 'px ' + zoom_h + 'px');
            }
        },

        init_zoomer: function () {
            var that = this;
            this.zoomer.min = this.get_min_zoom_width();
            this.zoomer.max = this.orig_width * 1.5;
            this.zoomer.value = this.$asset.width();

            $('#reset-zoomer').on('click', function () {
                that.$zoomer.val(that.orig_ratio * that.orig_width);
                that.update_zoomer();
                that.zoom(that.orig_ratio * that.orig_width);
                return false;
            });

            this.update_zoomer();
        },

        update_zoomer: function () {
            this.$zoomer.attr('min', this.zoomer.min)
                .attr('max', this.zoomer.max)
                .attr('value', this.zoomer.value);
        },

        zoom: function (val) {
            var width = val,
                height = Math.round(this.orig_height * (width / this.orig_width));
            this.$asset.css({
                'width': width,
                'height': height
            });

            $('#id_zoom_ratio').val(width / this.orig_width);
            this.calculate_crop_limits(width, height);
            this.move_cropper(undefined, undefined, width, height);
        },

        calculate_crop_limits: function (zoom_w, zoom_h) {
            this.disp_width = zoom_w;
            this.disp_height = zoom_h;

            this.crop.max_x = zoom_w - this.crop.width;
            this.crop.max_y = zoom_h - this.crop.height;

        },

        get_min_zoom_width: function () {
            var min_zoom = Math.min((this.$asset.width() / this.crop.width), (this.$asset.height() / this.crop.height));
            return this.$asset.width() / min_zoom;
        }
    };

    gusto.cropper.init();
});