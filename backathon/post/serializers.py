from .models import *
from rest_framework.serializers import ModelSerializer
from user.serializers import *
class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"

class FetchPostSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Post
        fields = "__all__"

class FetchCommentSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comments
        fields = "__all__"
