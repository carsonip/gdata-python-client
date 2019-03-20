"""
Compatibility layer to use requests instead of httplib
This allows us to have goodies like persistent connections and connection pools
"""
from __future__ import absolute_import, division, print_function
from requests import Request, Session

s = Session()


# http_core.HttpClient
class RequestsHttpClient(object):
    def request(self, http_request):
        for p in http_request._body_parts:
            assert isinstance(p, bytes)
        req = Request(http_request.method, str(http_request.uri),
                      data=''.join(http_request._body_parts), headers=http_request.headers)
        prepped = req.prepare()  # We don't like cookies, use prepare() instead of prepare_request()
        prepped.headers['Accept-Encoding'] = 'identity,gzip'  # Accept gzip, good for XML
        resp = s.send(prepped, allow_redirects=False)
        return RequestsHttpResponse(resp)


# httplib.HTTPResponse
class RequestsHttpResponse(object):
    def __init__(self, resp):
        self.resp = resp

    def read(self):
        return self.resp.content

    @property
    def status(self):
        return self.resp.status_code

    def getheader(self, value):
        return self.resp.headers.get(value)

    def getheaders(self):
        return self.resp.headers

    @property
    def reason(self):
        return self.resp.reason
