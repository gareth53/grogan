from django.forms import ModelForm

from .models import Crop

class CropForm(ModelForm):
	class Meta:
		model = Crop