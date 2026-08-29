from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.attendance_home,
        name='attendance_home'
    ),

    path(
        'recognize/',
        views.recognize_and_attend,
        name='recognize_and_attend'
    ),

    path(
        'clock-out/',
        views.clock_out,
        name='clock_out'
    ),

]