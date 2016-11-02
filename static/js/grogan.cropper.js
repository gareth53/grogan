//window.$ = django.jQuery;

/*
    TODO:
    - Handle if the specified crop is larger than the asset we're working with
 */

// to encapsulate
var grogan = window.grogan||{};
grogan.cropper = {

    create: function($form) {

        var this_crop = {

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

            init: function ($form) {
                if($form.hasClass('initialised')) {
                    return;
                }
                this.$container = $form.find('.image_container');
                this.$asset = $form.find('.displayed_image');
                this.$zoomer = $form.find('.zoomer');
                this.$zoom_reset = $form.find('.reset-zoom');

                // form elements
                this.$form_el__zoom_ratio = $form.find('#id_zoom_ratio');
                this.$form_el__crop_spec = $form.find('#id_crop_spec');
                this.$form_el__crop_left = $form.find('#id_crop_left');
                this.$form_el__crop_top = $form.find('#id_crop_top');

                this.orig_width = this.$asset.width();
                this.orig_height = this.$asset.height();
                this.orig_ratio = this.$form_el__zoom_ratio.val();

                this.disp_width = this.orig_width * this.orig_ratio;
                this.disp_height = this.orig_height * this.orig_ratio;

                this.$cropper = $('<div class="cropper" style="background-image:url(' + this.$asset.attr("src") + ');left:0;top:0;"></div>');

                this.$container.append('<div class="image_mask"></div>').append(this.$cropper);

                this.set_image_dimensions();
                this.init_crop();
                this.init_zoomer();
                $form.addClass('initialised');
            },

            set_image_dimensions: function () {
                var zoom = this.$form_el__zoom_ratio.val(),
                    width = Math.round(this.orig_width * zoom),
                    height = Math.round(this.orig_height * zoom);

                this.$asset.css({
                    'width': width,
                    'height': height
                });
            },

            init_crop: function () {
                var that = this,
                    $asset_type = this.$form_el__crop_spec;

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
                    if (that.dragging) {
                        that.dragging = false;
                        that.$cropper.css('border-color', '#fff');
                    }
                });

                $(document).on('mousemove', function (e) {
                    if (that.dragging) {
                        var coords = that.get_mouse_pos_in_img(e);
                        that.move_cropper(coords.x - that.drag_offset.x, coords.y - that.drag_offset.y);
                    }
                });

                $asset_type.on('change', function () {
                    that.init_crop();
                });

                this.move_cropper(this.$form_el__crop_left.val(), this.$form_el__crop_top.val(), this.orig_width * this.$form_el__zoom_ratio.val() , this.orig_height * this.$form_el__zoom_ratio.val());
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
                this.$form_el__crop_left.val(left);
                this.$form_el__crop_top.val(top);
                
                var pos_left = left - 1;
                var pos_top = top - 1;

                this.$cropper.css('background-position', -pos_left + 'px ' + -pos_top + 'px');

                if (zoom_w && zoom_h) {
                    this.$cropper.css('background-size', zoom_w + 'px ' + zoom_h + 'px');
                }
            },

            init_zoomer: function () {
                var that = this;

                this.zoomer.min = this.get_min_zoom_width();
                this.zoomer.max = this.orig_width * 1.5;
                this.zoomer.value = this.$asset.width();

                this.$zoomer.on('input', function() {
                   that.zoom(this.value);
                });

                this.$zoom_reset.on('click', function () {
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

                this.$form_el__zoom_ratio.val(width / this.orig_width);
                this.calculate_crop_limits(width, height);
                this.move_cropper(undefined, undefined, width, height);
            },

            calculate_crop_limits: function(zoom_w, zoom_h) {
                this.disp_width = zoom_w;
                this.disp_height = zoom_h;

                this.crop.max_x = zoom_w - this.crop.width;
                this.crop.max_y = zoom_h - this.crop.height;

            },

            get_min_zoom_width: function () {
                var min_zoom =  Math.min((this.$asset.width() / this.crop.width), (this.$asset.height() / this.crop.height));
                return Math.floor(this.$asset.width() / min_zoom);
            }
        };

        this_crop.init($form);
        return this_crop;
    }
};

$(function() {
    $('form.do_crop:visible').each(function(){
        grogan.cropper.create($(this));
	});
});
