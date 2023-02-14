import glob
import re
from os import makedirs, path

from google.cloud import storage

client = storage.Client()


def download_from_bucket(uri: str, destination: str, recursive: bool = False):
    print("Downloading from bucket {} to {}. Recursive: {}".format(
        uri, destination, recursive))
    matches = re.match("gs://(.*?)/(.*)", uri)

    if matches:
        bucket_name, object_name = matches.groups()
    else:
        raise RuntimeError("Invalid bucket URI: {}".format(uri))
    
    blobs = client.list_blobs(bucket_name, prefix=object_name)

    if not object_name.endswith("/"):
        object_name = object_name + "/"

    for file in blobs:
        file_name: str = file.name.replace(object_name, "")
        if len(file_name) == 0:
            continue
        if not recursive and file_name.find("/") > -1:
            continue
        file_name = "/".join([destination, file_name])
        makedirs(path.dirname(file_name), exist_ok=True)
        file.download_to_filename(file_name)
        print("Downloaded {}".format(file.name))



def upload_to_bucket(folder: str, uri: str):
    print("Uploading folder {} to bucket {}".format(folder, uri))
    matches = re.match("gs://(.*?)/(.*)", uri)

    if matches:
        bucket_name, object_name = matches.groups()
    else:
        raise RuntimeError("Invalid bucket URI: {}".format(uri))

    bucket = client.bucket(bucket_name)
    _upload_local_directory_to_gcs(folder, bucket, object_name)


def _upload_local_directory_to_gcs(local_path, bucket, gcs_path):
    assert path.isdir(local_path)
    for local_file in glob.glob(local_path + '/**'):
        if not path.isfile(local_file):
            _upload_local_directory_to_gcs(
                local_file, bucket, gcs_path + "/" + path.basename(local_file))
        else:
            remote_path = path.join(
                gcs_path, local_file[1 + len(local_path):])
            blob = bucket.blob(remote_path)
            blob.upload_from_filename(local_file)
            print("Uploaded {}".format(blob.name))
