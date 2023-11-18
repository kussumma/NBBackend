import pytest
from django.http import HttpRequest, HttpResponse
from rest_framework import status
from tools.file_server import FileAPIView
from tools.filestorage_helper import GridFSStorage
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile


def create_image(
    storage, filename, size=(100, 200), image_mode="RGB", image_format="JPEG"
):
    """
    Generate a test image, returning the filename that it was saved as.

    If ``storage`` is ``None``, the BytesIO containing the image data
    will be passed instead.
    """
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


@pytest.fixture
def file_api_view():
    return FileAPIView()


@pytest.fixture
def http_request():
    return HttpRequest()


@pytest.fixture
def http_response():
    return HttpResponse()


@pytest.fixture
def image_file():
    test_image = create_image(None, "test_image.jpg")
    return SimpleUploadedFile(
        "test_image.jpg", test_image.getvalue(), content_type="image/jpeg"
    )


def test_file_api_view_get_with_missing_filename(file_api_view, http_request):
    # Arrange
    collection = "test_collection"
    filename = ""
    http_request.method = "GET"

    # Act
    response = file_api_view.get(http_request, collection, filename)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {"error": "filename is required"}


def test_file_api_view_get_with_valid_filename(file_api_view, http_request, image_file):
    # Arrange
    collection = "test_collection"

    filename = GridFSStorage(collection=collection)._save(image_file.name, image_file)

    http_request.method = "GET"

    # Act
    response = file_api_view.get(http_request, collection, filename)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response["Content-Disposition"] == "inline; filename=" + filename


def test_file_api_view_get_with_invalid_filename(file_api_view, http_request):
    # Arrange
    collection = "test_collection"
    filename = "invalid_file.txt"
    http_request.method = "GET"

    # Act
    response = file_api_view.get(http_request, collection, filename)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_file_api_view_get_with_exception(file_api_view, http_request):
    # Arrange
    collection = "test_collection"
    filename = "test.jpg"
    http_request.method = "GET"

    # Act
    response = file_api_view.get(http_request, collection, filename)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
