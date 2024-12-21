from django import forms
from .models import Voter

class VoterRegistrationForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ['voter_id', 'image_path']
        widgets = {
            'image_path': forms.FileInput(),
        }
