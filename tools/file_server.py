from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient
from gridfs import GridFS
from django.conf import settings
from django.http import HttpResponse
import urllib.parse
from rest_framework.permissions import AllowAny


class FileAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, collection, filename):
        if not filename:
            return Response(
                {"error": "filename is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if settings.MONGODB_GRIDFS["UNIX_SOCKET_PATH"]:
            mongo_uri = "mongodb://" + urllib.parse.quote(
                settings.MONGODB_GRIDFS["UNIX_SOCKET_PATH"]
            )
            client = MongoClient(mongo_uri)
        else:
            client = MongoClient(
                settings.MONGODB_GRIDFS["HOST"],
                settings.MONGODB_GRIDFS["PORT"],
            )
        db = client[settings.MONGODB_GRIDFS["DB"]]
        if settings.MONGODB_GRIDFS["USERNAME"] and settings.MONGODB_GRIDFS["PASSWORD"]:
            db.authenticate(
                settings.MONGO_DB_USERNAME,
                settings.MONGO_DB_PASSWORD,
            )

        fs = GridFS(db, collection)
        file = fs.get_last_version(filename)

        response = HttpResponse(file.read(), content_type="image/jpeg")
        response["Content-Disposition"] = "attachment; filename=" + file.filename
        return response
