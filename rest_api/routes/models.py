from odoo import http, fields, _
from odoo.http import request, route
import base64
from odoo.exceptions import UserError

from ..jwt.login import token_required
from ..jwt.login import log_request

model_map = dict([
    ('employee', 'hr.employee'),
    ('attendance', 'hr.attendance'),
])


def modify_binary(model, result):
    for res in result:
        for key in res:
            if isinstance(model._fields[key], fields.Binary) and res[key]:
                res[key] = base64.b64encode(res[key]).decode()
    return result


class ApiModel(http.Controller):

    @route(route=['/api/v1/get/<req_model>',
                  '/api/v1/get/<req_model>/<int:record_id>'],
           methods=['GET'], type='json', auth='public', csrf=False)
    @token_required
    @log_request
    def get_data(self, req_model, record_id=False, debug=False, **kwargs):
        model = request.env[model_map[req_model]]
        arguments = request.httprequest.args
        limit = arguments.get('limit')
        offset = arguments.get('offset', 0)
        order = arguments.get('order')
        if limit:
            limit = int(limit)
        if offset:
            offset = int(offset)

        field_list = model._api_get_fields(req_model)
        offset, limit, order = model._api_search_param(req_model) if hasattr(
            model, '_api_search_param') else (offset, limit, order)
        search_domain = model._api_search_domain(req_model) if hasattr(
            model, '_api_search_domain') else []
        if record_id:
            search_domain.append(('id', '=', record_id))
        result = model.search_read(
            search_domain, field_list, offset,
            limit, order)
        modified_binary_result = modify_binary(model, result)
        modified_result = model._api_modify_result(modified_binary_result, req_model) if hasattr(
            model, '_api_modify_result') else result
        return {
            'result': {
                'count': len(modified_result),
                'datas': modified_result,
            }
        }

    @route(route=['/api/v1/employee/status'],
           methods=['GET'], type='json', auth='public', csrf=False)
    @token_required()
    def get_employee_status(self, **kwargs):
        employee = request.env['hr.employee'].sudo().search(
            [('user_id', '=', kwargs.get('uxid'))])
        if not employee:
            raise UserError(_('No Employee Defined for current user!'))

        return {
            'result': {
                'employee_name': employee.name,
                'identification_id': employee.identification_id,
                'active': employee.active,  # kalo resign status berdasarkan active dan non active/non active = resign
            }
        }

    @route(route=['/api/v1/post/attendance'],
           methods=['POST'], type='json', auth='public', csrf=False)
    @token_required
    @log_request
    def post_attendance(self, **kwargs):
        body = request.jsonrequest
        result = request.env['hr_attendance'].sudo(
        ).api_post_attedance(body, **kwargs)
        return {'result': result, 'code': 201}
