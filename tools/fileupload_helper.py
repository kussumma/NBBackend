import os
import cv2
import PIL
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError


class FileUploadHelper:
    """
    Helper class to validate uploaded files
    How to use:
        FileUploadHelper(uploaded_file, type="image", ratio=None, webp=False).validate()
    Parameters:
        uploaded_file: Uploaded file object
        type: File type, either "image" or "video"
        ratio: Image aspect ratio (width:height), e.g. "16:9"
        webp: Convert image to WebP format
    """

    def __init__(self, uploaded_file, type="image", ratio=None, webp=False):
        self.uploaded_file = uploaded_file
        self.max_file_size = 5 * 1024 * 1024
        self.max_video_duration = 35
        self.max_video_size = 30 * 1024 * 1024
        self.type = type
        self.ratio = ratio
        self.webp = webp

    def validate(self):
        if self.uploaded_file is None:
            return None

        if self.type == "image":
            return self.validate_image()
        elif self.type == "video":
            return self.validate_video()
        else:
            raise ValidationError("Invalid file type")

    def validate_image(self):
        # Check content type
        content_type = self.get_content_type()

        # Check file size
        if content_type in ["image/jpeg", "image/png"]:
            if self.get_file_size() > self.max_file_size:
                raise ValidationError(
                    "File size exceeds the maximum allowed size of 5 MB"
                )

            if self.ratio:
                ratio = self.get_ratio()
                file_ratio = self.get_file_ratio()
                width, height = file_ratio

                if ratio != width / height:
                    raise ValidationError(f"Image aspect ratio must be {self.ratio}")

                if width < 400 or height < 400:
                    raise ValidationError("Image resolution must be at least 400x400")

                if width > 2000 or height > 2000:
                    raise ValidationError("Image resolution must be at most 2000x2000")

            if self.webp:
                self.convert_to_webp()
        else:
            raise ValidationError("Unsupported file format")

        return self.uploaded_file

    def validate_video(self):
        # Check content type
        content_type = self.get_content_type()

        if content_type in ["video/mp4", "video/quicktime"]:
            if self.get_file_size() > self.max_video_size:
                raise ValidationError(
                    "File size exceeds the maximum allowed size of 30 MB"
                )

            try:
                # get the temporary path of the uploaded file
                video_path = self.get_file_path()

                # Analyze video file
                video_capture = cv2.VideoCapture(video_path)
                frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
                fps = int(video_capture.get(cv2.CAP_PROP_FPS))
                video_duration = frame_count / fps

                # Release the video capture resource
                video_capture.release()

            except Exception as e:
                raise ValidationError("Error analyzing video file: " + str(e))

            if video_duration > self.max_video_duration:
                raise ValidationError(
                    "Video duration exceeds the maximum allowed duration of 30 seconds"
                )
        else:
            raise ValidationError("Unsupported video format")

        return self.uploaded_file

    def get_content_type(self):
        return self.uploaded_file.content_type

    def get_file_size(self):
        return self.uploaded_file.size

    def get_file_name(self):
        return self.uploaded_file.name

    def get_file_path(self):
        if hasattr(self.uploaded_file, "temporary_file_path"):
            return self.uploaded_file.temporary_file_path()
        else:
            return self.uploaded_file.file

    def get_ratio(self):
        """
        1 inch = 96 pixels
        """
        ratio = self.ratio.split(":")
        width_ratio = int(ratio[0]) * 96
        height_ratio = int(ratio[1]) * 96
        new_ratio = width_ratio / height_ratio
        return new_ratio

    def get_file_ratio(self):
        img = PIL.Image.open(self.get_file_path())
        return img.size

    def convert_to_webp(self):
        img = PIL.Image.open(self.get_file_path())
        img = img.convert("RGB")

        # Save the image to a BytesIO object
        img_io = BytesIO()
        img.save(img_io, "webp", quality=85)
        img_io.seek(0)

        # Set the BytesIO object as the new file
        file_name = self.get_file_name() + ".webp"
        self.uploaded_file = InMemoryUploadedFile(
            img_io,
            "ImageField",
            file_name,
            "image/webp",
            img_io.getbuffer().nbytes,
            None,
        )

        return self.uploaded_file
