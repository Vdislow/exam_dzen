from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework import status
import telebot
from drf_yasg.utils import swagger_auto_schema

from .models import Post, Comment, Grade
from .serializers import PostSerializer, CommentSerializer, GradeSerializer
from account.models import User
from .permissions import PostPermission, CommentRUDPermission, GradePermission

bot = telebot.TeleBot("5717582821:AAF_FuaoW3JOi2uKRhskwTgQUl2PJPMcsXM", parse_mode=None)


class PostListCreate(ListCreateAPIView):
    """
        Post API endpoint to get list and create posts
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (PostPermission, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    @swagger_auto_schema(responses={200: PostSerializer(many=True)}, operation_description="Get list of posts")
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(auth=self.request.user)
            for i in User.objects.filter(username=self.request.user):
                bot.send_message(i.telegram_chat_id, 'Блог создан')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRUD(RetrieveUpdateDestroyAPIView):
    """
        Comment API endpoint to retrieve, update and delete comments
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (PostPermission,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)


class CommentListCreate(ListCreateAPIView):
    """
        Post API endpoint to get list and create comments
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = (CommentRUDPermission,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        try:
            serializer.save(
                auth=self.request.user,
                post=get_object_or_404(Post, id=self.kwargs['post_id'])
            )
        except ValueError:
            serializer.save(
                post=get_object_or_404(Post, id=self.kwargs['post_id'])
            )

    def get_queryset(self):
        return self.queryset.filter(post_id=self.kwargs['post_id'])


class CommentRUD(RetrieveUpdateDestroyAPIView):
    """
        Comment API endpoint to retrieve, update and delete comments
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (CommentRUDPermission,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)


class GradePost(ListCreateAPIView):
    """
        Grade API endpoint to get list and create grade for posts
    """
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = (GradePermission,)

    def perform_create(self, serializer):
        try:
            serializer.save(
                auth=self.request.user,
                post=get_object_or_404(Post, id=self.kwargs['post_id'])
            )
        except IntegrityError:
            post_upd = Grade.objects.filter(auth=self.request.user)
            post_upd.delete()
        return serializer.save(
                auth=self.request.user,
                post=get_object_or_404(Post, id=self.kwargs['post_id'])
            )

