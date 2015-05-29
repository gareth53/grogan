window.$ = django.jQuery;

$(function(){
    window.gusto = window.gusto || {};
    gusto.cropper = {
        $els: {
            asset : $('#id_asset'),
            asset_type : $('#id_asset_type'),
            resize_width : $('#id_resize_width'),
            resize_height : $('#id_resize_height'),
            crop_left : $('#id_crop_left'),
            crop_top : $('#id_crop_top'),
            ratio : $('#id_zoom_ratio'),
            displayed_image: $('#displayed_image')
        },
        current_image: null,
        asset: {
            orig_width: 1000,
            orig_height: 400,
            disp_width: 1000,
            disp_height: 400
        },
        zoomer: {
            min: 0,
            max: 0,
            value: 0
        },
        cropper: {
            width: 350,
            height: 200,
            max_x: 1000 - 350,
            max_y: 400 - 200
        },

        init: function() {
            var that = this;
            this.init_asset_and_type();
            // set up the resize controls
            this.init_zoomer();
            // add drag event handler
            this.init_cropper_drag();

            // listen for form field changes
            this.setup_listeners();

            $('#reset-zoomer').on('click', function(){
                that.update_zoomer();
            });
        },

        init_asset_and_type: function () {
            this.current_image = this.$els.displayed_image[0];
            this.asset.orig_width = this.asset.disp_width = this.current_image.width;
            this.asset.orig_height = this.asset.disp_height = this.current_image.height;

            var asset_type = this.$els.asset_type.children('option:selected');
            var regExp = /\[([^)]+)\]/;
            var matches = regExp.exec(asset_type.text());
            var crop_dimensions = matches[1].split(' x ');

            this.cropper.width = crop_dimensions[0];
            this.cropper.height = crop_dimensions[1];
            this.cropper.max_x = this.asset.orig_width - this.cropper.width;
            this.cropper.max_y = this.asset.orig_height - this.cropper.height;
        },

        init_cropper: function () {
            this.$els.cropper = $('#cropper');
            this.$els.cropper.css({
                width: this.cropper.width,
                height: this.cropper.height
            });
        },

        setup_listeners: function (){
            for (var key in this.$els) {
                this.$els[key].change(function(){
                    console.log($(this).attr('name'), $(this).val());
                });
            }
        },

        zoom: function(val) {
            // TODO = make this reusable for a page with multiple crops
            var w, h;

            w = val;
            h = Math.round(this.asset.orig_height * (val / this.asset.orig_width));

            //change the image
            var img = document.querySelector('#displayed_image');
            new_w = w + 'px';
            new_h = h + 'px';
            img.style.width = new_w;
            img.style.height = new_h;


            this.$els.ratio.val(val / this.asset.orig_width);
            this.calculate_crop_limits(w, h);
            this.move_cropper(undefined, undefined, w, h);
        },

        calculate_crop_limits: function(zoom_w, zoom_h) {
            this.asset.disp_width = zoom_w;
            this.asset.disp_height = zoom_h;

            this.cropper.max_x = zoom_w - this.cropper.width;
            this.cropper.max_y = zoom_h - this.cropper.height;

        },

        init_zoomer: function() {
            var img_wrap = document.querySelector('#image_container');
            var img = document.querySelector('#displayed_image');
            var mask = '<div class="image_mask"></div>';
            var cropper = '<div id="cropper" style="background-image:url('+ img.src +');left:0;top:0;"></div>';

            img_wrap.innerHTML += mask + cropper;

            this.init_cropper();

            this.zoomer.min = this.get_min_zoom_width();
            this.zoomer.max = this.current_image.width * 1.5;
            this.zoomer.value = this.current_image.width;

            this.update_zoomer();
        },

        update_zoomer: function () {
            $('#zoomer').attr('min', this.zoomer.min)
                        .attr('max', this.zoomer.max)
                        .attr('value', this.zoomer.value);
        },

        get_min_zoom_width: function () {
            var img = this.current_image;
            var min_zoom =  Math.min((img.width / this.cropper.width), (img.height / this.cropper.height));

            return img.width / min_zoom;
        },

        init_cropper_drag: function() {
            this.dragging = false;
            var that = this;

            document.querySelector('#cropper').addEventListener('mousedown', function(e) {
                var pos =  that.get_mouse_pos_in_img(e),
                    crop_style = document.querySelector('#cropper').style,
                    now_left = parseInt(crop_style.left),
                    now_top = parseInt(crop_style.top);

                crop_style.borderColor = '#ff0';
                that.dragging = true;

                that.drag_offset = {
                    'x': pos['x'] - now_left,
                    'y': pos['y'] - now_top
                }
            });

            document.addEventListener('mouseup', function() {
                that.dragging = false;
                document.querySelector('#cropper').style.borderColor = '#fff';
            });

            document.addEventListener('mousemove', function(e) {
        // TODO: could probably do with throttling this
                if (gusto.cropper.dragging) {
                    var coods = that.get_mouse_pos_in_img(e);
                    gusto.cropper.move_cropper(coods['x'] - that.drag_offset['x'], coods['y'] - that.drag_offset['y'])
                }
            });
        },

        get_mouse_pos_in_img: function(e) {
            var posX = e.pageX,
                posY = e.pageY,
                image = document.querySelector('#displayed_image'),
                img_coods = image.getBoundingClientRect();
            // TODO respect scroll position
            return {
                'x': posX - img_coods['left'],
                'y': posY - img_coods['top']
            }
        },

        move_cropper: function(left, top, zoom_w, zoom_h) {
            // move the cropper to a given co-ordinate and zoom
            var crop_style = document.querySelector('#cropper').style;

            left = left || parseInt(crop_style.left);
            top = top || parseInt(crop_style.top);
            // respect bounding box
            left = Math.min(left, this.cropper['max_x']);
            top = Math.min(top, this.cropper['max_y']);
            left = Math.max(0, left);
            top = Math.max(0, top);

            // now do the move...
            crop_style.left = left + 'px';
            crop_style.top = top + 'px';

            // update form values
            this.$els.crop_left.val(left);
            this.$els.crop_top.val(top);

            crop_style.backgroundPosition = -left + 'px ' + -top + 'px'
            if (zoom_w && zoom_h) {
                crop_style.backgroundSize = zoom_w + 'px ' + zoom_h + 'px'
            }
        }
    };

    gusto.cropper.init();
});
