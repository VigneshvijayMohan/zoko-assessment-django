from django.db import models
import uuid

# Create your models here.

def generate_message_id():
    return f"msg-{uuid.uuid4().hex[:8]}"


class Message(models.Model):
    message_id = models.CharField(max_length= 100, unique=True, default=generate_message_id)
    sender_id = models.CharField(max_length= 100)
    receiver_id = models.CharField(max_length= 100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
