
from django.shortcuts import render, get_object_or_404
from FinalProject.universities.models import University


def university_students(request, university_id):
    university = get_object_or_404(University, id=university_id)
    students = university.students.all()
    return render(request, 'students/university-students.html', {
        'university': university,
        'students': students,
    })