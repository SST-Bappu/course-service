from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from course_manager.models import Course, Enrollment
from course_manager.serializers.course_serializers import CourseSerializer
from django.apps import apps
from utils import utils

# Create your views here.
class RecommenderView(APIView):
    serializer_class = CourseSerializer
    
    def get(self, request):
        try:
            user_id = request.user.id
            recommender = apps.get_app_config('recommender').model
            
            if not recommender:
                return Response({"message": "Recommendation model not available."}, status=503)
            
            # Get all course IDs
            all_course_ids = Course.objects.values_list('id', flat=True)
            
            # Get courses the user has already enrolled in
            enrolled_course_ids = Enrollment.objects.filter(user=user_id).values_list('course_id', flat=True)
            
            # Predict ratings for all courses the user hasn't enrolled in
            predictions = []
            for course_id in all_course_ids:
                if course_id in enrolled_course_ids:
                    continue
                pred = recommender.predict(user_id, course_id)
                predictions.append((course_id, pred.est))
            
            # Sort predictions by estimated rating in descending order
            predictions.sort(key=lambda x: x[1], reverse=True)
            
            # Get top N recommendations
            top_n = 5
            top_courses = [course_id for course_id, _ in predictions[:top_n]]
            
            # Fetch course details
            recommended_courses = Course.objects.filter(id__in=top_courses)
            serializer = self.serializer_class(recommended_courses, many=True)
            response = utils.success_response(serializer.data, 'Courses recommendation retrieved successfully')
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            raise Exception('Error: ' + str(e))