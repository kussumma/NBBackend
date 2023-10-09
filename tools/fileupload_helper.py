import os
import cv2
from rest_framework.serializers import ValidationError


def validate_uploaded_file(uploaded_file, type):
    # Check file extension
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()

    # Check file size
    max_file_size = 5 * 1024 * 1024  # 5 MB

    if type == "image" and file_extension in [".jpg", ".jpeg", ".png", ".gif", ".pdf"]:
        if uploaded_file.size > max_file_size:
            raise ValidationError("File size exceeds the maximum allowed size of 5 MB")

    elif type == "video" and file_extension in [".mp4", ".avi", ".mov"]:
        if uploaded_file.size > max_file_size * 3:
            raise ValidationError("File size exceeds the maximum allowed size of 15 MB")

        try:
            video_capture = cv2.VideoCapture(uploaded_file.temporary_file_path())
            frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = int(video_capture.get(cv2.CAP_PROP_FPS))
            video_duration = frame_count / fps

            if video_duration > 60:
                raise ValidationError(
                    "Video duration exceeds the maximum allowed duration of 60 seconds"
                )
        except Exception as e:
            raise ValidationError("Error analyzing video file")

    else:
        raise ValidationError(
            "Unsupported file format. Allowed formats: jpg, jpeg, png, gif, mp4, avi, mov, pdf"
        )

    return uploaded_file
