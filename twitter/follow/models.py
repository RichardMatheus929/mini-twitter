from django.db import models

from twitter.accounts.models import User

# Create your models here.
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    start_follow = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.follower} follows {self.following}"