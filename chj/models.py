from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Chatting(models.Model):
    cuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chatuser")
    cusrep = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    chattts = models.CharField(max_length=1000000)
    useridhtml = models.CharField(max_length=1000000, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.cuser.username

        

from django.contrib.auth import get_user_model

def get_user_from_string(user_string):
    User = get_user_model()
    
    try:
        user = User.objects.get(username=user_string)  # Assuming the string is the username
    except User.DoesNotExist:
        # Handle the case where the user doesn't exist
        user = None
    
    return user
