import base64
import cv2
import numpy as np

from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import RegisteredFace
from fms.models import Attendance
from .face_recognition import recognize_face


@login_required
def attendance_home(request):

    records = Attendance.objects.select_related(
        'employee',
        'employee__employee'
    ).all().order_by('-timestamp')

    return render(
        request,
        'attendance/home.html',
        {'records': records}
    )


@login_required
def recognize_and_attend(request):

    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Invalid request.'
        })

    try:
        # Get camera image
        data = request.POST.get('image')

        if not data:
            return JsonResponse({
                'success': False,
                'message': 'No image received.'
            })

        # Remove data URL prefix
        if ',' in data:
            data = data.split(',', 1)[1]

        # Decode Base64 image
        image_bytes = base64.b64decode(data)

        image_array = np.frombuffer(
            image_bytes,
            dtype=np.uint8
        )

        # Convert to OpenCV image
        image = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR
        )

        if image is None:
            return JsonResponse({
                'success': False,
                'message': 'Could not process camera image.'
            })

        # Recognize registered face
        registered_face = recognize_face(image)

        if registered_face is None:
            return JsonResponse({
                'success': False,
                'message': 'Face not recognized. Please try again.'
            })

        # Get employee profile
        employee_profile = registered_face.employee
        employee = employee_profile.employee

        # Today's date
        today = timezone.localdate()

        # -------------------------------------------------
        # CHECK WHETHER EMPLOYEE ALREADY CLOCKED IN TODAY
        # -------------------------------------------------

        existing_attendance = Attendance.objects.filter(
            employee=employee_profile,
            date=today,
            status=Attendance.IN
        ).first()

        if existing_attendance:

            return JsonResponse({
                'success': False,
                'already_present': True,
                'message': (
                    f'{employee.name} is already clocked in today.'
                ),
                'employee_name': employee.name,
                'time': existing_attendance.timestamp.strftime(
                    '%I:%M:%S %p'
                )
            })

        # -------------------------------------------------
        # CREATE NEW ATTENDANCE RECORD
        # -------------------------------------------------

        attendance = Attendance.objects.create(
            employee=employee_profile,
            status=Attendance.IN,
            marked_by_admin=False
        )

        return JsonResponse({
            'success': True,
            'already_present': False,
            'message': (
                f'Face recognized! '
                f'{employee.name} clocked in successfully.'
            ),
            'employee_name': employee.name,
            'time': attendance.timestamp.strftime(
                '%I:%M:%S %p'
            )
        })

    except Exception as e:

        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        })
