from django.db import models
import uuid
import random


def generate_token():
    return ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=10))


class UserInfo(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    token = models.CharField(max_length=10, default=generate_token, editable=False)
    name = models.CharField(max_length=20)
    dob = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    cvd_test = models.CharField(max_length=10, null=True, blank=True)
    test_type = models.CharField(max_length=10)
    share_count = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.test_type}"


class IshiharaTest(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    responses = models.JSONField(default=list)
    score = models.IntegerField(null=True, blank=True)
    cvd_type = models.CharField(max_length=10, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.user.test_type}"


class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
