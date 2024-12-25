from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Voter, Candidate, Vote
from .forms import VoterRegistrationForm
from oauth2_provider.views import TokenView
from oauth2_provider.oauth2_backends import get_oauthlib_core
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

import face_recognition
import cv2
import numpy as np

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = VoterRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            voter = form.save(commit=False)
            voter.face_image = request.FILES.get('face_image')

            # Capture face encoding
            video_capture = cv2.VideoCapture(0)
            ret, frame = video_capture.read()

            if not ret:
                return JsonResponse({'message': 'Failed to capture image from camera.'}, status=400)

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)

            if face_locations:
                face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
                voter.face_encoding = face_encoding.tobytes()
                voter.save()
                video_capture.release()
                return JsonResponse({'message': 'Voter registered successfully!'})
            else:
                video_capture.release()
                return JsonResponse({'message': 'No face detected in the image.'}, status=400)

        return JsonResponse({'message': 'Invalid data'}, status=400)
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def face_recognition_view(request):
    return JsonResponse({'status': 'face recognition complete'})

class CustomTokenView(TokenView):
    def post(self, request, *args, **kwargs):
        voter_id = request.data.get('voter_id')
        face_data = request.FILES['face_image'].read()

        try:
            voter = Voter.objects.get(voter_id=voter_id)
            known_face_encoding = np.frombuffer(voter.face_encoding, dtype=np.float64)

            nparr = np.frombuffer(face_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)

            if face_locations:
                current_face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
                matches = face_recognition.compare_faces([known_face_encoding], current_face_encoding)

                if matches[0]:
                    oauthlib_core = get_oauthlib_core()
                    response = oauthlib_core.create_token_response(request)
                    return JsonResponse(response[0])
                else:
                    return JsonResponse({'error': 'Face not recognized'}, status=400)
            else:
                return JsonResponse({'error': 'No face detected'}, status=400)

        except Voter.DoesNotExist:
            return JsonResponse({'error': 'Voter ID not found'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred.', 'details': str(e)}, status=500)

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
        candidate_id = request.data.get('candidate_id')
        voter_id = request.data.get('voter_id')
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
