import threading
from io import BytesIO
from pathlib import PurePath
from types import TracebackType
from typing import Optional, Type
from unittest import TestCase
from unittest.mock import Mock

from pytest_httpserver import HTTPServer
from werkzeug import Response, Request

from core_get.catalog.network_service import NetworkService, NetworkError, NetworkTimeoutError, NetworkHTTPError
from core_get.options.common_options import CommonOptions


class TestBinaryStream(BytesIO):
    def __enter__(self) -> BytesIO:
        return self
    def __exit__(self, t: Optional[Type[BaseException]], value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> Optional[bool]:
        pass


class TestCatalogService(TestCase):
    httpserver = None

    @classmethod
    def setUpClass(cls):
        cls.httpserver = HTTPServer()
        cls.httpserver.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.httpserver.stop()

    def setUp(self) -> None:
        self.httpserver.clear()

    def test_get_returns_correct_data(self):
        network_service = NetworkService(Mock(), CommonOptions(), Mock())
        self.httpserver.expect_request('/get_path', 'get').respond_with_json({'a': 'b'})
        j = network_service.get(self.httpserver.url_for('/get_path'))
        self.assertEqual({'a': 'b'}, j)

    def test_get_sends_correct_headers(self):
        network_service = NetworkService(Mock(), CommonOptions(), Mock())
        self.httpserver.expect_request('/get_path', 'get', headers={'a': 'b'}).respond_with_json(None)
        network_service.get(self.httpserver.url_for('/get_path'), headers={'a': 'b'})

    def test_get_fails_due_to_offline_option(self):
        with self.assertRaises(RuntimeError):
            network_service = NetworkService(Mock(), CommonOptions(offline=True), Mock())
            network_service.get(self.httpserver.url_for('/get_path'))

    def test_get_fails_due_to_server_error(self):
        network_service = NetworkService(Mock(), CommonOptions(), Mock())
        self.httpserver.expect_request('/get_path', 'get').respond_with_data(status=500)
        with self.assertRaises(NetworkError):
            network_service.get(self.httpserver.url_for('/get_path'))

    def test_get_fails_due_to_timeout(self):
        network_service = NetworkService(Mock(), CommonOptions(network_timeout=0.01), Mock())
        timeout_flag = threading.Event()

        def handler(_: Request):
            timeout_flag.wait(5)
            return Response()

        self.httpserver.expect_request('/get_path', 'get').respond_with_handler(handler)
        with self.assertRaises(NetworkTimeoutError):
            network_service.get(self.httpserver.url_for('/get_path'))
        timeout_flag.set()

    def test_post_returns_correct_data(self):
        network_service = NetworkService(Mock(), CommonOptions(), Mock())
        self.httpserver.expect_request('/post_path', 'post') .respond_with_json({'a': 'b'})
        j = network_service.post(self.httpserver.url_for('/post_path'))
        self.assertEqual({'a': 'b'}, j)

    def test_post_sends_correct_headers(self):
        network_service = NetworkService(Mock(), CommonOptions(), Mock())
        self.httpserver.expect_request('/post_path', 'post', headers={'a': 'b'}).respond_with_json(None)
        network_service.post(self.httpserver.url_for('/post_path'), headers={'a': 'b'})

    def test_post_fails_due_to_offline_option(self):
        with self.assertRaises(RuntimeError):
            network_service = NetworkService(Mock(), CommonOptions(offline=True), Mock())
            network_service.post(self.httpserver.url_for('/post_path'))

    def test_post_sends_correct_file(self):
        file_system = Mock()
        file_system.open_read = Mock(return_value=BytesIO(b'1234'))
        network_service = NetworkService(Mock(), CommonOptions(), file_system)
        # We are unable to test for the correct data received at the moment
        self.httpserver.expect_request('/post_path', 'post').respond_with_json(None)
        network_service.post(self.httpserver.url_for('/post_path'), files={'hej.txt': PurePath('./hej.txt')})
        file_system.open_read.assert_called_once_with(PurePath('./hej.txt'))

    def test_post_fails_due_to_server_error(self):
        network_service = NetworkService(Mock(), CommonOptions(), Mock())
        self.httpserver.expect_request('/post_path', 'post').respond_with_data(status=500)
        with self.assertRaises(NetworkHTTPError):
            network_service.post(self.httpserver.url_for('/post_path'))

    def test_post_fails_due_to_timeout(self):
        network_service = NetworkService(Mock(), CommonOptions(network_timeout=0.01), Mock())
        timeout_flag = threading.Event()

        def handler(_: Request):
            timeout_flag.wait(5)
            return Response()

        self.httpserver.expect_request('/post_path', 'post').respond_with_handler(handler)
        with self.assertRaises(NetworkTimeoutError):
            network_service.post(self.httpserver.url_for('/post_path'))
        timeout_flag.set()

    def test_delete_returns_correct_data(self):
        network_service = NetworkService(Mock(), CommonOptions(), Mock())
        self.httpserver.expect_request('/delete_path', 'delete').respond_with_json({'a': 'b'})
        j = network_service.delete(self.httpserver.url_for('/delete_path'))
        self.assertEqual({'a': 'b'}, j)

    def test_delete_sends_correct_headers(self):
        network_service = NetworkService(Mock(), CommonOptions(), Mock())
        self.httpserver.expect_request('/delete_path', 'delete', headers={'a': 'b'}).respond_with_json(None)
        network_service.delete(self.httpserver.url_for('/delete_path'), headers={'a': 'b'})

    def test_delete_fails_due_to_offline_option(self):
        with self.assertRaises(RuntimeError):
            network_service = NetworkService(Mock(), CommonOptions(offline=True), Mock())
            network_service.delete(self.httpserver.url_for('/delete_path'))

    def test_delete_fails_due_to_server_error(self):
        network_service = NetworkService(Mock(), CommonOptions(), Mock())
        self.httpserver.expect_request('/delete_path', 'delete').respond_with_data(status=500)
        with self.assertRaises(NetworkError):
            network_service.delete(self.httpserver.url_for('/delete_path'))

    def test_delete_fails_due_to_timeout(self):
        network_service = NetworkService(Mock(), CommonOptions(network_timeout=0.01), Mock())
        timeout_flag = threading.Event()

        def handler(_: Request):
            timeout_flag.wait(5)
            return Response()

        self.httpserver.expect_request('/delete_path', 'delete').respond_with_handler(handler)
        with self.assertRaises(NetworkTimeoutError):
            network_service.delete(self.httpserver.url_for('/delete_path'))
        timeout_flag.set()

    def test_download_file_writes_correct_file(self):
        file_stream = TestBinaryStream()
        file_system = Mock()
        file_system.open_write = Mock(return_value=file_stream)
        network_service = NetworkService(Mock(), CommonOptions(), file_system)
        self.httpserver.expect_request('/hej.bin', 'get').respond_with_data(b'\x001234')
        network_service.download_file(self.httpserver.url_for('/hej.bin'), PurePath('./hej.bin'))
        self.assertEqual(b'\x001234', file_stream.getvalue())
        file_system.open_write.assert_called_once_with(PurePath('./hej.bin'))

    def test_download_file_sends_correct_headers(self):
        file_stream = TestBinaryStream()
        file_system = Mock()
        file_system.open_write = Mock(return_value=file_stream)
        network_service = NetworkService(Mock(), CommonOptions(), file_system)
        self.httpserver.expect_request('/download_file_path', 'get', headers={'a': 'b'}).respond_with_data(b'\x001234')
        network_service.download_file(self.httpserver.url_for('/download_file_path'), PurePath('./hej.bin'),
                                      headers={'a': 'b'})

    def test_download_file_fails_due_to_offline_option(self):
        with self.assertRaises(RuntimeError):
            network_service = NetworkService(Mock(), CommonOptions(offline=True), Mock())
            network_service.download_file(self.httpserver.url_for('/download_file_path'), PurePath('./hej.bin'))

    def test_download_file_fails_due_to_server_error(self):
        file_stream = TestBinaryStream()
        file_system = Mock()
        file_system.open_write = Mock(return_value=file_stream)
        network_service = NetworkService(Mock(), CommonOptions(), file_system)
        self.httpserver.expect_request('/download_file_path', 'download_file').respond_with_data(status=500)
        with self.assertRaises(NetworkError):
            network_service.download_file(self.httpserver.url_for('/download_file_path'), PurePath('./hej.bin'))

    def test_download_file_fails_due_to_timeout(self):
        file_stream = TestBinaryStream()
        file_system = Mock()
        file_system.open_write = Mock(return_value=file_stream)
        network_service = NetworkService(Mock(), CommonOptions(network_timeout=0.01), file_system)
        timeout_flag = threading.Event()

        def handler(_: Request):
            timeout_flag.wait(5)
            return Response()

        self.httpserver.expect_request('/download_file_path', 'get').respond_with_handler(handler)
        with self.assertRaises(NetworkTimeoutError):
            network_service.download_file(self.httpserver.url_for('/download_file_path'), PurePath('./hej.bin'))
        timeout_flag.set()
