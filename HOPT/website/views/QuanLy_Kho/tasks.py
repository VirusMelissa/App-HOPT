from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from website.models import ChatMessage

@shared_task
def delete_old_chat_messages():
    cutoff_date = timezone.now() - timedelta(days=30)
    ChatMessage.objects.filter(timestamp__lt=cutoff_date).delete()
