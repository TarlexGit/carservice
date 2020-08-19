from django.contrib.auth.models import User, Group
from django.shortcuts import redirect, get_object_or_404
from rest_framework import viewsets, generics
from rest_framework import permissions
from .serializers import (
    UserSerializer, 
    GroupSerializer, 
    CreateUserSerializer, 
    CreateUserProfileSerializer,
    MyTokenObtainPairSerializer,
    ProfileUpdate
)
from .models import Profile
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated 
from rest_framework.views import APIView
 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny
from .services import chek_and_return


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
     
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    parser_classes = (MultiPartParser,FormParser,JSONParser,) 
    permission_classes = (AllowAny,)

class LoginViev(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    parser_classes = (MultiPartParser,FormParser,JSONParser,) 


class UserCreateProfileView(APIView): 
    parser_classes = (MultiPartParser,FormParser,JSONParser,) 
    def post(self, request): 
        data = chek_and_return(request)
        serializer  = CreateUserProfileSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(status = 201)
        else: return Response(status=400)    
 
 
class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    parser_classes = (MultiPartParser,FormParser,JSONParser,) 

    queryset = Profile.objects.all()
    serializer_class = ProfileUpdate