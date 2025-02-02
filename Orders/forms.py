from django import forms


class AddProductLine(forms.Form):
    prov_order_number = forms.CharField(max_length=25)#
    family = forms.CharField(max_length=20, required=False)
    status = forms.CharField(max_length=30, required=False)#
    missing_elem = forms.CharField(max_length=40, required=False)#
    product = forms.CharField(max_length=60, required=False)#
    in_sn = forms.CharField(max_length=20, required=False)#
    client = forms.CharField(max_length=30, required=False)#
    seller = forms.CharField(max_length=30, required=False)#
    reason = forms.CharField(max_length=60, required=False)#
    cig = forms.CharField(max_length=6, required=False)#
    observations = forms.CharField(max_length=200, required=False)#
    out_sn = forms.CharField(max_length=20, required=False)#
    invoice = forms.CharField(max_length=20, required=False)#