import requests
from urllib.parse import urljoin
from typing import Any, Dict, Optional

"""
This code defines a class called `LionParcelHelper` that provides methods for interacting with the Lion Parcel API. It allows users to get tariff information for a shipment and make a booking for a shipment.

Example Usage:
    # Create an instance of LionParcelHelper with an API key
    helper = LionParcelHelper(api_key='your_api_key')

    # Get tariff information for a shipment
    tariff_info = helper.get_tariff(origin='kecamatan, kota', destination='kecamatan, kota', weight=10, commodity='commodity_code')

    # Make a booking for a shipment
    booking_info = helper.make_booking(stt_goods_estimate_price=100, stt_origin='kecamatan, kota', stt_destination='kecamatan, kota', stt_sender_name='Sender Name', stt_sender_phone='Sender Phone', stt_sender_address='Sender Address', stt_recipient_name='Recipient Name', stt_recipient_address='Recipient Address', stt_recipient_phone='Recipient Phone', stt_product_type='Product Type', stt_commodity_code='Commodity Code', stt_pieces={'piece1': 1, 'piece2': 2})

Main functionalities:
- The `LionParcelHelper` class provides methods for interacting with the Lion Parcel API.
- It allows users to get tariff information for a shipment and make a booking for a shipment.

Methods:
- `_make_request`: Makes an HTTP request to the Lion Parcel API.
- `get_tariff`: Gets tariff information for a shipment by origin, destination, weight, and commodity.
- `make_booking`: Makes a booking for a shipment.
- `get_booking`: Gets booking information by booking ID.

Fields:
- `BASE_URL`: The base URL of the Lion Parcel API.
"""


class LionParcelHelper:
    BASE_URL = "https://api-stg-middleware.thelionparcel.com"

    def __init__(self, api_key):
        self.api_key = api_key

    def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Makes an HTTP request to the Lion Parcel API.

        Args:
            endpoint (str): The API endpoint to send the request to.
            method (str, optional): The HTTP method to use for the request. Defaults to 'GET'.
            params (dict, optional): The query parameters to include in the request URL. Defaults to None.
            data (dict, optional): The JSON data to include in the request body. Defaults to None.

        Returns:
            dict: The JSON response from the API.

        Raises:
            Exception: If the response status code is not 200 or 201.
        """
        headers = {
            "Authorization": f"Basic {self.api_key}",
            "Content-Type": "application/json",
        }

        url = urljoin(self.BASE_URL, endpoint)
        response = requests.request(
            method, url, headers=headers, params=params, json=data
        )

        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(response.json())

    def get_tariff(
        self, origin: str, destination: str, weight: int, commodity: str
    ) -> Dict[str, Any]:
        """
        Get tariff information for a shipment by origin, destination, weight, and commodity.

        :param origin: The origin city with format "kecamatan, kota".
        :param destination: The destination city with format "kecamatan, kota".
        :param weight: The weight of the shipment in kilograms.
        :param commodity: The commodity code.
        :return: A dictionary containing the tariff information.
        """

        endpoint = "/v3/tariff"
        params = {
            "origin": origin,
            "destination": destination,
            "weight": weight,
            "commodity": commodity,
        }
        return self._make_request(endpoint, params=params)

    def make_booking(self, booking_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a booking using the provided booking data.

        Args:
            booking_data (Dict[str, Any]): A dictionary containing the booking data.
                - stt_no (str): The booking number.
                - stt_no_ref_external (str): The external reference number for the booking.
                - stt_tax_number (str): The tax number for the booking.
                - stt_goods_estimate_price (float): The estimated price of the goods for the booking.
                - stt_goods_status (str): The status of the goods for the booking.
                - stt_origin (str): The origin of the booking.
                - stt_destination (str): The destination of the booking.
                - stt_sender_name (str): The name of the sender for the booking.
                - stt_sender_phone (str): The phone number of the sender for the booking.
                - stt_sender_address (str): The address of the sender for the booking.
                - stt_recipient_name (str): The name of the recipient for the booking.
                - stt_recipient_address (str): The address of the recipient for the booking.
                - stt_recipient_phone (str): The phone number of the recipient for the booking.
                - stt_insurance_type (str): The insurance type for the booking.
                - stt_product_type (str): The product type for the booking.
                - stt_commodity_code (str): The commodity code for the booking.
                - stt_is_cod (bool): Indicates if the booking is cash on delivery.
                - stt_is_woodpacking (bool): Indicates if the booking requires wood packing.
                - stt_pieces (int): The number of pieces for the booking.
                - stt_piece_per_pack (int): The number of pieces per pack for the booking.
                - stt_next_commodity (str): The next commodity for the booking.
                - stt_cod_amount (float): The cash on delivery amount for the booking.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the API.
        """

        # validate the booking data
        if not isinstance(booking_data, dict):
            raise ValueError("booking_data must be a dictionary")

        # validate key in booking_data
        for key in booking_data:
            if booking_data[key] is None:
                raise ValueError(f"{key} is required")

        # create the booking data
        booking_data = {
            "stt_no": "",
            "stt_no_ref_external": "",
            "stt_tax_number": "",
            "stt_goods_estimate_price": booking_data["stt_goods_estimate_price"],
            "stt_goods_status": "",
            "stt_origin": booking_data["stt_origin"],
            "stt_destination": booking_data["stt_destination"],
            "stt_sender_name": booking_data["stt_sender_name"],
            "stt_sender_phone": booking_data["stt_sender_phone"],
            "stt_sender_address": booking_data["stt_sender_address"],
            "stt_recipient_name": booking_data["stt_recipient_name"],
            "stt_recipient_address": booking_data["stt_recipient_address"],
            "stt_recipient_phone": booking_data["stt_recipient_phone"],
            "stt_insurance_type": "free",
            "stt_product_type": booking_data["stt_product_type"],
            "stt_commodity_code": booking_data["stt_commodity_code"],
            "stt_is_cod": False,
            "stt_is_woodpacking": False,
            "stt_pieces": booking_data["stt_pieces"],
            "stt_piece_per_pack": 0,
            "stt_next_commodity": "",
            "stt_cod_amount": 0,
        }

        # reformat the data to follow the API format
        booking_data = {"stt": booking_data}

        endpoint = "/client/booking"
        return self._make_request(endpoint, method="POST", data=booking_data)

    def track_booking(self, booking_id: str) -> Dict[str, Any]:
        """
        Track booking information by booking ID (STT or External Reference Number)

        :param booking_id: The booking ID.
        :return: A dictionary containing the booking information.
        """

        endpoint = f"/v3/stt/track?q={booking_id}"
        return self._make_request(endpoint)
