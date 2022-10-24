from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class Userinfo(models.Model):
    Account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True, editable=True, upload_to='images/')
    First_name = models.CharField(max_length=40, validators=[MaxLengthValidator(40, 'Слишком большое значение')])
    Last_name = models.CharField(max_length=40, validators=[MaxLengthValidator(40, 'Слишком большое значение')])
    About_me = models.TextField(blank=True, max_length=600)
    stat = models.ForeignKey('Status', blank=True, on_delete=models.CASCADE)
    lessons = models.ManyToManyField(settings.AUTH_USER_MODEL, through='LessonDate', related_name='Lessons')

    def __str__(self):
        return self.Last_name


class LessonDate(models.Model):
    instructor = models.ForeignKey('Userinfo', blank=False, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_lesson = models.DateTimeField()
    end_lesson = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=100, validators=[MaxLengthValidator(100, 'Слишком большое значение')], blank=True)
    accepted = models.BooleanField(default=False)


class Status(models.Model):
    status = models.CharField(max_length=30)

    def __str__(self):
        return self.status


