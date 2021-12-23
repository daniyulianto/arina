from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Quota(models.Model):
    _name = 'quota.quota'
    _description = 'Quota'
    _order = 'id desc'

    name = fields.Char(string='Number', readonly=True, default='/')
    status = fields.Selection([("new", "New"), ("replace", "Replace")], string='Status Quota', default='replace')
    quota_id = fields.Many2one('quota.quota',
                               domain="[('partner_id', '=', partner_id), ('status', '=', 'new'), ('state', 'in', ['vacant', 'done'])]",
                               string='Quota Replace')
    # quota_id = fields.Many2many('quota.quota', relation="quota_rel", string='Quota Replace')
    no_ktp = fields.Char(string='NIP (NO KTP)')
    partner_id = fields.Many2one('res.partner', string='Principal', required=True)
    partner_ids = fields.Many2many('rate.card', compute='_compute_partner_ids', store=False, string='Partner Ids')
    employee_name = fields.Char(string='Employee Name')
    ratecard_id = fields.Many2one('rate.card', string='No. Rate Card',
                                  domain="[('id', 'in', partner_ids),('state', '=', 'approved')]", required=True)
    aro_id = fields.Many2one(related='ratecard_id.aro_id', string='ARO')
    hod_id = fields.Many2one(related='ratecard_id.hod_id', string='HOD')
    area = fields.Many2one('rate.card.line', string='Area - Job')
    # ratecard_ids = fields.Many2many('rate.card.line', compute='_compute_ratecard_ids', store=False, string='Ratecard Ids')
    secondary_city_id = fields.Many2one('city.city', string='Secondary City')
    job_title = fields.Char(related='area.job_title', string='Job Title')
    status_karyawan = fields.Selection([
        ("kontrak", "Kontrak"),
        ("magang", "Magang"),
        ("permanent", "Permanent")], string='Status Karyawan')
    quota_ratecard = fields.Float(related='area.quota', string="Quota Ratecard")
    quota_publish = fields.Float("Quota Publish")
    start_date = fields.Date(string='Tanggal Mulai')
    running_date = fields.Date(string='Tanggal Running')
    deadline_date = fields.Date(string='Tanggal Deadline')
    quota_status = fields.Selection([
        ("active", "Active"),
        ("hold", "Hold"),
        ("done", "Done")], string='Action Status')
    kualifikasi = fields.Text(string='Kualifikasi')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('validate', 'Validate'),
        ('vacant', 'Vacant'),
        ('done', 'Done'),
    ], string='Status', default='draft')
    template_pkwt = fields.Selection([
        ('template1', 'Template PKWT 1'),
        ('template2', 'Template PKWT 2'),
        ('template3', 'Template PKWT 3'),
    ], string='Template PKWT', default='template1')
    job_title_ref = fields.Char(string='Job Title')
    from_ratecard = fields.Boolean(string='from RateCard', default=False)

    # Change Number Format, Name Format is Number Ratecard - City - Area - Numbner Sequence
    @api.model
    def create(self, vals):
        if vals['from_ratecard']:
            return super(Quota, self).create(vals)
        if vals['quota_id']:
            vals['area'] = self.env['quota.quota'].search([('id', '=', vals['quota_id'])]).area.area.id
            vals['job_title_ref'] = self.env['quota.quota'].search([('id', '=', vals['quota_id'])]).job_title
        vals['name'] = self.env['rate.card'].search([('id', '=', vals['ratecard_id'])]).name + '-' + self.env[
            'city.city'].search([('id', '=', vals['area'])]).name + '-' + vals['job_title_ref'] + '-' + self.env[
                           'ir.sequence'].next_by_code('quota.quota')
        return super(Quota, self).create(vals)

    # Validation Quota Publish cannot bigger than Quota RateCard, Return Quota Publish to 0
    @api.onchange('quota_publish')
    def _onchange_quota_validation(self):
        for r in self:
            if r.quota_publish > r.quota_ratecard:
                r.quota_publish = 0.00
                raise UserError(_('Sorry, Quota Published can not more than Quota Ratecard'))

    # Filter Area based on selected RateCard
    # @api.depends('ratecard_id','area')
    # def _compute_ratecard_ids(self):
    #     for r in self:
    #         r.ratecard_ids = self.env['rate.card.line'].search([('ratecard_id', '=', r.ratecard_id.id)]).ids
    #         if r.area.id not in r.ratecard_ids.ids:
    #             r.area = False
    # Filter Ratecard based on selected Partner
    @api.depends('quota_id', 'partner_id', 'ratecard_id')
    def _compute_partner_ids(self):
        for r in self:
            r.partner_ids = self.env['rate.card'].search([('partner_id', '=', r.partner_id.id)]).ids

    # Change state from Draft to Pending
    def set_pending(self):
        for r in self:
            r.state = 'pending'

    # Change state from Pending to Validate, and Create Job Recruitment to Recreuitment Modul (hr.job)
    def set_validate(self):
        for r in self:
            create_job = self.env['hr.job'].create(
                {
                    'name': r.area.display_name,
                    'no_of_recruitment': r.quota_publish,
                    'ratecard_id': r.ratecard_id.id,
                    'quota_id': r.id,
                    'website_description': r.kualifikasi,
                    'address_id': r.partner_id.id,
                }
            )
            r.state = 'validate'

    # Run function set.recruit() in model hr.job and change the state to Vacant
    def set_vacant(self):
        for r in self:
            done_job = self.env['hr.job'].search(
                [('name', '=', r.area.display_name), ('quota_id', '=', r.id)]).set_recruit()
            r.state = 'vacant'

    # Run function set.open() in model hr.job and change the state to Done
    def set_done(self):
        for r in self:
            done_job = self.env['hr.job'].search(
                [('name', '=', r.area.display_name), ('quota_id', '=', r.id)]).set_open()
            r.state = 'done'

    # Change the state to Done for replace Quota
    def set_done_replace(self):
        for r in self:
            if r.quota_id:
                r.area = r.quota_id.area.id
                r.job_title = r.quota_id.job_title
                r.state = 'done'
            else:
                raise UserError(_('Please select Quota Repalce!'))

    # Copy value while value change
    @api.onchange('job_title')
    def _onchange_job_title(self):
        for r in self:
            r.job_title_ref = r.job_title

    # Display Data to Mini Dashboard on Tree/List View
    @api.model
    def retrieve_quota_dashboard(self):
        res_active = self.search([('quota_status', '=', 'active')])
        res_hold = self.search([('quota_status', '=', 'hold')])
        res_done = self.search([('quota_status', '=', 'done')])
        res = {
            "active": {
                "total": len(res_active),
                "kontrak": len(res_active.filtered(lambda r: r.status_karyawan == 'kontrak')),
                "magang": len(res_active.filtered(lambda r: r.status_karyawan == 'magang')),
                "permanent": len(res_active.filtered(lambda r: r.status_karyawan == 'permanent')),
            },
            "hold": {
                "total": len(res_hold),
                "kontrak": len(res_hold.filtered(lambda r: r.status_karyawan == 'kontrak')),
                "magang": len(res_hold.filtered(lambda r: r.status_karyawan == 'magang')),
                "permanent": len(res_hold.filtered(lambda r: r.status_karyawan == 'permanent')),
            },
            "done": {
                "total": len(res_done),
                "kontrak": len(res_done.filtered(lambda r: r.status_karyawan == 'kontrak')),
                "magang": len(res_done.filtered(lambda r: r.status_karyawan == 'magang')),
                "permanent": len(res_done.filtered(lambda r: r.status_karyawan == 'permanent')),

            },
        }
        return res
