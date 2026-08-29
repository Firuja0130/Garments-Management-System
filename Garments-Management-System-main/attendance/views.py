import base64
import cv2
import numpy as np

from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone

from .models import RegisteredFace
from fms.models import Attendance
from .face_recognition import recognize_face


# ============================================================
# ATTENDANCE HOME
# PUBLIC PAGE - NO EMPLOYEE LOGIN REQUIRED
# ============================================================

def attendance_home(request):

    records = Attendance.objects.select_related(
        'employee',
        'employee__employee'
    ).all().order_by(
        '-date',
        '-clock_in'
    )

    return render(
        request,
        'attendance/home.html',
        {
            'records': records
        }
    )


# ============================================================
# FACE RECOGNITION + CLOCK IN
# PUBLIC - NO EMPLOYEE LOGIN REQUIRED
# ============================================================

def recognize_and_attend(request):

    if request.method != 'POST':

        return JsonResponse({
            'success': False,
            'message': 'Invalid request.'
        })

    try:

        # ---------------------------------------------
        # GET CAMERA IMAGE
        # ---------------------------------------------

        data = request.POST.get('image')

        if not data:

            return JsonResponse({
                'success': False,
                'message': 'No image received.'
            })

        # ---------------------------------------------
        # REMOVE DATA URL PREFIX
        # ---------------------------------------------

        if ',' in data:

            data = data.split(
                ',',
                1
            )[1]

        # ---------------------------------------------
        # DECODE BASE64 IMAGE
        # ---------------------------------------------

        image_bytes = base64.b64decode(
            data
        )

        image_array = np.frombuffer(
            image_bytes,
            dtype=np.uint8
        )

        image = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR
        )

        if image is None:

            return JsonResponse({
                'success': False,
                'message': 'Could not process camera image.'
            })

        # ---------------------------------------------
        # RECOGNIZE FACE
        # ---------------------------------------------

        registered_face = recognize_face(
            image
        )

        if registered_face is None:

            return JsonResponse({
                'success': False,
                'message': 'Face not recognized. Please try again.'
            })

        # ---------------------------------------------
        # GET EMPLOYEE
        # ---------------------------------------------

        employee_profile = registered_face.employee
        employee = employee_profile.employee

        today = timezone.localdate()

        # ---------------------------------------------
        # FIND TODAY'S ATTENDANCE
        # ---------------------------------------------

        existing_attendance = Attendance.objects.filter(
            employee=employee_profile,
            date=today
        ).first()

        # ---------------------------------------------
        # ALREADY CLOCKED IN
        # ---------------------------------------------

        if (
            existing_attendance
            and existing_attendance.clock_in
        ):

            # -----------------------------------------
            # ALREADY CLOCKED OUT
            # -----------------------------------------

            if existing_attendance.clock_out:

                return JsonResponse({

                    'success': False,

                    'already_present': True,

                    'already_clocked_out': True,

                    'message': (
                        f'{employee.name} has already '
                        f'completed attendance for today.'
                    ),

                    'employee_name': employee.name,

                    'clock_in': (
                        existing_attendance.clock_in.strftime(
                            '%I:%M:%S %p'
                        )
                    ),

                    'clock_out': (
                        existing_attendance.clock_out.strftime(
                            '%I:%M:%S %p'
                        )
                    ),

                    'total_working_time': (
                        str(
                            existing_attendance.total_working_time
                        )
                        if existing_attendance.total_working_time
                        else None
                    )

                })

            # -----------------------------------------
            # CLOCKED IN BUT NOT CLOCKED OUT
            # -----------------------------------------

            return JsonResponse({

                'success': False,

                'already_present': True,

                'already_clocked_out': False,

                'message': (
                    f'{employee.name} is already '
                    f'clocked in today.'
                ),

                'employee_name': employee.name,

                'clock_in': (
                    existing_attendance.clock_in.strftime(
                        '%I:%M:%S %p'
                    )
                )

            })

        # ---------------------------------------------
        # CREATE / UPDATE CLOCK-IN RECORD
        # ---------------------------------------------

        current_time = timezone.now()

        if existing_attendance:

            # Existing empty attendance record

            existing_attendance.clock_in = current_time

            existing_attendance.marked_by_admin = False

            existing_attendance.save()

            attendance = existing_attendance

        else:

            # Create new attendance record

            attendance = Attendance.objects.create(

                employee=employee_profile,

                date=today,

                clock_in=current_time,

                marked_by_admin=False

            )

        # ---------------------------------------------
        # SUCCESS RESPONSE
        # ---------------------------------------------

        return JsonResponse({

            'success': True,

            'action': 'clock_in',

            'already_present': False,

            'message': (
                f'Face recognized! '
                f'{employee.name} clocked in successfully.'
            ),

            'employee_name': employee.name,

            'clock_in': (
                attendance.clock_in.strftime(
                    '%I:%M:%S %p'
                )
            )

        })

    except Exception as e:

        return JsonResponse({

            'success': False,

            'message': f'Error: {str(e)}'

        })


