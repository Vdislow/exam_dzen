from rest_framework import serializers

from .models import Post, Comment, Grade


class PostSerializer(serializers.ModelSerializer):
    average_rating = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ('auth', )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ('post', 'auth')


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = "__all__"
        read_only_fields = ('post', 'auth')