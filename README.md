# Note Management API

This project is a simple API for managing notes. a secure and scalable RESTful API that allows users to create,
read, update, and delete notes. This application allow users to share their notes with
other users and search for notes based on keywords

## Technologies Used

- **Django**: A high-level web framework.
- **Django REST framework**: A powerful and flexible toolkit for building Web APIs.
- **MySQL**: A robust and scalable relational database.
- **pytest**: A testing framework for Python

### Prerequisites

- Python 3.x
- pip (Python package installer)
- MySQL database server

### Setting Up the Project

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/note-project.git
2. Navigate to the project directory:
   ```bash 
   cd note-management-api
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   
4. Apply database migrations:
   ```bash
   python manage.py migrate

### Running the Application
   1. Start the development server:
   ```bash
   python manage.py runserver
   ```
   2. The API will be accessible at 
   http://localhost:8000/api/

### Running Tests
Run the test suite:
```bash
   pytest -v tests.py
```
### Project Structure
   The main components of the project are organized as follows:

   - note_project/: Django project settings and configurations.
   - notes/: Django app containing models, views, and serializers for notes.
   - notes/tests.py: Unit tests for the application.