from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from .models import Class, Student, Attendance
from .serializers import ClassSerializer, StudentSerializer, AttendanceSerializer
from rest_framework import status
from django.db.models import Count, Sum, F, Case, When
from django.db.models.functions import Cast
from django.db.models import FloatField
class ClassView(views.APIView):
    def get(self, request,id=None):
        if id:
            if Student.objects.filter(class_name=id).exists():
                students = Student.objects.filter(class_name=id)
                serializer = StudentSerializer(students,many=True)
                return Response(serializer.data)
        else:
            classes = Class.objects.all()
            class_data = []
            for c in classes:
                num_students = Student.objects.filter(class_name=c).count()
                average_attendance = calculate_average_attendance_rating(c.id)
                class_data.append({'id':c.id,'class': c.name, 'num_students': num_students, 'average_attendance': average_attendance})
            return Response(class_data)
            
    def post(self, request):
        serializer = ClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentView(views.APIView):
    def get(self, request,id=None):
        if id:
            if Student.objects.filter(id=id).exists():
                student = Student.objects.get(id=id)
                serializer = StudentSerializer(student)
                return Response(serializer.data)
            else:
                return Response({"message":"Student doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AttendanceView(views.APIView):
    def get(self, request,class_id=None,date=None):
        if class_id and date:
            attendance = Attendance.objects.filter(class_name_id=class_id,date=date)
            serializer = AttendanceSerializer(attendance, many=True)
            return Response(serializer.data)
        elif class_id:
            attendance = Attendance.objects.filter(class_name_id=class_id)
            serializer = AttendanceSerializer(attendance, many=True)
            return Response(serializer.data)

        else:
            attendance = Attendance.objects.all()
            serializer = AttendanceSerializer(attendance, many=True)
            return Response(serializer.data)

    def post(self, request):
        
        data = request.data
        class_name = data["class_name"] 
        student = data["student"]
        date = data["date"]
        if Attendance.objects.filter(date=date).filter(student=student).exists():
            return Response({"message":"Attendance for this date already marked"},status=status.HTTP_400_BAD_REQUEST) 
        # data["date"] = date
        serializer = AttendanceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentAttendanceView(views.APIView):
    def get(self, request, student_id=None, month=None):
        if student_id and month:
            attendance = Attendance.objects.filter(student_id=student_id, date__month=month)
            attendance_percentage = calculate_attendance_percentage(student_id, month)
            serializer = AttendanceSerializer(attendance, many=True)
            return Response({'attendance': serializer.data, 'attendance_percentage': attendance_percentage})
        elif student_id:
            attendance = Attendance.objects.filter(student_id=student_id)
            attendance_percentage = calculate_attendance_percentage(student_id)
            serializer = AttendanceSerializer(attendance, many=True)
            return Response({'attendance': serializer.data, 'attendance_percentage': attendance_percentage})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


def calculate_attendance_percentage(student_id, month=None):
    if month:
        total_classes = Attendance.objects.filter(student_id=student_id, date__month=month).count()
        attended_classes = Attendance.objects.filter(student_id=student_id, date__month=month, present=True).count()
    else:
        total_classes = Attendance.objects.filter(student_id=student_id).count()
        attended_classes = Attendance.objects.filter(student_id=student_id, present=True).count()

    if total_classes == 0:
        return 0
    else:
        return (attended_classes / total_classes) * 100


def calculate_average_attendance_rating(class_id):
    total_classes = Attendance.objects.filter(class_name_id=class_id).count()
    attended_classes = Attendance.objects.filter(class_name_id=class_id, present=True).count()

    if total_classes == 0:
        return 0
    else:
        return (attended_classes / total_classes) * 100