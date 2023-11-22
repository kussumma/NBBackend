from rest_framework.views import APIView
from midtransclient import Snap
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.orders.models import Order


class PaymentAPIViews(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # get order id from request
        ref_code = request.data.get("ref_code")
        try:
            # get order from database
            order = Order.objects.get(ref_code=ref_code)

            # get order id
            ref_code = order.ref_code

            # get order total amount
            total_amount = order.total_amount

            # get order shipping cost
            shipping_amount = order.shipping_amount

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
        # settings.DEBUG will be True if the environment is development
        snap = Snap(
            is_production=not settings.DEBUG, server_key=settings.MIDTRANS["SERVER_KEY"]
        )

        # create transaction details
        param = {
            "transaction_details": {
                "order_id": ref_code,
                "gross_amount": total_amount,
            },
            "credit_card": {"secure": True},
            "customer_details": {
                "first_name": user_first_name,
                "last_name": user_last_name,
                "email": user_email,
                "phone": user_phone,
            },
            "item_details": [
                {
                    "id": 1,
                    "price": total_amount - shipping_amount,
                    "quantity": 1,
                    "name": f"Order {ref_code}",
                },
                {
                    "id": 2,
                    "price": shipping_amount,
                    "quantity": 1,
                    "name": "Misc Fee",
                },
            ],
        }

        # create transaction token
        try:
            transaction_token = snap.create_transaction(param)

            order.payment_token = transaction_token
            order.save()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # return transaction token
        return Response({"data": transaction_token}, status=status.HTTP_200_OK)


class PaymentStatusAPIViews(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # get order id from request
        ref_code = request.data.get("ref_code")

        try:
            # get order from database
            order = Order.objects.get(ref_code=ref_code)

            # get order id
            ref_code = order.ref_code
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        snap = Snap(
            is_production=not settings.DEBUG, server_key=settings.MIDTRANS["SERVER_KEY"]
        )

        # get transaction status
        try:
            transaction_status = snap.transactions.status(ref_code)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # update order status
        if transaction_status["transaction_status"]:
            # update order status
            try:
                order.payment_status = transaction_status["transaction_status"]
                order.payment_ref_code = transaction_status["transaction_id"]
                order.save()
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(transaction_status, status=status.HTTP_200_OK)


class PaymentNotificationAPIView(APIView):
    """
    Midtrans Webhook API View to handle payment status
    https://docs.midtrans.com/docs/https-notification-webhooks
    payment status:
    - settlement : payment is successful
    - capture : payment is successful, but waiting for settlement
    - pending : payment is pending
    - deny : payment is denied
    - cancel : payment is canceled
    - expire : payment is expired
    - failure : payment is failed
    - refund : payment is refunded
    - partial_refund : payment is partially refunded
    fraud status:
    - accept : payment is not detected as fraud
    - deny : payment is detected as fraud
    """

    permission_classes = [AllowAny]

    def post(self, request):
        # get transaction status
        snap = Snap(
            is_production=not settings.DEBUG, server_key=settings.MIDTRANS["SERVER_KEY"]
        )

        try:
            transaction = snap.transactions.notification(request.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # get transaction data
        order_id = transaction["order_id"]
        transaction_id = transaction["transaction_id"]
        transaction_status = transaction["transaction_status"]
        fraud_status = transaction["fraud_status"]

        # check the transaction status
        status = "pending"
        if transaction_status == "capture":
            if fraud_status == "accept":
                status = "capture"
            else:
                status = "pending"
        elif transaction_status == "settlement":
            status = "settlement"
        elif transaction_status == "cancel":
            status = "cancel"
        elif transaction_status == "deny":
            status = "deny"
        elif transaction_status == "expire":
            status = "expire"
        elif transaction_status == "failure":
            status = "failure"
        elif transaction_status == "refund":
            status = "refund"
        elif transaction_status == "partial_refund":
            status = "partial_refund"

        # get order from database
        try:
            order = Order.objects.get(ref_code=order_id)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # update order status
        try:
            order.payment_status = status
            order.payment_ref_code = transaction_id
            order.save()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "success"}, status=status.HTTP_200_OK)
