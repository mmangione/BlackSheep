from typing import Any, Callable, Dict, Generator, List, Optional, Union

from guardpost.authentication import Identity

from .asgi import ASGIScopeInterface
from .contents import Content, FormPart
from .cookies import Cookie
from .headers import Headers, HeaderType
from .plugins import json as json_plugin
from .sessions import Session
from .url import URL

class Message:
    @property
    def headers(self) -> Headers: ...
    def content_type(self) -> bytes: ...
    def get_first_header(self, key: bytes) -> bytes: ...
    def get_headers(self, key: bytes) -> List[bytes]: ...
    def get_single_header(self, key: bytes) -> bytes: ...
    def remove_header(self, key: bytes) -> None: ...
    def has_header(self, key: bytes) -> bool: ...
    def add_header(self, name: bytes, value: bytes) -> None: ...
    def set_header(self, key: bytes, value: bytes) -> None: ...
    async def read(self) -> Optional[bytes]: ...
    async def stream(self) -> Generator[bytes, None, None]: ...
    async def text(self) -> str: ...
    async def form(self) -> Union[Dict[str, str], Dict[str, List[str]], None]:
        """
        Returns values read either from multipart or www-form-urlencoded
        payload.

        This function adopts some compromises to provide a consistent api,
        returning a dictionary of key: values pairs.
        If a key is unique, the value is a single string; if a key is
        duplicated (licit in both form types), the value is a list of strings.

        Multipart form parts values that can be decoded as UTF8 are decoded,
        otherwise kept as raw bytes.
        In case of ambiguity, use the dedicated `multiparts()` method.
        """
    async def multipart(self) -> List[FormPart]:
        """
        Returns parts read from multipart/form-data, if present, otherwise
        None
        """
    def declares_content_type(self, type: bytes) -> bool: ...
    def declares_json(self) -> bool: ...
    def declares_xml(self) -> bool: ...
    async def files(self, name: Optional[str] = None) -> List[FormPart]: ...
    async def json(self, loads: Callable[[str], Any] = json_plugin.loads) -> Any: ...
    def has_body(self) -> bool: ...
    @property
    def charset(self) -> str: ...

Cookies = Dict[str, Cookie]

def method_without_body(method: str) -> bool: ...

class Request(Message):
    def __init__(
        self, method: str, url: bytes, headers: Optional[List[HeaderType]]
    ) -> None:
        self.method: str = ...
        self._url: URL = ...
        self.route_values: Optional[Dict[str, str]] = ...
        self.content: Optional[Content] = ...
        self.identity: Optional[Identity] = ...
        self.scope: ASGIScopeInterface = ...
        self._session: Optional[Session]
    @classmethod
    def incoming(
        cls, method: str, path: bytes, query: bytes, headers: List[HeaderType]
    ) -> "Request": ...
    @property
    def query(self) -> Dict[str, List[str]]: ...
    @property
    def url(self) -> URL: ...
    @url.setter
    def url(self, value: Union[URL, bytes, str]) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def session(self) -> Session: ...
    @session.setter
    def session(self, value: Session) -> None: ...
    @property
    def cookies(self) -> Dict[str, str]: ...
    def get_cookie(self, name: str) -> Optional[str]: ...
    def set_cookie(self, name: str, value: str) -> None: ...
    @property
    def etag(self) -> Optional[bytes]: ...
    @property
    def if_none_match(self) -> Optional[bytes]: ...
    def expect_100_continue(self) -> bool: ...
    def with_content(self, content: Content) -> "Request": ...
    @property
    def session(self) -> Session: ...
    @session.setter
    def session(self, value: Session) -> None: ...
    @property
    def base_path(self) -> str: ...
    @base_path.setter
    def base_path(self, value: str) -> None: ...
    @property
    def scheme(self) -> str: ...
    @scheme.setter
    def scheme(self, value: str) -> None: ...
    @property
    def host(self) -> str: ...
    @host.setter
    def host(self, value: str) -> None: ...
    @property
    def client_ip(self) -> str: ...
    @property
    def original_client_ip(self) -> str: ...
    @original_client_ip.setter
    def original_client_ip(self, value: str) -> None: ...
    @property
    def path(self) -> str: ...

class Response(Message):
    def __init__(
        self,
        status: int,
        headers: Optional[List[HeaderType]] = None,
        content: Optional[Content] = None,
    ) -> None:
        self.__headers = headers or []
        self.status = status
        self.content = content
    def __repr__(self) -> str: ...
    @property
    def cookies(self) -> Cookies: ...
    @property
    def reason(self) -> str: ...
    def get_cookies(self) -> Cookies: ...
    def get_cookie(self, name: str) -> Optional[Cookie]: ...
    def set_cookie(self, cookie: Cookie) -> None: ...
    def set_cookies(self, cookies: List[Cookie]) -> None: ...
    def unset_cookie(self, name: str) -> None: ...
    def remove_cookie(self, name: str) -> None: ...
    def is_redirect(self) -> bool: ...
    def with_content(self, content: Content) -> "Response": ...

def is_cors_request(request: Request) -> bool: ...
def is_cors_preflight_request(request: Request) -> bool: ...
def get_request_absolute_url(request: Request) -> URL: ...
def get_absolute_url_to_path(request: Request, path: str) -> URL: ...
