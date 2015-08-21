from django.test import TestCase
from grogan.apps.assets.utils import order_crops_by_suitability, get_crop_props

def crop_factory(w, h, l, t, resize_width, resize_height, expected_order=None):
	return {
		'width': w,
		'height': h,
		'ratio': w/h,
		'crop_left': l,
		'crop_top': t,
		'resize_width': resize_width,
		'resize_height': resize_height,
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
			crop_factory(200, 200, 0, 0, 200, 200, 0),
		]
		returned = order_crops_by_suitability(crops, 200, 200)
		for i, crop in enumerate(returned):
			assert crop['expected_order'] == i

	def test_order_crops_by_suitability2(self):
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

class GetCropProps(TestCase):

	def test_get_crop_props_simple(self):
		crops = [
			crop_factory(1600, 800, 0, 0, 1600, 800),
		]
		# this should just return the data as is
		returned = get_crop_props(1600, 800, crops, 1600, 800)

		assert returned['resize_width'] == 1600
		assert returned['resize_height'] == 800
		assert returned['crop_top'] == 0
		assert returned['crop_right'] == 1600
		assert returned['crop_bottom'] == 800
		assert returned['crop_left'] == 0

	def test_get_crop_props_first_is_unsuitable(self):
		crops = [
			crop_factory(1600, 800, 0, 0, 1800, 900),
			crop_factory(1600, 800, 0, 0, 1600, 800),
		]
		# this should return the second in the list
		returned = get_crop_props(1600, 800, crops, 1600, 800)

		assert returned['resize_width'] == 1600
		assert returned['resize_height'] == 800
		assert returned['crop_top'] == 0
		assert returned['crop_right'] == 1600
		assert returned['crop_bottom'] == 800
		assert returned['crop_left'] == 0


	def test_get_crop_props_all_are_unsuitable(self):
		crops = [
			crop_factory(1600, 800, 0, 0, 1800, 900),
			crop_factory(1600, 800, 0, 0, 1600, 800),
		]
		returned = get_crop_props(800, 400, crops, 1600, 800)
		assert returned is None


	def test_get_crop_props_scales_down(self):
		crops = [
			crop_factory(1600, 800, 0, 0, 1600, 800),
		]
		returned = get_crop_props(1600, 800, crops, 800, 400)
		assert returned['resize_width'] == 800
		assert returned['resize_height'] == 400
		assert returned['crop_top'] == 0
		assert returned['crop_right'] == 800
		assert returned['crop_bottom'] == 400
		assert returned['crop_left'] == 0


	def test_get_crop_props_reworks_diff_aspect_ratio1(self):
		"""
		the crop here is shallower
		"""
		crops = [
			crop_factory(1600, 600, 0, 100, 1600, 800),
		]
		returned = get_crop_props(1600, 800, crops, 800, 400)
		assert returned['resize_width'] == 800
		assert returned['resize_height'] == 400
		assert returned['crop_top'] == 0
		assert returned['crop_right'] == 800
		assert returned['crop_bottom'] == 400
		assert returned['crop_left'] == 0

	def test_get_crop_props_reworks_diff_aspect_ratio2(self):
		"""
		the crop here is deeper
		"""
		crops = [
			# (width, height, left, top, resize_width, resize_height
			crop_factory(600, 500, 100, 100, 800, 400),
		]
		returned = get_crop_props(1600, 800, crops, 600, 400)
		assert returned['resize_width'] == 800
		assert returned['resize_height'] == 400
		assert returned['crop_top'] == 0
		assert returned['crop_bottom'] == 400
		assert returned['crop_left'] == 100
		assert returned['crop_right'] == 700

# TODO, test rework of leak to the left
# TODO test rework of height leak

