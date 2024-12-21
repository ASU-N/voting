from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100)
    imageUrl = models.URLField()
    manifesto = models.TextField()
    promises = models.JSONField()

    def __str__(self):
        return self.name

class Vote(models.Model):
    votingId = models.CharField(max_length=100)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return self.votingId
