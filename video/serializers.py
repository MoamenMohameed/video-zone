from rest_framework import serializers
from .models import Video
from django.contrib.auth.models import User
class VideoSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    class Meta:
        model = Video
        fields = ['id','title', 'description','video_file','owner', 'uploaded_at']
        


class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only= True , required=True , style = {'input_type':'password'})
    password2 = serializers.CharField(write_only= True , required=True , style = {'input_type':'password'})

    class Meta :
        model = User
        fields = ['username', 'email', 'password' , 'password2']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError ({"password": 'password not match ,Try Again'})
        return data
    
    def create(self, validated_data):
        user = User(username= validated_data['username'] 
                    ,email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user