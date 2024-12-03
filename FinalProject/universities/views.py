from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

from FinalProject.universities.forms import UniversityForm
from FinalProject.universities.models import University


def catalog(request):
    country_query = request.GET.get('query', '')

    if not country_query:
        return redirect('all-unis')

    universities = University.objects.filter(country__icontains=country_query)

    context = {
        'universities': universities,
        'country_query': country_query,
    }
    return render(request, 'universities/catalog.html', context)


def all_unis(request):
    unis = University.objects.all()

    context = {
        'unis': unis,
    }

    return render(request, 'universities/all-unis.html', context)


@login_required
def add_university(request):
    user_university = University.objects.filter(created_by=request.user).first()

    if user_university:
        return redirect('my-university', university_id=user_university.id)

    if not request.user.profile.is_student:
        return redirect('home')  # Redirect non-student users

    if request.method == 'POST':
        form = UniversityForm(request.POST)
        if form.is_valid():
            university = form.save(commit=False)
            university.created_by = request.user  # Associate university with the creator
            university.save()
            return redirect('my-university')
    else:
        form = UniversityForm()

    context = {
        'form': form,
    }
    return render(request, 'universities/add-university.html', context)


@login_required
def edit_university(request):
    university = getattr(request.user, 'university', None)  # Get the user's university
    if not university:
        return HttpResponseForbidden("You don't have a university to edit.")

    if request.method == 'POST':
        form = UniversityForm(request.POST, instance=university)
        if form.is_valid():
            form.save()
            return redirect('my-university')
    else:
        form = UniversityForm(instance=university)

    context = {
        'form': form,
    }
    return render(request, 'universities/edit-university.html', context)


@login_required
def delete_university(request):
    university = getattr(request.user, 'university', None)
    if not university:
        return HttpResponseForbidden("You don't have a university to delete.")

    if request.method == 'POST' and 'confirm' in request.POST:
        university.delete()
        return redirect('my-university')

    context = {
        'university': university,
    }
    return render(request, 'universities/delete-university.html', context)


@login_required
def my_university(request):
    # Fetch the university associated with the logged-in user
    university = getattr(request.user, 'university', None)

    # If no university is found, show an error or redirect
    if not university:
        return HttpResponseForbidden("You don't have a university to view.")

    context = {
        'university': university,
    }
    return render(request, 'universities/my-university.html', context)
