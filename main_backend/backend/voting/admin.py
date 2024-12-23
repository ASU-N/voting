from django.contrib import admin
from .models import Voter, Candidate, Vote

class VoterAdmin(admin.ModelAdmin):
    list_display = ('voter_id', 'image_tag')
    readonly_fields = ('image_tag',)  # Ensure this is set to display the image

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'party', 'image_tag')
    readonly_fields = ('image_tag',)

class VoteAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'vote_date')

admin.site.register(Voter, VoterAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Vote, VoteAdmin)
