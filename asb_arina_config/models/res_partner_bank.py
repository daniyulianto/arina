# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResBank(models.Model):
    _inherit = 'res.bank'

    total_digit_bank = fields.Char('Jumlah Digit Bank', size=20)
