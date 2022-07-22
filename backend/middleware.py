from base64 import b64encode
from collections import OrderedDict
from hashlib import sha256
from hmac import HMAC
from urllib.parse import urlencode

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, \
    RequestResponseEndpoint
from starlette.responses import Response, JSONResponse
from starlette.types import ASGIApp


class VKValidationMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: ASGIApp, client_secret: str,  api_doc_prefix: str, debug: bool = True):
        super().__init__(app)
        self.app = app
        self.client_secret = client_secret
        self.debug = debug
        self.api_doc_prefix = api_doc_prefix

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        is_doc = request.url.path.split('/')[1] == self.api_doc_prefix
        if is_doc or self.debug or self.is_valid(request=request):
            return await call_next(request)
        return JSONResponse(status_code=403, content={'reason': 'Unauthorized!'})

    def is_valid(self, request: Request) -> bool:
        vk_subset = OrderedDict(sorted(x for x in request.items()
                                       if x[0][:3] == 'vk_'))
        hash_code = b64encode(HMAC(
            key=self.client_secret.encode(),
            msg=urlencode(vk_subset, doseq=True).encode(),
            digestmod=sha256
        ).digest())
        decoded_hash_code = hash_code.decode('utf-8')[:-1] \
            .replace('+', '-') \
            .replace('/', '_')
        return request.get('sign') == decoded_hash_code
