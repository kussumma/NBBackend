import requests


class LionParcelHelper:
    BASE_URL = 'https://api-stg-middleware.thelionparcel.com'
    
    def __init__(self, api_key):
        self.api_key = api_key

    def _make_request(self, endpoint, method='GET', params=None, data=None):
        headers = {
            'Authorization': f'Basic {self.api_key}',
            'Content-Type': 'application/json',
        }

        url = f'{self.BASE_URL}/{endpoint}'
        response = requests.request(method, url, headers=headers, params=params, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.json()['message']['en'])

    def get_tariff(self, origin, destination, weight, commodity):
        """
        Get tariff information for a shipment by origin, destination, weight, and commodity.

        :param origin: The origin city with format "kecamatan, kota".
        :param destination: The destination city with format "kecamatan, kota".
        :param weight: The weight of the shipment in kilograms.
        :param commodity: The commodity code.
        :return: A dictionary containing the tariff information.
        """

        endpoint = '/v3/tariffv3'
        params = {
            'origin': origin,
            'destination': destination,
            'weight': weight,
            'commodity': commodity,
        }
        return self._make_request(endpoint, params=params)
    
    def make_booking(self, stt_goods_estimate_price, stt_origin, stt_destination, stt_sender_name, stt_sender_phone, stt_sender_address, stt_recipient_name, stt_recipient_address, stt_recipient_phone, stt_product_type, stt_pieces):
        """
        Make a booking for a shipment.

        :param stt_no_ref_external: The reference number for the shipment, from the internal system.
        :param stt_goods_estimate_price: The estimated price of the shipment.
        :param stt_origin: The origin city with format "kecamatan, kota".
        :param stt_destination: The destination city with format "kecamatan, kota".
        :param stt_sender_name: The name of the sender.
        :param stt_sender_phone: The phone number of the sender.
        :param stt_sender_address: The address of the sender.
        :param stt_recipient_name: The name of the recipient.
        :param stt_recipient_address: The address of the recipient.
        :param stt_recipient_phone: The phone number of the recipient.
        :param stt_product_type: The product type of the shipment.
        :param stt_pieces: The dictionary containing the pieces information.
        :return: A dictionary containing the booking information.
        """

        # validate data
        if not stt_goods_estimate_price:
            raise Exception("stt_goods_estimate_price is required")
        
        if not stt_origin:
            raise Exception("stt_origin is required")
        
        if not stt_destination:
            raise Exception("stt_destination is required")
        
        if not stt_sender_name:
            raise Exception("stt_sender_name is required")
        
        if not stt_sender_phone:
            raise Exception("stt_sender_phone is required")
        
        if not stt_sender_address:
            raise Exception("stt_sender_address is required")
        
        if not stt_recipient_name:
            raise Exception("stt_recipient_name is required")
        
        if not stt_recipient_address:
            raise Exception("stt_recipient_address is required")
        
        if not stt_recipient_phone:
            raise Exception("stt_recipient_phone is required")
        
        if not stt_product_type:
            raise Exception("stt_product_type is required")
        
        if not stt_pieces:
            raise Exception("stt_pieces is required")

        # create the booking data
        booking_data = {
            "stt_goods_estimate_price": stt_goods_estimate_price,
            "stt_origin": stt_origin,
            "stt_destination": stt_destination,
            "stt_sender_name": stt_sender_name,
            "stt_sender_phone": stt_sender_phone,
            "stt_sender_address": stt_sender_address,
            "stt_recipient_name": stt_recipient_name,
            "stt_recipient_address": stt_recipient_address,
            "stt_recipient_phone": stt_recipient_phone,
            "stt_product_type": stt_product_type,
            "stt_commodity_code": 'COS 2',
            "stt_is_cod": False,
            "stt_is_woodpacking": False,
            "stt_pieces": stt_pieces,
        }

        # reformat the data to follow the API format
        booking_data = {
            "stt": booking_data
        }

        endpoint = '/client/booking'
        return self._make_request(endpoint, method='POST', data=booking_data)

    def get_booking(self, booking_id):
        """
        Get booking information by booking ID (STT or External Reference Number)

        :param booking_id: The booking ID.
        :return: A dictionary containing the booking information.
        """

        endpoint = f'/v3/stt/track?q={booking_id}'
        return self._make_request(endpoint)