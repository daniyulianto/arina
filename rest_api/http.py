from odoo.http import HttpRequest, JsonRequest, WebRequest, Response, Root
from odoo.http import SessionExpiredException, AuthenticationError, serialize_exception
from odoo.http import request
from odoo import fields, registry
import json
import odoo
import werkzeug
from .lib import simplejson
import logging
import datetime
import base64
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT,\
    DEFAULT_SERVER_DATE_FORMAT

_logger = logging.getLogger(__name__)


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
        self.request_time = fields.Datetime.now()

        request = self.httprequest.stream.read()

        # Read POST content or POST Form Data named "request"
        if self.httprequest.method in ["POST", "PUT"]:
            try:
                self.jsonrequest = simplejson.loads(request)
            except simplejson.JSONDecodeError:
                msg = 'Invalid JSON data: %r' % (request,)
                _logger.error('%s: %s', self.httprequest.path, msg)
                raise werkzeug.exceptions.BadRequest(msg)

            # self.params = dict(self.jsonrequest.get("params", {}))
            # self.context = self.params.pop('context', dict(self.session.context))

    def _date_converter(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        if isinstance(o, datetime.date):
            return o.strftime(DEFAULT_SERVER_DATE_FORMAT)

    def _json_response(self, result=None, error=None):
        # ---------------------Begin of New Part---------------------------- #
        status = 200

        def process_result(result):
            status = 200
            new_error = result.get('error')
            if new_error:
                error_code = new_error.get('code')
                if error_code:
                    status = error_code
            new_result = result.get('result')
            new_count = result.get('count')
            new_status = result.get('code', status)
            return new_result, new_count, new_error, new_status

        # ---------------------End of New Part---------------------------- #
        response = {
            'version': '1.0',
        }
        if error is not None:
            response['error'] = error
            status = error.get('code')
        if result is not None:
            result, count, error, status = process_result(result)
            if result is not None:
                response['result'] = result
            if count is not None:
                response['count'] = count
            if error:
                response['error'] = error

        mime = 'application/json'
        body = json.dumps(response, default=self._date_converter)

        # ---------------------Begin of New Part---------------------------- #
        return Response(
            response=body,
            status=status,
            headers=[('Content-Type', mime),
                     ('Content-Length', len(body))])
        # ---------------------End of New Part---------------------------- #

    def _handle_exception(self, exception):
        """Called within an except block to allow converting exceptions
           to arbitrary responses. Anything returned (except None) will
           be used as response."""
        try:
            return WebRequest._handle_exception(self, exception)
        except Exception:
            if not isinstance(exception, (odoo.exceptions.Warning, SessionExpiredException)):
                _logger.exception("Exception during JSON request handling.")
            error_log = serialize_exception(exception)
            error = {
                'code': 500,
                'message': "Odoo Server Error",
                'data': error_log
            }
            if isinstance(exception, AuthenticationError):
                error['code'] = 100
                error['message'] = "Odoo Session Invalid"
            if isinstance(exception, odoo.exceptions.AccessDenied):
                error['code'] = 401
                error['message'] = "Unauthorized"
            if isinstance(exception, SessionExpiredException):
                error['code'] = 100
                error['message'] = "Odoo Session Expired"
            if isinstance(exception, werkzeug.exceptions.NotFound):
                error['code'] = 404
                error['message'] = "Not found"
                error.pop('data', None)
            if isinstance(exception, werkzeug.exceptions.BadRequest):
                error['code'] = 400
                error['message'] = "Bad Request"
            if isinstance(exception, odoo.exceptions.AccessError):
                error['code'] = 403
                error['message'] = "Forbidden"
                error.pop('data', None)
            if isinstance(exception, werkzeug.exceptions.MethodNotAllowed):
                error['code'] = 405
                error['message'] = "MethodNotAllowed"

            response = self._json_response(error=error)

            vals = {}
            vals['url'] = request.httprequest.url.replace(
                request.httprequest.url_root, '')
            vals['request_method'] = request.httprequest.method
            vals['request_time'] = request.request_time
            vals['request_header'] = base64.b64encode(
                json.dumps(dict(request.httprequest.headers)).encode())
            if hasattr(request, 'jsonrequest'):
                vals['request_body'] = base64.b64encode(
                    json.dumps(request.jsonrequest).encode())
            vals['response_time'] = fields.Datetime.now()
            vals['status_code'] = error['code']
            vals['response_body'] = base64.b64encode(
                error_log['debug'].encode())
            cr = registry(request.env.cr.dbname).cursor()
            request.env['rest.api.log'].with_env(
                request.env(cr=cr)).sudo().create(vals)
            cr.commit()
            return response


def get_request_new(self, httprequest):
    if ('/api/v1/' in httprequest.path):
        if (httprequest.mimetype == "application/json"):
            return ApiRequest(httprequest)
        else:
            return ApiRequest(httprequest)
    elif httprequest.args.get('jsonp'):
        return JsonRequest(httprequest)
    elif httprequest.mimetype in ("application/json", "application/json-rpc"):
        return JsonRequest(httprequest)
    else:
        return HttpRequest(httprequest)


Root.get_request = get_request_new
