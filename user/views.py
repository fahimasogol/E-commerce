from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from rest_framework.authtoken.models import Token


# Create your views here.
# class RegistrationApiView(generics.CreateAPIView):
#     serializer_class = RegisterSerializer
#
#     def perfom_create(self, serializer):
#         token, create = Token.objects.get_or_create(user=user)
#         response_data = {"token": token.key, "user": user.username}
#         return Response(response_data, status=status.HTTP_201_CREATED)
# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = RegisterSerializer
#
#     def perform_create(self, serializer):
#         # user = User.objects.create_user(**serializer.validated_data)
#         user = serializer.save()
#         token, create = Token.objects.get_or_create(user=user)
#         # response_data = {"token": token.key, "user": user.username}
#         # return Response(response_data, status=status.HTTP_201_CREATED)
#         serializer.instance.token = token.key
#
#     def create(self, request, *args, **kwargs):
#         response = super().create(request, *args, **kwargs)
#         # Correctly add the token to the response data
#         response.data['token'] = getattr(serializer.instance, 'token', None)
#         return response
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()  # Save the user using the serializer's create method
        token, created = Token.objects.get_or_create(user=user)
        response_data = {"token": token.key, "user": user.username}
        self.response_data = response_data  # Store response data to use in the response

    def create(self, request, *args, **kwargs):
        response = super(RegisterView, self).create(request, *args, **kwargs)
        response.data = self.response_data  # Add the token to the response
        return response


# The clever part of this approach is using the perform_create method to prepare additional data (token and username)
# and storing it in an instance variable (self.response_data). This data is then added to the response in the create
# method. This method ensures that the token, which is essential for immediate authentication, is included in the
# response to the client after a successful registration, following RESTful best practices for API design.


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not User.objects.filter(username=username).exists():
            return Response({'error': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key,
                             'user_id': user.pk,
                             'username': user.username})

        return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# from rest_framework.generics import RetrieveUpdateAPIView
# from rest_framework.permissions import IsAuthenticated
# from .models import UserProfile
# from .serializers import UserProfileSerializer
#
# class UserProfileView(RetrieveUpdateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = UserProfileSerializer
#
#     def get_object(self):
#         # Retrieve and return the UserProfile for the current user
#         return UserProfile.objects.get(user=self.request.user)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = ProfileSerializer(user_profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = ProfileSerializer(user_profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = ProfileSerializer(user_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

