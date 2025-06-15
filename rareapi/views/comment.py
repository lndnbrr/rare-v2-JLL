from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Comment, Post, User
from rareapi.filters import CommentFilter


class CommentView(ViewSet):
    """Rare comments view"""

    def list(self, request):
        if "post" in request.GET:
            filterset = CommentFilter(
                data=request.GET, queryset=Comment.objects.all().order_by('-created_on'))
            comments = filterset.qs
            serializer = CommentPostSerializer(comments, many=True)
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
        author = User.objects.get(pk=request.data["author"])
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

    def get_author_full_name(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}".strip()

    def get_creation_date(self, obj):
        return obj.created_on.strftime("%m/%d/%Y at %I:%M %p")

    class Meta:
        model = Comment
        fields = ('id', 'author_full_name', 'content', 'creation_date')
