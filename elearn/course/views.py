from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course
from course.forms import CourseForm

@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('course_list')  # Redirect to a course list view
    else:
        form = CourseForm()
    return render(request, 'create_course.html', {'form': form})

@login_required
def update_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if course.instructor != request.user:
        return redirect('course_list')  # Redirect if not the course instructor
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')  # Redirect to a course list view
    else:
        form = CourseForm(instance=course)
    return render(request, 'update_course.html', {'form': form, 'course': course})

@login_required
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if course.instructor == request.user:
        course.delete()
    return redirect('course_list')  # Redirect to a course list view

@login_required
def register_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    # Add registration logic here (e.g., adding the student to the course)
    return redirect('course_detail', pk=pk)  # Redirect to a course detail view

# You can define your course list, detail, and other views here
