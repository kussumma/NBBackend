import pytest
from django.core.files.base import ContentFile
from gridfs.errors import NoFile
from tools.filestorage_helper import GridFSStorage


@pytest.fixture
def gridfs_storage():
    return GridFSStorage(collection="test_collection")


def test_save_and_open_file(gridfs_storage):
    # Save a file
    file_content = b"Hello, world!"
    file = ContentFile(file_content)
    file_name = "test_file.txt"
    saved_file_name = gridfs_storage.save(file_name, file)

    # Open the saved file
    opened_file = gridfs_storage.open(saved_file_name, "rb")
    opened_file_content = opened_file.read()

    # Check that the opened file has the same content as the saved file
    assert opened_file_content == file_content


def test_delete_file(gridfs_storage):
    # Save a file
    file_content = b"Hello, world!"
    file = ContentFile(file_content)
    file_name = "test_file.txt"
    saved_file_name = gridfs_storage.save(file_name, file)

    # Delete the saved file
    gridfs_storage.delete(saved_file_name)

    # Check that the file no longer exists
    with pytest.raises(NoFile):
        gridfs_storage.fs.get_last_version(saved_file_name)


def test_exists(gridfs_storage):
    # Save a file
    file_content = b"Hello, world!"
    file = ContentFile(file_content)
    file_name = "test_file.txt"
    saved_file_name = gridfs_storage.save(file_name, file)

    # Check that the saved file exists
    assert gridfs_storage.exists(saved_file_name)

    # Check that a non-existent file does not exist
    assert not gridfs_storage.exists("non_existent_file.txt")


def test_listdir(gridfs_storage):
    # Save some files
    file_content = b"Hello, world!"
    file1 = ContentFile(file_content)
    file2 = ContentFile(file_content)
    file1_name = "test_file1.txt"
    file2_name = "test_file2.txt"
    saved_file1_name = gridfs_storage.save(file1_name, file1)
    saved_file2_name = gridfs_storage.save(file2_name, file2)

    # Get the list of files
    _, filenames = gridfs_storage.listdir("")

    # Check that the saved files are in the list of files
    assert saved_file1_name in filenames
    assert saved_file2_name in filenames


def test_size(gridfs_storage):
    # Save a file
    file_content = b"Hello, world!"
    file = ContentFile(file_content)
    file_name = "test_file.txt"
    saved_file_name = gridfs_storage.save(file_name, file)

    # Check that the saved file has the correct size
    assert gridfs_storage.size(saved_file_name) == len(file_content)


def test_url(gridfs_storage):
    # Save a file
    file_content = b"Hello, world!"
    file = ContentFile(file_content)
    file_name = "test_file.txt"
    saved_file_name = gridfs_storage.save(file_name, file)

    # Check that the saved file has the correct URL
    assert (
        gridfs_storage.url(saved_file_name)
        == "/media/test_collection/" + saved_file_name
    )


def test_get_available_name(gridfs_storage):
    # Check that get_available_name always returns the same name
    assert gridfs_storage.get_available_name("test_file.txt") == "test_file.txt"
