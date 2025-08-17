from django.shortcuts import render
from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
import requests
import uuid
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Payment, Listing, Booking

CHAPA_URL = f"{settings.CHAPA_BASE_URL}/transaction/initialize"

@api_view(["POST"])
def initiate_payment(request):
    amount = request.data.get("amount")
    email = request.data.get("email")
    first_name = request.data.get("first_name", "Traveler")
    last_name = request.data.get("last_name", "User")
    booking_reference = str(uuid.uuid4())

    payload = {
        "amount": str(amount),
        "currency": "ETB",
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "tx_ref": booking_reference,
        "callback_url": "http://localhost:8000/api/payments/verify/",  # adjust for prod
    }

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(CHAPA_URL, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        Payment.objects.create(
            booking_reference=booking_reference,
            amount=amount,
            transaction_id=booking_reference,  # tx_ref works as unique ID
            status="Pending"
        )
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Payment initiation failed"}, status=response.status_code)

@api_view(["GET"])
def verify_payment(request, tx_ref):
    url = f"{settings.CHAPA_BASE_URL}/transaction/verify/{tx_ref}"
    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        try:
            payment = Payment.objects.get(transaction_id=tx_ref)
            if data["status"] == "success":
                payment.status = "Completed"
                payment.save()
                return Response({"message": "Payment successful", "data": data})
            else:
                payment.status = "Failed"
                payment.save()
                return Response({"message": "Payment failed", "data": data})
        except Payment.DoesNotExist:
            return Response({"error": "Payment record not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "Verification failed"}, status=response.status_code)

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

