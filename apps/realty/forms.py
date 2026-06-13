from django import forms
from django.conf import settings
from .models import Realty, RealtyPhoto


class RealtyForm(forms.ModelForm):
    class Meta:
        model = Realty
        fields = ('title', 'realty_type', 'description', 'address', 'price', 'area', 'floors', 'rooms')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'realty_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'area': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'floors': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100}),
            'rooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        labels = {
            'title': 'Название объекта',
            'realty_type': 'Тип',
            'description': 'Описание',
            'address': 'Адрес',
            'price': 'Цена, ₽',
            'area': 'Площадь, м²',
            'floors': 'Кол-во этажей',
            'rooms': 'Кол-во комнат',
        }


class RealtyPhotoForm(forms.ModelForm):
    class Meta:
        model = RealtyPhoto
        fields = ('image',)
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }


class CatalogFilterForm(forms.Form):
    price_min = forms.IntegerField(
        required=False, min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'от'}),
        label='Цена от',
    )
    price_max = forms.IntegerField(
        required=False, min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'до'}),
        label='до',
    )
    area_min = forms.DecimalField(
        required=False, min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'от'}),
        label='Площадь от',
    )
    area_max = forms.DecimalField(
        required=False, min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'до'}),
        label='до',
    )
    floors_min = forms.IntegerField(
        required=False, min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'от'}),
        label='Этажей от',
    )
    floors_max = forms.IntegerField(
        required=False, min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'до'}),
        label='до',
    )
