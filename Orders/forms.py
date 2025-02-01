from django import forms


class AddAlarmLine(forms.Form):
    family = forms.CharField(max_length=20)