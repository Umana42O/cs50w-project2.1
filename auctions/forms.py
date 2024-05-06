from django.forms import ModelForm
from django import forms
from .models import *

class AuctionsForm(forms.ModelForm):
    class Meta:
        model = Auctions
        fields = ['title', 'description', 'category', 'initial_price', 'image']
        widgets = {
            'category': forms.Select(choices=Category.objects.all()),
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