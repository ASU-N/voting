# views.py
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Voter, Candidate, Vote
from .forms import VoterRegistrationForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import cv2
import face_voting_system

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = VoterRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Voter registered successfully!'})
        return JsonResponse({'message': 'Invalid data'}, status=400)
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def face_recognition_view(request):
    if request.method == 'POST':
        voter_id = request.POST.get('voter_id')
        try:
            voter = Voter.objects.get(voter_id=voter_id)
            known_image = cv2.imread(voter.image_path)
            video_capture = cv2.VideoCapture(0)
            ret, frame = video_capture.read()

            if not ret:
                return JsonResponse({'success': False, 'message': 'Failed to capture image from camera.'})

            faces = face_voting_system.detect_faces(frame)
            video_capture.release()

            if faces:
                match = face_voting_system.verify_face(known_image, frame)
                if match:
                    refresh = RefreshToken.for_user(voter)
                    return JsonResponse({
                        'success': True,
                        'message': 'Face recognized successfully.',
                        'access': str(refresh.access_token),
                        'refresh': str(refresh)
                    })
                else:
                    return JsonResponse({'success': False, 'message': 'Face not recognized.'})
            else:
                return JsonResponse({'success': False, 'message': 'No face detected in the image.'})

        except Voter.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Voter ID not found.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_candidates(request):
    candidates = Candidate.objects.all()
    candidate_list = [{"id": candidate.id, "name": candidate.name, "party": candidate.party, "image": candidate.image.url} for candidate in candidates]
    return JsonResponse(candidate_list, safe=False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def cast_vote(request):
    if request.method == 'POST':
        candidate_id = request.POST.get('candidate_id')
        voter_id = request.POST.get('voter_id')
        encrypted_voter_id = Vote.encrypt_voter_id(voter_id)
        try:
            candidate = Candidate.objects.get(id=candidate_id)
            Vote.objects.create(candidate=candidate, encrypted_voter_id=encrypted_voter_id)
            return JsonResponse({'success': True, 'message': 'Vote cast successfully!'})
        except Candidate.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Candidate not found.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_results(request):
    candidates = Candidate.objects.all()
    results = []
    for candidate in candidates:
        vote_count = Vote.objects.filter(candidate=candidate).count()
        results.append({
            'name': candidate.name,
            'party': candidate.party,
            'vote_count': vote_count
        })
    return JsonResponse(results, safe=False)
