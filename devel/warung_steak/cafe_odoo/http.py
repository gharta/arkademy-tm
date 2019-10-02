# -*- coding: utf-8 -*-
__metaclass__ = type

import json
import logging
import odoo
from odoo import exceptions
from odoo.http import HttpRequest, JsonRequest, WebRequest, Response, Root
from odoo.http import SessionExpiredException, AuthenticationError, serialize_exception
import werkzeug

class DetailException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message



class ApiRequest(JsonRequest, WebRequest):
    """ Handler for the ``http`` request type.

    matched routing parameters, query string parameters, form_ parameters
    and files are passed to the handler method as keyword arguments.

    In case of name conflict, routing parameters have priority.

    The handler method's result can be:

    * a falsy value, in which case the HTTP response will be an
      `HTTP 204`_ (No Content)
    * a werkzeug Response object, which is returned as-is
    * a ``str`` or ``unicode``, will be wrapped in a Response object and
      interpreted as HTML

    .. _form: http://www.w3.org/TR/html401/interact/forms.html#h-17.13.4.2
    .. _HTTP 204: http://tools.ietf.org/html/rfc7231#section-6.3.5
    """
    _request_type = "json"

    def __init__(self, *args):
        super(JsonRequest, self).__init__(*args)
        self.jsonp_handler = None
        self.params = {}
        args = self.httprequest.args
        jsonp = args.get('jsonp')
        self.jsonp = jsonp
        request = None
        request_id = args.get('id')

        request = self.httprequest.stream.read().decode('utf8')

        # Read POST content or POST Form Data named "request"
        if self.httprequest.method in ["POST", "PUT"]:
            try:
                self.jsonrequest = json.loads(request)
            except json.JSONDecodeError:
                msg = 'Invalid JSON data: %r' % (request,)
                # _logger.error('%s: %s', self.httprequest.path, msg)
                raise werkzeug.exceptions.BadRequest(msg)

            # self.params = dict(self.jsonrequest.get("params", {}))
            # self.context = self.params.pop('context', dict(self.session.context))


    def _json_response(self, result=None, error=None):
        #Harus ditambahkan, karena secara default baik Odoo 8 dan Odoo 10, tidak memiliki error parameter pada JSON Endpoint
        #---------------------Begin of New Part----------------------------#
        status=200
        def process_result(result):
            status=200
            new_error = result.get('error')
            if new_error:
                error_code = new_error.get('code')
                if error_code:
                    status = error_code
            new_result = result.get('data')
            new_count = result.get('count')
            new_status = result.get('code', status)
            new_meta = result.get('meta')
            return new_result, new_count, new_error, new_status, new_meta

        #---------------------End of New Part----------------------------#

        response = {
            'meta': '1.5.0', #APIVERSION
        }
        if error is not None:
            response['error'] = error
            status = error.get('code')
        if result is not None:
            result, count, error, status, meta = process_result(result)
            if not result is None:
                response['data'] = result
            if not count is None:
                response['count'] = count
            if error :
                response['error'] = error
            if meta :
                response['meta'] = meta
            if status :
                response['code'] = status
                status_string = {
                    200 : 'success',
                    201 : 'created',
                    401 : 'unauthorized',
                    400 : 'bad request',
                    403 : 'forbidden',
                    404 : 'not found',
                    500 : 'error'
                }
                response['message'] = status_string[status]

        mime = 'application/json'
        body = json.dumps(response)

        #Harus ditambahkan, karena secara default baik Odoo 8 dan Odoo 10, tidak memiliki STATUS CODE pada JSON Endpoint
        #---------------------Begin of New Part----------------------------#
        return Response(
                    response=body,
                    status=status,
                    headers=[
                        ('Access-Control-Allow-Origin', "*"),
                        ('Access-Control-Allow-Methods', "*"),
                        ('Access-Control-Allow-Headers', "Origin, X-Requested-With, Content-Type, Accept, Authorization"),
                        ('Content-Type', mime),
                        ('Content-Length', len(body))])
        #---------------------End of New Part----------------------------#


def get_request_new(self, httprequest):
    if '/api/' in httprequest.url and httprequest.mimetype in ("application/json", "application/json-rpc"):
        return ApiRequest(httprequest)
    elif httprequest.args.get('jsonp'):
        return JsonRequest(httprequest)
    elif httprequest.mimetype in ("application/json", "application/json-rpc"):
        return JsonRequest(httprequest)
    else:
        return HttpRequest(httprequest)

Root.get_request = get_request_new
