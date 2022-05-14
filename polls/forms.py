from django import forms

#new
class DateForm(forms.Form):
    s_date = forms.DateTimeField(widget=forms.DateInput(attrs={'class': 'dateStyles commonStyle'}), input_formats=['%d/%m/%Y %H:%M'])
    e_date = forms.DateTimeField(widget=forms.DateInput(attrs={'class': 'dateStyles commonStyle'}), input_formats=['%d/%m/%Y %H:%M'])