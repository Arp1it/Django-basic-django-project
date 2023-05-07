from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Chatting(models.Model):
    cuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chatuser")
    cusrep = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    chattts = models.CharField(max_length=1000000)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.cuser.username