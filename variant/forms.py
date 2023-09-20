from django import forms
from .models import VariantImage


class ImageForm(forms.ModelForm):
    class Meta:
        model=VariantImage
        fields=('image',)