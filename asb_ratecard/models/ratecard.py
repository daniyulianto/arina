# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class RateCard(models.Model):
    _name = 'rate.card'
    _description = 'Rate Card'
    _order = 'id desc'

    name = fields.Char(string='Number', readonly=True, default='/')
    partner_id = fields.Many2one('res.partner', string='Customer')
    is_pkp = fields.Boolean(string='PKP/Non PKP')
    type_contract = fields.Selection([("permanent","Permanent"),("pkwt","PKWT"),("pkhl","PKHL"),("borongan","Borongan")], string='Type')
    ratecard_category_id = fields.Many2one('rate.card.category', string='Rate Card Category', domain=[('is_active', '=', True)])
    hide = fields.Boolean(string='Hide', default=True)
    start_date = fields.Date(string='Start Date', default=fields.Date.today())
    end_date = fields.Date(string='End Date', default=fields.Date.today())
    agency_fee = fields.Integer(string='Agency Fee (%)')
    period_payroll_date = fields.Date(string='Periode Payroll/Cut off periode')
    aro_id = fields.Many2one('hr.employee', string='ARO')
    hod_id = fields.Many2one('hr.employee', string='HOD')
    ratecard_line_ids = fields.One2many('rate.card.line', 'ratecard_id', string='Rate Card Line')
    state = fields.Selection([
            ('draft', 'Draft'),
            ('quotation', 'Quotation'),
            ('approved', 'Approved'),
        ], string='Status', default='draft')
    recruitment_start_date = fields.Date(string="Tanggal Mulai", default=fields.Date.today())
    recruitment_deadline_date = fields.Date(string="Tanggal Deadline", default=fields.Date.today())
    purchase_ref = fields.Char(string='PO Number')
    purchase_date = fields.Date(string='PO Date')
    purchase_amount = fields.Float(string='PO Amount')
    realization_amount = fields.Float(string='Realization Amount')
    purchase_outstanding_amount = fields.Float(compute='_compute_purchase_ourstanding_amount', string='Outstanding amount PO', store=True)
    alert_amount = fields.Float(string='Alert Amount')
    total_quota = fields.Float(compute='_compute_total_quota', string='Total Quota', store=True)
    total_filled = fields.Float(string='Total Terpenuhi')
    company_id = fields.Many2one('res.company', related='create_uid.company_id', readonly=True, string='Company')
    
    # Result of Purchase Outstanding Amount is Purchase Amount - Realization Amount
    @api.depends('purchase_amount', 'realization_amount')
    def _compute_purchase_ourstanding_amount(self):
        for r in self:
            r.purchase_outstanding_amount = r.purchase_amount - r.realization_amount
    # Get total of Quota in one2many of selected Rate Card Line
    @api.depends('ratecard_line_ids')
    def _compute_total_quota(self):
        for r in self:
            total = sum(r.ratecard_line_ids.mapped('quota'))
            r.total_quota = total
    # Change State from Draft to Quotation
    def set_quotation(self):
        for r in self:
            r.state = 'quotation'
    # Chante State from Quotation to Apprived, Purchase Ref can not be null
    def set_approved(self):
        for r in self:
            if not r.purchase_ref:
                raise UserError('You can not "Approve" this RateCard because PO number is empty! ')
            r.state = 'approved'
            for i in r.ratecard_line_ids:
                create_quota = self.env['quota.quota'].create({
                    'name' : r.name + '-' + i.area.name + '-' + i.job_title + '-' + self.env['ir.sequence'].next_by_code('quota.quota'),
                    'status' : 'new',
                    'partner_id' : r.partner_id.id,
                    'ratecard_id': r.id,
                    'area': i.area.id,
                    'start_date': r.recruitment_start_date,
                    'deadline_date': r.recruitment_deadline_date,
                    'job_title': i.job_title,
                    'from_ratecard': 1
                })
    # Display Data to Mini Dashboard on Tree/List View
    @api.model
    def retrieve_ratecard_dashboard(self):
        res_draft = self.search([('state', '=', 'draft')])
        res_quotation = self.search([('state', '=', 'quotation')])
        res_approved = self.search([('state', '=', 'approved')])
        res = {
            "draft" : {
                "total": len(res_draft),
                "permanent": len(res_draft.filtered(lambda r: r.type_contract == 'permanent')),
                "pkwt": len(res_draft.filtered(lambda r: r.type_contract == 'pkwt')),
                "pkhl": len(res_draft.filtered(lambda r: r.type_contract == 'pkhl')),
                "borongan": len(res_draft.filtered(lambda r: r.type_contract == 'borongan')),
            },
            "quotation" : {
                "total": len(res_quotation),
                "permanent": len(res_quotation.filtered(lambda r: r.type_contract == 'permanent')),
                "pkwt": len(res_quotation.filtered(lambda r: r.type_contract == 'pkwt')),
                "pkhl": len(res_quotation.filtered(lambda r: r.type_contract == 'pkhl')),
                "borongan": len(res_quotation.filtered(lambda r: r.type_contract == 'borongan')),
                
            },
            "approved" : {
                "total": len(res_approved),
                "permanent": len(res_approved.filtered(lambda r: r.type_contract == 'permanent')),
                "pkwt": len(res_approved.filtered(lambda r: r.type_contract == 'pkwt')),
                "pkhl": len(res_approved.filtered(lambda r: r.type_contract == 'pkhl')),
                "borongan": len(res_approved.filtered(lambda r: r.type_contract == 'borongan')),
                
            },
        }
        return res

    # Hide Column
    is_area = fields.Boolean('is Area')
    is_quota = fields.Boolean('is Quota')
    is_job_title = fields.Boolean('is Job Title')
    is_working_day = fields.Boolean('is Working Day')
    is_umk = fields.Boolean('is UMK')
    is_basic_salary = fields.Boolean('is Basic Salary')
    is_meal_allowance = fields.Boolean('is Meal Allowance')
    is_transport_allowance = fields.Boolean('is Transport Allowance')
    is_positional_allowance = fields.Boolean('is Positional Allowance')
    is_cost_travelling = fields.Boolean('is Cost Traveling')
    is_motorcycle = fields.Boolean('is Motorcycle')
    is_rent_computer = fields.Boolean('is Rent Computer')
    is_bbm = fields.Boolean('is BBM')
    is_credit = fields.Boolean('is Credit')
    is_internet = fields.Boolean('is Internet')
    is_cosmetic_allowance = fields.Boolean('is Cosmetic Allowance')
    is_working_time_allowance = fields.Boolean('is Working Time Allowance')
    is_job_allowance = fields.Boolean('is Job Allowance')
    is_deptstore_allowance = fields.Boolean('is Deptstore Allowance')
    is_general_allowance = fields.Boolean('is General Allowance')
    is_end_of_year_gift = fields.Boolean('is End of Year Gift')
    is_pencadangan_tali_kasih = fields.Boolean('is Pencadangan Tali Kasih')
    is_insentive = fields.Boolean('is Insentive')
    is_total_honor = fields.Boolean('is Total Honor')
    is_overtime = fields.Boolean('is Overtime')
    is_operational = fields.Boolean('is Operational')
    is_uniform_and_safety_shoes = fields.Boolean('is Uniform and Safety Shoes')
    is_medical_check_up = fields.Boolean('is Medical Check Up')
    is_kost = fields.Boolean('is Kost')
    is_medical = fields.Boolean('is Medical')
    is_bpjs_tk = fields.Boolean('is BPJS Ketenagakerjaan')
    is_bpjs_ks = fields.Boolean('is BPJS Kesehatan')
    is_pensiun = fields.Boolean('is Pensiun')
    is_overhead = fields.Boolean('is Overhead')
    is_bank_transfer = fields.Boolean('is Bank Transfer')
    is_budget_meeting = fields.Boolean('is Budget Meeting')
    is_stationary = fields.Boolean('is Stationary')
    is_transport_meeting = fields.Boolean('is Transport Meeting')
    is_thr = fields.Boolean('is THR')
    is_compensation = fields.Boolean('is Compensation')
    is_total_person = fields.Boolean('is Total Person')
    is_subtotal_honor = fields.Boolean('is Subtotal Honor')
    is_subtotal_honor_per_year = fields.Boolean('is Subtotal Honor Per Year')
    # Change name while creating Rate Card, Number format is Number Sequence - Partner Name
    @api.model
    def create(self, vals):
        no = self.env['ir.sequence'].next_by_code('rate.card')
        vals['name'] = no + '-' + self.env['res.partner'].search([('id', '=', vals['partner_id'])]).name
        return super(RateCard, self).create(vals)
    # Hide field based on Rate Card Category (Optional in Rate Card Category Line)
    @api.onchange('ratecard_category_id')
    def _hide(self):
        if self.ratecard_category_id:
            self.hide = False
            for rec in self.ratecard_category_id.ratecard_category_line_ids:
                if rec.field_name == 'area':
                    self.is_area = rec.field_active
                if rec.field_name == 'quota':
                    self.is_quota = rec.field_active
                if rec.field_name == 'job_title':
                    self.is_job_title = rec.field_active
                if rec.field_name == 'working_day':
                    self.is_working_day = rec.field_active
                if rec.field_name == 'umk':
                    self.is_umk = rec.field_active
                if rec.field_name == 'basic_salary':
                    self.is_basic_salary = rec.field_active
                if rec.field_name == 'meal_allowance':
                    self.is_meal_allowance = rec.field_active
                if rec.field_name == 'transport_allowance':
                    self.is_transport_allowance = rec.field_active
                if rec.field_name == 'positional_allowance':
                    self.is_positional_allowance = rec.field_active
                if rec.field_name == 'cost_travelling':
                    self.is_cost_travelling = rec.field_active
                if rec.field_name == 'motorcycle':
                    self.is_motorcycle = rec.field_active
                if rec.field_name == 'rent_computer':
                    self.is_rent_computer = rec.field_active
                if rec.field_name == 'bbm':
                    self.is_bbm = rec.field_active
                if rec.field_name == 'credit':
                    self.is_credit = rec.field_active
                if rec.field_name == 'internet':
                    self.is_internet = rec.field_active
                if rec.field_name == 'cosmetic_allowance':
                    self.is_cosmetic_allowance = rec.field_active
                if rec.field_name == 'working_time_allowance':
                    self.is_working_time_allowance = rec.field_active
                if rec.field_name == 'job_allowance':
                    self.is_job_allowance = rec.field_active
                if rec.field_name == 'deptstore_allowance':
                    self.is_deptstore_allowance = rec.field_active
                if rec.field_name == 'general_allowance':
                    self.is_general_allowance = rec.field_active
                if rec.field_name == 'end_of_year_gift':
                    self.is_end_of_year_gift = rec.field_active
                if rec.field_name == 'pencadangan_tali_kasih':
                    self.is_pencadangan_tali_kasih = rec.field_active
                if rec.field_name == 'insentive':
                    self.is_insentive = rec.field_active
                if rec.field_name == 'total_honor':
                    self.is_total_honor = rec.field_active
                if rec.field_name == 'overtime':
                    self.is_overtime = rec.field_active
                if rec.field_name == 'operational':
                    self.is_operational = rec.field_active
                if rec.field_name == 'uniform_and_safety_shoes':
                    self.is_uniform_and_safety_shoes = rec.field_active
                if rec.field_name == 'medical_check_up':
                    self.is_medical_check_up = rec.field_active
                if rec.field_name == 'kost':
                    self.is_kost = rec.field_active
                if rec.field_name == 'medical':
                    self.is_medical = rec.field_active
                if rec.field_name == 'bpjs_tk':
                    self.is_bpjs_tk = rec.field_active
                if rec.field_name == 'bpjs_ks':
                    self.is_bpjs_ks = rec.field_active
                if rec.field_name == 'pensiun':
                    self.is_pensiun = rec.field_active
                if rec.field_name == 'overhead':
                    self.is_overhead = rec.field_active
                if rec.field_name == 'bank_transfer':
                    self.is_bank_transfer = rec.field_active
                if rec.field_name == 'budget_meeting':
                    self.is_budget_meeting = rec.field_active
                if rec.field_name == 'stationary':
                    self.is_stationary = rec.field_active
                if rec.field_name == 'transport_meeting':
                    self.is_transport_meeting = rec.field_active
                if rec.field_name == 'thr':
                    self.is_thr = rec.field_active
                if rec.field_name == 'compensation':
                    self.is_compensation = rec.field_active
                if rec.field_name == 'total_person':
                    self.is_total_person = rec.field_active
                if rec.field_name == 'subtotal_honor':
                    self.is_subtotal_honor = rec.field_active
                if rec.field_name == 'subtotal_honor_per_year':
                    self.is_subtotal_honor_per_year = rec.field_active
        else:
            self.hide = True
            self.ratecard_line_ids.unlink()
    
