import json

from odoo import http, fields, _
from odoo.http import request, route
from odoo.tools.config import config
from basicauth import decode

import werkzeug
import jwt
import datetime
import json

import functools
from odoo.tools import date_utils
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT,\
    DEFAULT_SERVER_DATE_FORMAT
import base64

secret_key = config.options.get('jwt_secret_key', 'Ark@na2019')


def _response(headers, body, status=200, request_type='http'):
    if request_type == 'json':
        response = {}
        response['error'] = [{
            'code': status,
            'message': body['message'],
        }]
        response['route'] = True
        return response
    elif request_type == 'http':
        response = {}
        response['route'] = True
        return response
    try:
        fixed_headers = {str(k): v for k, v in headers.items()}
    except:
        fixed_headers = headers
    response = werkzeug.Response(response=json.dumps(
        body), status=status, headers=fixed_headers)
    return response


def token_required(**kw):

    def decorator(f):

        @functools.wraps(f)
        def wrapper(*args, **kw):
            headers = dict(request.httprequest.headers.items())
            request_type = request._request_type
            auth = headers.get('Authorization', None)
            # Ref
            # https://github.com/mgonto/auth0-python-flaskapi-sample/blob/master/server.py
            if not auth:
                return {'error': {'code': 403, 'message': 'No Authorization'}}
            parts = auth.split()
            if parts[0].lower() != 'bearer':
                return {'error': {'code': 403, 'message': 'Authorization header must start with Bearer'}}
            elif len(parts) == 1:
                return {'error': {'code': 403, 'message': 'Token not found'}}
            elif len(parts) > 2:
                return {'error': {'code': 403, 'message': 'Authorization header must be Bearer + \s + token'}}
            token = parts[1]
            try:
                data = jwt.decode(token, secret_key)
                kw['uid'] = data['uid']
                request.uid = data['uid']
            except jwt.ExpiredSignature:
                return {'error': {'code': 401, 'message': 'Token is expired'}}
            except jwt.DecodeError:
                return {'error': {'code': 401, 'message': 'Token signature is invalid'}}
            except Exception:
                return {'error': {'code': 401, 'message': 'Token is invalid'}}
            response = f(*args, **kw)
            return response

        return wrapper

    return decorator


def log_request(func):
    @functools.wraps(func)
    def wrapper(*aargs, **kwargs):
        def date_converter(o):
            if isinstance(o, datetime.datetime):
                return o.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            if isinstance(o, datetime.date):
                return o.strftime(DEFAULT_SERVER_DATE_FORMAT)
        vals = {}
        vals['url'] = request.httprequest.url.replace(
            request.httprequest.url_root, '')
        vals['request_method'] = request.httprequest.method
        vals['request_time'] = fields.Datetime.now()
        vals['request_header'] = base64.b64encode(
            json.dumps(dict(request.httprequest.headers)).encode())
        if hasattr(request, 'jsonrequest'):
            vals['request_body'] = base64.b64encode(
                json.dumps(request.jsonrequest).encode())
            reference_index = [
                'purchase',
                'delivery_ref',
                'picking',
                'receiving_ref',
                'checking',
                'sale',
                'production_id',
                'ref',
            ]
            vals['reference'] = False
            if isinstance(request.jsonrequest, dict):
                for idx in reference_index:
                    ref = request.jsonrequest.get(idx)
                    if not vals['reference'] and ref:
                        vals['reference'] = ref
        request.uid = kwargs.get('uid', 1)

        # =====================================
        response = func(*aargs, **kwargs)
        # =====================================
        vals['response_time'] = fields.Datetime.now()
        vals['status_code'] = 200
        vals['response_body'] = base64.b64encode(
            json.dumps(response, default=date_converter).encode())

        request.env['rest.api.log'].sudo().create(vals)
        return response
    return wrapper

def oauth_log_request(func):
    @functools.wraps(func)
    def wrapper(*aargs, **kwargs):
        def date_converter(o):
            if isinstance(o, datetime.datetime):
                return o.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            if isinstance(o, datetime.date):
                return o.strftime(DEFAULT_SERVER_DATE_FORMAT)
        vals = {}
        vals['url'] = request.httprequest.url.replace(
            request.httprequest.url_root, '')
        vals['request_method'] = request.httprequest.method
        vals['request_time'] = fields.Datetime.now()
        vals['request_header'] = base64.b64encode(
            json.dumps(dict(request.httprequest.headers)).encode())
        if hasattr(request, 'httprequest'):
            vals['request_body'] = base64.b64encode(
                json.dumps(request.params).encode())
        request.uid = kwargs.get('uid', 1)

        # =====================================
        response = func(*aargs, **kwargs)
        # =====================================
        vals['response_time'] = fields.Datetime.now()
        vals['status_code'] = 200
        if response.data:
            vals['response_body'] = base64.b64encode(\
                json.dumps(response.data.decode('utf8')).encode())

        request.env['rest.api.log'].sudo().create(vals)
        return response
    return wrapper


