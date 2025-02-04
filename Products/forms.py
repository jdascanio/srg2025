from django import forms

class AddProduct(forms.Form):
    name = forms.CharField(max_length=60)
    family = forms.CharField(max_length=20)
    subcat = forms.CharField(max_length=20)

class EditProduct(forms.Form):
    product_id = forms.IntegerField()
    name = forms.CharField(max_length=60)
    family = forms.CharField(max_length=20)
    subcat = forms.CharField(max_length=20)

class DeleteProduct(forms.Form):
    product_id = forms.IntegerField()
