import io
import itertools
import os
import shutil
from dataclasses import dataclass
from pathlib import PurePath, Path
from typing import IO, List, Callable, Tuple, Any

from injector import inject

from core_get.file.hash import Hash, HashDigest
from core_get.options.common_options import CommonOptions


# Taken from shutil
COPY_BUFSIZE = 1024 * 1024 if os.name == 'nt' else 64 * 1024


class DryRunFile(io.BytesIO):
    def __init__(self, file_name: PurePath):
        super().__init__()
        self._file_name = file_name

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        prev_pos = self.tell()
        self.seek(0, io.SEEK_END)
        length = self.tell()
        self.seek(prev_pos, io.SEEK_SET)
        print(f'Write {length} bytes to {self._file_name}')


@inject
@dataclass
class FileSystem:
    common_options: CommonOptions

    def open_read(self, file_path: PurePath) -> IO[bytes]:
        return open(file_path, 'rb')

    def open_write(self, file_path: PurePath) -> IO[bytes]:
        if self.common_options.dry_run:
            return DryRunFile(file_path)

        return open(file_path, 'wb')

    def read_file(self, file_path: PurePath) -> bytes:
        with self.open_read(file_path) as file:
            return file.read()

    def write_file(self, file_path: PurePath, contents: bytes) -> HashDigest:
        return self.write_stream(file_path, io.BytesIO(contents))

    def write_stream(self, file_path: PurePath, source_stream: IO[bytes]) -> HashDigest:
        read = source_stream.read

        if self.common_options.dry_run:
            h, size = self.transfer_and_hash(read, lambda b: None)
            print(f'Write {size} bytes to {file_path.as_posix()}')
            return h

        destination_path = Path(file_path)
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        with self.open_write(destination_path) as destination_stream:
            h, _ = self.transfer_and_hash(read, destination_stream.write)
            return h

    def transfer_and_hash(self, read: Callable[[int], bytes], write: Callable[[bytes], Any])\
            -> Tuple[HashDigest, int]:
        h = Hash()
        size = 0
        # Adapted from shutil.copyfileobj
        while True:
            buf = read(COPY_BUFSIZE)
            if not buf:
                break
            size += len(buf)
            h.update(buf)
            write(buf)
        return h.digest(), size

    def delete_file(self, file_path: PurePath):
        if self.common_options.dry_run:
            print(f'Deleted file {file_path.as_posix()}')
            return

        Path(file_path).unlink(missing_ok=True)

    def get_hierarchy(self, path: PurePath) -> List[PurePath]:
        return list(itertools.chain([path], path.parents))

    def glob(self, path: PurePath, pattern: str) -> List[PurePath]:
        return [path for path in Path(path).glob(pattern) if path.is_file()]

    def get_file_name(self, path: PurePath) -> str:
        return Path(path).absolute().name

    def make_directory(self, path: PurePath) -> None:
        if self.common_options.dry_run:
            print(f'Created directory {path.as_posix()}')
            return

        Path(path).mkdir(parents=True, exist_ok=True)

    def remove_directory(self, path: PurePath) -> None:
        if self.common_options.dry_run:
            print(f'Removed directory {path.as_posix()}')
            return

        try:
            shutil.rmtree(str(Path(path).absolute()))
        except FileNotFoundError:
            pass
