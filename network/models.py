from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # M2M Relationshps
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following")


class Post(models.Model):

    # Required fields, Manually assigned
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(max_length=1000)

    # Required Fields, Automatically Assigned
    creation_date = models.DateTimeField(auto_now_add=True)
    

    # M2M Relationships
    liked_by = models.ManyToManyField(User, related_name = "liked_posts")

    def __str__(self):
        return f"Post No.{self.pk} by {self.owner}"
