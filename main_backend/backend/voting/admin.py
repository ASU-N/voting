from django.contrib import admin
from .models import CustomUser, Candidate, Election, Vote, ElectionResult

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('voter_id', 'is_voter')
    search_fields = ('voter_id',)
    ordering = ('voter_id',)

admin.site.register(CustomUser, CustomUserAdmin)

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'party_name', 'manifesto')
    search_fields = ('name', 'party_name')
    ordering = ('name',)

admin.site.register(Candidate, CandidateAdmin)

class ElectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)
    ordering = ('-start_date',)

admin.site.register(Election, ElectionAdmin)

class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'candidate', 'election', 'timestamp')
    search_fields = ('user__voter_id', 'candidate__name', 'election__name')
    ordering = ('-timestamp',)

admin.site.register(Vote, VoteAdmin)

class ElectionResultAdmin(admin.ModelAdmin):
    list_display = ('election', 'candidate', 'vote_count')
    search_fields = ('election__name', 'candidate__name')
    ordering = ('-vote_count',)

admin.site.register(ElectionResult, ElectionResultAdmin)
