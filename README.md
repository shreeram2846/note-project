# Note Management API

This project is a simple API for managing notes. a secure and scalable RESTful API that allows users to create,
read, update, and delete notes. This application allow users to share their notes with
other users and search for notes based on keywords

# Steps to execute note_project on local environment
## Technologies Used

- **Django**: A high-level web framework.
- **Django REST framework**: A powerful and flexible toolkit for building Web APIs.
- **MySQL**: A robust and scalable relational database.
- **pytest**: A testing framework for Python
- **Postman**: A testing APIs(optional)
- **Virtual environment**: A virtual environment [Virtual environment](https://docs.python.org/3/tutorial/venv.html) (optional, but recommended)

### Prerequisites

- Python 3.x
- pip (Python package installer)
- MySQL database server

### Setting Up the Project

1. Clone the repository:

   ```bash
   git clone https://github.com/shreeram2846/note-project.git
   
2. Set up a virtual environment (optional but recommended):
   ```bash
   # for ubuntu
   python3 -m venv venv
   source venv/bin/activate
   
   # for window 
   
   pip install virtualenv
   virtualenv venv
   cd venv/Scripts
   activate
   ```
   
3. Navigate to the project directory:
   ```bash 
   cd note-project
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
5. Create a MySQL database:
   ```sql
   CREATE DATABASE database_name;
   USE database_name;
   e.g. CREATE DATABASE notes_db;
   USE notes_db;
6. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate

### Running the Application
   1. Start the development server:
   ```bash
   python manage.py runserver
   ```
   2. The API will be accessible at 
   http://localhost:8000
   3. API details 
   ```bash

      
    1. create a new user account   
      POST /api/api/auth/signup/ HTTP/1.1
      Host: localhost:8000
      Content-Type: application/json
      Content-Length: 57
      
      {
          "username":"ramesh3",
          "password":"ramesh3"
      }
      
    2. log in to an existing user account and receive an access token
      POST /api/api/auth/login/ HTTP/1.1
      Host: localhost:8000
      Content-Type: application/json
      Content-Length: 57
      
      {
          "username":"ramesh2",
          "password":"ramesh2"
      }
      
    3. get a list of all notes for the authenticated user
      GET /api/api/notes/ HTTP/1.1
      Host: localhost:8000
      Authorization: Token c1c53c5e938796eeb7b4ac89ae15f91782e56c81
      Content-Type: application/json
      Content-Length: 67
      {
          "title": "ramesh notes",
          "content": "this is sample"
      }
      
    4. create a new note for the authenticated user
      POST /api/api/notes/ HTTP/1.1
      Host: localhost:8000
      Authorization: Token c1c53c5e938796eeb7b4ac89ae15f91782e56c81
      Content-Type: application/json
      Content-Length: 79
      
      {
          "title": "This is my notes4",
          "content": "This is my contents4."
      }
         
    5. get a note by ID for the authenticated user
        GET /api/api/notes/2/ HTTP/1.1
        Host: localhost:8000
        Authorization: Token c1c53c5e938796eeb7b4ac89ae15f91782e56c81
        
    6.  update an existing note by ID for the authenticated user
        PUT /api/api/notes/2/ HTTP/1.1
        Host: localhost:8000
        Authorization: Token c1c53c5e938796eeb7b4ac89ae15f91782e56c81
        Content-Type: application/json
        Content-Length: 86
         
        {
             "title": "This is my notes2",
             "content": "This is my contents2 upated."
        }
        
    7.  delete a note by ID for the authenticated user
        DELETE /api/api/notes/1/ HTTP/1.1
        Host: localhost:8000
        Authorization: Token c1c53c5e938796eeb7b4ac89ae15f91782e56c81
       
    8. search for notes based on keywords for the authenticated user
        GET /api/api/search/?q=Note HTTP/1.1
        Host: localhost:8000
        Authorization: Token c1c53c5e938796eeb7b4ac89ae15f91782e56c81
       
       
    9. share a note with another user for the authenticated user
        PUT /api/api/notes/6/share/ HTTP/1.1
        Host: localhost:8000
        Authorization: Token c1c53c5e938796eeb7b4ac89ae15f91782e56c81
        Content-Type: application/json
        Content-Length: 44
      
        {
          "shared_with": [
              5
          ]
        }
        
    10. share a note with another user for the authenticated user      
        POST /api/api/notes/6/share/ HTTP/1.1
        Host: localhost:8000
        Authorization: Token 4ae05a3d0d9fdc1f4659c0f830ba3fb6cb043063
        Content-Type: application/json
        Content-Length: 44

        {
          "shared_with": [
           3
          ]
        }
```

### Running Tests
1. Navigate to the application directory:
   ```bash 
   cd notes
   e.g.\note-project\notes>
   
Run the test suite:
```bash
   pytest -v tests.py
   e.g.\note-project\notes>pytest -v tests.py
```
### Project Structure
   The main components of the project are organized as follows:

   - note_project/: Django project settings and configurations.
   - notes/: Django app containing models, views, and serializers for notes.
   - notes/tests.py: Unit tests for the application.