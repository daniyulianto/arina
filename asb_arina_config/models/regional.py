# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class City(models.Model):
    _name = 'city.city'
    _sql_constraints = [
        ('c_code_uniq', 'unique(c_code)', 'Nomor Kode harus unik !')
    ]

    c_code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Kota', required=True)
    province_id = fields.Many2one('province.province', string='Provinsi', required=True, index=True, copy=False)


class Province(models.Model):
    _name = 'province.province'
    _sql_constraints = [
        ('p_code_uniq', 'unique(p_code)', 'Nomor Kode harus unik !')
    ]

    p_code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Provinsi', required=True)


class Region(models.Model):
    _name = 'region.region'
    _sql_constraints = [
        ('r_code_uniq', 'unique(r_code)', 'Nomor Kode harus unik !')
    ]

    r_code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Region', required=True)
    city_ids = fields.Many2many('city.city', string='Kota')

