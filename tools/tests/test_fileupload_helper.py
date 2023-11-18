import io
from io import BytesIO
import cv2
import os
import numpy as np
from django.core.files.base import ContentFile
import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from tools.fileupload_helper import FileUploadHelper


def create_image(
    storage, filename, size=(100, 200), image_mode="RGB", image_format="JPEG"
):
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


def create_dummy_video(
    filename="dummy_video.mp4", width=640, height=480, fps=30, duration=5
):
    video_data = io.BytesIO()  # Create a BytesIO object for in-memory storage

    try:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video = cv2.VideoWriter(filename, fourcc, fps, (width, height))

        for _ in range(fps * duration):
            frame = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
            video.write(frame)

        video.release()

        video_data.write(
            open(filename, "rb").read()
        )  # Write the video data to the BytesIO object
        video_data.seek(0)  # Reset the file pointer to the beginning
        video_data.content_type = "video/mp4"
        video_data.size = video_data.getbuffer().nbytes  # Get the size of the data
        video_data.temporary_file_path = (
            lambda: filename
        )  # Provide a temporary file path

        return video_data
    except Exception as e:
        print(f"An error occurred: {e}")


@pytest.fixture
def image_file():
    test_image = create_image(None, "test_image.jpg")
    return SimpleUploadedFile(
        "test_image.jpg", test_image.getvalue(), content_type="image/jpeg"
    )


@pytest.fixture
def video_file():
    test_video = create_dummy_video()
    return test_video


def test_validate_image_valid(image_file):
    helper = FileUploadHelper(image_file, type="image")
    assert helper.validate() == image_file


def test_validate_image_invalid_type(image_file):
    helper = FileUploadHelper(image_file, type="video")
    with pytest.raises(ValidationError):
        helper.validate()


def test_validate_image_invalid_size(image_file):
    helper = FileUploadHelper(image_file, type="image")
    helper.max_file_size = 1
    with pytest.raises(ValidationError):
        helper.validate()


def test_validate_image_invalid_ratio(image_file):
    helper = FileUploadHelper(image_file, type="image", ratio="16:9")
    with pytest.raises(ValidationError):
        helper.validate()


def test_validate_image_invalid_resolution(image_file):
    helper = FileUploadHelper(image_file, type="image", ratio="1:1")
    image = Image.open(io.BytesIO(image_file.read()))
    helper.get_file_ratio = lambda: image.size
    with pytest.raises(ValidationError):
        helper.validate()


def test_validate_image_valid_webp(image_file):
    helper = FileUploadHelper(image_file, type="image", webp=True)
    assert helper.validate() != image_file


def test_validate_video_valid(video_file):
    helper = FileUploadHelper(video_file, type="video")
    assert helper.validate() == video_file


def test_validate_video_invalid_type(video_file):
    helper = FileUploadHelper(video_file, type="image")
    with pytest.raises(ValidationError):
        helper.validate()


def test_validate_video_invalid_size(video_file):
    helper = FileUploadHelper(video_file, type="video")
    helper.max_video_size = 1
    with pytest.raises(ValidationError):
        helper.validate()


def test_validate_video_invalid_duration(video_file):
    helper = FileUploadHelper(video_file, type="video")
    helper.max_video_duration = 1
    with pytest.raises(ValidationError):
        helper.validate()


def test_delete_video_file(video_file):
    helper = FileUploadHelper(video_file, type="video")
    helper.validate()
    os.remove(helper.get_file_path())
    assert not os.path.exists(helper.get_file_path())
