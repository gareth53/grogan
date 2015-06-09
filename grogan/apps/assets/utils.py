import math

def order_crops_by_suitability(crops, width, height):
	"""
	WiP
	"""
	# compare all crops, orded them based on
	# variance from dimensions and 
	# variance from aspect ratio
	# return an ordered list
	desired_ratio = width / height
	for crop in crops:
		# TODO - we probably need to favour aspect ratio a smidge over width...
		try:
			crop['ratio_variance'] = abs(1 - desired_ratio / crop['ratio'])
			crop['width_variance'] = abs(1 - width / crop['width'])
			crop['total_variance'] = crop['ratio_variance'] + crop['width_variance']
		except ZeroDivisionError:
			crop['total_variance'] = 10000000
	return sorted(crops, key=lambda item: item['total_variance'])

def get_crop_props(asset_w, asset_h, crops, width, height):
	"""
	WiP
	"""
	# the crop might not be bang on for aspect-ratio so we'll have to
	# use it in a 'fuzzy style'
	# also, ensure that we don't return crop dimensions that try to 
	# crop outside the image - we'll have to wiggle it...
	for crop in crops:
		# first convert the resize & crop dimensions to support the new size
		change = width / crop['width']
		for key, val in crop.items():
			crop[key] = math.floor(val * change)

		if crop['resize_height'] < asset_h or crop['resize_width'] < asset_w:
			continue
		# find the center point:
		centre_x = math.floor(crop['crop_left'] + (crop['width'] / 2))
		centre_y = math.floor(crop['crop_top'] + (crop['height'] / 2))

		# position the new dimensions around the center point
		crop['crop_left'] = max(0, centre_x - round(width/2))
		crop['crop_top'] = max(0, centre_x - round(height/2))
		# adjust for boundaries of image
		if crop['crop_left'] + width > crop['resize_width']:
			crop['crop_left'] = crop['resize_width'] - width
		if crop['crop_top'] + height > crop['resize_height']:
			crop['crop_top'] = crop['resize_height'] - height
		# adjust crop_bottom and crop_right, width & height
		crop['height'] = height
		crop['width'] = width
		crop['crop_bottom'] = crop['crop_top'] + height
		crop['crop_right'] = crop['crop_left'] + width
		for key, val in crop.items():
			crop[key] = int(val	)
		return crop

	return None