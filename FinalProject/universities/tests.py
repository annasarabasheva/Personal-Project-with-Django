
from django.test import TestCase, Client
from django.urls import reverse

from FinalProject.students.models import Student
from FinalProject.universities.forms import UniversityForm, UniversitySelectionForm
from FinalProject.universities.models import University
from django.contrib.auth import get_user_model

User = get_user_model()


class UniversityModelTest(TestCase):  # Tests for University Model
    def setUp(self):
        # Create a user to test the `created_by` field
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",  # Include email as it's required
            password="testpassword"
        )

        # Create a university instance for testing
        self.university = University.objects.create(
            name="Test University",
            country="Test Country",
            city="Test City",
            description="A top-notch university.",
            logo_url="http://example.com/logo.png",
            year_established=1990,
            created_by=self.user,
        )

    def test_university_creation(self):
        """Test that a University instance is created successfully."""
        self.assertEqual(self.university.name, "Test University")
        self.assertEqual(self.university.country, "Test Country")
        self.assertEqual(self.university.city, "Test City")
        self.assertEqual(self.university.description, "A top-notch university.")
        self.assertEqual(self.university.logo_url, "http://example.com/logo.png")
        self.assertEqual(self.university.year_established, 1990)
        self.assertEqual(self.university.created_by, self.user)

    def test_university_str_representation(self):
        """Test the string representation of the University model."""
        self.assertEqual(str(self.university), "Test University")

    def test_university_ordering(self):
        """Test that universities are ordered by name."""
        university_b = University.objects.create(
            name="Another University",
            country="Another Country",
            city="Another City",
        )
        universities = University.objects.all()
        self.assertEqual(list(universities), [university_b, self.university])

    def test_university_unique_name(self):
        """Test that the name field is unique."""
        with self.assertRaises(Exception):
            University.objects.create(
                name="Test University",
                country="Another Country",
                city="Another City",
            )

    def test_blank_and_null_fields(self):
        """Test that optional fields can be blank or null."""
        university = University.objects.create(
            name="Blank University",
            country="Blank Country",
            city="Blank City",
        )
        self.assertIsNone(university.description)
        self.assertIsNone(university.logo_url)
        self.assertIsNone(university.year_established)
        self.assertIsNone(university.created_by)


class UniversityFormTest(TestCase):  # Tests for UniversityForm
    def test_valid_form(self):
        """Test that a valid form is accepted."""
        form_data = {
            "name": "Test University",
            "country": "Test Country",
            "city": "Test City",
            "description": "A top university for science and technology.",
            "logo_url": "http://example.com/logo.png",
            "year_established": 1999,
        }
        form = UniversityForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_year_established(self):
        """Test that the form rejects invalid year_established values."""
        form_data = {
            "name": "Test University",
            "country": "Test Country",
            "city": "Test City",
            "description": "A top university for science and technology.",
            "logo_url": "http://example.com/logo.png",
            "year_established": 900,  # Invalid year
        }
        form = UniversityForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("year_established", form.errors)
        self.assertEqual(
            form.errors["year_established"][0], "Year of establishment must be a valid year."
        )

    def test_missing_required_fields(self):
        """Test that missing required fields causes validation errors."""
        form_data = {
            "name": "",
            "country": "",
            "city": "",
            "description": "A top university for science and technology.",
            "logo_url": "http://example.com/logo.png",
            "year_established": 1999,
        }
        form = UniversityForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("country", form.errors)
        self.assertIn("city", form.errors)

    def test_optional_fields(self):
        """Test that optional fields can be left blank."""
        form_data = {
            "name": "Test University",
            "country": "Test Country",
            "city": "Test City",
            "description": "",
            "logo_url": "",
            "year_established": 2005,
        }
        form = UniversityForm(data=form_data)
        self.assertTrue(form.is_valid())


class UniversitySelectionFormTest(TestCase):  # Tests for UniversitySelectionForm
    def setUp(self):
        # Set up a sample university for testing
        self.university = University.objects.create(
            name="Existing University",
            country="Existing Country",
            city="Existing City",
        )

    def test_valid_existing_university(self):
        """Test form validation when an existing university is selected."""
        form_data = {
            "existing_university": self.university.id,
            "new_university_name": "",
            "country": "",
            "city": "",
            "description": "",
            "year_established": "",
            "logo_url": "",
        }
        form = UniversitySelectionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_new_university(self):
        """Test form validation when a new university is provided."""
        form_data = {
            "existing_university": "",
            "new_university_name": "New University",
            "country": "New Country",
            "city": "New City",
            "description": "A new university for testing.",
            "year_established": 2022,
            "logo_url": "http://example.com/new-logo.png",
        }
        form = UniversitySelectionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_duplicate_university_name(self):
        """Test form validation when a duplicate university name is provided."""
        form_data = {
            "existing_university": "",
            "new_university_name": "Existing University",  # Duplicate name
            "country": "New Country",
            "city": "New City",
            "description": "A duplicate name test.",
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
        """Test that form validates properly when only necessary fields are provided."""
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
        # Create a test user and student
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

        # Create an existing university for testing
        self.existing_university = University.objects.create(
            name="Existing University",
            country="Test Country",
            city="Test City",
            year_established=1985,
        )

        # Log in the test user
        self.client = Client()
        self.client.login(username="testuser", password="testpassword")

    # Test for add_university
    def test_add_new_university(self):
        """Test successfully adding a new university."""
        response = self.client.post(reverse("add-university"), {
            "new_university_name": "New University",
            "country": "New Country",
            "city": "New City",
            "year_established": 2000,
            "description": "A new university for testing.",
            "logo_url": "http://example.com/logo.png",
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(University.objects.filter(name="New University").exists())
        self.student.refresh_from_db()
        self.assertEqual(self.student.university.name, "New University")

    def test_add_existing_university_to_student(self):
        """Test associating an existing university with a student."""
        response = self.client.post(reverse("add-university"), {
            "existing_university": self.existing_university.id,
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.student.refresh_from_db()
        self.assertEqual(self.student.university, self.existing_university)

    def test_edit_university_no_access(self):
        """Test forbidden access when no university is associated with the user."""
        response = self.client.get(reverse("edit-university"))
        self.assertEqual(response.status_code, 403)  # Forbidden access