from django.db import models
from django.utils.translation import gettext_lazy as _

from django.db.models import Count, Sum, Avg

from account.models import User


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    auth = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def average_rating(self):
        average = Grade.objects.filter(post=self).aggregate(Avg('grade_number'))
        for i in average.values():
            return i


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    auth = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    text = models.CharField(max_length=255)
    user_name = models.CharField(verbose_name='Name', max_length=100, blank=True,
                                 help_text=_('Если вы незарегестнрированный пользователь укажите временный username'),)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Grade(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    auth = models.ForeignKey(User, on_delete=models.CASCADE)
    grade_number = models.IntegerField(choices=[
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ], null=True, blank=True)

    class Meta:
        unique_together = ('post', 'auth')

    def __str__(self):
        return self.grade_number
