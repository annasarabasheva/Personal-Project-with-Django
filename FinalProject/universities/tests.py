from django.test import TestCase

from FinalProject.universities.forms import UniversityForm, UniversitySelectionForm
from FinalProject.universities.models import University
from django.contrib.auth import get_user_model

User = get_user_model()


class UniversityModelTest(TestCase):
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


class UniversityFormTest(TestCase):
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


class UniversitySelectionFormTest(TestCase):
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
