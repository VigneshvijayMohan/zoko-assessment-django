from django.shortcuts import render
from .models import Message
from .serializers import MessageSerializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
# Create your views here.

class MessagesView(APIView):
    def get(self, request):
        user1 = request.GET.get("user1")
        user2 = request.GET.get("user2")
        
        if not user1 or not user2:
            return Response({"error": "Missing user1 or user2 in query params"}, status=400)

        messages = Message.objects.filter(sender_id = user1, receiver_id = user2).order_by("timestamp") 
        serialized_data = MessageSerializers(messages, many = True)
        return Response(serialized_data.data)
    def post(self, request):
        data = request.data

        sender_id = data.get("sender_id")
        receiver_id = data.get("receiver_id")
        content = data.get("content")

        if not sender_id or not receiver_id or not content:
            return Response({"error": "sender_id, receiver_id, and content are required."}, status=400)

        message = Message.objects.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content
        )

        serialized = MessageSerializers(message)
        return Response(serialized.data, status=201)



# @api_view(["PATCH"])
# def status_change_messages(request, message_id):
#     data = request.data
    
#     if not data:
#         return Response({"error": "Missing Data"}, status=400)

#     message = Message.objects.get(message_id = message_id)
#     print(message)
#     if data.get("status") == "read":
#         message.read = True
#         message.save()
#         serialized = MessageSerializers(message)
#         return Response(serialized.data, status=200)
#     else:
#         return Response({"error": "Invalid data"}, status=400)

@api_view(["GET"])
def get_all_messages(request):
    user1 = request.GET.get("user1")
    user2 = request.GET.get("user2")
    
    if not user1 or not user2:
        return Response({"error": "Missing user1 or user2 in query params"}, status=400)

    messages = Message.objects.filter(sender_id = user1, receiver_id = user2).order_by("timestamp") 
    serialized_data = MessageSerializers(messages, many = True)
    return Response(serialized_data.data)
