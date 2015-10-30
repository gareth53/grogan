from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from .models import Asset, CropSize, Crop
from .forms import CropForm

@staff_member_required
def do_crops(request, asset_id):
	"""
	the admin screen that allows creation of crops in a nice flow.
	"""
	asset = Asset.objects.get(pk=asset_id)
	if request.POST:
		return do_crops_post(request, asset)
	else:
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
		# facilitate the editing flow by specifying which crop is the enxt to be edited
		hashid = request.GET.get('hash', '')
		return render_to_response('assets/admin/do_crops.html', {
		    'user': request.user,
		    'asset': asset,
		    'cropforms': ordered_cropforms,
		    'hash': hashid,
		    },
		    context_instance=RequestContext(request)
		)

def do_crops_post(request, asset):
	"""
	handle POST data
	"""
	crop_spec_id = request.POST.get('crop_spec')
	crop_left = request.POST.get('crop_left')
	crop_top = request.POST.get('crop_top')
	zoom_ratio = request.POST.get('zoom_ratio')
		
	# get the crop sepc & crop (if this is an edit)
	crop_spec = CropSize.objects.get(id=crop_spec_id)
	crop, _ = Crop.objects.get_or_create(asset=asset, crop_spec=crop_spec)
	# updated the details...
	crop.crop_left=crop_left
	crop.crop_top=crop_top
	crop.zoom_ratio=zoom_ratio
	crop.save()
	# either continue editing, or default ot list view...
	if '_next' in request.POST.keys():
		next_tab = request.POST.get('next_tab')
		changeview_url = reverse('do_crops', args=[asset.id])
		return HttpResponseRedirect('%s?hash=%s' % (changeview_url, next_tab.replace('#', '')))
	else:
		return HttpResponseRedirect(reverse("admin:assets_asset_changelist"))