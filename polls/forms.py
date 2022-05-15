from django import forms
from polls.models import Choise_video, Restaurants

#new
class DateForm(forms.Form):
    s_date = forms.DateTimeField(
        widget=forms.DateInput(
            attrs={'class': 'dateStyles commonStyle'}), 
        input_formats=['%d/%m/%Y %H:%M'])
    e_date = forms.DateTimeField(
        widget=forms.DateInput(
            attrs={'class': 'dateStyles commonStyle'}), 
        input_formats=['%d/%m/%Y %H:%M'])
    
    
class ChoiseVideoForm(forms.ModelForm):
    class Meta:
        model = Choise_video
        fields = '__all__'
        widgets = {
            "start_date": forms.DateInput(
                attrs={'class': 'dateStyles commonStyle'}),
            "end_date": forms.DateInput(
                attrs={'class': 'dateStyles commonStyle'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['restaurants'].queryset = Restaurants.objects.none()
        
        
        if 'restaurants' in self.data:
            print("Govna")
            try:
                shift_id = int(self.data.get('shift'))
                self.fields['restaurants'].queryset = Restaurants.objects.filter(shift_id=shift_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            print("dermo")
            self.fields['restaurants'].queryset = self.instance.shift.restaurants_set.order_by('name')
            

