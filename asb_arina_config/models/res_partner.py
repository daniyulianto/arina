# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PrincipleDivision(models.Model):
    _name = 'principle.division'
    _sql_constraints = [
        ('pd_code_uniq', 'unique(pd_code)', 'Nomor Kode harus unik !')
    ]

    pd_code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Nama Divisi', required=True)


class CutOffTime(models.Model):
    _name = 'cutoff.time'

    name = fields.Char(string='Nama', required=True)
    start = fields.Char(string='start', size=2)
    end = fields.Char(string='end', size=2)


class PayrollPartnerConf(models.Model):
    _name = 'payroll.partner.conf'

    principal_division_id = fields.Many2one('principle.division', string='Divisi')
    cutoff_id = fields.Many2one('cutoff.time', string='Cut Off')
    salary_disbursement = fields.Char('Pencairan gaji')
    partner_id = fields.Many2one('res.partner')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    _sql_constraints = [
        ('rp_code_uniq', 'unique(p_code)', 'Nomor Kode harus unik !')
    ]

    rp_code = fields.Char(string='Code')
    division_ids = fields.Many2many('principle.division', string='List Divisi')
    cutoff_time_id = fields.Many2one('cutoff.time', string='Cut Off Time')
    national_admin = fields.Many2one('hr.employee', string='Admin Nasional')
    hod_name = fields.Many2one('hr.employee', string='Nama HOD')
    status = fields.Selection([("regular", "Regular"), ("event", "Event")], string='Status')
    management_fee = fields.Monetary('Management Fee', currency_field='currency_id', default=0.0)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    ppn_option = fields.Selection([("only_fee", "Fee Only"), ("combine", "10% Gross + Fee")], string='Opsi PPN')
    payroll_conf_ids = fields.One2many('payroll.partner.conf', 'partner_id','Payroll Configuration')
    is_grossup = fields.Boolean(default=False)
    is_minimum_approval_po = fields.Boolean(default=False)
#   Legal field Information
    tdp = fields.Char('TDP')
    siup = fields.Char('SIUP')
    skt = fields.Char('SKT/NIB')
    sppkp = fields.Char('SPPKP')
