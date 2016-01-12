import json
from django.core import serializers
from django.http import HttpResponse

from .models import Asset
from .utils import order_crops_by_suitability, get_crop_props

from StringIO import StringIO
from PIL import Image

def asset_image(request, asset_id):
	"""
	possible query string params:
		- width
		- height
	"""
	try:
		asset = Asset.objects.get(id=asset_id)
	except Asset.DoesNotExist:
    	# TODO, return 404 image
		return HttpResponse('Image not found in db', content_type="text/plain")

	# TODO: support aspect ratio?
	width = request.GET.get('width', None)
	height = request.GET.get('height', None)
	if not width and not height:
		return HttpResponse(asset.image, content_type="image/jpeg")
	width = width or height
	height = height or width

	reqd_width = float(width)
	reqd_height = float(height)

	try:
		image = Image.open(asset.image)
	except IOError:
    	# TODO, return 404 image
		return HttpResponse('Image not found on filesystem', content_type="text/plain")

	asset_w, asset_h = image.size
	# TODO - refactor - we can just pass ORM objects here...?
	# start with the full image as the 'default' crop
	all_crops = [{
		'width': asset_w,
		'height': asset_h,
		'ratio': asset_w/asset_h,
		'crop_left': 0,
		'crop_top': 0,
		'resize_width': asset_w,
		'resize_height': asset_h
	}]
	db_crops = asset.crop_set.all()
	for crop in db_crops:
		all_crops.append({
			'width': crop.crop_spec.width,
			'height': crop.crop_spec.height,
			'ratio': crop.aspect_ratio,
			'crop_left': crop.crop_left,
			'crop_top': crop.crop_top,
			'resize_width': asset_h * crop.zoom_ratio,
			'resize_height': asset_w * crop.zoom_ratio
		})
	ordered_crops = order_crops_by_suitability(all_crops, reqd_width, reqd_height)
#	import pdb
#	pdb.set_trace()
	crop = get_crop_props(asset_w, asset_h, ordered_crops, reqd_width, reqd_height)
	if not crop:
    	# TODO, return 404 image
		return HttpResponse('Could not create crop', content_type="text/plain")

	# now do the pillow stuff
	image = image.resize((crop['resize_height'], crop['resize_width']))
	cropbox = (crop['crop_left'], crop['crop_top'], crop['crop_right'], crop['crop_bottom'])
	image = image.crop(box=cropbox)

	# new return the image as a bytestring
	image_io = StringIO()
	image.save(image_io, 'JPEG', quality=70)
	image_io.seek(0)
	return HttpResponse(image_io, content_type="image/jpeg")


def asset_search(request):
	query = request.GET.get('q', None)
	if query:
		assets = Asset.objects.filter(do_not_use=False, title__contains=query)
		return HttpResponse(serializers.serialize('json', assets, fields=('title', 'id', 'description', 'alt_text')), content_type="application/javascript")
	return HttpResponse(json.dumps([]), mimetype='application/javascript')
