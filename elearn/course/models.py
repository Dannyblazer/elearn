from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    media_file = models.FileField(upload_to='course_media/')
    start_date = models.DateField()
    end_date = models.DateField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name='courses_enrolled', blank=True)

    def __str__(self):
        return self.title
