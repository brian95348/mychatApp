from chat.models import Profile, Message
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileSerializer, MessageSerializer
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ValidationError
from django.shortcuts import redirect
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework import permissions

User = get_user_model()

class IsProfileOwnerOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class ProfileList(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get(self,request):
        profile_obj = Profile.objects.filter(user=self.request.user)
        if not profile_obj.exists():
            return redirect('api-profile-create')
        else:
            return self.list(request)
    
    def get_queryset(self):
        return Profile.objects.exclude(user=self.request.user)

class ProfileCreate(generics.CreateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
              
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
        return Response(status=status.HTTP_201_CREATED)

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated,IsProfileOwnerOrReadOnly]
    queryset = Profile.objects.all()
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    

class ChatMessages(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
        
    def get_queryset(self):
        user2 = get_object_or_404(User,username=self.kwargs['username'])
        lookups = Q(user=self.request.user,receiver=self.kwargs['username']) | Q(receiver=self.request.user.username,user=user2) 
        return Message.objects.filter(lookups)

    def perform_create(self,serializer):
        serializer.save(user=self.request.user,receiver=self.kwargs['username'])

class ChatMessageDetail(generics.RetrieveDestroyAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

@method_decorator(csrf_exempt, name='dispatch')            
class UserSignUp(APIView):
    permission_classes = []
    parser_classes = [JSONParser]

    def post(self,request):
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        User.objects.create_user(username,email,password)
        return Response(status=status.HTTP_201_CREATED)


