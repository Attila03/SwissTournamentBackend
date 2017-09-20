from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import generics
from rest_framework import authentication, permissions

from .serializers import UserRegistrationSerializer, UserDetailSerializer, TokenSerializer


class UserRegistraionView(generics.ListCreateAPIView):

    authentication_classes = ()
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


@method_decorator(csrf_exempt, name='dispatch')
class RegistrationView(View):

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try_user = User.objects.filter(username=username)
        if try_user:
            return JsonResponse({
                "error": "Username '{}' is already taken.".format(username)
            })
        else:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            new_user.save()
            return new_user


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):

    def post(self, request, *args, **kwargs):
        # import pdb
        # pdb.set_trace()
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username)
        if not user:
            return JsonResponse({
                "error": "Username '{}' is invalid.".format(username)
            })
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                return JsonResponse({
                    "error": "Invalid password for username '{}'".format(username)
                })
            else:
                token = TokenSerializer(user.auth_token)
                return JsonResponse({
                    "id": user.id,
                    "username": user.username,
                    "auth_token": token.data
                })


