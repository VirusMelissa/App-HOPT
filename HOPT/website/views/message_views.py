from django.shortcuts import render, redirect
from django.http import JsonResponse
from website.models import Accounts, ChatMessage, MessageReadStatus
from django.views.decorators.csrf import csrf_exempt
import json

def get_chat_messages(request, department):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Unauthorized"}, status=401)

    messages = ChatMessage.objects.filter(department=department).order_by('timestamp')
    message_statuses = MessageReadStatus.objects.filter(user=request.user)

    read_status_dict = {status.message.id: status.is_read for status in message_statuses}

    return JsonResponse({
        "current_user_id": request.user.id,
        "messages": [
            {
                "user": msg.user.fullname or msg.user.username,
                "user_id": msg.user.id,
                "message": msg.message,
                "is_read": read_status_dict.get(msg.id, False)
            }
            for msg in messages
        ]
    })

@csrf_exempt
def send_message(request, department):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Unauthorized"}, status=401)

    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message")
        if message:
            chat_message = ChatMessage.objects.create(user=request.user, message=message, department=department)
            recipients = Accounts.objects.exclude(id=request.user.id)  # Hoặc danh sách người dùng cụ thể
            for recipient in recipients:
                MessageReadStatus.objects.create(message=chat_message, user=recipient)

            return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)

def get_unread_count(request, department):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Unauthorized"}, status=401)

    # Đếm số lượng tin nhắn chưa đọc của phòng ban tương ứng cho người dùng hiện tại
    unread_count = MessageReadStatus.objects.filter(
        is_read=False,
        user=request.user,
        message__department=department  # Lọc theo phòng ban
    ).count()
    return JsonResponse({"unread_count": unread_count})

@csrf_exempt
def mark_messages_as_read(request, department):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Unauthorized"}, status=401)

    # Đánh dấu tất cả tin nhắn chưa đọc của phòng ban tương ứng là đã đọc
    MessageReadStatus.objects.filter(
        is_read=False,
        user=request.user,
        message__department=department  # Lọc theo phòng ban
    ).update(is_read=True)
    return JsonResponse({"status": "success"})


