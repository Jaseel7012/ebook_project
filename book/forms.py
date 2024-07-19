from django.forms import ModelForm,DateInput
from .models import Book
from django import forms


class PublishDateInput(DateInput):
    input_type='date'
class BookCreateForm(ModelForm):
    class Meta:
        model=Book
        fields='__all__'
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'serial_no':forms.TextInput(attrs={'class':'form-control'}),
            'publish_date':PublishDateInput(attrs={'class':'form-control'}),
            'author':forms.Select(attrs={'class':'form-control'}),
            'price':forms.TextInput(attrs={'class':'form-control'}),
            


        }