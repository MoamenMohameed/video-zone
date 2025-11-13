from django.shortcuts import render
from .models import Video , Like
from .serializers import VideoSerializer , RegisterSerializers
from rest_framework import mixins,viewsets , status
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated




class AuthViewSet(viewsets.ViewSet):
    
    permission_classes = []

    @action(detail=False, methods=['post'])
    def register(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if User.objects.filter(username=username).exists():
            return Response({"message": "User exists"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        return Response({"message": "User registered"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"message": "Login successful", "token": token.key}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
        except Token.DoesNotExist:
            pass
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def renew_token(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
        except Token.DoesNotExist:
            pass
        new_token = Token.objects.create(user=request.user)
        return Response({"message": "Token renewed", "token": new_token.key}, status=status.HTTP_200_OK)




    
class Videos(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self,request):
        serializer = VideoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner = request.user)
        
        return Response ({
            "message" : 'User has created successful',
            "user" : serializer.data,
            
        }, status=status.HTTP_201_CREATED)
    
    def list(self,request):
        queryset = Video.objects.filter(owner=request.user)
        serializer = VideoSerializer(queryset,many=True, context={'request': request})
        return Response ({
            "message" : 'this is videos',
            "data" : serializer.data,
        }, status=status.HTTP_200_OK)
    
    
    def retrieve(self,request,pk=None):
        try:
            queryset = Video.objects.get(pk=pk , owner=request.user)
        except Video.DoesNotExist:
            return Response("video not found", status=status.HTTP_404_NOT_FOUND)
            
        serializer = VideoSerializer(queryset, context={'request': request})
        return Response ({
            "message" : 'this is videos',
            "data" : serializer.data,
        }, status=status.HTTP_200_OK)
    
    def update(self,request, pk=None):
        queryset = Video.objects.get(pk=pk , owner = request.user)
        serializer = VideoSerializer(queryset ,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner = request.user)
        
        return Response ({
            "message" : 'User has updated successful',
            "data" : serializer.data,
            
        }, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self,request,pk=None):
        try:
            queryset = Video.objects.get(pk=pk , owner=request.user)
        except Video.DoesNotExist:
            return Response("video not found")
            
        queryset.delete()
        return Response ({
            "message" : 'video has been deleted',
        }, status=status.HTTP_204_NO_CONTENT)
    
    
    @action(detail=True, methods=(['post']))
    def likes(self,request, pk=None):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response("video not found", status=status.HTTP_404_NOT_FOUND)

        user = request.user
        like , created =  Like.objects.get_or_create(video=video , user=user)
        if not created :
            like.delete()
            video.likes = Like.objects.filter(video=video).count()
            video.save()
        else :
            video.likes = Like.objects.filter(video=video).count()
            video.save()

    @action(detail=True, methods=['post'])
    def View(self, request, pk=None):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response({"message": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
        
        session_key = f"watching_video_{video.id}"
        if not request.session.get(session_key):
            video.views += 1
            video.save()
            request.session[session_key] = True

        return Response({
            "message": "Video played",
            "views": video.views
        }, status=status.HTTP_200_OK)



