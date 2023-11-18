from django.db import models


class Member(models.Model):
  name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
