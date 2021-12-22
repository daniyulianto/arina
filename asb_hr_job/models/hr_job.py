from odoo import models, fields, api


class Job(models.Model):
    _inherit = "hr.job"

    ratecard_id = fields.Many2one('rate.card', string='Ratecard')
    quota_id = fields.Many2one('quota.quota', string='Quota')
    partner_id = fields.Many2one('res.partner', string='Principal')
    principal_division_id = fields.Many2one('principle.division', string='Divisi')
    aro_id = fields.Many2one('hr.employee', related='ratecard_id.aro_id', store=True, string='ARO')
    hod_id = fields.Many2one('hr.employee', string='HOD', related='ratecard_id.hod_id', store=True,)
    start_date = fields.Date(string='Tanggal Mulai', related='quota_id.start_date', store=True,)
    end_date = fields.Date(string='Tanggal Selesai')
    deadline_date = fields.Date(string='Tanggal Deadline', related='quota_id.deadline_date', store=True)
