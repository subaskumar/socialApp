from django import forms
from moviesApp.models import movieUpcoming

class moviesAdd(forms.ModelForm):
    class Meta:
        model = movieUpcoming
        fields = '__all__'
