from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model with only the voter_id field
class CustomUser(AbstractUser):
    voter_id = models.CharField(max_length=255, default='default_voter_id')

    is_voter = models.BooleanField(default=True)  # Mark user as a valid voter
    
    def __str__(self):
        return self.voter_id

class Candidate(models.Model):
    name = models.CharField(max_length=255)
    party_name = models.CharField(max_length=255,null=True)
    party_logo = models.ImageField(upload_to='party_logos/', null=True, blank=True)
    manifesto = models.TextField()
    
    def __str__(self):
        return self.name

class Election(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Vote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class ElectionResult(models.Model):
    election = models.ForeignKey(Election, related_name='results', on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    vote_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.candidate.name} - {self.vote_count} votes'
