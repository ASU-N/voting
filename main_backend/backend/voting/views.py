import cv2
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Voter
import face_voting_system

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
                    return JsonResponse({'success': True, 'message': 'Face recognized successfully.'})
                else:
                    return JsonResponse({'success': False, 'message': 'Face not recognized.'})
            else:
                return JsonResponse({'success': False, 'message': 'No face detected in the image.'})

        except Voter.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Voter ID not found.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
