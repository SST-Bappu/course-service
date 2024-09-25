from http.client import responses

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

import utils.utils
from course_manager.models import Enrollment
from course_manager.serializers.enrollment_serializers import EnrollmentSerializer


class EnrollmentView(APIView):
    serializer_class = EnrollmentSerializer
    
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user.id)
                response = utils.utils.success_response(serializer.data, 'Enrollment created successfully')
                return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise ValidationError('Error: ' + str(e))
    
    def get(self, request):
        try:
            user_id = request.user.id
            enrollments = Enrollment.objects.filter(user=user_id)
            serializer = self.serializer_class(enrollments, many=True)
            response = utils.utils.success_response(serializer.data, 'Enrollments retrieved successfully')
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            raise Exception('Error: ' + str(e))