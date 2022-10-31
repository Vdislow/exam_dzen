from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


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

    def validate(self, data):
        user = self.context['request'].user.is_authenticated
        if not user:
            if not data['user_name']:
                raise ValidationError("нет юзернейма")
            return data
        if user:
            return data



class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = "__all__"
        read_only_fields = ('post', 'auth')