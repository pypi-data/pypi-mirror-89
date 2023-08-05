import posixpath
import shutil
from hub.store.cache import Cache
from hub.store.lru_cache import LRUCache

from hub.client.hub_control import HubControlClient
import configparser
from typing import MutableMapping, Tuple

import fsspec
import gcsfs
import zarr
from hub.store.azure_fs import AzureBlobFileSystem
import os
import re


def _connect(tag):
    """Connects to the backend and receives credentials"""

    creds = HubControlClient().get_config()
    dataset = HubControlClient().get_dataset_path(tag)

    # If dataset is in DB then return the path
    # Otherwise construct the path from the tag
    if dataset and "path" in dataset:
        path = dataset["path"]
    else:
        sub_tags = tag.split("/")
        # Get repository path from the cred location
        path = "/".join(creds["bucket"].split("/")[:-1])
        path = f"{path}/{sub_tags[0]}/{sub_tags[-1]}"
    return path, creds


def get_fs_and_path(url: str, token=None) -> Tuple[fsspec.AbstractFileSystem, str]:
    if url.startswith("s3://"):
        token = token or dict()
        token = read_aws_creds(token) if isinstance(token, str) else token
        return (
            fsspec.filesystem(
                "s3",
                key=token.get("aws_access_key_id"),
                secret=token.get("aws_secret_access_key"),
                token=token.get("aws_session_token"),
            ),
            url[5:],
        )
    elif url.startswith("gcs://"):
        return gcsfs.GCSFileSystem(token=token), url[6:]
    elif url.find("blob.core.windows.net/") != -1:
        account_name = url.split(".")[0]
        account_name = account_name[8:] if url.startswith("https://") else account_name
        return (
            AzureBlobFileSystem(
                account_name=account_name,
                account_key=token.get("account_key"),
            ),
            url[url.find("blob.core.windows.net/") + 22 :],
        )
    elif (
        url.startswith("../")
        or url.startswith("./")
        or url.startswith("/")
        or url.startswith("~/")
    ):
        return fsspec.filesystem("file"), url
    elif (
        # windows local file system
        re.search("^[A-Za-z]:", url)
    ):
        return fsspec.filesystem("file"), url
    else:
        # TOOD check if url is username/dataset:version
        url, creds = _connect(url)
        fs = fsspec.filesystem(
            "s3",
            key=creds["access_key"],
            secret=creds["secret_key"],
            token=creds["session_token"],
            client_kwargs={
                "endpoint_url": creds["endpoint"],
                "region_name": creds["region"],
            },
        )
        return (fs, url)


def read_aws_creds(filepath: str):
    parser = configparser.ConfigParser()
    parser.read(filepath)
    return {section: dict(parser.items(section)) for section in parser.sections()}


def _get_storage_map(fs, path):
    return StorageMapWrapperWithCommit(fs.get_mapper(path, check=False, create=False))


def get_cache_path(path, cache_folder="~/.activeloop/cache/"):
    if path.startswith("s3://") or path.startswith("gcs://"):
        path = "//".join(path.split("//")[1:])
    elif (
        path.startswith("../")
        or path.startswith("./")
        or path.startswith("/")
        or path.startswith("~/")
    ):
        path = "/".join(path.split("/")[1:])
    elif path.find("://") != -1:
        path = path.split("://")[-1]
    elif path.find(":\\") != -1:
        path = path.split(":\\")[-1]
    else:
        # path is username/dataset or username/dataset:version
        path = path.replace(":", "/")
    return os.path.expanduser(posixpath.join(cache_folder, path))


def get_storage_map(fs, path, memcache=2 ** 26, lock=True, storage_cache=2 ** 28):
    store = _get_storage_map(fs, path)
    cache_path = get_cache_path(path)
    if storage_cache and storage_cache > 0:
        os.makedirs(cache_path, exist_ok=True)
        store = LRUCache(
            zarr.LMDBStore(cache_path, buffers=True, lock=lock), store, storage_cache
        )
    if memcache and memcache > 0:
        store = LRUCache(zarr.MemoryStore(), store, memcache)
    return store


class StorageMapWrapperWithCommit(MutableMapping):
    def __init__(self, map):
        self._map = map
        self.root = self._map.root

    def __getitem__(self, slice_):
        return self._map[slice_]

    def __setitem__(self, slice_, value):
        self._map[slice_] = value

    def __delitem__(self, slice_):
        del self._map[slice_]

    def __len__(self):
        return len(self._map)

    def __iter__(self):
        yield from self._map

    def flush(self):
        pass

    def commit(self):
        """ Deprecated alias to flush()"""
        self.flush()

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()
