from django.core.files.storage import Storage
from django.conf import settings
from gridfs import GridFS
from django.utils.deconstruct import deconstructible
import os
import uuid


@deconstructible
class GridFSStorage(Storage):
    """
    GridFSStorage is a Django storage backend that uses MongoDB's GridFS
    for storing files. It is based on the Storage class from Django
    https://docs.djangoproject.com/en/4.2/ref/files/storage/#django.core.files.storage.Storage
    """

    def __init__(self, location=None, base_url=None, collection=None):
        self.db = settings.MONGODB_DATABASE
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
