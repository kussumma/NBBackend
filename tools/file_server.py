from django.http import HttpResponse
from rest_framework import status, views
from rest_framework.response import Response
from gridfs import GridFS
from django.conf import settings
from rest_framework.permissions import AllowAny


class FileAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, collection, filename):
        if not filename:
            return Response(
                {"error": "filename is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            # open the file from GridFS
            db = settings.MONGODB_DATABASE
            fs = GridFS(db, collection)
            file = fs.get_last_version(filename)

            # get the file content type from the filename
            ext = filename.split(".")[-1].lower()
            content_type = "application/octet-stream"
            if ext == "jpg" or ext == "jpeg":
                content_type = "image/jpeg"
            elif ext == "png":
                content_type = "image/png"
            elif ext == "webp":
                content_type = "image/webp"
            elif ext == "mp4" or ext == "mov":
                content_type = "video/mp4"

            # return the file directly to the client
            response = HttpResponse(file.read(), content_type=content_type)
            response["Content-Disposition"] = "inline; filename=" + file.filename
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return response
