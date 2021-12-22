from odoo import models, fields, api


class Job(models.Model):
    _inherit = "hr.contract"
    is_deposit = fields.Boolean(string='Sudah Deposit')
    currency_id = fields.Many2one('res.currency', 'Currency', readonly=True,
                                  default=lambda s: s.env.ref('base.IDR'))
    deposit_amount = fields.Monetary(string='Amount')
    salary_applicant_rule_ids = fields.One2many('hr.salary.applicant.rule', 'applicant_id',
                                                string='Salary Applicant Rule')
    pkwt_template_id = fields.Many2one('hr.template.pkwt', string='Template PKWT')
    file_template_pkwt = fields.Binary(string='Template PKWT', attachment=True,
                                       related='pkwt_template_id.file_template_pkwt', store=True)
    file_name_template_pkwt = fields.Char('File Name PKWT',
                                          related='pkwt_template_id.file_name_template_pkwt', store=True)
    file_pkwt_ttd = fields.Binary(string='File PKWT TTD', attachment=True)
    file_name_pkwt_ttd = fields.Char('File PKWT TTD')
