from rest_framework.views import APIView
from midtransclient import Snap
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import Order


class PaymentAPIViews(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # get order id from request
        order_id = request.data.get("order_id")
        try:
            # get order from database
            order = Order.objects.get(id=order_id)

            # get ref code
            ref_code = order.ref_code

            # get order total amount
            total_amount = order.total_amount

            # get user first & last name
            user_first_name = order.user.first_name
            user_last_name = order.user.last_name

            # get order user email
            user_email = order.user.email

            # get order user phone
            user_phone = order.user.user_details.phone_number
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # create snap client
        snap = Snap(is_production=False, server_key=settings.MIDTRANS["SERVER_KEY"])

        # create transaction details
        param = {
            "transaction_details": {"order_id": ref_code, "gross_amount": total_amount},
            "credit_card": {"secure": True},
            "customer_details": {
                "first_name": user_first_name,
                "last_name": user_last_name,
                "email": user_email,
                "phone": user_phone,
            },
        }

        # create transaction token
        try:
            transaction_token = snap.create_transaction(param)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # return transaction token
        return Response({"data": transaction_token}, status=status.HTTP_200_OK)


class FinishPaymentAPIViews(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # get order id from request
        order_id = request.data.get("order_id")

        snap = Snap(is_production=False, server_key=settings.MIDTRANS["SERVER_KEY"])

        # get transaction status
        try:
            transaction_status = snap.transactions.status(order_id)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(transaction_status, status=status.HTTP_200_OK)
