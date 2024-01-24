from django.urls import path
from .views import (
    NoteListCreateView,   # View for listing and creating notes
    NoteDetailView,       # View for retrieving, updating, and deleting a specific note
    NoteShareView,        # View for sharing a note with other users
    SignupView,           # View for user registration/signup
    LoginView,            # View for user login/authentication
    NoteSearchView        # View for searching notes based on keywords
)

# Define URL patterns for the API endpoints
urlpatterns = [
    # Endpoint for user registration/signup
    path('api/auth/signup/', SignupView.as_view(), name='signup'),

    # Endpoint for user login/authentication
    path('api/auth/login/', LoginView.as_view(), name='login'),

    # Endpoint for listing all notes and creating a new note
    path('api/notes/', NoteListCreateView.as_view(), name='note-list-create'),

    # Endpoint for retrieving, updating, and deleting a specific note
    path('api/notes/<int:pk>/', NoteDetailView.as_view(), name='note-detail'),

    # Endpoint for sharing a note with other users
    path('api/notes/<int:pk>/share/', NoteShareView.as_view(), name='note-share'),

    # Endpoint for searching notes based on keywords
    path('api/search/', NoteSearchView.as_view(), name='note-search'),
]