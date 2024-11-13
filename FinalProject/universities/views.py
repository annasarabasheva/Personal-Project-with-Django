
from django.shortcuts import render
from FinalProject.universities.models import University


def catalog(request):
    # Get the search query from the request
    country_query = request.GET.get('query', '')

    # Filter universities based on the country specified in the search bar
    universities = University.objects.filter(country__icontains=country_query)

    # Pass universities and search query to the template
    context = {
        'universities': universities,
        'country_query': country_query,
    }
    return render(request, 'universities/catalog.html', context)