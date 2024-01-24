from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Note
from .serializers import NoteSerializer, NoteShareSerializer

from rest_framework.throttling import UserRateThrottle


class SignupView(APIView):
    # Allow any user to access this view
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]  # Apply throttling here

    def post(self, request):
        # Retrieve username and password from request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if both username and password are provided
        if not username or not password:
            return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new user with the provided username and password
        user = User.objects.create_user(username=username, password=password)

        return Response({'user_id': user.pk, 'username': user.username}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    # Allow any user to access this view
    permission_classes = ()
    throttle_classes = [UserRateThrottle]  # Apply throttling here

    def post(self, request, *args, **kwargs):
        # Retrieve username and password from request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if both username and password are provided
        if not username or not password:
            return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate the user based on the provided username and password
        user = authenticate(username=username, password=password)

        # Check if the user is authenticated
        if user:
            # Generate or retrieve a token for the user
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.pk, 'username': user.username}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class NoteListCreateView(generics.ListCreateAPIView):
    # Specify the model and serializer for the view
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    # Allow only authenticated users to access this view
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]  # Apply throttling here

    def perform_create(self, serializer):
        # Set the owner field before saving a new note
        serializer.save(owner=self.request.user)


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Specify the model and serializer for the view
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    # Allow only authenticated users to access this view
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]  # Apply throttling here


class NoteShareView(generics.UpdateAPIView, generics.CreateAPIView):
    # Specify the model and serializer for the view
    queryset = Note.objects.all()
    serializer_class = NoteShareSerializer
    # Allow only authenticated users to access this view
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]  # Apply throttling here

    def perform_update(self, serializer):
        # Update the shared_with field of an existing note
        shared_with_users = self.request.data.get('shared_with', [])
        owner = self.request.user

        # Exclude the owner from the list if present
        shared_with_users = [user_id for user_id in shared_with_users if user_id != owner.pk]

        # Update the existing note's shared_with field
        serializer.save(shared_with=shared_with_users)

        data = {'shared_with': shared_with_users}
        return Response(data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        # Create a new note with shared users
        shared_with_users = self.request.data.get('shared_with', [])
        owner = self.request.user

        # Exclude the owner from the list if present
        shared_with_users = [user_id for user_id in shared_with_users if user_id != owner.pk]

        # Set the owner field before saving
        serializer.save(owner=owner, shared_with=shared_with_users)

        data = {'shared_with': shared_with_users}
        return Response(data, status=status.HTTP_201_CREATED)


class NoteSearchView(generics.ListAPIView):
    # Specify the serializer for the view
    serializer_class = NoteSerializer
    # Allow only authenticated users to access this view
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]  # Apply throttling here

    def get_queryset(self):
        # Retrieve the search query from the request parameters
        query = self.request.query_params.get('q', '')
        user = self.request.user

        # Search notes based on keywords in title or content
        queryset = Note.objects.filter(owner=user, title__icontains=query) | \
                   Note.objects.filter(owner=user, content__icontains=query)

        return queryset
