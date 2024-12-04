from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from FinalProject.students.models import Student
from FinalProject.universities.forms import UniversitySelectionForm, UniversityForm
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
    student = get_object_or_404(Student, profile=request.user.profile)

    if request.method == 'POST':
        form = UniversitySelectionForm(request.POST)
        if form.is_valid():
            existing_university = form.cleaned_data.get('existing_university')
            new_university_name = form.cleaned_data.get('new_university_name')
            country = form.cleaned_data.get('country')
            city = form.cleaned_data.get('city')
            description = form.cleaned_data.get('description')
            year_established = form.cleaned_data.get('year_established')
            logo_url = form.cleaned_data.get('logo_url')

            if existing_university:
                student.university = existing_university
                student.save()
                return redirect('all-unis')
            elif new_university_name:
                # Create a new university
                university = University.objects.create(
                    name=new_university_name,
                    country=country,
                    city=city,
                    description=description,
                    year_established=year_established,
                    logo_url=logo_url,
                    created_by=request.user,
                )
                student.university = university
                student.save()
            else:
                form.add_error(None, "Please select an existing university or provide a new one.")
                return render(request, 'universities/add-university.html', {'form': form})

            # Redirect to all universities
            return redirect('all-unis')

    else:
        form = UniversitySelectionForm()

    return render(request, 'universities/add-university.html', {'form': form})

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



