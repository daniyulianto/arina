from odoo import models, fields, tools, api, _
from odoo.modules.module import get_module_resource
import base64
from odoo.exceptions import UserError


class Applicant(models.Model):
    _inherit = 'hr.applicant'

    ratecard_id = fields.Many2one('rate.card', string='Ratecard', compute='_compute_ratecard', store=True, )
    quota_id = fields.Many2one('quota.quota', string='Quota', compute='_compute_quota', store=True, )
    stage_arina = fields.Selection(
        related='stage_id.stage_arina', store=True)
    employee_id = fields.Many2one('hr.employee', string='ARO', compute='_compute_aro', store=True, )
    karyawan_status = fields.Selection(string='Status Karyawan', related='quota_id.status_karyawan', store=True)
    grade = fields.Char(string='Grade')
    ktp_address = fields.Char(string='Alamat KTP')
    ktp_city = fields.Many2one('city.city', string='Kota KTP')
    domicile_address = fields.Char(string='Alamat Domisili')
    domicile_city = fields.Many2one('city.city', string='Kota Domisili')
    province_id = fields.Many2one('province.province', string='Provinsi Domisili')
    birth = fields.Date(string='Tanggal Lahir')
    place_of_birth = fields.Many2one('city.city', string='Kota Lahir')
    no_ktp = fields.Char(string='No. KTP')
    nip = fields.Char(string='NIP')
    gender = fields.Selection([
        ("male", "Male"), ("female", "Female")], string='Gender')
    height = fields.Integer(string='Height')
    weight = fields.Integer(string='Weight')
    religion = fields.Char(string='Religion')
    marital_status = fields.Selection([
        ("k0", "K/0 - Nikah, Tanpa Anak"), ("k1", "K/1 - Nikah, Anak 1"), ("k2", "K/2 - Nikah, Anak 2"),
        ("k3", "K/3 - Nikah, Anak 3"), ("tk0", "Belum Menikah"), ("tk1", "TK/1 - Tidak Nikah, 1 Tanggungan"),
        ("tk2", "TK/2 - Tidak Nikah, 2 Tanggungan"), ("tk3", "TK/3 - Tidak Nikah, 3 Tanggungan")],
        string='Status Kawin')
    social_media = fields.Char(string='Nama Social Media')
    education_id = fields.Many2one('hr.employee.education', string='Pendidikan Terakhir')
    major_education = fields.Char(string='Jurusan')
    bank_id = fields.Many2one('res.bank', string='Nama Bank')
    account_number = fields.Char(sting='Nomor Rekening')
    account_name = fields.Char(string='Atas Nama Rekening')
    no_kk = fields.Char(string='No. KK')
    have_npwp = fields.Boolean(string='Tidak Memiliki NPWP', default=False)
    no_npwp = fields.Char(string='No. NPWP')
    no_bpjsks = fields.Char(string='No. BPJS KES')
    no_bpkstk = fields.Char(string='No. BPJS TK')
    assurance = fields.Char(string='Asuransi Tambahan')
    vaksin_status = fields.Selection([("vaksin", "Sudah Vaksin"), ("not_vaksin", "Belum Vaksin")],
                                     string='Status Vaksin')
    principle_id = fields.Many2one('res.partner', "Principle", related='quota_id.partner_id', store=True)
    priciple_division_id = fields.Many2one('principle.division', "Divisi")
    representative_office = fields.Many2one('representative.office', string='Kantor Perwakilan')
    second_city = fields.Many2one('city.city', string='Second City')
    emergency_name = fields.Char(string='Contact Name')
    emergency_mobile = fields.Char(string='Contact Number', size=32)
    emergency_relation = fields.Selection(
        [("parent", "Orang Tua"), ("husband_wife", "Suami/Istri"), ("siblings", "Sudara Kandung"),
         ("uncle_aunt", "Paman / Bibi"), ("others", "Lainnya")])
    mother_name = fields.Char(string='Nama Ibu Kandung')
    husban_or_wife = fields.Char(string='Nama Suami/Istri')
    first_child = fields.Char(string='Nama Anak Pertama ')
    second_child = fields.Char(string='Nama Anak Kedua')
    third_child = fields.Char(string='Nama Anak Ketiga')
    first_child_birth = fields.Date(string='Tanggal Lahir Anak ')
    second_child_birth = fields.Date(string='Tanggal Lahir')
    third_child_birth = fields.Date(string='Tanggal Lahir')
    image_applicant = fields.Binary(string='File Foto Applicant', attachment=True,
                                    max_width=128, max_height=128)
    file_name_image_applicant = fields.Char('Foto Applicant')
    file_ktp = fields.Binary(string='File KTP', attachment=True)
    file_name_ktp = fields.Char('File Name KTP')
    file_ijazah = fields.Binary(string='File Ijazah', attachment=True)
    file_name_ijazah = fields.Char('File Name ijazah')
    file_skck = fields.Binary(string='File SKSCK', attachment=True)
    file_name_skck = fields.Char('File Name Surat Refrensi')
    file_surat_refrensi = fields.Binary(string='File Surat Refrensi', attachment=True)
    file_name_surat_refrensi = fields.Char('File Name Surat Refrensi')
    file_buku_tabungan = fields.Binary(string='File Buku Tabungan', attachment=True)
    file_name_buku_tabungan = fields.Char('File Name Buku Tabungan')
    file_npwp = fields.Binary(string='File NPWP', attachment=True)
    file_name_npwp = fields.Char('File Name NPWP')
    file_bpjstk = fields.Binary(string='File BPJSTK', attachment=True)
    file_name_bpjstk = fields.Char('File Name BPJSTK')
    file_bpjsks = fields.Binary(string='File BPJSKES', attachment=True)
    file_name_bpjsks = fields.Char('File Name BPJSKESs')
    file_asuransi = fields.Binary(string='File Asuransi', attachment=True)
    file_name_asuransi = fields.Char('File Name Asuransi')
    file_kartu_vaksin = fields.Binary(string='File Kartu Vaksin', attachment=True)
    file_name_kartu_vaksin = fields.Char('File Name Kartu Vaksin')
    file_kk = fields.Binary(string='File Kartu Kelaurga', attachment=True)
    file_name_kk = fields.Char('File Name Kartu Kelaurga')
    file_surat_sehat = fields.Binary(string='File Surat Sehat', attachment=True)
    file_name_surat_sehat = fields.Char('File Name Surat Sehat')
    file_form_interview = fields.Binary(string='Form Interview Dengan Ttd Principle', attachment=True)
    file_name_form_interview = fields.Char('File Form Interview')
    file_elerning = fields.Binary(string='Sertifikat Elerning', attachment=True)
    file_name_elerning = fields.Char('File Name Elerning')
    start_date_contract = fields.Date(string='Tanggal Mulai Kontrak')
    end_date_contract = fields.Date(string='Tanggal Selesai Kontrak')
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
    is_allowed = fields.Boolean(compute='_is_allowed')

    @api.depends('stage_arina')
    def _is_allowed(self):
        for rec in self:
            if rec.stage_arina == 'first_interview':
                rec.is_allowed = self.user_has_groups(
                    'asb_hr_recruitment.group_hr_recruitment_ro1')
            elif rec.stage_arina not in ['first_interview', 'applicant_data']:
                rec.is_allowed = self.user_has_groups(
                    'asb_hr_recruitment.group_hr_recruitment_ro2')
            else:
                rec.is_allowed = True

    @api.depends('job_id')
    def _compute_ratecard(self):
        for applicant in self:
            applicant.ratecard_id = applicant.job_id.ratecard_id.id or False

    @api.depends('job_id')
    def _compute_quota(self):
        for applicant in self:
            applicant.quota_id = applicant.job_id.quota_id.id or False

    @api.depends('job_id')
    def _compute_aro(self):
        for applicant in self:
            applicant.employee_id = applicant.job_id.aro_id.id or False

    def action_nextstep(self):
        for rec in self:
            if rec.stage_arina == 'applicant_data':
                stage_id = rec.stage_id.search([('stage_arina', '=', 'first_interview')])
                rec.write({'stage_id': stage_id.id})
            elif rec.stage_arina == 'first_interview':
                stage_id = rec.stage_id.search([('stage_arina', '=', 'second_interview')])
                rec.write({'stage_id': stage_id.id})
            elif rec.stage_arina == 'second_interview':
                stage_id = rec.stage_id.search([('stage_arina', '=', 'principal_approval')])
                rec.nip = self.env['ir.sequence'].next_by_code('nip_employee')
                rec.write({'stage_id': stage_id.id})
            elif rec.stage_arina == 'principal_approval':
                stage_id = rec.stage_id.search([('stage_arina', '=', 'e_learning')])
                rec.write({'stage_id': stage_id.id})
            elif rec.stage_arina == 'e_learning':
                stage_id = rec.stage_id.search([('stage_arina', '=', 'pkwt_created')])
                rec.write({'stage_id': stage_id.id})
            elif rec.stage_arina == 'pkwt_created':
                stage_id = rec.stage_id.search([('stage_arina', '=', 'joined')])
                rec.write({'stage_id': stage_id.id})

    def action_backstep(self):
        for rec in self:
            if rec.stage_arina == 'first_interview':
                stage_id = rec.stage_id.search([('stage_arina', '=', 'applicant_data')])
                rec.write({'stage_id': stage_id.id})
            elif rec.stage_arina == 'second_interview':
                stage_id = rec.stage_id.search([('stage_arina', '=', 'first_interview')])
                rec.write({'stage_id': stage_id.id})
            elif rec.stage_arina == 'principal_approval':
                stage_id = rec.stage_id.search([('stage_arina', '=', 'second_interview')])
                rec.write({'stage_id': stage_id.id})
            elif rec.stage_arina == 'e_learning':
                stage_id = rec.stage_id.search([('stage_arina', '=', 'principal_approval')])
                rec.write({'stage_id': stage_id.id})
            elif rec.stage_arina == 'pkwt_created':
                stage_id = rec.stage_id.search([('stage_arina', '=', 'e_learning')])
                rec.write({'stage_id': stage_id.id})
            elif rec.stage_arina == 'joined':
                stage_id = rec.stage_id.search([('stage_arina', '=', 'pkwt_created')])
                rec.write({'stage_id': stage_id.id})

    def create_employee_from_applicant(self):
        """ Create an hr.employee from the hr.applicants """
        employee = False
        for applicant in self:
            contact_name = False
            if applicant.partner_id:
                address_id = applicant.partner_id.address_get(['contact'])['contact']
                contact_name = applicant.partner_id.display_name
            else:
                if not applicant.partner_name:
                    raise UserError(_('You must define a Contact Name for this applicant.'))
                new_partner_id = self.env['res.partner'].create({
                    'is_company': False,
                    'type': 'private',
                    'name': applicant.partner_name,
                    'email': applicant.email_from,
                    'phone': applicant.partner_phone,
                    'mobile': applicant.partner_mobile
                })
                applicant.partner_id = new_partner_id
                address_id = new_partner_id.address_get(['contact'])['contact']
            if applicant.partner_name or contact_name:
                employee_data = {
                    'name': applicant.partner_name or contact_name,
                    'job_id': applicant.job_id.id,
                    'job_title': applicant.job_id.name,
                    'address_home_id': address_id,
                    'department_id': applicant.department_id.id or False,
                    'address_id': applicant.company_id and applicant.company_id.partner_id
                                  and applicant.company_id.partner_id.id or False,
                    'work_email': applicant.department_id and applicant.department_id.company_id
                                  and applicant.department_id.company_id.email or False,
                    'work_phone': applicant.department_id.company_id.phone,
                    'applicant_id': applicant.ids,
                    'ratecard_id': applicant.ratecard_id.id,
                    'quota_id': applicant.quota_id.id,
                    'grade': applicant.grade,
                    'aro_id': applicant.employee_id.id,
                    'registration_number': applicant.nip,
                    # Education
                    'study_field': applicant.major_education,
                    'education_id': applicant.education_id.id,
                    # Private Contact
                    'image_1920': applicant.image_applicant,
                    'identification_id': applicant.no_ktp,
                    'birthday': applicant.birth,
                    'place_of_birth': applicant.place_of_birth.name,
                    'mobile_phone': applicant.partner_mobile,
                    'account_number': applicant.account_number,
                    'account_name': applicant.account_name,
                    # Citizenship
                    'gender': applicant.gender,
                    'marital_status': applicant.marital_status,
                    'no_kk': applicant.no_kk,
                    'no_npwp': applicant.no_npwp,
                    'domicile_address': applicant.domicile_address,
                    'domicile_city': applicant.domicile_city.id,
                    'province_id': applicant.domicile_city.id,
                    'height': applicant.height,
                    'weight': applicant.weight,
                    'religion': applicant.religion,
                    'social_media': applicant.social_media,
                    # Emergency
                    'emergency_contact': applicant.emergency_name,
                    'emergency_phone': applicant.emergency_mobile,
                    'emergency_relation': applicant.emergency_relation,
                    # Assurance
                    'no_bpjsks': applicant.no_bpjsks,
                    'no_bpkstk': applicant.no_bpkstk,
                    'assurance': applicant.assurance,
                    'vaksin_status': applicant.vaksin_status,
                    # Princple Detail
                    'partner_id': applicant.partner_id.id,
                    'priciple_division_id': applicant.priciple_division_id.id,
                    'representative_office': applicant.representative_office.id,
                    'second_city': applicant.second_city.id,
                    # Family
                    'mother_name': applicant.mother_name,
                    'husban_or_wife': applicant.husban_or_wife,
                    'first_child': applicant.first_child,
                    'second_child': applicant.second_child,
                    'third_child': applicant.third_child,
                    'first_child_birth': applicant.first_child_birth,
                    'second_child_birth': applicant.second_child_birth,
                    'third_child_birth': applicant.third_child_birth,
                    # # File Data Pribadi
                    'file_name_image_applicant': applicant.file_name_image_applicant,
                    'file_ktp': applicant.file_ktp,
                    'file_name_ktp': applicant.file_name_ktp,
                    'file_ijazah': applicant.file_ijazah,
                    'file_name_ijazah': applicant.file_name_ijazah,
                    'file_skck': applicant.file_skck,
                    'file_name_skck': applicant.file_name_skck,
                    'file_surat_refrensi': applicant.file_surat_refrensi,
                    'file_name_surat_refrensi': applicant.file_name_surat_refrensi,
                    'file_buku_tabungan': applicant.file_buku_tabungan,
                    'file_name_buku_tabungan': applicant.file_name_buku_tabungan,
                    'file_npwp': applicant.file_npwp,
                    'file_name_npwp': applicant.file_name_npwp,
                    'file_bpjstk': applicant.file_bpjstk,
                    'file_name_bpjstk': applicant.file_name_bpjstk,
                    'file_bpjsks': applicant.file_bpjsks,
                    'file_name_bpjsks': applicant.file_name_bpjsks,
                    'file_asuransi': applicant.file_asuransi,
                    'file_name_asuransi': applicant.file_name_asuransi,
                    'file_kartu_vaksin': applicant.file_kartu_vaksin,
                    'file_name_kartu_vaksin': applicant.file_name_kartu_vaksin,
                    'file_kk': applicant.file_kk,
                    'file_name_kk': applicant.file_name_kk,
                    'file_surat_sehat': applicant.file_surat_sehat,
                    'file_name_surat_sehat': applicant.file_name_surat_sehat,
                    'file_form_interview': applicant.file_form_interview,
                    'file_name_form_interview': applicant.file_name_form_interview,
                    'file_elerning': applicant.file_elerning,
                    'file_name_elerning': applicant.file_name_elerning,
                }
            employee = self.env['hr.employee'].create(employee_data)
            applicant.write({'emp_id': employee.id})
            address = applicant.emp_id.address_home_id
            address.update({
                'street': applicant.ktp_address,
                'city': applicant.ktp_city.name,
            })
            # contract detail
            self.env['hr.contract'].create({
                'name': applicant.partner_name,
                'employee_id': applicant.emp_id.id,
                'job_id': applicant.job_id.id,
                'date_start': applicant.start_date_contract,
                'date_end': applicant.end_date_contract,
                'is_deposit': applicant.is_deposit,
                'wage': 0,  # temporary for initial wage for contract
                'deposit_amount': applicant.deposit_amount,
                'salary_applicant_rule_ids': applicant.salary_applicant_rule_ids,
                'pkwt_template_id': applicant.pkwt_template_id.id,
                'file_template_pkwt': applicant.file_template_pkwt,
                'file_name_template_pkwt': applicant.file_name_template_pkwt,
                'file_pkwt_ttd': applicant.file_pkwt_ttd,
                'file_name_pkwt_ttd': applicant.file_name_pkwt_ttd,
                'state': 'open'
            })

        employee_action = self.env.ref('hr.open_view_employee_list')
        dict_act_window = employee_action.read([])[0]
        dict_act_window['context'] = {'form_view_initial_mode': 'edit'}
        dict_act_window['res_id'] = employee.id
        return dict_act_window


