from django.shortcuts import render
from django.http import JsonResponse
from .models import Election, Candidate, Vote, ElectionResult
from .serializers import CandidateSerializer, ElectionSerializer
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


def home(request):
    elections = Election.objects.filter(is_active=True)
    return JsonResponse(ElectionSerializer(elections, many=True).data, safe=False)

def election_detail(request, election_id):
    election = Election.objects.get(id=election_id)
    candidates = Candidate.objects.filter(election=election)
    return JsonResponse({
        'election': election.name,
        'candidates': [CandidateSerializer(candidate).data for candidate in candidates]
    })

def vote(request, election_id):
    # Voting logic here
    return JsonResponse({'message': 'Vote casted successfully'})

def election_results(request, election_id):
    election = Election.objects.get(id=election_id)
    results = ElectionResult.objects.filter(election=election)
    return JsonResponse({
        'results': [{'candidate': result.candidate.name, 'vote_count': result.vote_count} for result in results]
    })

def signup(request):
    # User registration logic here (can be handled by DRF's serializers)
    return JsonResponse({'message': 'User registered successfully'})

def user_login(request):
    # Login logic here (token or session-based login)
    return JsonResponse({'message': 'User logged in successfully'})

def user_logout(request):
    # Logout logic here (clearing session or token)
    return JsonResponse({'message': 'User logged out successfully'})
