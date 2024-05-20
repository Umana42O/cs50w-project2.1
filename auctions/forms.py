from django.forms import ModelForm
from django import forms
from .models import *

class AuctionsForm(forms.ModelForm):
    class Meta:
        model = Auctions
        fields = ['title', 'description', 'category', 'initial_price', 'image']
        widgets = {
            'category': forms.Select(choices=Category.objects.all()),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa el titulo'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la descripción'}),
            'initial_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
# class new_listForm(ModelForm):
#     title = forms.CharField(label="Title",widget=forms.TextInput)
#     description = forms.CharField(label="Description", widget=forms.Textarea(attrs={
#         'style' : 'width:100%'}))
#     category = forms.ChoiceField(widget=forms.Select)
#     initial_price = forms.FloatField(label="Price(US$)")
#     owner = 
#     image = forms.ImageField(label="Image")
#     class Meta:
#         model = Auctions
#         fields = ["name", "description", "price", "category"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('id', 'created_at', 'user', 'auctions', )

class UpdatePriceForm(forms.ModelForm):
    class Meta:
        model = Auctions
        fields = ['current_price']