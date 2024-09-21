from http.client import responses

from django.db.models import Q
from django.utils.datetime_safe import datetime
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from course_manager.models import Course, CourseView as CV
from course_manager.serializers.course_serializers import CourseSerializer
from utils import utils


# Create your views here.
class CourseView(APIView):
    serializer_class = CourseSerializer
    
    def get(self, request):
        try:
            if request.query_params.get('query'):
                query = request.query_params.get('query')
                query = Q(title__icontains=query) | Q(tags__iregex=query) | Q(category__icontains=query)
                courses = Course.objects.filter(query)
            elif request.query_params.get('id'):
                id = request.query_params.get('id')
                courses = Course.objects.filter(id=id)
                if courses:
                    view, _ = CV.objects.get_or_create(
                        course=courses[0],
                        user=request.user.id,
                        ip_address=utils.get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')[:255]
                    )
                    view.viewed_at = datetime.now()
                    view.save()
            else:
                courses = Course.objects.all()
            serializer = self.serializer_class(courses, many=True)
            response = utils.success_response(serializer.data, 'Courses retrieved successfully')
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            raise Exception('Error: ' + str(e))
    
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = utils.success_response(serializer.data, 'Course created successfully')
                return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise ValidationError('Error: ' + str(e))
