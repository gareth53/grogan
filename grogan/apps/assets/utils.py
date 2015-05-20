from StringIO import StringIO
from PIL import Image
from .models import Asset

def prepare_crop(asset, width=None, height=None):
	"""
	if only one dimension, return original asset resized
	if no dimensions, return original asset
	if two dimensions, ah, here comes the magic...
	"""
	# convert strings to numbers
	if width:
		width = float(width)
	if height:
		height = float(height)

	if not width and not height:
		return asset.image

	image = Image.open(asset.image)
	asset_w, asset_h = image.size 

	if width and height:
		crops = order_crops_by_suitability(asset, width, height)
		crop = get_crop_props(asset, crops, width, height)

		# now do the pillow stuff
		image = image.resize((crop['resize_width'], crop['resize_height']))
		cropbox = (crop['crop_left'], crop['crop_top'], crop['crop_right'], crop['crop_bottom'])
		image = image.crop(box=cropbox)

	else:
		# TODO: use tjhe crop logic here too...
		if width and not height:
			height = (width/asset_w) * asset_h
		if height and not width:
			width = (height/asset_h) * asset_w
		image = image.resize((int(width), int(height)))

	# new return the image as a bytestring
	image_io = StringIO()
	image.save(image_io, 'JPEG', quality=70)
	image_io.seek(0)
	return image_io


def order_crops_by_suitability(asset, width, height):
	crops = asset.crop_set.all()
	# stitch the raw image in here too as theb 'default' crop
	# compare all crops, orded them based on variance from dimensions and 
	# variance from aspect ratio
	# return an ordered list

	return crops

def get_crop_props(asset, crops, width, height):
	# the crop might not be bang on for aspect-ratio so we'll have to
	# use it in a 'fuzzy style'
	# also, ensure that we don'l't return crop dimensions that try to crop outside the image
	best = crops[0]
	return {
		'resize_width': best.resize_width,
		'resize_height': best.resize_height,
		'crop_left': best.crop_left,
		'crop_top': best.crop_top,
		'crop_right': best.crop_right,
		'crop_bottom': best.crop_bottom
	}