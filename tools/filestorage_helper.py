from django.core.files.storage import Storage
from django.conf import settings
from pymongo import MongoClient
from gridfs import GridFS
from django.utils.deconstruct import deconstructible
import os
import uuid
import urllib.parse


@deconstructible
class GridFSStorage(Storage):
    """
    GridFSStorage is a Django storage backend that uses MongoDB's GridFS
    for storing files. It is based on the Storage class from Django
    https://docs.djangoproject.com/en/4.2/ref/files/storage/#django.core.files.storage.Storage
    """

    def __init__(self, location=None, base_url=None, collection=None):
        if settings.MONGODB_GRIDFS["UNIX_SOCKET_PATH"]:
            # encode the UNIX_SOCKET_PATH as URL encoding
            # https://docs.mongodb.com/manual/reference/connection-string/#unix-domain-sockets
            mongo_uri = "mongodb://" + urllib.parse.quote(
                settings.MONGODB_GRIDFS["UNIX_SOCKET_PATH"]
            )
            self.client = MongoClient(mongo_uri)
        else:
            self.client = MongoClient(
                settings.MONGODB_GRIDFS["HOST"],
                settings.MONGODB_GRIDFS["PORT"],
            )
        self.db = self.client[settings.MONGODB_GRIDFS["DB"]]
        if settings.MONGODB_GRIDFS["USERNAME"] and settings.MONGODB_GRIDFS["PASSWORD"]:
            self.db.authenticate(
                settings.MONGO_DB_USERNAME,
                settings.MONGO_DB_PASSWORD,
            )
        self.collection = collection or settings.MONGODB_GRIDFS["COLLECTION"]
        self.fs = GridFS(self.db, self.collection)
        self.location = location or ""
        self.base_url = "/media/" + self.collection + "/"

    def _open(self, name, mode="rb"):
        return self.fs.get_last_version(name)

    def _save(self, name, content):
        ext = os.path.splitext(name)[1]
        filename = str(uuid.uuid4()) + ext
        self.fs.put(content, filename=filename)

        return filename

    def delete(self, name):
        self.fs.delete(self.fs.find_one({"filename": name})["_id"])

    def exists(self, name):
        return self.fs.exists({"filename": name})

    def listdir(self, path):
        return [], self.fs.find({"filename": {"$regex": "^" + path}}).distinct(
            "filename"
        )

    def size(self, name):
        return self.fs.find_one({"filename": name}).length

    def url(self, name):
        return self.base_url + name

    def get_available_name(self, name, max_length=None):
        return name
