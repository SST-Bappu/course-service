from django.contrib.postgres.fields import ArrayField
from django.db import models


class Course(models.Model):
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    ADVANCED = 'advanced'
    
    DIFFICULTY_CHOICES = [
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
    ]
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255)
    difficulty_level = models.CharField(
        max_length=15,
        choices=DIFFICULTY_CHOICES,
        default=BEGINNER,
    )
    duration_hours = models.IntegerField()
    # instructor = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming User model for instructors
    prerequisites = ArrayField(models.CharField(max_length=50), blank=True,
                               null=True)  # Using JSONField for a list of strings
    tags = ArrayField(models.CharField(max_length=50), blank=True)  # Using ArrayField for a list of tags
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.IntegerField()
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"User {self.user} enrolled in {self.course}"


class CourseView(models.Model):
    """
    Tracks when a user views a course.
    """
    user = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_views')
    viewed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # Optional: Track user's IP
    user_agent = models.CharField(max_length=255, null=True, blank=True)  # Optional: Track user's browser/device
    
    def __str__(self):
        return f"{self.user} viewed {self.course.title} at {self.viewed_at}"
