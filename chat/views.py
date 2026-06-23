from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import ChatMessage
from .serializers import ChatMessageSerializer


class ChatViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]