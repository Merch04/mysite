from django import forms

class TimeInterval_Form(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'dateStyles commonStyle'}))    
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'timeStyles commonStyle'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'dateStyles commonStyle'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'timeStyles commonStyle'}))
