from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework import views
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import StoreUser, HintQuestion
from .serializers import RegistrationSerializer, LoginSerializer, ForgotPasswordSerializer, HintSerializer
from .helpers import JWTAuthenticationGenerator, update_session_in_response


# Create your views here.

@api_view(['GET'])
def get_username(request, username):
    if StoreUser.objects.filter(username=username).exists():
        return Response(status=status.HTTP_226_IM_USED)
    else:
        return Response(status=status.HTTP_200_OK)


class UserRegistrationView(views.APIView):

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        readable_password = serializer.validated_data.get('readable_password')
        storeUser = serializer.save()

        data = {
            'msg': 'Thank you for registering.',
            'status': 'success',
            'token': JWTAuthenticationGenerator.encode(storeUser.id)
        }

        return update_session_in_response(
            request,
            Response(status=status.HTTP_200_OK, data=data),
            storeUser
        )


class UserLogin(views.APIView):

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            storeUser = StoreUser.objects.get(username=username)
            if check_password(password, storeUser.password):
                data = {
                    'msg': 'Welcome! you have successfully logged in.',
                    'status': 'success',
                    'token': JWTAuthenticationGenerator.encode(storeUser.id)
                }
                return update_session_in_response(request, Response(data), storeUser)
            else:
                return Response(data={"non_field errors": ["Invalid Username/Password"]},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(views.APIView):

    def post(self, request, *args, **kwargs):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            storeUser = StoreUser.objects.get(username=serializer.validated_data.get('username'))
            storeUser.password = serializer.validated_data.get('password')
            storeUser.save()
            return Response(data={"msg": 'Password changed successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HintQuestionsView(ListAPIView):
    model = HintQuestion
    serializer_class = HintSerializer
    queryset = HintQuestion.objects.all()



