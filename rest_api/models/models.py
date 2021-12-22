from odoo import models, fields
from odoo.http import request
from datetime import datetime
from _collections import defaultdict


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    is_time_off = fields.Boolean(default=False)
    time_of_type = fields.Selection([
        ('annual_leave', 'Annual Leave'),
        ('permission', 'Permission'),
        ('sick', 'Sick'),
    ], store=True)

    def post_attendance(self, body, **kwargs):
        new_attendance = body.get('data', False)
        uid = kwargs.get('uid', 1)
        validation_errors = []
        if new_attendance:
            if not new_attendance.get('employee_id'):
                attribute = "employee_id/nik/employee_name"
                message = "Employee is Required (not defined correctly in Request Body)"
                if new_attendance.get('employee_id'):
                    new_attendance['employee_id'] = new_attendance.pop('employee_id')
                    attribute = "employee_id"
                elif new_attendance.get('identification_id'):
                    attribute = "identification_id"
                    domain = [('name', '=', new_attendance.get('identification_id'))]
                    fields = ['id', 'name']
                    data = request.env['hr.employee'].sudo().search_read(
                        domain=domain, fields=fields)
                    if data:
                        new_attendance['identification_id'] = data[0].get('id')
                    else:
                        message = "Employee {customer} not found".format(
                            customer=new_attendance.get('identification_id'))
                elif new_attendance.get('employee_name'):
                    attribute = "employee_name"
                    domain = [('name', '=', new_attendance.get('employee_name'))]
                    fields = ['id', 'name']
                    data = request.env['hr.employee'].sudo().search_read(
                        domain=domain, fields=fields)
                    if data:
                        new_attendance['employee_id'] = data[0].get('id')
                    else:
                        message = "Employee {customer} not found".format(
                            customer=new_attendance.get('employee_name'))
            if not new_attendance.get('employee_id'):
                validation_errors.append({
                    "attribute": attribute,
                    "error": message
                })
            new_attendance.pop('employee_name', None)

            if not new_attendance.get('check_in'):
                validation_errors.append({
                    "attribute": 'check_in',
                    "error": 'Employee Check in  is Required (not defined correctly in Request Body)'
                })
            if not new_attendance.get('check_out'):
                validation_errors.append({
                    "attribute": 'check_out',
                    "error": 'Employee Check Out is Required (not defined correctly in Request Body)'
                })
            if not new_attendance.get('check_out'):
                validation_errors.append({
                    "attribute": 'check_out',
                    "error": 'Employee Check Out is Required (not defined correctly in Request Body)'
                })
            if not new_attendance.get('is_time_off'):
                validation_errors.append({
                    "attribute": 'is_time_off',
                    "error": 'Time Off Status Out is Required (not defined correctly in Request Body)'
                })
            if validation_errors:
                return {'error': {'code': 401, 'message': validation_errors, }}

            attendance_id = self.with_user(uid).create(new_attendance)
        return {
            "attendance_id": attendance_id.id,
            "is_time_off": attendance_id.is_time_off,
            "worked_hours": attendance_id.worked_hours}


