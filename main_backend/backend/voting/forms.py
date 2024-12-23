from django import forms
from .models import Voter

class VoterRegistrationForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ['voter_id', 'face_image']  # Include only the editable fields
        widgets = {
            'face_image': forms.FileInput(),  # Use the correct field name 'face_image'
        }
