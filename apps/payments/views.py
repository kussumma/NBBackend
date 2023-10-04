from rest_framework.views import APIView
from midtransclient import Snap
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
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
            order_id = order.id

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
        snap = Snap(
            is_production=settings.DEBUG, server_key=settings.MIDTRANS["SERVER_KEY"]
        )

        # create transaction details
        param = {
            "transaction_details": {"order_id": order_id, "gross_amount": total_amount},
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


class PaymentStatusAPIViews(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # get order id from request
        order_id = request.data.get("order_id")

        snap = Snap(
            is_production=settings.DEBUG, server_key=settings.MIDTRANS["SERVER_KEY"]
        )

        # get transaction status
        try:
            transaction_status = snap.transactions.status(order_id)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # update order status
        if transaction_status["transaction_status"]:
            # update order status
            try:
                order = Order.objects.get(id=order_id)
                order.payment_status = transaction_status["transaction_status"]
                order.payment_ref_code = transaction_status["transaction_id"]
                order.save()
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(transaction_status, status=status.HTTP_200_OK)
