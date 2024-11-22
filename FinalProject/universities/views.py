from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from FinalProject.universities.forms import UniversityCreationForm
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
    if not request.user.profile.is_student:
        return redirect('home')

    if request.method == 'POST':
        form = UniversityCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all-unis')
    else:
        form = UniversityCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'universities/add-university.html', context)