from django import forms
from polls.models import Choise_video, Shift
    
class ChoiseVideoForm(forms.ModelForm):
    class Meta:
        model = Choise_video
        fields = '__all__'
        widgets = {
            "start_date": forms.DateInput(
                attrs={'class': 'dateStyles commonStyle', 'autocomplete': 'off'}),
            "end_date": forms.DateInput(
                attrs={'class': 'dateStyles commonStyle', 'autocomplete': 'off'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shift'].queryset = Shift.objects.none()
        
        if 'restaurants' in self.data:
            try:
                restaurants_id = int(self.data.get('restaurants'))
                self.fields['shift'].queryset = Shift.objects.filter(restaurants_id=restaurants_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['shift'].queryset = self.instance.shift.shift_set

