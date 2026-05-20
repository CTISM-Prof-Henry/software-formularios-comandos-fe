from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    return render(request, "dashboard.html")


def healthcheck(_request):
    return JsonResponse({"status": "ok"})
