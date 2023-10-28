import os
import cv2
from django.core.exceptions import ValidationError
import tempfile


def validate_uploaded_file(uploaded_file, type):
    # Check file extension
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()

    # Check file size
    max_file_size = 5 * 1024 * 1024  # 5 MB

    if type == "image" and file_extension in [".jpg", ".jpeg", ".png"]:
        if uploaded_file.size > max_file_size:
            raise ValidationError("File size exceeds the maximum allowed size of 5 MB")

    elif type == "video" and file_extension in [".mp4", ".mov"]:
        if uploaded_file.size > max_file_size * 6:
            raise ValidationError("File size exceeds the maximum allowed size of 15 MB")

        try:
            # opencv requires a file path to analyze video files
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.read())
                video_path = temp_file.name

            # analyze video file
            video_capture = cv2.VideoCapture(video_path)
            frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = int(video_capture.get(cv2.CAP_PROP_FPS))
            video_duration = frame_count / fps

            # release video capture
            video_capture.release()

        except Exception as e:
            raise ValidationError("Error analyzing video file: " + str(e))

        finally:
            # delete temp file
            os.unlink(video_path)

        if video_duration > 35:
            raise ValidationError(
                "Video duration exceeds the maximum allowed duration of 30 seconds"
            )

    else:
        raise ValidationError(
            "Unsupported file format. Image must be in .jpg, .jpeg, .png. Video must be in .mp4, or .mov format"
        )

    return uploaded_file
