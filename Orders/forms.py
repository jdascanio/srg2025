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
    user_name = forms.CharField(max_length=20, required=False)

class SaveOrder(forms.Form):
    order_number = forms.CharField(max_length=10, required=False)
    prov_order_number_hd = forms.CharField(max_length=25)
    user_name = forms.CharField(max_length=20, required=False)
    total_products = forms.IntegerField(required=False)
    tracking = forms.CharField(max_length=50, required=False)
    send_date = forms.DateField(required=False)
    reception_date = forms.DateField(required=False)
    start_date = forms.DateField(required=False)
    finish_date = forms.DateField(required=False)
    return_date = forms.DateField(required=False)
    order_stage = forms.CharField(max_length=60, required=False)

class DeleteRow(forms.Form):
    row_id = forms.CharField(max_length=30)

class EditProductLine(forms.Form):
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
    user_name = forms.CharField(max_length=20, required=False)