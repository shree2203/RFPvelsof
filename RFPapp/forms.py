from django import forms

from RFPapp.models import RFP


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RFPForm(forms.ModelForm):
    class Meta:
        model = RFP
        fields = ['rfp_title', 'rfp_last_date', 'min_amount', 'max_amount', 'vendor']

    rfp_last_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Select a date'
    )