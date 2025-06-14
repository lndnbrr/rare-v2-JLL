from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Post, User, Category

class PostView(ViewSet):
 
  def retrieve(self, request, pk):
    """ Handle GET requests for single post"""
    try:
      post = Post.objects.get(pk=pk)
      serializer = PostSerializer(post)
      return Response(serializer.data)
    except Post.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
   
  def list(self, request):
    """ Handle GET requests to get all tags"""
    posts = Post.objects.all()
   
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
 
  def create(self, request):
    """ Handle POST operations for Post instance"""

    userId = User.objects.get(uid=request.data["user"])
    category = Category.objects.get(pk=request.data["categoryid"])
    post = Post.objects.create(
      user=userId,
      category=category,
      title=request.data["title"],
      publication_date=request.data["publication_date"],
      image_url=request.data["image_url"],
      content=request.data["content"],
      approved=request.data["approved"],
    )
    serializer = PostSerializer(post)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostSerializer(serializers.ModelSerializer):
   """ JSON serializer for posts """
   class Meta:
      model = Post
      fields = ('id', 'category', 'user', 'title', 'publication_date', 'image_url', 'content', 'approved')
      depth = 1
 