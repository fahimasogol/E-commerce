from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
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

    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not User.objects.filter(username=username).exists():
            return Response({'error': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key,
                             'user_id': user.pk,
                             'username':user.username})

        return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
