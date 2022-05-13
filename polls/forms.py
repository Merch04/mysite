from django import forms

class TimeInterval_Form(forms.Form):
    start_date = forms.DateField()    
    start_time = forms.TimeField()
    end_date = forms.DateField()
    end_time = forms.TimeField()