from django import forms

class TimeInterval_Form(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'dateStyles'}))    
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'timeStyles'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'dateStyles'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'timeStyles'}))
