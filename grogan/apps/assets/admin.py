import os
import md5
from django.conf import settings
from django.contrib import admin
from .models import Asset, Category, Person, Location, Group, Crop, AssetType

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

    list_display = ('asset', 'width', 'height', 'crop_left', 'crop_top', 'width', 'height', 'aspect_ratio')


@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    fields = ('name', 'width', 'height')

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):

    list_display = ('title', 'upload_date', 'uploaded_by', 'do_not_use', 'file_hash')

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
