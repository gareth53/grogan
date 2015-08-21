import math

def order_crops_by_suitability(crops, reqd_width, reqd_height):
	"""
	WiP
	"""
	# compare all crops, orded them based on
	# variance from dimensions and 
	# variance from aspect ratio
	# return an ordered list
	reqd_ratio = reqd_width / reqd_height
	for crop in crops:
		# TODO - we probably need to favour aspect ratio a smidge over width...
		try:
			crop['ratio_variance'] = abs(1 - reqd_ratio / crop['ratio'])
			crop['width_variance'] = abs(1 - reqd_width / crop['width'])
			crop['total_variance'] = crop['ratio_variance'] + crop['width_variance']
		except ZeroDivisionError:
			crop['total_variance'] = 10000000
	return sorted(crops, key=lambda item: item['total_variance'])

def get_crop_props(asset_w, asset_h, crops, reqd_width, reqd_height):
	"""
	given the asset dimenions and a list of crops, figuire out
	exactly how we need to crop
	"""
	# the crop might not be bang on for aspect-ratio so we'll have to
	# use it in a 'fuzzy style'
	# also, ensure that we don't return crop dimensions that try to 
	# crop outside the image - we'll have to wiggle it...
	for crop in crops:
		# first convert the resize & crop dimensions to support the new size
		change = float(reqd_width) / float(crop['width'])
		for key in ['resize_width', 'resize_height', 'crop_left', 'crop_top']:
			crop[key] = math.floor(crop[key] * change)

		# if we're resizing this to distortion point, skip
		if crop['resize_height'] > asset_h or crop['resize_width'] > asset_w:
			continue

		# find the center point:
		centre_x = math.floor(crop['crop_left'] + (crop['width'] / 2))
		centre_y = math.floor(crop['crop_top'] + (crop['height'] / 2))

		# position the new dimensions around the center point
		crop['crop_left'] = max(0, centre_x - round(reqd_width/2))
		crop['crop_top'] = max(0, centre_x - round(reqd_height/2))

		# adjust for boundaries of image
		if crop['crop_left'] + reqd_width > crop['resize_width']:
			crop['crop_left'] = crop['resize_width'] - reqd_width
		if crop['crop_top'] + reqd_height > crop['resize_height']:
			crop['crop_top'] = crop['resize_height'] - reqd_height
		# adjust crop_bottom and crop_right, width & height
		crop['crop_bottom'] = crop['crop_top'] + reqd_height
		crop['crop_right'] = crop['crop_left'] + reqd_width
		for key in ['resize_width', 'resize_height', 'crop_left', 'crop_top', 'crop_bottom', 'crop_right']:
			crop[key] = int(crop[key])
		return crop

	return None