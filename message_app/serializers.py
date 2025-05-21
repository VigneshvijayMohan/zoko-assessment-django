from rest_framework import serializers
from .models import Message


class MessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        
    def validate(self, data):
        if data['sender_id'] == data['receiver_id']:
            raise serializers.ValidationError("Sender and receiver must be different users.")
        return data