def oauth_token_required(**kw):

    def decorator(f):

        @functools.wraps(f)
        def wrapper(*args, **kw):
            headers = dict(request.httprequest.headers.items())
            request_type = request._request_type
            auth = headers.get('Authorization', None)
            if not auth:
                return {
                    'ErrorCode': 403,
                    'ErrorMessage': {
                        'Indonesian': 'Tidak Ada Otorisasi',
                        'English': 'No Authorization'
                    }
                }
            parts = auth.split()
            if parts[0].lower() != 'bearer':
                return {
                    'ErrorCode': 403,
                    'ErrorMessage': {
                        'Indonesian': 'Header otorisasi harus dimulai dengan Bearer',
                        'English': 'Authorization header must start with Bearer'
                    }
                }
            elif len(parts) == 1:
                return {
                    'ErrorCode': 403,
                    'ErrorMessage': {
                        'Indonesian': 'Token tidak ditemukan',
                        'English': 'Token not found'
                    }
                }
            elif len(parts) > 2:
                return {
                    'ErrorCode': 403,
                    'ErrorMessage': {
                        'Indonesian': 'Authorization header must be Bearer + \s + token',
                        'English': 'Authorization header must be Bearer + \s + token'
                    }
                }
            token = parts[1]
            try:
                data = jwt.decode(token, secret_key)
                kw['uid'] = data['uid']
            except jwt.ExpiredSignature:
                return {
                    'ErrorCode': 401,
                    'ErrorMessage': {
                        'Indonesian': 'Token kedaluwarsa',
                        'English': 'Token is expired'
                    }
                }
            except jwt.DecodeError:
                return {
                    'ErrorCode': 401,
                    'ErrorMessage': {
                        'Indonesian': 'Tanda tangan token tidak valid',
                        'English': 'Token signature is invalid'
                    }
                }
            except Exception:
                return {
                    'ErrorCode': 401,
                    'ErrorMessage': {
                        'Indonesian': 'Token tidak valid',
                        'English': 'Token is invalid'
                    }
                }
            response = f(*args, **kw)
            return response

        return wrapper

    return decorator


class ApiLogin(http.Controller):

    def _response(self, headers, body, status=200):
        try:
            fixed_headers = {str(k): v for k, v in headers.items()}
        except Exception:
            fixed_headers = headers
        response = werkzeug.Response(
            response=body, status=status, headers=fixed_headers)
        return response

    @route('/api/v1/login', type='json', methods=['POST'], auth='public', csrf=False)
    @log_request
    def get_login(self, **kw):
        headers = dict(request.httprequest.headers.items())
        body = request.jsonrequest
        username = body.get('username', False)
        password = body.get('password', False)
        grant_type = body.get('grant_type', False)
        refresh_token = body.get('refresh_token', False)
        uid = body.get('user_id', False)
        if grant_type == "refresh_token" and (refresh_token and uid):
            request_result = request.env['rest.cr'].sudo(
            ).get_refresh_token(uid, refresh_token)
            if request_result:
                uid = request_result[0]
                username = request_result[1]
                token = jwt.encode({'uid': uid, 'user': username, 'exp': datetime.datetime.utcnow(
                ) + datetime.timedelta(seconds=86400)}, secret_key)
                result = {}
                result['token'] = token.decode('UTF-8')
                result['token_live'] = 86400
                result['refresh_token'] = refresh_token
                return {'result': result}
            else:
                return {'error': {'code': 401, 'message': 'Invalid Refresh Token'}}

        if username and password:
            # or request.cr.dbname for dbname
            uid = request.session.authenticate(
                request.session.db, username, password)
            if uid:
                token = jwt.encode({'uid': uid, 'user': username, 'exp': datetime.datetime.utcnow(
                ) + datetime.timedelta(seconds=86400)}, secret_key)
                request_result = request.env['rest.cr'].login(uid)
                if request_result:
                    request_result['token'] = token.decode('UTF-8')
                    request_result['token_live'] = 86400
                    return {'result': request_result}
                else:
                    return {'error': {'code': 401, 'message': 'Unauthorized Login'}}
            else:
                return {'error': {'code': 401, 'message': 'Invalid Username or Password'}}
        else:
            return {'error': {'code': 400, 'message': 'Invalid Request Parameter'}}

    @route('/api/oauth/token', type='http', methods=['POST', 'GET'], auth='public', csrf=False)
    @oauth_log_request
    def get_oauth_token(self, **kw):
        headers = request.httprequest.headers
        auth = headers.get('Authorization', None)
        body = json.dumps({
            'ErrorCode': 403,
            'ErrorMessage': {
                'Indonesian': 'Tidak Ada Otorisasi',
                'English': 'No Authorization'
            }
        }, default=date_utils.json_default)
#         if not auth:
#             return {'error' : {'code': 403, 'message': 'No Authorization'}}
        try:
            username, password = decode(auth)
            if username and password:
                # or request.cr.dbname for dbname
                uid = request.session.authenticate(
                    request.session.db, username, password)
                if uid:
                    token = jwt.encode({'uid': uid, 'user': username, 'exp': datetime.datetime.utcnow(
                    ) + datetime.timedelta(seconds=86400)}, secret_key)
                    request_result = request.env['rest.cr'].sudo().login(uid)
                    user_id = http.request.env['res.users'].sudo().browse(uid)
                    if request_result and user_id:
                        response_dict = {}
                        response_dict['access_token'] = token.decode('UTF-8')
                        response_dict['token_type'] = 'bearer'
                        response_dict['expires_in'] = 86400
                        scopes = []
                        for group_id in user_id.groups_id:
                            for model_access in group_id.model_access:
                                if model_access.perm_read:
                                    scopes.append('%s.READ' %
                                                  (model_access.model_id.model))
                                if model_access.perm_write:
                                    scopes.append('%s.WRITE' %
                                                  (model_access.model_id.model))
                                if model_access.perm_create:
                                    scopes.append('%s.CREATE' %
                                                  (model_access.model_id.model))
                                if model_access.perm_unlink:
                                    scopes.append('%s.DELETE' %
                                                  (model_access.model_id.model))
                        response_dict['scope'] = ' '.join(scopes)
                        body = json.dumps(
                            response_dict, default=date_utils.json_default)
        except Exception as e:
            body = json.dumps({
                'ErrorCode': 401,
                'ErrorMessage': {
                    'Indonesian': e,
                    'English': e
                }
            }, default=date_utils.json_default)
        response = request.make_response(body, [
            ('Content-Type', 'application/json')
        ])
        return response