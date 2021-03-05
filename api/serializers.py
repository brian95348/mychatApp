from rest_framework import serializers
from chat.models import Profile, Message

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    class Meta:
        model = Profile
        fields = ['username','profile_picture','status','created']

class MessageSerializer(serializers.ModelSerializer):
    receiver = serializers.ReadOnlyField()
    
    class Meta:
        model = Message
        fields = ['id','text','receiver','created']