class HrTemplatePKWT(models.Model):
    _name = "hr.template.pkwt"
    _description = "Template PKWT"

    name = fields.Char('Template Name')
    file_template_pkwt = fields.Binary(string='Template PKWT', attachment=True)
    file_name_template_pkwt = fields.Char('File Name Template PKWT')


class HrSalaryApplicantRule(models.Model):
    _name = "hr.salary.applicant.rule"
    _description = "Salary Applicant Rule Line"

    rule_id = fields.Many2one('hr.salary.rule', string='Rule')
    name = fields.Char('Rule Code', related='rule_id.code',
                       index=True, store=True)
    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    currency_id = fields.Many2one('res.currency', 'Currency', readonly=True,
                                  default=lambda s: s.env.ref('base.IDR'))
    amount = fields.Monetary(string='Amount')


class HrRecruitmentStage(models.Model):
    _inherit = 'hr.recruitment.stage'

    stage_arina = fields.Selection([
        ('applicant_data', 'Data Pelamar'),
        ('first_interview', 'First Interview'),
        ('second_interview', 'Second Interview'),
        ('principal_approval', 'Principle Approval'),
        ('e_learning', 'E Learning'),
        ('pkwt_created', 'Pembuatan PKWT'),
        ('joined', 'Joined'),
    ], 'Related Arina Recruitment Stage', copy=False)

    _sql_constraints = [
        ('stage_arina_uniq', 'unique(stage_arina)',
         'There is already Recruitment Stage linked with selected Arina Recruitment Stage!'),
    ]
