from django.db import models
from django.utils.html import format_html
from cryptography.fernet import Fernet 
import base64 
import os

class Voter(models.Model):
    voter_id = models.CharField(max_length=100, unique=True)
    face_encoding = models.BinaryField()  # Ensure face_encoding field is present
    face_image = models.ImageField(upload_to='voters/', null=True, blank=True)  # Field to store face image

    def __str__(self):
        return self.voter_id

    def image_tag(self):
        if self.face_image:
            return format_html('<img src="{}" width="150" height="150" />', self.face_image.url)
        return "No image"
    image_tag.short_description = 'Face Image'

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=50)
    image = models.ImageField(upload_to='candidates/')

    def __str__(self):
        return self.name

    def image_tag(self):
        if self.image:
            return format_html('<img src="{}" width="150" height="150" />', self.image.url)
        return "No image"
    image_tag.short_description = 'Image'

# Generate a key for encryption
key = base64.urlsafe_b64encode(os.urandom(32))
cipher = Fernet(key)

class Vote(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    encrypted_voter_id = models.CharField(max_length=256)  # Store encrypted voter ID
    vote_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote for {self.candidate.name} on {self.vote_date}"

    @staticmethod
    def encrypt_voter_id(voter_id):
        encrypted_voter_id = cipher.encrypt(voter_id.encode())
        return encrypted_voter_id

    @staticmethod
    def decrypt_voter_id(encrypted_voter_id):
        voter_id = cipher.decrypt(encrypted_voter_id).decode()
        return voter_id
