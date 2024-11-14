from django.shortcuts import render, redirect
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