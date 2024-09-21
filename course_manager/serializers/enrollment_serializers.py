from rest_framework import serializers
from course_manager.models import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ('id', 'user', 'enrolled_at')