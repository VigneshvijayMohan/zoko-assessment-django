from django.urls import path
from .views import get_all_messages, MessagesView


urlpatterns = [
    path("messages/", get_all_messages, name="all_messages"),
    # path("messages/", post_messages, name="send_messages"),
    path("something/", MessagesView.as_view(), name="new" ),
    # path("messages/<str:message_id>/read", status_change_messages, name="status_change_messages" )
]
