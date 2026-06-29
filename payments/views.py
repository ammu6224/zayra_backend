import razorpay
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer


# Razorpay client
client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID,
          settings.RAZORPAY_KEY_SECRET)
)


# =========================
# CREATE ORDER
# =========================
@api_view(["POST"])
def create_payment_order(request):

    amount = request.data.get("amount")

    if not amount:
        return Response(
            {"error": "Amount required"},
            status=400
        )

    try:
        amount = float(amount)
    except:
        return Response(
            {"error": "Invalid amount"},
            status=400
        )

    # create razorpay order
    razorpay_order = client.order.create({
        "amount": int(amount * 100),
        "currency": "INR",
        "payment_capture": 1
    })

    # save in DB
    payment = Payment.objects.create(
        user=request.user,
        order_id=razorpay_order["id"],
        amount=amount
    )

    return Response({
        "order_id": razorpay_order["id"],
        "amount": amount,
        "key": settings.RAZORPAY_KEY_ID,
        "payment_db_id": payment.id
    })


# =========================
# VERIFY PAYMENT
# =========================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_payment(request):

    razorpay_order_id = request.data.get("razorpay_order_id")
    razorpay_payment_id = request.data.get("razorpay_payment_id")
    razorpay_signature = request.data.get("razorpay_signature")

    try:
        # verify signature
        client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        })

        payment = Payment.objects.get(
            order_id=razorpay_order_id
        )

        payment.payment_id = razorpay_payment_id
        payment.status = "success"
        payment.save()

        return Response({
            "message": "Payment successful"
        })

    except Exception as e:

        return Response({
            "error": str(e)
        }, status=400)