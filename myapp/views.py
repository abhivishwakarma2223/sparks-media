from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
import requests # <--- We use this instead of Twilio Client
import json

def base(request):
    return render (request, 'base.html')

def index(request):
    return render(request, 'index.html')


def learnmore(request):
    return render(request, 'learnmore.html')



def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        whatsapp_body = (
            f"🚀 *New Lead: Spark Media*\n\n"
            f"👤 *Name:* {name}\n"
            f"📧 *Email:* {email}\n"
            f"📱 *Phone:* {phone}\n"
            f"📝 *Message:* {message}\n"
        )

        # --- DIRECT API METHOD (No Library Needed) ---
        url = f"https://api.twilio.com/2010-04-01/Accounts/{settings.TWILIO_ACCOUNT_SID}/Messages.json"
        
        payload = {
            "From": settings.TWILIO_WHATSAPP_NUMBER,
            "To": settings.MY_WHATSAPP_NUMBER,
            "Body": whatsapp_body
        }

        try:
            # Send request directly to Twilio servers
            response = requests.post(
                url, 
                data=payload, 
                auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            )
            
            # Check if successful (200 or 201 means Created)
            if response.status_code in [200, 201]:
                return JsonResponse({'status': 'success', 'message': 'Message Sent Successfully!'})
            else:
                # If Twilio rejects it, print why
                error_data = response.json()
                print(f"Twilio Error: {error_data}")
                return JsonResponse({'status': 'error', 'message': f"Twilio Failed: {error_data.get('message')}"}, status=500)

        except Exception as e:
            print(f"System Error: {e}")
            return JsonResponse({'status': 'error', 'message': "Internal Server Error"}, status=500)

    # Handle GET request (someone typing url directly)
    return redirect('/')