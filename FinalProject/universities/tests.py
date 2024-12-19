
from django.test import TestCase, Client
from django.urls import reverse

from FinalProject.students.models import Student
from FinalProject.universities.forms import UniversityForm, UniversitySelectionForm
from FinalProject.universities.models import University
from django.contrib.auth import get_user_model

User = get_user_model()


class UniversityModelTest(TestCase):  # Tests for University Model
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )

        self.university = University.objects.create(
            name="Test University",
            country="Test Country",
            city="Test City",
            logo_url="http://example.com/logo.png",
            year_established=1990,
            created_by=self.user,
        )

    def test_university_creation(self):
        self.assertEqual(self.university.name, "Test University")
        self.assertEqual(self.university.country, "Test Country")
        self.assertEqual(self.university.city, "Test City")
        self.assertEqual(self.university.logo_url, "http://example.com/logo.png")
        self.assertEqual(self.university.year_established, 1990)
        self.assertEqual(self.university.created_by, self.user)

    def test_university_str_representation(self):
        self.assertEqual(str(self.university), "Test University")

    def test_university_ordering(self):
        university_b = University.objects.create(
            name="Another University",
            country="Another Country",
            city="Another City",
        )
        universities = University.objects.all()
        self.assertEqual(list(universities), [university_b, self.university])

    def test_university_unique_name(self):
        with self.assertRaises(Exception):
            University.objects.create(
                name="Test University",
                country="Another Country",
                city="Another City",
            )

    def test_blank_and_null_fields(self):
        university = University.objects.create(
            name="Blank University",
            country="Blank Country",
            city="Blank City",
        )
        self.assertIsNone(university.logo_url)
        self.assertIsNone(university.year_established)
        self.assertIsNone(university.created_by)


class UniversityFormTest(TestCase):  # Tests for UniversityForm
    def test_valid_form(self):
        form_data = {
            "name": "Test University",
            "country": "Test Country",
            "city": "Test City",
            "logo_url": "http://example.com/logo.png",
            "year_established": 1999,
        }
        form = UniversityForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_year_established(self):
        form_data = {
            "name": "Test University",
            "country": "Test Country",
            "city": "Test City",
            "logo_url": "http://example.com/logo.png",
            "year_established": 900,
        }
        form = UniversityForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("year_established", form.errors)
        self.assertEqual(
            form.errors["year_established"][0], "Year of establishment must be a valid year."
        )

    def test_missing_required_fields(self):
        form_data = {
            "name": "",
            "country": "",
            "city": "",
            "logo_url": "http://example.com/logo.png",
            "year_established": 1999,
        }
        form = UniversityForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("country", form.errors)
        self.assertIn("city", form.errors)

    def test_optional_fields(self):
        form_data = {
            "name": "Test University",
            "country": "Test Country",
            "city": "Test City",
            "logo_url": "",
            "year_established": 2005,
        }
        form = UniversityForm(data=form_data)
        self.assertTrue(form.is_valid())


class UniversitySelectionFormTest(TestCase):  # Tests for UniversitySelectionForm
    def setUp(self):
        self.university = University.objects.create(
            name="Existing University",
            country="Existing Country",
            city="Existing City",
        )

    def test_valid_existing_university(self):
        form_data = {
            "existing_university": self.university.id,
            "new_university_name": "",
            "country": "",
            "city": "",
            "year_established": "",
            "logo_url": "",
        }
        form = UniversitySelectionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_new_university(self):
        form_data = {
            "existing_university": "",
            "new_university_name": "New University",
            "country": "New Country",
            "city": "New City",
            "year_established": 2022,
            "logo_url": "http://example.com/new-logo.png",
        }
        form = UniversitySelectionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_duplicate_university_name(self):
        form_data = {
            "existing_university": "",
            "new_university_name": "Existing University",  # Duplicate name
            "country": "New Country",
            "city": "New City",
            "year_established": 2022,
            "logo_url": "http://example.com/new-logo.png",
        }
        form = UniversitySelectionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("new_university_name", form.errors)
        self.assertEqual(
            form.errors["new_university_name"][0],
            "A university with the name 'Existing University' already exists in our database.",
        )

    def test_missing_fields(self):
        form_data = {
            "existing_university": "",
            "new_university_name": "Partial University",
            "country": "",
            "city": "",
        }
        form = UniversitySelectionForm(data=form_data)
        self.assertTrue(form.is_valid())


class UniversityIntegrationTests(TestCase): # Integration test for add_university and edit_university views
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
        self.student = Student.objects.create(
            profile=self.user.profile,
            first_name="John",
            last_name="Doe",
            field_of_study="Computer Science",
            year_of_study=2,
            location="New York",
            bio="Test student bio.",
        )

        self.existing_university = University.objects.create(
            name="Existing University",
            country="Test Country",
            city="Test City",
            year_established=1985,
        )

        self.client = Client()
        self.client.login(username="testuser", password="testpassword")

    def test_add_new_university(self):
        response = self.client.post(reverse("add-university"), {
            "new_university_name": "New University",
            "country": "New Country",
            "city": "New City",
            "year_established": 2000,
            "logo_url": "http://example.com/logo.png",
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(University.objects.filter(name="New University").exists())
        self.student.refresh_from_db()
        self.assertEqual(self.student.university.name, "New University")

    def test_add_existing_university_to_student(self):
        response = self.client.post(reverse("add-university"), {
            "existing_university": self.existing_university.id,
        })
        self.assertEqual(response.status_code, 302)
        self.student.refresh_from_db()
        self.assertEqual(self.student.university, self.existing_university)

    def test_edit_university_no_access(self):
        response = self.client.get(reverse("edit-university"))
        self.assertEqual(response.status_code, 403)