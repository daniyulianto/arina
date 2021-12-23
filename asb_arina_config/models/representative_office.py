# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RepresentativeOffice(models.Model):
    _name = 'representative.office'
    _sql_constraints = [
        ('ro_code_uniq', 'unique(ro_code)', 'Nomor Kode harus unik !')
    ]

    ro_code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Nama Area', required=True)
    employee_id = fields.Many2one('hr.employee', string='Nama ARO')
    phone = fields.Char(string='Telephone', size=32)
    city_ids = fields.Many2many('city.city', string='Secondary City')
