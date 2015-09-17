import os
import md5

from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse

from .models import Asset, Category, Person, Location, Group, Crop, CropSize

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    change_form_template = 'admin/assets/crop_changeform.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        crop = Crop.objects.get(pk=object_id)
        extra_context['asset'] = crop.asset
        return super(CropAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

    class Media:
        js = ['/static/js/cropper-admin.js']
        css = {
            "all": ("/static/css/crop-admin.css",)
        }

    list_display = ('__unicode__', 'crop_left', 'crop_top', 'zoom_ratio', 'aspect_ratio')


@admin.register(CropSize)
class CropSizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'enabled', 'width', 'height')
    fields = ('name', 'width', 'height')

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):

    def preview(img):
        return '<img src="/api/1.0/assets/image/%d/?width=100&height=100">' % img.id

    def edit_crops(img):
        return '<a href="%s" class="crop">edit crops</a>' % reverse('do_crops', args=[img.id])

    preview.allow_tags = True
    edit_crops.allow_tags = True

    list_display = (preview, 'title', 'upload_date', edit_crops)

    fieldsets = (
        ('Basic Detail', {
            'fields': ('title', 'image', 'description')
        }),
        ('Usages & Credits', {
            'fields': ('author', 'author_url', 'notes', 'do_not_use', 'licence')
        }),
        ('Metadata', {
            'fields': ('category', 'people', 'groups', 'locations')
        })
    )
	# TODO - custom widgets for metatags

    def add_view(self, request, form_url='', extra_context=None):
        # TODO - check file extension
#        valid_extensions = settings.ALLOWED_FILE_EXTENSIONS
#            raw_file_name = os.path.join(settings.MEDIA_ROOT, request.GET.get('raw_file'))
#        if not os.path.exists(raw_file_name):
#            raise Http404

        # TODO - add uploader
        if request.method == "POST":
            request.POST['uploaded_by'] = request.user.id
        # TODO - add file hash
        # TODO - check file hasn't already been uploaded
#            request.POST['file_hash'] = md5.new(request.upload_handlers[0].file.read()).hexdigest()
        # TODO - redirect to custom cropping view
        return super(AssetAdmin, self).add_view(request, form_url, extra_context=extra_context)
