from django.http import HttpResponse

from .models import Asset
from .utils import prepare_crop


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

	# TODO: hoik out query str name values
	width = request.GET.get('width', None)
	height = request.GET.get('height', None)

	image = prepare_crop(asset, width, height)

	try:
		return HttpResponse(image, content_type="image/jpeg")
	except IOError, TypeError:
    	# TODO, return 404 image
		return HttpResponse('Image not found on filesystem', content_type="text/plain")
