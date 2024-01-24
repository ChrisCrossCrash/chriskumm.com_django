from django.shortcuts import render


def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})


def echo_room(request):
    return render(request, "chat/echo.html")


def ai_chat(request):
    return render(request, "chat/ai_chat.html")