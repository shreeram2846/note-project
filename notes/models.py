from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    # Title of the note, limited to 255 characters
    title = models.CharField(max_length=255)

    # Content of the note, a longer text field
    content = models.TextField()

    # Owner of the note, linked to the User model and deleted if the owner is deleted
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # Users with whom the note is shared, many-to-many relationship with User model
    shared_with = models.ManyToManyField(User, related_name='shared_notes', blank=True)

    # Date and time when the note was created, set automatically on creation
    created_at = models.DateTimeField(auto_now_add=True)

    # Date and time when the note was last updated, set automatically on each update
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # String representation of the note, displayed as its title
        return self.title
