from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    completed = ArrayField(
       models.IntegerField() , default=list, blank=True
   )

    def __str__(self):
        return str(self.user)

class Content(models.Model):
    text = models.TextField()
    code = models.TextField()
    output = models.TextField()
    ranges = ArrayField(
       models.TextField() , default=list, blank=True
   )

    def __str__(self):
        return (self.text,self.code,self.output)

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=255)
    content = models.ManyToManyField(Content)

    def __str__(self):
        return (self.name)







