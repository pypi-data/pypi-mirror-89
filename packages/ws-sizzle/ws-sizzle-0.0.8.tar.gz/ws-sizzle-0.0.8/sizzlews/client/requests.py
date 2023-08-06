#    sizzlews
#    Copyright (C) 2020 Dmitry Berezovsky
#    The MIT License (MIT)
#    
#    Permission is hereby granted, free of charge, to any person obtaining
#    a copy of this software and associated documentation files
#    (the "Software"), to deal in the Software without restriction,
#    including without limitation the rights to use, copy, modify, merge,
#    publish, distribute, sublicense, and/or sell copies of the Software,
#    and to permit persons to whom the Software is furnished to do so,
#    subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be
#    included in all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import requests

from sizzlews.client.common import SizzleWsClient, JsonRpcRequest, InvocationResultType


class SizzleWsHttpClient(SizzleWsClient):
    def __init__(self, endpoint: str = None) -> None:
        super().__init__()
        self.endpoint = endpoint

    def _invoke_request(self, rq: JsonRpcRequest, expected_response_type: InvocationResultType = None):
        if self.endpoint is None:
            raise ValueError("Endpoint must be configured before any invocation")
        return self._parse_rpc_response(requests.post(self.endpoint, json=rq.to_dict()).json(), expected_response_type)

    async def _async_invoke_request(self, rq: JsonRpcRequest, expected_response_type: InvocationResultType = None):
        raise NotImplementedError()
