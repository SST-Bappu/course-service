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
    user = models.IntegerField()
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
    prerequisites = ArrayField(models.CharField(max_length=50), blank=True)  # Using JSONField for a list of strings
    tags = ArrayField(models.CharField(max_length=50), blank=True)  # Using ArrayField for a list of tags
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
