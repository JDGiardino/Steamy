import logging
from typing import Optional

import requests
from requests.adapters import HTTPAdapter, Response
from urllib3 import Retry
from dataclasses import dataclass, field

DEFAULT_HTTP_METHODS: tuple[str, ...] = (
    "POST",
    "HEAD",
    "GET",
    "PUT",
    "DELETE",
    "OPTIONS",
    "TRACE",
)

DEFAULT_HTTP_RETRY_CODES: tuple[int, ...] = (
    429,  # too many requests
    500,  # internal server err
    502,  # bad gateway
    503,  # unavailable
    504,  # gateway timeout
    507,  # insufficient storage
    509,  # bandwidth limit exceeded
    511,  # network auth
)


def make_retry_strategy(
    backoff_factor: Optional[int] = None,
    total: Optional[int] = None,
    retry_codes: Optional[list[int]] = None,
    methods: Optional[list[int]] = None,
) -> Retry:
    if not total:
        total = 3
    if not backoff_factor:
        backoff_factor = 3
    if not retry_codes:
        retry_codes = list(DEFAULT_HTTP_RETRY_CODES)
    if not methods:
        methods = list(DEFAULT_HTTP_METHODS)

    return Retry(
        backoff_factor=backoff_factor,
        total=total,
        status_forcelist=list(retry_codes),
        allowed_methods=methods,
    )


@dataclass
class RequestsRetryClient:

    retry_strategy: Retry = field(default_factory=make_retry_strategy)

    def request(
        self, method: str, url: str, headers: Optional[dict[str, str]] = None, json: Optional[dict] = None
    ) -> Response:
        logging.info(f"Retry request: method: {method} | url: {url} | retry: {self.retry_strategy} | json: {json}")
        adapter = HTTPAdapter(max_retries=self.retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        return http.request(method, url, headers=headers, json=json)