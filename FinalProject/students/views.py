from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from FinalProject.students.forms import MessageForm, StudentForm
from FinalProject.students.models import Student, Message
from FinalProject.universities.models import University


def university_students(request, university_id):
    university = get_object_or_404(University, id=university_id)
    students = university.students.all()
    return render(request, 'students/university-students.html', {
        'university': university,
        'students': students,
    })


def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    messages = student.messages.filter(parent_message__isnull=True).order_by('timestamp')  # Fetch parent messages only

    if request.method == 'POST' and request.user.is_authenticated:
        parent_message_id = request.POST.get('parent_message_id')
        content = request.POST.get('content')

        if parent_message_id:
            parent_message = get_object_or_404(Message, id=parent_message_id)
            Message.objects.create(
                sender=request.user,
                student=student,
                parent_message=parent_message,
                content=content,
            )
        else:
            Message.objects.create(
                sender=request.user,
                student=student,
                content=content,
            )
        return redirect('student-detail', student_id=student.id)  # Redirect to avoid duplicate submissions

    context = {
        'student': student,
        'messages': messages,
        'form': MessageForm(),
    }
    return render(request, 'students/student-detail.html', context)


@login_required
def student_edit(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    # Ensure only the owner can edit their profile
    if student.profile.user != request.user:
        return redirect('student-detail', student_id=student.id)

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student-detail', student_id=student.id)
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/student-edit.html', {'form': form, 'student': student})


@login_required
def student_delete(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    # Ensure only the owner can delete their profile
    if student.profile.user != request.user:
        return redirect('student-detail', student_id=student.id)

    if request.method == 'POST':
        student.delete()
        profile = request.user.profile
        profile.is_student = False
        profile.save()

        return redirect('all-unis')

    return redirect('student-detail', student_id=student.id)


@login_required
def student_form_view(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.profile = profile  # Link the student to the current user's profile
            student.save()
            return redirect('add-university')  # Adjust the redirect as needed
    else:
        form = StudentForm()

    return render(request, 'students/student-form.html', {'form': form})