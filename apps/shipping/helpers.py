from rest_framework import status
from rest_framework.response import Response
from django.conf import settings

from .models import ShippingGroupTariff, ShippingType
from apps.store.models import Contact
from tools.lionparcel_helper import LionParcelHelper

def lionparcel_original_tariff(weight, shipping):
    # get store contact
    try:
        store = Contact.objects.get(is_active=True)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    lionparcel = LionParcelHelper(settings.LIONPARCEL_API_KEY)
    try:
        response = lionparcel.get_tariff(
            origin=store.origin,
            destination=shipping.destination.route,
            weight=weight,
            commodity=store.commodity,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    return response

def lionparcel_tariff_mapping(api_response: dict):
    # get the weight
    weight = api_response.get('weight')

    # get the destination
    destination = api_response.get('destination')

    # get the result from the response
    result = api_response.get('result')

    # get all enabled shipping types
    shipping_types = ShippingType.objects.all()
    if not shipping_types:
        raise Exception('No shipping types found.')

    # create new list to store the filtered result
    filtered_result = []
    default_result = []

    # get the tariff and product from each result
    for result_item in result:
        product = result_item.get('product')
        is_embargo = result_item.get('is_embargo')
        estimasi_sla = result_item.get('estimasi_sla')
        tariff = result_item.get('total_tariff')

        # check the product is not embargo
        if not is_embargo:

            # check if product and destination available in shipping group
            try:
                shipping_tariff = ShippingGroupTariff.objects.get(
                    shipping_group__shipping_group_items__shipping_route__route=destination,
                    shipping_type__code=product
                )
            except ShippingGroupTariff.DoesNotExist:
                shipping_tariff = None

            if shipping_tariff:
                new_tariff = shipping_tariff.tariff * weight
                group_name = shipping_tariff.shipping_group.name
                
                filtered_result.append({
                    'weight': weight,
                    'destination': destination,
                    'total_tariff': new_tariff,
                    'shipping_type': product,
                    'shipping_type_name': shipping_tariff.shipping_type.name,
                    'is_embargo': is_embargo,
                    'estimasi_sla': estimasi_sla,
                    'shipping_group': group_name
                })
            else:
                for shipping_type in shipping_types:
                    if shipping_type.code == product:
                        filtered_result.append({
                            'weight': weight,
                            'destination': destination,
                            'total_tariff': tariff,
                            'shipping_type': product,
                            'shipping_type_name': shipping_type.name,
                            'is_embargo': is_embargo,
                            'estimasi_sla': estimasi_sla,
                            'shipping_group': None
                        })

    return filtered_result if filtered_result else default_result