from django.db import models
from django.utils import timezone

# Create your models here.


class Users(models.Model):

    name = models.CharField(max_length=50)
    consumer_key = models.CharField(max_length=200)
    consumer_secret_key = models.CharField(max_length=200)
    access_token = models.CharField(max_length=200)
    access_secret_token = models.CharField(max_length=200)
    # def __int__(self,_name='',_consumer_key='',_consumer_secret_key='',_access_token='',_access_secret_token=''):
    #     self.
    # def (self):
    #     return "Name : " + str(self.name) + ".\nDetails are -> Consumer Key - " + str(self.consumer_key) + \
    #                "\n\t\tConsumer Secret Key - " + str(self.consumer_secret_key) + "\n\t\t Access Token - " + \
    #                str(self.access_token) + "\n\t\t Access Secret Token - " + str(self.access_secret_token)


class Tweet(models.Model):
    tweet = models.TextField(max_length=200, default="tweet me !!")
    document = models.FileField(upload_to='documents/', null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    # schedule = models.DateTimeField(auto_now=True, blank=True)


class DmUserList(models.Model):
    user_id = models.BigIntegerField()
    user_name = models.CharField(max_length=20)


class Template(models.Model):

    temp_name = models.CharField(max_length=50, blank=True, null=True)
    text = models.TextField()

    def __str__(self):
        return self.temp_name


# class TemplateText(models.Model):
#     text = models.TextField()