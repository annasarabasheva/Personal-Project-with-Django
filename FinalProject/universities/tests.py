from django.test import TestCase
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
