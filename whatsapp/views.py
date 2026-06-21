from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from requests import request
from .utils import send_whatsapp_message
import json
from .handlers import handle_message
@method_decorator(csrf_exempt, name="dispatch")
class WhatsAppWebhook(View):

    def get(self, request):
        print("GET HIT")
        verify_token = "yessare123"

        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == verify_token:
            return JsonResponse(int(challenge), safe=False)

        return JsonResponse({"error": "verification failed"}, status=403)

    def post(self, request):
        data = json.loads(request.body)

        try:
            value = data["entry"][0]["changes"][0]["value"]

            # Ignore status updates
            if "messages" not in value:
                return JsonResponse({"status": "ignored"})

            msg = value["messages"][0]

            phone = msg["from"]

            if msg["type"] == "text":
                message = msg["text"]["body"]

            elif msg["type"] == "interactive":
                message = msg["interactive"]["button_reply"]["id"]

            else:
                return JsonResponse({"status": "unsupported"})

            handled = handle_message(phone, message)

            if not handled:
                send_whatsapp_message(
                    phone,
                    "Unknown command"
                )
        
        except Exception as e:
            print("ERROR:", e)
        
        return JsonResponse({"status": "ok"})
        