from django.urls import path
from .views import ClassView, StudentView, AttendanceView, StudentAttendanceView

urlpatterns = [
    path('classes/', ClassView.as_view()),
    path('classes/<int:class_id>/', ClassView.as_view()),
    path('students/', StudentView.as_view()),
    path('students/<str:id>/', StudentView.as_view()),
    path('attendance/', AttendanceView.as_view()),
    path('attendance/<int:class_id>/<int:student_id>/<str:date>/', AttendanceView.as_view()),
    path('student-attendance/', StudentAttendanceView.as_view()),
    path('student-attendance/<int:student_id>/', StudentAttendanceView.as_view()),
    path('student-attendance/<int:student_id>/<int:month>/', StudentAttendanceView.as_view()),
]
