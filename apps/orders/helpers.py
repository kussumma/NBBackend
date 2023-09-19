from rest_framework import serializers, status
from rest_framework.response import Response

from django.conf import settings

from .models import Order, OrderItem, OrderShipping
from apps.store.models import Contact
from tools.lionparcel_helper import LionParcelHelper

def lionparcel_booking(order_id):
    order = Order.objects.get(id=order_id)
    if not order:
        return Response({'message': 'Order not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    order_items = OrderItem.objects.filter(order=order)
    if not order_items:
        return Response({'message': 'Order items not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    shipping = OrderShipping.objects.get(order=order)
    if not shipping:
        return Response({'message': 'Shipping not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    contact = Contact.objects.get(is_active=True)
    if not contact:
        return Response({'message': 'Active contact not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    lionparcel = LionParcelHelper(settings.LIONPARCEL_API_KEY)

    # create stt pieces
    stt_pieces = []
    for order_item in order_items:
        stt_pieces.append({
            'stt_piece_gross_weight': order_item.stock_weight,
            'stt_piece_length': order_item.stock_length,
            'stt_piece_width': order_item.stock_width,
            'stt_piece_height': order_item.stock_height
        })

    # create booking data
    booking_data = {
        "stt_goods_estimate_price": order.total_amount,
        "stt_origin": contact.origin,
        "stt_destination": shipping.destination_route,
        "stt_sender_name": contact.name,
        "stt_sender_phone": contact.phone,
        "stt_sender_address": contact.address,
        "stt_recipient_name": shipping.receiver_name,
        "stt_recipient_address": shipping.receiver_address,
        "stt_recipient_phone": shipping.receiver_phone,
        "stt_product_type": shipping.shipping_type,
        "stt_commodity_code": contact.commodity,
        "stt_pieces": stt_pieces
    }
        
    try:
        booking = lionparcel.make_booking(booking_data)

        # get shipping ref code
        if booking['success']:
            shipping_ref_code = booking['data']['stt'][0]['stt_no']

            # save shipping ref code
            shipping.shipping_ref_code = shipping_ref_code
            shipping.save()
        else:
            raise serializers.ValidationError(booking['message']['en'])
    except Exception as e:
        raise serializers.ValidationError(str(e))
    
    return