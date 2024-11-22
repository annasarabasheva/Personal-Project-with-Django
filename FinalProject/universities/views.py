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
    if hasattr(request.user, 'university'):
        return HttpResponseForbidden("You have already added a university.")

    if not request.user.profile.is_student:
        return redirect('home')  # Redirect non-student users

    if request.method == 'POST':
        form = UniversityForm(request.POST)
        if form.is_valid():
            university = form.save(commit=False)
            university.created_by = request.user  # Associate university with the creator
            university.save()
            return redirect('all-unis')
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
            return redirect('all-unis')
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
        return redirect('all-unis')

    context = {
        'university': university,
    }
    return render(request, 'universities/delete-university.html', context)