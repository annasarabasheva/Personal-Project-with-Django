from django.test import TestCase, Client
from django.urls import reverse

from FinalProject.accounts.models import Profile
from FinalProject.students.forms import StudentForm
from FinalProject.students.models import Student
from FinalProject.universities.models import University
from django.contrib.auth import get_user_model

User = get_user_model()


class StudentIntegrationTests(TestCase): # Integration tests for Student model
    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            username="testuser1",
            email="testuser1@example.com",
            password="testpassword"
        )
        self.profile, _ = Profile.objects.get_or_create(user=self.user)

        self.university = University.objects.create(
            name="Test University",
            country="Test Country",
            city="Test City",
            year_established=1990,
        )

    def tearDown(self):
        # Clean up any created objects
        Student.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()
        University.objects.all().delete()

    def test_create_student_with_university(self):
        student = Student.objects.create(
            profile=self.profile,
            university=self.university,
            first_name="John",
            last_name="Doe",
            field_of_study="Computer Science",
            year_of_study=2,
            location="New York",
            bio="Test bio",
            photo="http://example.com/photo.jpg",
        )
        self.assertEqual(student.university, self.university)
        self.assertEqual(student.first_name, "John")
        self.assertEqual(student.last_name, "Doe")
        self.assertEqual(student.field_of_study, "Computer Science")

    def test_create_student_without_university(self):
        student = Student.objects.create(
            profile=self.profile,
            university=None,  # No university
            first_name="Jane",
            last_name="Smith",
            field_of_study="Biology",
            year_of_study=1,
            location="Boston",
            bio="Another test bio",
        )
        self.assertIsNone(student.university)
        self.assertEqual(student.first_name, "Jane")
        self.assertEqual(student.field_of_study, "Biology")

    def test_cascade_delete_student_with_profile(self):
        student = Student.objects.create(
            profile=self.profile,
            university=self.university,
            first_name="John",
            last_name="Doe",
            field_of_study="Physics",
            year_of_study=3,
            location="Los Angeles",
        )
        self.profile.delete()
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(pk=student.pk)


class StudentFormTests(TestCase):  # Integration tests for StudentForm
    def test_valid_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'field_of_study': 'Computer Science',
            'year_of_study': 2,
            'location': 'New York',
            'bio': 'I love programming.',
            'photo': 'http://example.com/photo.jpg',
        }
        form = StudentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_year_of_study(self):
        form_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'field_of_study': 'Mathematics',
            'year_of_study': -1,
            'location': 'Boston',
            'bio': 'A curious mathematician.',
            'photo': 'http://example.com/photo.jpg',
        }
        form = StudentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('year_of_study', form.errors)
        self.assertEqual(
            form.errors['year_of_study'][0],
            "Year of study must be greater than or equal to 1."
        )


class StudentViewsIntegrationTests(TestCase):  # Integration test for edit, delete and detail student views
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")

        if not hasattr(cls.user, 'profile'):
            cls.profile = Profile.objects.create(user=cls.user)

        cls.university = University.objects.create(name="Test University", country="Test Country", city="Test City")

    def setUp(self):
        self.client = Client()
        self.client.login(username="testuser", password="password123")
        self.student = Student.objects.create(
            profile=self.user.profile,
            first_name="Test",
            last_name="Student",
            field_of_study="Computer Science",
            year_of_study=2,
            location="Test City",
            bio="This is a test student.",
            photo="http://example.com/photo.jpg",
        )

    def test_student_detail_view(self):
        url = reverse("student-detail", args=[self.student.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Student")
        self.assertContains(response, "Computer Science")

    def test_student_edit_view(self):
        url = reverse("student-edit", args=[self.student.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit your student information")

    def test_student_edit_view_post(self):
        """Test editing a student's details."""
        url = reverse("student-edit", args=[self.student.id])
        data = {
            "first_name": "Updated",
            "last_name": "Student",
            "field_of_study": "Data Science",
            "year_of_study": 3,
            "location": "Updated City",
            "bio": "Updated bio.",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.student.refresh_from_db()
        self.assertEqual(self.student.first_name, "Updated")
        self.assertEqual(self.student.field_of_study, "Data Science")

    def test_student_delete_view(self):
        url = reverse("student-delete", args=[self.student.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(id=self.student.id)



