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
            crop_bottom : $('#id_crop_bottom'),
            crop_right : $('#id_crop_right'),
            width : $('#id_width'),
            height : $('#id_height'),
            ratio : $('#id_ratio'),
            displayed_image: $('#displayed_image')
        },
        asset: {
            orig_width: 1000,
            orig_height: 400,
            disp_width: 1000,
            disp_height: 400
        },

        cropper: {
            width: 350,
            height: 200,
            max_x: 1000 - 350,
            max_y: 400 - 200
        },

        init: function() {
            this.init_asset();

            // set up the resize controls
            this.init_zoomer();
            // add drag event handler
            this.init_cropper_drag();

            // listen for form field changes
            this.setup_listeners();
        },

        init_asset: function () {
            var image = this.$els.displayed_image;

            this.asset.orig_height
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

            // update form values
            document.querySelector('#cropwidth').value = w;
            document.querySelector('#cropheight').value = h;

            //change the image
            var img = document.querySelector('#displayed_image');
            new_w = w + 'px';
            new_h = h + 'px';
            img.style.width = new_w;
            img.style.height = new_h;

            this.calculate_crop_limits(w, h);
            this.move_cropper(undefined, undefined, w, h)
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

            // fix min value of resize slider
            var frame_h = parseInt(document.querySelector('#cropper').clientHeight);
            var frame_w = parseInt(document.querySelector('#cropper').clientWidth);
            var min_scale = frame_h / gusto.cropper.asset.orig_height;
            var min_width = Math.ceil(min_scale * gusto.cropper.asset.orig_width);


            document.querySelector('#zoomer').setAttribute('min', Math.max(frame_w, min_width))
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
            console.log(this.cropper['max_x'])
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
            document.querySelector('#cropx').value = left;
            document.querySelector('#cropy').value = top;

            crop_style.backgroundPosition = -left + 'px ' + -top + 'px'
            if (zoom_w && zoom_h) {
                crop_style.backgroundSize = zoom_w + 'px ' + zoom_h + 'px'
            }
        }

    };

    gusto.cropper.init();
});
