from rest_framework import serializers
from .models import Post, Comment, PostLikes


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "published_date", "like_count"]

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["author"] = user
        return super().create(validated_data)

    def get_like_count(self, obj):
        return obj.post_likes.count()


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "author", "text", "post"]

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["author"] = user
        return super().create(validated_data)


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLikes
        fields = "__all__"
