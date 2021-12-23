from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class EmployeeEducation(models.Model):
    _name = 'hr.employee.education'
    _sql_constraints = [
        ('e_code_uniq', 'unique(c_code)', 'Nomor Kode harus unik !')
    ]

    e_code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Nama Pendidikan', required=True)