class RateCardLine(models.Model):
    _name = 'rate.card.line'
    _description = 'Rate Card Line'

    ratecard_id = fields.Many2one('rate.card', string='Rate Card', required=True, index=True, copy=False)
    area = fields.Many2one('city.city', string='Area')
    quota = fields.Float(string='Quota', default=0.00)
    job_title = fields.Char(string='Job Title')
    working_day = fields.Float(string='HK/Working Day', default=0.00)
    umk = fields.Float(string='UMK', default=0.00)
    basic_salary = fields.Float(string='Basic Salary', default=0.00)
    meal_allowance = fields.Float(string='Meal Allowance', default=0.00)
    transport_allowance = fields.Float(string='Transport Allowance', default=0.00)
    positional_allowance = fields.Float(string='Positional Allowance', default=0.00)
    cost_travelling = fields.Float(string='Cost Traveling', default=0.00)
    motorcycle = fields.Float(string='Motorcycle', default=0.00)
    rent_computer = fields.Float(string='Rent Computer', default=0.00)
    bbm = fields.Float(string='BBM', default=0.00)
    credit = fields.Float(string='Credit', default=0.00)
    internet = fields.Float(string='Internet', default=0.00)
    cosmetic_allowance = fields.Float(string='Cosmetic Allowance', default=0.00)
    working_time_allowance = fields.Float(string='Working Time Allowance', default=0.00)
    job_allowance = fields.Float(string='Job Allowance', default=0.00)
    deptstore_allowance = fields.Float(string='Deptstore Allowance', default=0.00)
    general_allowance = fields.Float(string='General Allowance', default=0.00)
    end_of_year_gift = fields.Float(string='End of Year Gift', default=0.00)
    pencadangan_tali_kasih = fields.Float(string='Pencadangan Tali Kasih', default=0.00)
    insentive = fields.Float(string='Insentive', default=0.00)
    total_honor = fields.Float(string='Honor', compute='_depends_total_honor', store=True, default=0.00)
    medical_check_up = fields.Float(string='Medical Check Up', default=0.00)
    kost = fields.Float(string='Kost', default=0.00)
    medical = fields.Float(string='Medical', compute='_depends_medical', store=True, default=0.00)
    bpjs_tk = fields.Float(string='BPJS Ketenagakerjaan', compute='_depends_bpjs_tk', store=True, default=0.00)
    bpjs_ks = fields.Float(string='BPJS Kesehatan', compute='_depends_bpjs_ks', store=True, default=0.00)
    pensiun = fields.Float(string='Pensiun', compute='_depends_pensiun', store=True, default=0.00)
    overhead = fields.Float(string='Overhead', default=0.00)
    bank_transfer = fields.Float(string='Bank Transfer', default=0.00)
    budget_meeting = fields.Float(string='Budget Meeting', default=0.00)
    stationary = fields.Float(string='Stationary', default=0.00)
    transport_meeting = fields.Float(string='Transport Meeting', default=0.00)
    thr = fields.Float(string='THR', default=0.00)
    compensation = fields.Float(string='Compensation', default=0.00)
    total_person = fields.Float(string='Total Person', compute='_depends_total_person', store=True, default=0.00)
    subtotal_honor = fields.Float(string='Total Honor', compute='_depends_subtotal_honor', store=True, default=0.00)
    subtotal_honor_per_year = fields.Float(string='Total Honor Per Year', compute='_depends_subtotal_honor_per_year', store=True, default=0.00)
    # Change Area name (city.city) while called by other class 
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, '%s - %s' %(record.area.name, record.job_title)))
        return result
    # Compute Total Honor
    @api.depends('basic_salary','meal_allowance','credit','cosmetic_allowance','working_time_allowance','job_allowance','deptstore_allowance','general_allowance','end_of_year_gift')
    def _depends_total_honor(self):
        for r in self:
            for i in r.ratecard_id.ratecard_category_id.ratecard_category_line_ids:
                data_id = i.search([('id', '=', i.id)])
                if i.field_name == 'total_honor':
                    if not i.field_condition and not i.field_active:
                        r.total_honor = 0.0
                    if i.field_condition:
                        raw = i.field_condition
                        raw_split = raw.split()
                        for d in raw_split:
                            if d in raw_split:
                                data = data_id.search([('field_code', '=', d)])
                                if data:
                                    if data.field_active:
                                        raw = str(raw).replace(d, str(r[data.field_name]))
                                    else:
                                        raise UserError(_('The field %s in selected Rate Card Category must be set active first!', data.field_name))
                                elif not data and d not in ['*', '+', '-', '/', '(', ')'] and (d.isdecimal() != True and isinstance(float(d), float) != True):
                                    raise UserError(_('Code %s is not found in selected Rate Card Category!', d))
                        r.total_honor = float(eval(raw))
    # Compute Medical
    @api.depends('basic_salary')
    def _depends_medical(self):
        for r in self:
            for i in r.ratecard_id.ratecard_category_id.ratecard_category_line_ids:
                data_id = i.search([('id', '=', i.id)])
                if i.field_name == 'medical':
                    if not i.field_condition and not i.field_active:
                        r.medical = 0.0
                    if i.field_condition:
                        raw = i.field_condition
                        raw_split = raw.split()
                        for d in raw_split:
                            if d in raw_split:
                                data = data_id.search([('field_code', '=', d)])
                                if data:
                                    if data.field_active:
                                        raw = str(raw).replace(d, str(r[data.field_name]))
                                    else:
                                        raise UserError(_('The field %s in selected Rate Card Category must be set active first!', data.field_name))
                                elif not data and d not in ['*', '+', '-', '/', '(', ')'] and (d.isdecimal() != True and isinstance(float(d), float) != True):
                                    raise UserError(_('Code %s is not found in selected Rate Card Category!', d))
                        r.medical = float(eval(raw))
    # Compute BPJS TK
    @api.depends('basic_salary')
    def _depends_bpjs_tk(self):
        for r in self:
            for i in r.ratecard_id.ratecard_category_id.ratecard_category_line_ids:
                data_id = i.search([('id', '=', i.id)])
                if i.field_name == 'bpjs_tk':
                    if not i.field_condition and not i.field_active:
                        r.bpjs_tk = 0.0
                    if i.field_condition:
                        raw = i.field_condition
                        raw_split = raw.split()
                        for d in raw_split:
                            if d in raw_split:
                                data = data_id.search([('field_code', '=', d)])
                                if data:
                                    if data.field_active:
                                        raw = str(raw).replace(d, str(r[data.field_name]))
                                    else:
                                        raise UserError(_('The field %s in selected Rate Card Category must be set active first!', data.field_name))
                                elif not data and d not in ['*', '+', '-', '/', '(', ')'] and (d.isdecimal() != True and isinstance(float(d), float) != True):
                                    raise UserError(_('Code %s is not found in selected Rate Card Category!', d))
                        r.bpjs_tk = float(eval(raw))
    # Compute BPJS KS
    @api.depends('basic_salary')
    def _depends_bpjs_ks(self):
        for r in self:
            for i in r.ratecard_id.ratecard_category_id.ratecard_category_line_ids:
                data_id = i.search([('id', '=', i.id)])
                if i.field_name == 'bpjs_ks':
                    if not i.field_condition and not i.field_active:
                        r.bpjs_ks = 0.0
                    if i.field_condition:
                        raw = i.field_condition
                        raw_split = raw.split()
                        for d in raw_split:
                            if d in raw_split:
                                data = data_id.search([('field_code', '=', d)])
                                if data:
                                    if data.field_active:
                                        raw = str(raw).replace(d, str(r[data.field_name]))
                                    else:
                                        raise UserError(_('The field %s in selected Rate Card Category must be set active first!', data.field_name))
                                elif not data and d not in ['*', '+', '-', '/', '(', ')'] and (d.isdecimal() != True and isinstance(float(d), float) != True):
                                    raise UserError(_('Code %s is not found in selected Rate Card Category!', d))
                        r.bpjs_ks = float(eval(raw))
    # Compute Pensiun
    @api.depends('basic_salary')
    def _depends_pensiun(self):
        for r in self:
            for i in r.ratecard_id.ratecard_category_id.ratecard_category_line_ids:
                data_id = i.search([('id', '=', i.id)])
                if i.field_name == 'pensiun':
                    if not i.field_condition and not i.field_active:
                        r.pensiun = 0.0
                    if i.field_condition:
                        raw = i.field_condition
                        raw_split = raw.split()
                        for d in raw_split:
                            if d in raw_split:
                                data = data_id.search([('field_code', '=', d)])
                                if data:
                                    if data.field_active:
                                        raw = str(raw).replace(d, str(r[data.field_name]))
                                    else:
                                        raise UserError(_('The field %s in selected Rate Card Category must be set active first!', data.field_name))
                                elif not data and d not in ['*', '+', '-', '/', '(', ')'] and (d.isdecimal() != True and isinstance(float(d), float) != True):
                                    raise UserError(_('Code %s is not found in selected Rate Card Category!', d))
                        r.pensiun = float(eval(raw))
    # Compute BPJS KS
    @api.depends('basic_salary')
    def _depends_bpjs_ks(self):
        for r in self:
            for i in r.ratecard_id.ratecard_category_id.ratecard_category_line_ids:
                data_id = i.search([('id', '=', i.id)])
                if i.field_name == 'bpjs_ks':
                    if not i.field_condition and not i.field_active:
                        r.bpjs_ks = 0.0
                    if i.field_condition:
                        raw = i.field_condition
                        raw_split = raw.split()
                        for d in raw_split:
                            if d in raw_split:
                                data = data_id.search([('field_code', '=', d)])
                                if data:
                                    if data.field_active:
                                        raw = str(raw).replace(d, str(r[data.field_name]))
                                    else:
                                        raise UserError(_('The field %s in selected Rate Card Category must be set active first!', data.field_name))
                                elif not data and d not in ['*', '+', '-', '/', '(', ')'] and (d.isdecimal() != True and isinstance(float(d), float) != True):
                                    raise UserError(_('Code %s is not found in selected Rate Card Category!', d))
                        r.bpjs_ks = float(eval(raw))
    # Compute Total Person
    @api.depends('total_honor','medical','bpjs_tk','bpjs_ks','pensiun')
    def _depends_total_person(self):
        for r in self:
            for i in r.ratecard_id.ratecard_category_id.ratecard_category_line_ids:
                data_id = i.search([('id', '=', i.id)])
                if i.field_name == 'total_person':
                    if not i.field_condition and not i.field_active:
                        r.total_person = 0.0
                    if i.field_condition:
                        raw = i.field_condition
                        raw_split = raw.split()
                        for d in raw_split:
                            if d in raw_split:
                                data = data_id.search([('field_code', '=', d)])
                                if data:
                                    if data.field_active:
                                        raw = str(raw).replace(d, str(r[data.field_name]))
                                    else:
                                        raise UserError(_('The field %s in selected Rate Card Category must be set active first!', data.field_name))
                                elif not data and d not in ['*', '+', '-', '/', '(', ')'] and (d.isdecimal() != True and isinstance(float(d), float) != True):
                                    raise UserError(_('Code %s is not found in selected Rate Card Category!', d))
                        r.total_person = float(eval(raw))
    # Compute Total Honor
    @api.depends('quota','total_person')
    def _depends_subtotal_honor(self):
        for r in self:
            for i in r.ratecard_id.ratecard_category_id.ratecard_category_line_ids:
                data_id = i.search([('id', '=', i.id)])
                if i.field_name == 'subtotal_honor':
                    if not i.field_condition and not i.field_active:
                        r.subtotal_honor = 0.0
                    if i.field_condition:
                        raw = i.field_condition
                        raw_split = raw.split()
                        for d in raw_split:
                            if d in raw_split:
                                data = data_id.search([('field_code', '=', d)])
                                if data:
                                    if data.field_active:
                                        raw = str(raw).replace(d, str(r[data.field_name]))
                                    else:
                                        raise UserError(_('The field %s in selected Rate Card Category must be set active first!', data.field_name))
                                elif not data and d not in ['*', '+', '-', '/', '(', ')'] and (d.isdecimal() != True and isinstance(float(d), float) != True):
                                    raise UserError(_('Code %s is not found in selected Rate Card Category!', d))
                        r.subtotal_honor = float(eval(raw))
    # Compute Total Honor Per Year
    @api.depends('quota','total_person')
    def _depends_subtotal_honor_per_year(self):
        for r in self:
            for i in r.ratecard_id.ratecard_category_id.ratecard_category_line_ids:
                data_id = i.search([('id', '=', i.id)])
                if i.field_name == 'subtotal_honor_per_year':
                    if not i.field_condition and not i.field_active:
                        r.subtotal_honor_per_year = 0.0
                    if i.field_condition:
                        raw = i.field_condition
                        raw_split = raw.split()
                        for d in raw_split:
                            if d in raw_split:
                                data = data_id.search([('field_code', '=', d)])
                                if data:
                                    if data.field_active:
                                        raw = str(raw).replace(d, str(r[data.field_name]))
                                    else:
                                        raise UserError(_('The field %s in selected Rate Card Category must be set active first!', data.field_name))
                                elif not data and d not in ['*', '+', '-', '/', '(', ')'] and (d.isdecimal() != True and isinstance(float(d), float) != True):
                                    raise UserError(_('Code %s is not found in selected Rate Card Category!', d))
                        r.subtotal_honor_per_year = float(eval(raw))
                        
