import json
from contextlib import ExitStack
from dataclasses import dataclass
from pathlib import PurePath
from typing import Dict, Any

import requests
from injector import inject
from requests import HTTPError, ReadTimeout

from core_get.catalog.download_status_interface import DownloadStatusInterface
from core_get.file.file_system import FileSystem
from core_get.options.common_options import CommonOptions


class NetworkError(Exception):
    pass


class NetworkHTTPError(NetworkError):
    def __init__(self, status_code, *args: object) -> None:
        super().__init__(*args)
        self.status_code = status_code


class NetworkTimeoutError(NetworkError):
    pass


@inject
@dataclass
class NetworkService:
    download_status_interface: DownloadStatusInterface
    common_options: CommonOptions
    file_system: FileSystem

    def get(self, url: str, params: Dict[str, str] = None, headers: Dict[str, str] = None) -> Any:
        self._check_offline()
        with self._request('get', url, params=params, headers=headers) as response:
            return json.loads(response.content)

    def post(self, url: str, files: Dict[str, PurePath] = None, headers: Dict[str, str] = None) -> Any:
        self._check_offline()
        if self.common_options.dry_run:
            raise RuntimeError("POST with --dry-run flag")
        with ExitStack() as stack:
            file_streams = {key: stack.enter_context(self.file_system.open_read(file_name))
                            for key, file_name in files.items()} \
                if files is not None else None
            with self._request('post', url, files=file_streams, headers=headers) as response:
                return json.loads(response.content)

    def delete(self, url: str, headers: Dict[str, str] = None) -> Any:
        self._check_offline()
        if self.common_options.dry_run:
            raise RuntimeError("DELETE with --dry-run flag")
        with self._request('delete', url, headers=headers) as response:
            return json.loads(response.content)

    def download_file(self, url: str, destination_path: PurePath, headers: Dict[str, str] = None) -> None:
        self._check_offline()
        if self.common_options.dry_run:
            raise RuntimeError("Download file with --dry-run flag")
        with self.file_system.open_write(destination_path) as destination_stream:
            with self._request('get', url, headers=headers, stream=True) as response:
                try:
                    total_length = int(response.headers.get('Content-Length', '0'))
                except ValueError:
                    total_length = 0
                self.download_status_interface.download_begin(destination_path.name)
                count = 0
                for chunk in response.iter_content(chunk_size=8192):
                    destination_stream.write(chunk)
                    count += len(chunk)
                    self.download_status_interface.download_progress(min(total_length, count), count)
                self.download_status_interface.download_done()

    def _request(self, method: str, url: str, **kwargs):
        try:
            response = requests.request(method, url, timeout=self.common_options.network_timeout, **kwargs)
        except ReadTimeout:
            raise NetworkTimeoutError
        try:
            response.raise_for_status()
        except HTTPError:
            response.close()
            raise NetworkHTTPError(response.status_code)
        return response

    def _check_offline(self):
        if self.common_options.offline:
            raise RuntimeError("Network accessed with --offline flag")
