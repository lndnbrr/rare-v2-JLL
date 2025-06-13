from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Comment, Post, User


class CommentView(ViewSet):
    """Rare comments view"""

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


class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments"""

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'content', 'created_on')
        depth = 1
