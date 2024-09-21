from http.client import responses

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

import utils.utils
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