class RateCardCategory(models.Model):
    _name = 'rate.card.category'
    _description = 'Rate Card Categotry'
    
    name = fields.Char(string='Name', required=True)
    is_active = fields.Boolean(string='Active')
    ratecard_category_line_ids = fields.One2many('rate.card.category.line', 'ratecard_category_id', string='Rate Card Category Line')
    # Check Name
    @api.constrains('name')
    def _check_name(self):
        for r in self:
            res = r.search([('name', '=ilike', r.name),('id', '!=', r.id)])
            if res:
                raise ValidationError(_('Name must be unique!')) 
    # Query and append data to One2many (rate.card.category.line)
    @api.model
    def default_get(self, fields):
        res=super(RateCardCategory,self).default_get(fields)
        data = []
        query = self.env.cr.execute("""
                                    select column_name, data_type, col_description('public.rate_card_line'::regclass, ordinal_position)
                                    from information_schema.columns
                                    where table_schema = 'public' and table_name = 'rate_card_line';
                                    """)
        get_data = self.env.cr.fetchall()
        for i in get_data:
            if i[0] not in ['id', 'create_uid', 'create_date', 'write_uid', 'write_date', 'ratecard_id']:
                value = {
                    'field_name' : i[0],
                    'field_desc' : '' if i[2] == None else i[2],
                    'field_code' : '',
                    'field_condition' : '',
                }
                data.append((0, 0, value))
        res['ratecard_category_line_ids'] = data
        return res

class RateCardCategoryLine(models.Model):
    _name = 'rate.card.category.line'
    _description = 'Rate Card Category Line'
    
    ratecard_category_id = fields.Many2one('rate.card.category')
    field_name = fields.Char(string='Field Name')
    field_desc = fields.Char(string='Field Description')
    field_code = fields.Char(string='Code')
    field_condition = fields.Char(string='Condition')
    field_active = fields.Boolean(string='Active', default=False)