# ============================================================
# CLOCK OUT
# PUBLIC - NO EMPLOYEE LOGIN REQUIRED
# ============================================================

def clock_out(request):

    if request.method != 'POST':

        return JsonResponse({

            'success': False,

            'message': 'Invalid request.'

        })

    try:

        # ---------------------------------------------
        # GET CAMERA IMAGE
        # ---------------------------------------------

        data = request.POST.get('image')

        if not data:

            return JsonResponse({

                'success': False,

                'message': 'No image received.'

            })

        # ---------------------------------------------
        # REMOVE DATA URL PREFIX
        # ---------------------------------------------

        if ',' in data:

            data = data.split(
                ',',
                1
            )[1]

        # ---------------------------------------------
        # DECODE BASE64 IMAGE
        # ---------------------------------------------

        image_bytes = base64.b64decode(
            data
        )

        image_array = np.frombuffer(
            image_bytes,
            dtype=np.uint8
        )

        image = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR
        )

        if image is None:

            return JsonResponse({

                'success': False,

                'message': (
                    'Could not process camera image.'
                )

            })

        # ---------------------------------------------
        # RECOGNIZE FACE
        # ---------------------------------------------

        registered_face = recognize_face(
            image
        )

        if registered_face is None:

            return JsonResponse({

                'success': False,

                'message': (
                    'Face not recognized. '
                    'Please try again.'
                )

            })

        # ---------------------------------------------
        # GET EMPLOYEE
        # ---------------------------------------------

        employee_profile = registered_face.employee
        employee = employee_profile.employee

        today = timezone.localdate()

        # ---------------------------------------------
        # FIND TODAY'S ATTENDANCE
        # ---------------------------------------------

        attendance = Attendance.objects.filter(

            employee=employee_profile,

            date=today

        ).first()

        # ---------------------------------------------
        # NO CLOCK-IN
        # ---------------------------------------------

        if (
            attendance is None
            or attendance.clock_in is None
        ):

            return JsonResponse({

                'success': False,

                'message': (
                    f'{employee.name} has not '
                    f'clocked in today.'
                )

            })

        # ---------------------------------------------
        # ALREADY CLOCKED OUT
        # ---------------------------------------------

        if attendance.clock_out:

            total_time = None

            if attendance.total_working_time:

                total_seconds = int(
                    attendance.total_working_time.total_seconds()
                )

                hours = total_seconds // 3600

                minutes = (
                    total_seconds % 3600
                ) // 60

                seconds = (
                    total_seconds % 60
                )

                total_time = (
                    f'{hours} hours, '
                    f'{minutes} minutes, '
                    f'{seconds} seconds'
                )

            return JsonResponse({

                'success': False,

                'already_clocked_out': True,

                'message': (
                    f'{employee.name} has already '
                    f'clocked out today.'
                ),

                'employee_name': employee.name,

                'clock_in': (
                    attendance.clock_in.strftime(
                        '%I:%M:%S %p'
                    )
                ),

                'clock_out': (
                    attendance.clock_out.strftime(
                        '%I:%M:%S %p'
                    )
                ),

                'total_working_time': total_time

            })

        # ---------------------------------------------
        # CLOCK OUT
        # ---------------------------------------------

        clock_out_time = timezone.now()

        attendance.clock_out = clock_out_time

        # ---------------------------------------------
        # CALCULATE TOTAL WORKING TIME
        # ---------------------------------------------

        attendance.total_working_time = (
            clock_out_time
            - attendance.clock_in
        )

        attendance.save()

        # ---------------------------------------------
        # FORMAT TOTAL WORKING TIME
        # ---------------------------------------------

        total_seconds = int(
            attendance.total_working_time.total_seconds()
        )

        hours = total_seconds // 3600

        minutes = (
            total_seconds % 3600
        ) // 60

        seconds = (
            total_seconds % 60
        )

        total_time = (
            f'{hours} hours, '
            f'{minutes} minutes, '
            f'{seconds} seconds'
        )

        # ---------------------------------------------
        # SUCCESS RESPONSE
        # ---------------------------------------------

        return JsonResponse({

            'success': True,

            'action': 'clock_out',

            'message': (
                f'{employee.name} '
                f'clocked out successfully.'
            ),

            'employee_name': employee.name,

            'clock_in': (
                attendance.clock_in.strftime(
                    '%I:%M:%S %p'
                )
            ),

            'clock_out': (
                attendance.clock_out.strftime(
                    '%I:%M:%S %p'
                )
            ),

            'total_working_time': total_time

        })

    except Exception as e:

        return JsonResponse({

            'success': False,

            'message': f'Error: {str(e)}'

        })