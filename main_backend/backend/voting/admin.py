from django.contrib import admin
from .models import Voter, Candidate

class VoterAdmin(admin.ModelAdmin):
    list_display = ('voter_id', 'image_tag')
    search_fields = ['voter_id']

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'party', 'image_tag')
    search_fields = ['name', 'party']
    list_filter = ['party']

admin.site.register(Voter, VoterAdmin)
admin.site.register(Candidate, CandidateAdmin)
