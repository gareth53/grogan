from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from .models import Asset, CropSize, Crop
from .forms import CropForm

@staff_member_required
def do_crops(request, asset_id):
	"""
	"""
	if request.POST:
		pass
		# process form
		
		# handle errors
		
		# redirect to the right place
		# either the specified tab or to the Assets ListView
	else:
		asset = Asset.objects.get(pk=asset_id)
		cropsizes = CropSize.objects.filter(enabled=True)
		existing_crops = Crop.objects.filter(asset=asset)
		cropforms = {}
		for sz in cropsizes:
			cropforms[sz.dimensions] = {
					'cropsize': sz,
					'form': CropForm(initial={
						    'asset': asset,
						    'crop_spec': sz,
						    'crop_left': 0,
						    'crop_top': 0,
						    'zoom_ratio': 1
						})
				}
		for crop in existing_crops:
			cropforms[crop.crop_spec.dimensions] = {
					'cropsize': crop.crop_spec,
					'form': CropForm(instance=crop)
				}

		# order the forms based on dimensions
		order = cropforms.keys()
		order = sorted(order)
		ordered_cropforms = [cropforms[key] for key in order]

		return render_to_response('assets/admin/do_crops.html', {
		    'user': request.user,
		    'asset': asset,
		    'cropforms': ordered_cropforms
		    },
		    context_instance=RequestContext(request)
		)