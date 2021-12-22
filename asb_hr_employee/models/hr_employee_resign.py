from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class EmployeeResign(models.Model):
    _name = "hr.employee.resign"
    _rec_name = "employee_id"
    _description = "Employee Resign"

    @api.model
    def _default_employee(self):
        return self.env.user.employee_ids and self.env.user.employee_ids[0]

    name = fields.Char('Number Request Employee Resign ')
    officer_id = fields.Many2one('hr.employee', string='Officer', default=_default_employee)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    nip = fields.Char('NIP Employee', related='employee_id.registration_number', store=True)
    partner_id = fields.Many2one('res.partner', related='employee_id.principle_id', store=True)
    ratecard_id = fields.Many2one('rate.card', string='Ratecard', related='employee_id.ratecard_id')
    departure_reason = fields.Selection([
        ('fired', 'Fired'),
        ('resigned', 'Resigned'),
        ('retired', 'Retired')
    ], string="Departure Reason", default="fired")
    resign_type = fields.Selection([
        ('peralihan', 'Peralihan'),
        ('end_project', 'End Project'),
        ('resign', 'Resign'),
        ('end_contract', 'End Contract')
    ], string="Resign Type", default="resign")
    departure_description = fields.Text(string="Additional Information")
    departure_date = fields.Date(string="Departure Date", required=True, default=fields.Date.today)
    archive_private_address = fields.Boolean('Archive Private Address', default=True)
    set_date_end = fields.Boolean(string="Set Contract End Date", default=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submit'), ('confirm', 'Confirmed')],
        string='Status', default='draft', tracking=True)

    def action_submit(self):
        for rec in self:
            if rec.employee_id:
                resignation_request = self.env['hr.employee.resign'].search([('employee_id', '=', rec.employee_id.id),
                                                                             ('state', 'in', ['submit', 'confirm'])])
                if resignation_request:
                    raise ValidationError(_('There is a resignation request in confirmed or'
                                            ' approved state for this employee'))
            rec.write({'state': 'submit'})

    def action_confirm(self):
        for rec in self:
            employee = rec.employee_id
            employee.departure_reason = rec.departure_reason
            employee.departure_description = rec.departure_description
            employee.departure_date = rec.departure_date
            employee.active = False
            employee.resign_type = rec.resign_type

            if rec.archive_private_address:
                # ignore contact links to internal users
                private_address = employee.address_home_id
                if private_address and private_address.active and not rec.env['res.users'].search(
                        [('partner_id', '=', private_address.id)]):
                    private_address.toggle_active()

            current_contract = rec.employee_id.contract_id
            if current_contract and current_contract.date_start > rec.departure_date:
                raise UserError(_("Departure date can't be earlier than the start date of current contract."))

            if rec.set_date_end:
                rec.employee_id.contract_ids.filtered(lambda c: c.state == 'draft').write({'state': 'cancel'})
                if current_contract:
                    rec.employee_id.contract_id.write({'date_end': rec.departure_date})
                if current_contract.departure_date > current_contract.date_start:
                    rec.employee_id.contract_id.write({'state': 'close'})
            rec.write({'state': 'confirm'})

    def action_only_employee(self):
        for rec in self:
            employee = rec.employee_id
            employee.active = False
            rec.write({'state': 'confirm'})
