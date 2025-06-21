from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from django.db import IntegrityError
from rareapi.models import User

class UserViews (ViewSet):
    ''' user viewset for rare server'''


    def list (self, request):
        '''
        This is a method that will display a list of all user profiles
        
        Args: 
          
          request = The incoming info about what a user is asking for
          and where that info is coming from.
          
        Returns:
          A serialized array of objects of all users. 
          
        '''

        user = User.objects.all()
        serialized = UserSerializer(user, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve (self, request, pk):
        '''
        This is a method that will retrieve a single user's profile
        
        Args: 
          
          request = The incoming info about what a user is asking for
          and where that info is coming from.
          
          pk = The primary key of the data that a user is hoping to identify 
          and grab additional detail about.
          
        Returns:
          A serialized object of a user's details. 
          
        '''
        
        # Utilizing try/except for better error handling.
        try:
            user = User.objects.get(pk=pk)
            serialized = UserSerializer(user)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

    def create (self, request):
        '''
          This is a method that will create a profile for a user
          
          Args: 
            
            request = The incoming info about what a user is asking for
            and where that info is coming from.
            
          Returns:
            A serialized object of a new user's details.
          
        '''
        
        try:
            user = User.objects.create(
              first_name = request.data["first_name"],
              last_name = request.data["last_name"],
              bio = request.data["bio"],
              profile_image_url = request.data["profile_image_url"],
              email = request.data["email"],
              active = request.data["active"],
              is_staff = request.data["is_staff"],
              uid = request.data["uid"]
            )
            serialized = UserSerializer(user)
            return Response(serialized.data, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response({"message": "Uid is already in use. Try another one."},
                            status=status.HTTP_409_CONFLICT)

    def update (self, request, pk):
        '''
          This is a method that will update a user's profile
          
          Args: 
            
            request = The incoming info about what a user is asking for
            and where that info is coming from.
            
            pk = The primary key of the data that a user is hoping to identify 
            and grab additional detail about.
            
          Returns:
            A serialized object of a user's updated details.
          
        '''
        
        try:
            user = User.objects.get(pk = pk)
            user.first_name = request.data["firstName"]
            user.last_name = request.data["lastName"]
            user.bio = request.data["bio"]
            user.profile_image_url = request.data["PFP"]
            user.email = request.data["email"]
            user.active = request.data["active"]
            user.is_staff = request.data["isStaff"]
            user.save()
            serialized = UserSerializer(user)
            return Response(serialized.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

    def destroy (self, request, pk):
        '''
          This is a method that will delete a user profile
          
          Args: 
            
            request = The incoming info about what a user is asking for
            and where that info is coming from.

            pk = The primary key of the data that a user is hoping to identify 
            and grab additional detail about.

        '''

        try:
            user = User.objects.get(pk = pk)
            user.delete()

            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except User.DoesNotExist:
            return Response({"message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

class UserSerializer (serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'bio',
                  'profile_image_url', 'email', 'created','active', 'is_staff', 'uid')
