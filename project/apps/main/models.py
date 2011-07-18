from django.db import models

class Person(models.Model):
  name = models.CharField(max_length=64,db_index=True)
  age = models.IntegerField(max_length=512)
  gender = models.CharField(max_length=6, null=True, default=None)

