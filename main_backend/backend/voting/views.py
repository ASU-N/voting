from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Voter, Candidate, Vote
from .forms import VoterRegistrationForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import face_recognition
import cv2
import face_recognition
import numpy as np

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = VoterRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the voter ID and face image
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
                voter.face_encoding = face_encoding.tobytes()  # Save the face encoding
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
    if request.method == 'POST':
        voter_id = request.POST.get('voter_id')
        try:
            voter = Voter.objects.get(voter_id=voter_id)
            face_encoding = np.frombuffer(voter.face_encoding, dtype=np.float64)

            video_capture = cv2.VideoCapture(0)
            ret, frame = video_capture.read()

            if not ret:
                return JsonResponse({'success': False, 'message': 'Failed to capture image from camera.'})

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)

            if face_locations:
                login_face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
                match = face_recognition.compare_faces([face_encoding], login_face_encoding)

                video_capture.release()

                if match[0]:
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
                video_capture.release()
                return JsonResponse({'success': False, 'message': 'No face detected in the image.'})

        except Voter.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Voter ID not found.'})
        except Exception as e:
            print(f"Unexpected error: {e}")
            return JsonResponse({'success': False, 'message': 'An unexpected error occurred.', 'error': str(e)})
    
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
