import requests
import logging
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from typing import Optional, Dict, Any, Union

from syncast.core.config import SyncCastRequestConfig
from syncast.exceptions.core import SyncCastDispatchError, SyncCastAPIError

logger = logging.getLogger(__name__)


class SyncCastDispatcher:
    """
    HTTP client for communicating with SyncCast APIs.
    Handles secret injection, retries, and structured error reporting.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 5,
        retries: Optional[int] = 3,
        backoff_factor: float = 0.3,
        logger_instance: Optional[logging.Logger] = None
    ):
        config = SyncCastRequestConfig()

        self.base_url = (base_url or config.base_url).rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout
        self.logger = logger_instance or logger
        self.session = requests.Session()

        retry_strategy = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Inject credentials from config
        if config.app_id and config.app_secret:
            self.with_secret(config.app_id, config.app_secret)

    def with_base_url(self, url: str) -> 'SyncCastDispatcher':
        self.base_url = url.rstrip("/")
        return self

    def with_headers(self, headers: Dict[str, str]) -> 'SyncCastDispatcher':
        self.headers.update(headers)
        return self

    def with_auth_token(self, token: str, header_name: str = "Authorization") -> 'SyncCastDispatcher':
        self.headers[header_name] = f"Bearer {token}"
        return self

    def with_secret(
        self,
        app_id: str,
        app_secret: str,
        id_header: str = "X-App-Id",
        secret_header: str = "X-App-Secret"
    ) -> 'SyncCastDispatcher':
        self.headers[id_header] = app_id
        self.headers[secret_header] = app_secret
        return self

    def _build_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _log_request(self, method: str, url: str, **kwargs):
        self.logger.debug(f"[SyncCastDispatcher] {method.upper()} {url} | kwargs={kwargs}")

    def _safe_request(self, method: str, *args, **kwargs) -> requests.Response:
        try:
            return getattr(self.session, method)(*args, timeout=self.timeout, **kwargs)
        except requests.exceptions.RequestException as e:
            self.logger.exception(f"[SyncCastDispatcher] {method.upper()} request failed")
            raise SyncCastDispatchError(
                message=f"{method.upper()} request failed",
                extra={"exception": str(e), "url": args[0] if args else None}
            ) from e

    def _handle_response(self, response: requests.Response) -> Union[Dict[str, Any], str]:
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"[SyncCastDispatcher] HTTP {e.response.status_code} - {e.response.text}")
            raise SyncCastAPIError(
                message=f"API responded with status {e.response.status_code}",
                extra={
                    "status_code": e.response.status_code,
                    "body": e.response.text,
                    "url": e.response.url
                }
            ) from e

        try:
            return response.json()
        except ValueError:
            return response.text
        except Exception as e:
            self.logger.exception("[SyncCastDispatcher] Failed to parse JSON response")
            raise SyncCastAPIError(
                message="Invalid JSON response",
                extra={"body": response.text, "url": response.url}
            ) from e

    # Public request methods

    def post(self, endpoint: str, **kwargs) -> Union[Dict[str, Any], str]:
        url = self._build_url(endpoint)
        self._log_request("post", url, **kwargs)
        response = self._safe_request("post", url, **kwargs)
        return self._handle_response(response)

    def get(self, endpoint: str, **kwargs) -> Union[Dict[str, Any], str]:
        url = self._build_url(endpoint)
        self._log_request("get", url, **kwargs)
        response = self._safe_request("get", url, **kwargs)
        return self._handle_response(response)

    def put(self, endpoint: str, **kwargs) -> Union[Dict[str, Any], str]:
        url = self._build_url(endpoint)
        self._log_request("put", url, **kwargs)
        response = self._safe_request("put", url, **kwargs)
        return self._handle_response(response)

    def delete(self, endpoint: str, **kwargs) -> Union[Dict[str, Any], str]:
        url = self._build_url(endpoint)
        self._log_request("delete", url, **kwargs)
        response = self._safe_request("delete", url, **kwargs)
        return self._handle_response(response)
