from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import datetime
from datetime import datetime, timedelta


class EmployeeBlacklist(models.Model):
    _name = "hr.employee.blacklist"
    _rec_name = "employee_id"
    _description = "Employee Blacklist"

    @api.model
    def _default_employee(self):
        return self.env.user.employee_ids and self.env.user.employee_ids[0]

    name = fields.Char('Number Request Employee Blacklist')
    officer_id = fields.Many2one('hr.employee', string='Officer', default=_default_employee)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    nip = fields.Char('NIP Employee', related='employee_id.registration_number', store=True)
    partner_id = fields.Many2one('res.partner', "Principle", related='employee_id.principle_id', store=True)
    ratecard_id = fields.Many2one('rate.card', string='Ratecard', related='employee_id.ratecard_id', store=True)
    blacklist_reason = fields.Char('Blacklist Reason')
    file_document = fields.Binary(string='Document', attachment=True)
    file_name_document = fields.Char('Document File Name')
    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submit'), ('confirm', 'Confirmed')],
        string='Status', default='draft', tracking=True)

    def action_submit(self):
        for rec in self:
            if rec.employee_id:
                blacklist_request = self.env['hr.employee.blacklist'].search(
                    [('employee_id', '=', rec.employee_id.id),
                     ('state', 'in', ['submit', 'confirm'])])
                if blacklist_request:
                    raise ValidationError(_('There is a Blacklist request in Submit or'
                                            ' Confirm state for this employee'))
            rec.write({'state': 'submit'})

    def action_confirm(self):
        for rec in self:
            current_contract = rec.employee_id.contract_id
            if current_contract:
                rec.employee_id.contract_ids.filtered(lambda c: c.state == 'draft').write({'state': 'cancel'})
                rec.employee_id.contract_id.write({'date_end': str(datetime.now()),
                                                   'state': 'close'})
            employee = rec.employee_id
            employee.blacklist = True
            employee.active = False
            rec.write({'state': 'confirm'})
