from django.utils.html import mark_safe
from django.db import models

class Voter(models.Model):
    voter_id = models.CharField(max_length=100, unique=True)
    image_path = models.CharField(max_length=255)

    def __str__(self):
        return self.voter_id

    def image_tag(self):
        if self.image_path:
            return mark_safe(f'<img src="{self.image_path}" width="150" height="150" />')
        return "No image"
    
    image_tag.short_description = 'Image'
