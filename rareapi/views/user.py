from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from rareapi.models import User

class UserViews (ViewSet):

    def retrieve (self, request, pk):
        '''
        This is a method that will retrieve a single user profile
        
        Args: 
          
          request = The incoming info about what a user is asking for
          and where that info is coming from.
          
          pk = The primary key of the data that a user is hoping to identify 
          and grab additional detail about.
          
        Returns:
          An serialized object of a user's details. 
          
        '''
        user = User.objects.get(pk=pk)
        serialized = UserSerializer(user)
        return Response(serialized.data, status=status.HTTP_200_OK)

class UserSerializer (serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'bio',
                  'profile_image_url', 'email', 'active', 'is_staff', 'uid')
