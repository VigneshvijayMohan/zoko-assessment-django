from .models import Message
from .serializers import MessageSerializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .kafka_producer import produce_message
from .kafka_worker import consume_messages
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

        output_topic = "messages001"
        group_id = "messages001"
        produce_message(output_topic, data )
        message = consume_messages(output_topic, group_id)
        return Response(message.data, status=201)

class MarkMessageAsReadView(APIView):
    def patch(self, request, message_id):
        try:
            message = Message.objects.get(message_id=message_id)
        except Message.DoesNotExist:
            return Response({"error": "Message not found."}, status=status.HTTP_404_NOT_FOUND)
        
        message.read = True
        message.save()
        
        serializer = MessageSerializers(message)
        return Response(serializer.data, status=status.HTTP_200_OK)
