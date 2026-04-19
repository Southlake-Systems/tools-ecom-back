import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

def product_capture_view(request):
    return render(request, "product_capture.html")

@csrf_exempt
def save_images(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")

        base_path = f"/home/das/Documents/yessare/{product_id}"
        os.makedirs(base_path, exist_ok=True)

        for i in range(1, 6):
            file = request.FILES.get(f'image_{i}')
            if file:
                with open(os.path.join(base_path, f"{i}.jpg"), 'wb+') as f:
                    for chunk in file.chunks():
                        f.write(chunk)

        return JsonResponse({"status": "ok"})