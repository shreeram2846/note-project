import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "note_project.settings")

import django
django.setup()

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import pytest
from django.contrib.auth.models import User
from .models import Note


@pytest.mark.django_db
def test_signup_view():
    # Test user signup view

    client = APIClient()
    url = reverse('signup')
    data = {'username': 'ramesh2', 'password': 'ramesh2'}

    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'user_id' in response.data
    assert 'username' in response.data


@pytest.fixture
def test_user():
    # Fixture to create a test user
    return User.objects.create_user(username='ramesh2', password='ramesh2')


@pytest.fixture
def authenticated_user(test_user):
    # Fixture to authenticate a test user

    client = APIClient()
    client.force_authenticate(user=test_user)
    return test_user


@pytest.mark.django_db
def test_login_view(test_user):
    # Test user login view

    client = APIClient()
    url = reverse('login')
    data = {'username': 'ramesh2', 'password': 'ramesh2'}

    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.data
    assert 'user_id' in response.data
    assert 'username' in response.data


@pytest.mark.django_db
def test_note_list_create_view(authenticated_user):
    # Test creating a note with an authenticated user

    url = reverse('note-list-create')
    data = {'title': 'Test Note', 'content': 'Test Content'}

    client = APIClient()
    client.force_authenticate(user=authenticated_user)

    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in response.data
    assert 'title' in response.data
    assert 'content' in response.data


@pytest.mark.django_db
def test_note_detail_view(authenticated_user):
    # Test retrieving a note detail with an authenticated user

    # Create a Note instance for testing
    note = Note.objects.create(title='Test Note', content='Test Content', owner=authenticated_user)

    url = reverse('note-detail', args=[note.id])

    client = APIClient()
    client.force_authenticate(user=authenticated_user)

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'id' in response.data
    assert 'title' in response.data
    assert 'content' in response.data
    assert response.data['id'] == note.id
    assert response.data['title'] == note.title
    assert response.data['content'] == note.content


@pytest.mark.django_db
def test_note_update_view(authenticated_user):
    # Test updating a note with an authenticated user

    # Create a Note instance for testing
    note = Note.objects.create(title='Test Note', content='Test Content', owner=authenticated_user)

    url = reverse('note-detail', args=[note.id])

    client = APIClient()
    client.force_authenticate(user=authenticated_user)

    # Test perform_update method
    data_update = {'title': 'Updated Title', 'content': 'Updated Content'}
    response_update = client.patch(url, data_update, format='json')

    assert response_update.status_code == status.HTTP_200_OK
    assert 'id' in response_update.data
    assert 'title' in response_update.data
    assert 'content' in response_update.data
    assert response_update.data['id'] == note.id
    assert response_update.data['title'] == data_update['title']
    assert response_update.data['content'] == data_update['content']


@pytest.mark.django_db
def test_note_delete_view(authenticated_user):
    # Test deleting a note with an authenticated user

    # Create a Note instance for testing
    note = Note.objects.create(title='Test Note', content='Test Content', owner=authenticated_user)

    url = reverse('note-detail', args=[note.id])

    client = APIClient()
    client.force_authenticate(user=authenticated_user)

    # Test perform_destroy method
    response_delete = client.delete(url)

    assert response_delete.status_code == status.HTTP_204_NO_CONTENT

    # Verify that the note has been deleted
    with pytest.raises(Note.DoesNotExist):
        Note.objects.get(pk=note.id)


@pytest.mark.django_db
def test_note_share_view(authenticated_user):
    # Test sharing a note with other users

    # Create a Note instance for testing
    note = Note.objects.create(title='Test Note', content='Test Content', owner=authenticated_user)

    # Create users with primary keys 2 and 3
    user2 = User.objects.create_user(username='user2', password='password2')
    user3 = User.objects.create_user(username='user3', password='password3')

    url = reverse('note-share', args=[note.id])

    client = APIClient()
    client.force_authenticate(user=authenticated_user)

    # Test perform_update method
    data_update = {'shared_with': [user2.pk, user3.pk]}
    response_update = client.patch(url, data_update, format='json')

    assert response_update.status_code == status.HTTP_200_OK
    assert 'shared_with' in response_update.data
    assert response_update.data['shared_with'] == data_update['shared_with']


@pytest.mark.django_db
def test_note_search_view(authenticated_user):
    # Test searching for notes with an authenticated user

    # Create some notes for testing
    Note.objects.create(title='Test Note 1', content='Test Content 1', owner=authenticated_user)
    Note.objects.create(title='Test Note 2', content='Test Content 2', owner=authenticated_user)
    Note.objects.create(title='Another Note', content='More Content', owner=authenticated_user)

    url = reverse('note-search')
    client = APIClient()
    client.force_authenticate(user=authenticated_user)

    # Test with a search query that matches notes 1 and 2
    response = client.get(url, {'q': 'Test'})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    # Verify that the expected notes are in the response
    expected_titles = {'Test Note 1', 'Test Note 2'}
    response_titles = {note['title'] for note in response.data}
    assert response_titles == expected_titles

    # Test with a search query that matches note 3
    response = client.get(url, {'q': 'Another'})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1

    # Verify that the expected note is in the response
    assert response.data[0]['title'] == 'Another Note'
    assert response.data[0]['content'] == 'More Content'
