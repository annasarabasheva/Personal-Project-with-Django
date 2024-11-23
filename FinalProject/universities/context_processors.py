from FinalProject.universities.models import University


def user_university(request):
    if request.user.is_authenticated:
        # Check if the user has a university
        user_uni = University.objects.filter(created_by=request.user).first()
        return {'user_university': user_uni}
    return {'user_university': None}
