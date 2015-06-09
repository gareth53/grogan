from django.http import HttpResponse

from .models import Asset
from .utils import order_crops_by_suitability, get_crop_props

from StringIO import StringIO
from PIL import Image
from .models import Asset

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

	if width:
		width = float(width)
	if height:
		height = float(height)

	if not width and not height:
		return HttpResponse(asset.image, content_type="image/jpeg")

	try:
		image = Image.open(asset.image)
	except IOError:
    	# TODO, return 404 image
		return HttpResponse('Image not found on filesystem', content_type="text/plain")

	asset_w, asset_h = image.size

	all_crops = [{
		'id': crop.id,
		'width': crop.asset_type.width,
		'height': crop.asset_type.height,
		'ratio': crop.aspect_ratio,
		'crop_left': crop.crop_left,
		'crop_top': crop.crop_top,
		'resize_width': crop.resize_height,
		'resize_height': crop.resize_width
	} for crop in asset.crop_set.all()]
	# add the full image as the 'default' crop
	all_crops.append({
		'id': 'original',
		'width': asset_w,
		'height': asset_h,
		'ratio': asset_w/asset_h,
		'crop_left': 0,
		'crop_top': 0,
		'resize_width': asset_w,
		'resize_height': asset_h
	})
	crops = order_crops_by_suitability(all_crops, width, height)
	crop = get_crop_props(asset_w, asset_h, crops, width, height)
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