from django.urls import path
from .views import MessagesView, MarkMessageAsReadView

urlpatterns = [
    path("messages/", MessagesView.as_view(), name="new" ),
    path("messages/<str:message_id>/read", MarkMessageAsReadView.as_view(), name="all_read_messages"),
]
