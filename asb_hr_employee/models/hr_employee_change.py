from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class EmployeeChange(models.Model):
    _name = "hr.employee.change"
    _rec_name = "employee_id"
    _description = "Employee Change"

    @api.model
    def _default_employee(self):
        return self.env.user.employee_ids and self.env.user.employee_ids[0]

    name = fields.Char('Number Request Employee Change ')
    officer_id = fields.Many2one('hr.employee', string='Officer', default=_default_employee)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    nip = fields.Char('NIP Employee', related='employee_id.registration_number', store=True)
    partner_id = fields.Many2one('res.partner', "Principle", related='employee_id.principle_id', store=True)
    ratecard_id = fields.Many2one('rate.card', string='Ratecard', related='employee_id.ratecard_id', store=True)
    data_change = fields.Selection([
        ("email", "Email"), ("handphone", "NO Handphone"),
        ("npwp", "Nomor NPWP"), ("ktp", "Nomor KTP"),
        ("rekening", "Nomor Rekening")],
        string='Data Change')
    new_data = fields.Char('Data Baru')
    file_document = fields.Binary(string='Document', attachment=True)
    file_name_document = fields.Char('Document File Name')
    description = fields.Char('Description')
    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submit'), ('confirm', 'Confirmed')],
        string='Status', default='draft', tracking=True)

    def action_submit(self):
        for rec in self:
            if rec.employee_id:
                change_request = self.env['hr.employee.change'].search(
                    [('employee_id', '=', rec.employee_id.id),
                     ('state', 'in', ['submit', 'confirm'])])
                if change_request:
                    raise ValidationError(_('There is a Change Data request in Submit or'
                                            ' Confirm state for this employee'))
            rec.write({'state': 'submit'})

    def action_confirm(self):
        for rec in self:
            if rec.new_data:
                employee = rec.employee_id
                if rec.data_change == 'email':
                    employee.work_email = rec.new_data
                elif rec.data_change == 'handphone':
                    employee.work_email = rec.new_data
                elif rec.data_change == 'npwp':
                    employee.work_email = rec.new_data
                elif rec.data_change == 'ktp':
                    employee.work_email = rec.new_data
                elif rec.data_change == 'rekening':
                    employee.work_email = rec.new_data
                rec.write({'state': 'confirm'})
