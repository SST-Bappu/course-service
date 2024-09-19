from django.db.transaction import commit
from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from course_manager.models import Course
from course_manager.serializers import CourseSerializer


# Create your views here.
class CourseView(APIView):
    serializer_class = CourseSerializer
    
    def get(self, request):
        courses = Course.objects.filter(user=request.user.id)
        serializer = self.serializer_class(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise ValidationError('Error: ' + str(e))
    
    
