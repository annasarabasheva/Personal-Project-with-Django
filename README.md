# 🎓 UniMatch: Student Forum Platform 🎓

UniMatch is a web-based platform built with the **Django Framework** to connect future students with current university students. The application allows users to interact through forums and direct messages and get guidance about universities.
## 🚀 Here you can find a link to my deployed project: 
  ```bash
    https://unimatchapp.azurewebsites.net/
   ```
## 🌟 What Exactly is the Project About?
UniMatch aims to provide a community-driven space where:

Future students can connect with actual students from various universities.
Users can ask questions, receive insights, and gain valuable information about university life.
The platform promotes collaboration and knowledge sharing through forums and direct interactions.

## 🔑 Application Usage

### Public Part
- **Home Page**: A welcoming introduction to the platform, where users can search for universities based on the selected country using a search bar.
- **All Unis Page**: Users can view details about each university, including location, description, and related information.
- **University-students Page**: User can see all students from specific university by clicking on it and will see small information about each student.
- **Student Detail Page**: User can see detailed information about specific student and see his/her discussions with other users but won't be able to rate or post a message to the student.
- **Forum Page** : Displays categories, threads and posts in an organized format. Users without accounts will only be able to view them, any other action is not allowed for them.
- **Login Page**: Allows existing users to log in with their username and password.
- **Register Page**: Enables new users to create an account by providing a username, email and password. Additionally, users can indicate if they are current students by checking the "Are you a student ?" box at the end of the registration form.

### Private Part (if authenticated user is not a student)
- **My Profile Page**: Users can view their personal profile information, including their activity summary (threads created, posts made, and likes received). They can also edit or delete their profile.
- **Forum Page**: Allows users to create new categories and threads, reply to existing threads, and interact with other users' posts by liking them.
- **Student Detail Page**: Provides detailed information about specific students, this time user is able to message and rate the student's helpfulness.
- **Logout Page**: Allows users to log out of the application.

### Private Part (additional information if authenticated user is a student)
- **Student Form**: After registration, if the user checked the box 'Are you a student ?', he/she will be redirected to fill in additional information about his/her student details.
- **University Form**: After filling the Student form,  user will be redirected to fill in the University form, where he/she will give information about their current university if this university doesn't already exist in our database.
- **My Student Profile Page**: Authenticated student can reply on messages from logged-in users, edit and delete his/her profile.

## ✨ Features Section

| **Feature**              | **Description**                                                                |
|---------------------------|------------------------------------------------------------------------------|
| **User Authentication**   | Secure login, registration, and logout functionality for all users.          |
| **Forum Functionality**   | Create categories, threads, and posts. Like, reply, and interact with posts.  |
| **Student Profiles**      | Manage personal profiles, send messages, and rate students' helpfulness.     |
| **University Management** | View university details, add new universities, and edit existing entries.    |
| **Search Functionality**  | Search for universities by country and filter results efficiently.           |
| **Activity Summary**      | View user activity, including threads created, posts made, and likes received.|
| **Student Management**    | Current students can provide information about their studies and university. |
| **Custom Admin Panel**    | Enhanced admin interface for managing users, students, universities, and forums.|


## 📂 Folder Structure

