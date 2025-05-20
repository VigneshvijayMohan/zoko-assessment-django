from django.shortcuts import render
from .models import Message
from .serializers import MessageSerializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.



@api_view(["GET"])
def get_all_messages(request):
    user1 = request.GET.get("user1")
    user2 = request.GET.get("user2")
    
    if not user1 or not user2:
        return Response({"error": "Missing user1 or user2 in query params"}, status=400)

    messages = Message.objects.filter(sender_id = user1, receiver_id = user2).order_by("timestamp") 
    serialized_data = MessageSerializers(messages, many = True)
    return Response(serialized_data.data)
