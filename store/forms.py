from django import forms

class ShippingForm(forms.Form):
    first_name = forms.CharField(max_length=100, initial="")
    last_name = forms.CharField(max_length=100, initial="")
    email = forms.EmailField(initial="")
    address = forms.CharField(max_length=255, initial="")
    city = forms.CharField(max_length=100, initial="")
    state = forms.CharField(max_length=100, initial="")
    zip_code = forms.CharField(max_length=10, initial="")