- **`FinalProject/`**: Root folder for the Django project configuration.
  - **`__init__.py`**: Initializes the project as a Python package.
  - **`asgi.py`**: ASGI configuration for the project
  - **`settings.py`**: Project settings, including installed apps, database configuration, and static files setup.
  - **`urls.py`**: Main URL routing for the entire project.
  - **`wsgi.py`**: WSGI configuration for deployment.

  - **`accounts/`**: (User Management):
    - - **`management/commands/create_student_group.py`**: A custom management command to create or update a group called "Student Group" with appropriate permissions.
    - - **`migrations/`**: Auto-generated migration files for account-related models.
    - - **`models/`**: Defines custom user models and profiles.
    - - **`views.py`**: Handles user registration, login, logout, and profile management.
    - - **`forms.py`**: Contains forms for user registration and profile updates.
    - - **`managers.py`**: Contains the AppUserManager class, which overrides the default user manager to manage custom user creation.
    - - **`signals.py`**: Implements a post-save signal to automatically create or update the Profile instance when a new user is created.
    - - **`urls.py`**: URL routing for account-related views.
    - - **`admin.py`**: Admin site customization for user and profile management.

  - **`common/`**: (Shared Templates and Utilities):
    - - **`views.py`**: Handles home rendering.
    - - **`urls.py`**: URL routing for common-related views.

  - **`forum/`**: (Forum Functionality):
    - - **`migrations/`**: Auto-generated migration files for forum-related models.
    - - **`models/`**: Defines following models: Category, Thread, Post.
    - - **`views.py`**: Handles CRUD operations for categories, threads and posts.
    - - **`forms.py`**: Contains forms for categories, threads and posts.
    - - **`urls.py`**: URL routing for forum-related views.
    - - **`admin.py`**: Admin site customization for Thread, Post and Category.

  - **`students/`**: (Student-Specific Functionality):
    - - **`migrations/`**: Auto-generated migration files for student-related models.
    - - **`models/`**: Defines Student, Message and Rating models.
    - - **`views.py`**: Handles CRUD operations regarding students.
    - - **`forms.py`**: Contains forms for Student and Message models.
    - - **`tests.py`**: Unit and integration tests to ensure the functionality of the students app, covering model behaviors, form validations, and view responses.
    - - **`urls.py`**: URL routing for student-related views.
    - - **`admin.py`**: Admin site customization for Student and Message.
    
  - **`universities/`**: (University Information):
    - - **`migrations/`**: Auto-generated migration files for university-related models.
    - - **`models/`**: Defines University model.
    - - **`views.py`**: Handles CRUD operations for universities.
    - - **`forms.py`**: Contains forms for existing and new universities.
    - - **`tests.py`**: Unit and integration tests to ensure the functionality of the universities app, covering model behaviors, form validations, and view responses.
    - - **`urls.py`**: URL routing for university-related views.
    - - **`admin.py`**: Admin site customization for University.

- **`static/`**: Contains following static assets:
   - - **`css/`**: Custom stylesheets for the project.
   - - **`images/`**: Default images.

- **`templates/`**: Contains global templates shared across the project:
   - - **`accounts/`**: Templates for user management features like login, register, profile details, profile editing and deleting.
   - - **`common/`**: Shared templates such as base.html, which serves as the main layout for the entire project.
   - - **`forum/`**: Templates for forum section: home page for forum, thread and category creation and detail, edit and delete of thread.
   - - **`students/`**: Templates for student-specific functionality, such as: student form, view edit and details of student.
   - - **`universities/`**: Templates related to university information, including: university form, view and edit of university.
   - - **`404.html`**: Custom 404 error page displayed when a user accesses an invalid route.

- **`.gitignore`**: Specifies files and directories to exclude from version control.
- **`manage.py`**: Django's management script for running the server, migrations, and other commands.
- **`requirements.txt`**: Lists all required dependencies to run the project.



## 🛠️ **Technologies Used**
- **Backend**: Django 4.2
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Custom CSS
- **Environment Management**: `python-decouple` (for secure credentials)



## 🚀 Getting Started

To run the project locally on your machine, follow these steps:

1. **Clone the Repository**:
    Download the project code to your local machine using Git.


2. **Create and Activate a Virtual Environment**:
    Set up a virtual environment to isolate project dependencies:
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    
    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install Dependencies**:
    Install the required dependencies listed in the requirements.txt file:
    ```bash
    pip install -r requirements.txt

    ```

4. **Configure the Environment Variables**:
    Create a .env file in the root directory, and if you have the necessary credentials and configurations ready, add them securely to the file.


5. **Set Up the Database**:
    Apply database migrations to create the necessary tables:
    ```bash
    python manage.py makemigrations
    python manage.py migrate

    ```

6. **Create a Superuser**:
    To access the Django Admin panel, create a superuser account:
    ```bash
    python manage.py createsuperuser
    ```
   

7. **Run the Development Server**:
    Start the Django development server:
    ```bash
    python manage.py runserver
    ```
  After starting the server, open your web browser and go to:
  http://127.0.0.1:8000/  


## 🔒 Future Enhancements  

- Implement a **chat feature** for real-time messaging between students and users.  
- Add notifications for new messages or replies in the forum.  
- Integrate a university ranking system based on user ratings.  
- Enhance search functionality with advanced filters.  
