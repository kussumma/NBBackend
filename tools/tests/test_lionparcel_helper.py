import pytest
from tools.lionparcel_helper import LionParcelHelper
from django.conf import settings
import random
import string


@pytest.fixture
def lion_parcel_helper():
    api_key = settings.LIONPARCEL_API_KEY
    return LionParcelHelper(api_key)


@pytest.fixture
def random_string():
    return "".join(random.choice(string.ascii_letters) for i in range(10)).upper()


def test_get_tariff(lion_parcel_helper):
    # Arrange
    origin = "KUTA SELATAN, BADUNG"
    destination = "DAWAN, KLUNGKUNG"
    weight = 10
    commodity = "COS3"

    # Act
    result = lion_parcel_helper.get_tariff(origin, destination, weight, commodity)

    # Assert
    assert "forward_area" in result


def test_make_booking(lion_parcel_helper, random_string):
    # Arrange
    booking_data = {
        "stt_goods_estimate_price": 300000,
        "stt_no_ref_external": random_string,
        "stt_origin": "KUTA SELATAN, BADUNG",
        "stt_destination": "DAWAN, KLUNGKUNG",
        "stt_sender_name": "TEST",
        "stt_sender_phone": "08123456789",
        "stt_sender_address": "JL. TEST",
        "stt_recipient_name": "TEST 2",
        "stt_recipient_address": "JL. TEST 2",
        "stt_recipient_phone": "081234567892",
        "stt_product_type": "REGPACK",
        "stt_commodity_code": "COS 2",
        "stt_pieces": [
            {
                "stt_piece_gross_weight": 10,
                "stt_piece_length": 10,
                "stt_piece_width": 10,
                "stt_piece_height": 10,
            }
        ],
    }

    # Act
    result = lion_parcel_helper.make_booking(booking_data)

    # Assert
    assert "stt_no" in result["data"]["stt"][0]


def test_track_booking(lion_parcel_helper, random_string):
    # Arrange
    booking_id = "99LP1700230905237"

    # Act
    result = lion_parcel_helper.track_booking(booking_id)

    # Assert
    assert "current_status" in result["stts"][0]
