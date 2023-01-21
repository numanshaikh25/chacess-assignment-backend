from rest_framework import serializers
from .models import Class, Student, Attendance

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ('id', 'name')

class StudentSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField()
    class Meta:
        model = Student
        fields = '__all__'
    
    def create(self, validated_data):
        class_data= validated_data.pop('class_name')
        class_name = Class.objects.get(id = class_data)
        student = Student.objects.create(class_name=class_name, **validated_data)
        return student


class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.CharField()
    class_name = serializers.CharField()
    class Meta:
        model = Attendance
        fields = '__all__'

    def create(self, validated_data):
        class_data = validated_data.pop('class_name')
        class_name = Class.objects.get(id=class_data)
        student_data = validated_data.pop('student')
        student = Student.objects.get(id=student_data)
        date = validated_data.pop('date')
        present = validated_data.pop('present')
        attendance = Attendance.objects.create(class_name=class_name,student = student ,date=date,present=present)
        return attendance
