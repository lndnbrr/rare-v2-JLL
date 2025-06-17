from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Comment, Post, User
from rareapi.filters import CommentFilter
from django.utils.timezone import localtime


class CommentView(ViewSet):
    """Rare comments view"""

    def list(self, request):
        if "post" in request.GET:
            filterset = CommentFilter(
                data=request.GET, queryset=Comment.objects.all().order_by('-created_on'))
            comments = filterset.qs
            serializer = CommentPostSerializer(
                comments, many=True, context={'request': request})
        else:
            filterset = CommentFilter(
                data=request.GET, queryset=Comment.objects.all())
            comments = filterset.qs
            serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests for comments

        Returns JSON serialized comment instance
        """
        # Gets the UID from authorization header, sets author equal to the user object with a matching uid, if one exists
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        uid = None
        if auth_header.startswith('Bearer '):
            uid = auth_header.split(' ')[1]
        try:
            author = User.objects.get(uid=uid)
        except User.DoesNotExist:
            return Response({'error-details': 'Invalid uid or unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        post = Post.objects.get(pk=request.data["post"])

        comment = Comment.objects.create(
            content=request.data["content"],
            created_on=request.data["created_on"],
            author=author,
            post=post
        )

        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        """Handle PUT requests for a comment

        Returns: Response - empty body with 204 status code
        """
        comment = Comment.objects.get(pk=pk)
        comment.content = request.data["content"]
        comment.created_on = request.data["created_on"]

        author = User.objects.get(pk=request.data["author"])
        post = Post.objects.get(pk=request.data["post"])
        comment.author = author
        comment.post = post

        comment.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments"""

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'content', 'created_on')


class CommentPostSerializer(serializers.ModelSerializer):
    """JSON serializer for comments on a specific post"""
    author_full_name = serializers.SerializerMethodField()
    creation_date = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()

    def get_author_full_name(self, obj):
        """Combines the first and last name of a comment's author to get their full name

        Args:
            obj (Comment): A Comment instance being serialized

        Returns:
            (string): The full name of the author of the comment
        """
        return f"{obj.author.first_name} {obj.author.last_name}".strip()

    def get_creation_date(self, obj):
        """Displays the creation date by parsing the datetime object stored in the database

        Args:
            obj (Comment): A Comment instance being serialized

        Returns:
            (string): A properly formatted date and time to be displayed on the front end
        """
        return localtime(obj.created_on).strftime("%m/%d/%Y at %I:%M %p")

    def get_is_author(self, obj):
        """Checks if the uid of the user viewing the comment matches the uid of the author of the comment

        Args:
            obj (Comment): A Comment instance being serialized

        Returns:
            (bool): true or false depending on whether the logged in user authored the comment
        """
        request = self.context.get('request')
        uid = None
        # Send auth header in frontend request
        auth_header = request.META.get(
            'HTTP_AUTHORIZATION', '') if request else ''
        if auth_header.startswith('Bearer '):
            uid = auth_header.split(' ')[1]
        return str(obj.author.uid) == uid

    class Meta:
        model = Comment
        fields = ('id', 'author_full_name', 'content',
                  'creation_date', 'is_author')
