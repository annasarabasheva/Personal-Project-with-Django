from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from FinalProject.students.forms import MessageForm, StudentForm
from FinalProject.students.models import Student, Message, Rating
from FinalProject.universities.models import University


def university_students(request, university_id):
    university = get_object_or_404(University, id=university_id)
    students = university.students.annotate(average_rating=Avg('ratings__stars'))  # Annotate with average_rating

    return render(request, 'students/university-students.html', {
        'university': university,
        'students': students,
        'star_range': range(1, 6),
    })


def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    messages = student.messages.filter(parent_message__isnull=True).order_by('timestamp')

    # Ensure average_rating is rounded or cast to an int
    average_rating = int(student.average_rating())

    # Provide a range for 1 to 5 stars
    star_range = range(1, 6)

    if request.method == 'POST' and request.user.is_authenticated:
        # Process message form
        parent_message_id = request.POST.get('parent_message_id')  # Check for a parent message
        content = request.POST.get('content')  # Message content

        if parent_message_id:
            # Handle replies
            parent_message = get_object_or_404(Message, id=parent_message_id)
            Message.objects.create(
                sender=request.user,
                student=student,
                parent_message=parent_message,
                content=content,
            )
        else:
            # Handle new messages
            Message.objects.create(
                sender=request.user,
                student=student,
                content=content,
            )

        # Redirect to avoid form resubmission
        return redirect('student-detail', student_id=student.id)

    context = {
        'student': student,
        'messages': messages,
        'form': MessageForm(),
        'average_rating': average_rating,
        'star_range': star_range,
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


@login_required
def rate_student(request, student_id):
    if request.method == 'POST':
        try:
            stars = int(request.POST.get('stars', 0))
            if stars < 1 or stars > 5:
                return JsonResponse({'error': 'Invalid rating value.'}, status=400)

            student = get_object_or_404(Student, id=student_id)
            if student.profile.user == request.user:
                return JsonResponse({'error': 'You cannot rate yourself.'}, status=403)

            rating, created = Rating.objects.update_or_create(
                student=student,
                user=request.user,
                defaults={'stars': stars}
            )

            average_rating = student.average_rating()
            return JsonResponse({'message': 'Rating submitted successfully.', 'average_rating': average_rating})
        except Exception as e:
            print(f"Error: {e}")  # Log the error
            return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)