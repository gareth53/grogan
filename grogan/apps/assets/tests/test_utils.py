from django.test import TestCase
from grogan.apps.assets.utils import order_crops_by_suitability

def crop_factory(w, h, l, t, zoom_w, zoom_h, expected_order):
	return {
		'width': w,
		'height': h,
		'ratio': w/h,
		'crop_left': l,
		'crop_top': t,
		'resize_width': zoom_w,
		'resize_height': zoom_h,
		'expected_order': expected_order
	}

class OrderCropsTestCase(TestCase):
	"""
	testing the order_crops_by_suitability function
	"""

	def setup(self):
		pass

	def test_order_crops_by_suitability1(self):
		# simple case
		crops = [
			crop_factory(1600, 800, 0, 0, 1600, 900, 2),
			crop_factory(1600, 900, 0, 0, 1600, 900, 0),
			crop_factory(800, 450, 0, 0, 1600, 900, 3),
			crop_factory(1500, 900, 0, 0, 1600, 900, 1)
		]
		returned = order_crops_by_suitability(crops, 1600, 900)
		for i, crop in enumerate(returned):
			assert crop['expected_order'] == i