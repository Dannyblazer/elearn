from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'description', 'media_file', 'start_date', 'end_date')  # Add more fields as needed

