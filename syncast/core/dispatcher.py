# syncast/core/dispatcher.py

import requests
import logging
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from typing import Optional, Dict, Any, Union

from syncast.core.config import SyncCastRequestConfig

logger = logging.getLogger(__name__)


class SyncCastDispatcher:
    """
    SyncCastDispatcher is an HTTP client for SyncCast APIs with retry, logging, and credential support.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 5,
        retries: Optional[int] = None,
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
            total=retries if retries is not None else config.max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

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
        self.logger.debug(f"{method.upper()} Request to {url} with: {kwargs}")

    def _handle_response(self, response: requests.Response) -> Union[Dict[str, Any], str]:
        try:
            response.raise_for_status()
            try:
                return response.json()
            except ValueError:
                return response.text
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            raise

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Union[Dict[str, Any], str]:
        url = self._build_url(endpoint)
        self._log_request("post", url, data=data, json=json, files=files)
        response = self.session.post(
            url,
            data=data,
            json=json,
            files=files,
            headers={**self.headers, **(headers or {})},
            timeout=self.timeout
        )
        return self._handle_response(response)

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Union[Dict[str, Any], str]:
        url = self._build_url(endpoint)
        self._log_request("get", url, params=params)
        response = self.session.get(
            url,
            params=params,
            headers={**self.headers, **(headers or {})},
            timeout=self.timeout
        )
        return self._handle_response(response)

    def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Union[Dict[str, Any], str]:
        url = self._build_url(endpoint)
        self._log_request("put", url, data=data, json=json)
        response = self.session.put(
            url,
            data=data,
            json=json,
            headers={**self.headers, **(headers or {})},
            timeout=self.timeout
        )
        return self._handle_response(response)

    def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None
    ) -> Union[Dict[str, Any], str]:
        url = self._build_url(endpoint)
        self._log_request("delete", url)
        response = self.session.delete(
            url,
            headers={**self.headers, **(headers or {})},
            timeout=self.timeout
        )
        return self._handle_response(response)
