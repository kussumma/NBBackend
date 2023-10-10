from django.http import HttpResponse
from rest_framework import status, views
from rest_framework.response import Response
from pymongo import MongoClient
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
            client = MongoClient(settings.MONGODB_GRIDFS["URL"])
            db = client[settings.MONGODB_GRIDFS["DB"]]
            fs = GridFS(db, collection)
            file = fs.get_last_version(filename)

            response = HttpResponse(file.read(), content_type="image/jpeg")
            response["Content-Disposition"] = "inline; filename=" + file.filename
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return response
