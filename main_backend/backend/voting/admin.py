from django.contrib import admin
from .models import Voter

class VoterAdmin(admin.ModelAdmin):
    list_display = ('voter_id', 'image_tag')
    readonly_fields = ('image_tag',)
    search_fields = ['voter_id']  # search functionality
    list_filter = ['voter_id']    # filtering functionality

admin.site.register(Voter, VoterAdmin)
