from google.cloud.storage import Bucket
import typing as t
from google.cloud import storage
import os

from ml_idm.core.reader.path_providers.path_provider import PathProvider
from ml_idm.core.utils.common_utils import get_filename

GS_PATH_PREFIX = "gs://"


class GsPathProvider(PathProvider):
    def get_local_path(self, initial_path: str, local_dir: str) -> str:
        bucket, blob_name = self.gs_bucket_and_rel_path(path=initial_path)
        blob = bucket.get_blob(blob_name)
        filename = get_filename(path=initial_path)
        result = os.path.join(local_dir, filename)
        blob.download_to_filename(result)
        return result

    @staticmethod
    def gs_bucket_and_rel_path(path: str) -> t.Tuple[Bucket, str]:
        client = storage.Client()
        if path.startswith(GS_PATH_PREFIX):
            path = path.replace(GS_PATH_PREFIX, "")

        split_path = path.split("/")
        bucket_name = split_path[0]
        blob_name = "/".join(split_path[1:])

        bucket = client.get_bucket(bucket_name)

        return bucket, blob_name

    @staticmethod
    def iterate_blobs(path: str, only_in_bucket: bool):
        bucket, gs_rel_path = GsPathProvider.gs_bucket_and_rel_path(path=path)

        blobs = bucket.list_blobs(prefix=None if only_in_bucket else gs_rel_path)
        for blob in blobs:
            yield blob
