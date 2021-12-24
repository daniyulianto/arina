# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from werkzeug.exceptions import NotFound
from odoo.addons.website_hr_recruitment.controllers.main import WebsiteHrRecruitment  # Import the class
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.exceptions import UserError, ValidationError
import json
import base64


class CustomeWebsiteHrRecruitment(WebsiteHrRecruitment):

    @http.route('''/jobs/apply/<model("hr.job"):job>''', type='http', auth="public", website=True, sitemap=True)
    def jobs_apply(self, job, **kwargs):
        if not job.can_access_from_current_website():
            raise NotFound()

        error = {}
        default = {}
        province = request.env['province.province'].sudo().search([])
        city = request.env['city.city'].sudo().search([])
        employee_education = request.env['hr.employee.education'].sudo().search([])
        bank = request.env['res.bank'].sudo().search([])
        nik_applicant = []
        applicant = request.env['hr.applicant'].sudo().search([])
        for rec in applicant:
            nik_applicant.append(rec.no_ktp)
        if 'website_hr_recruitment_error' in request.session:
            error = request.session.pop('website_hr_recruitment_error')
            default = request.session.pop('website_hr_recruitment_default')
        return request.render("website_hr_recruitment.apply", {
            'job': job,
            'error': error,
            'default': default,
            'province': province,
            'city': city,
            'employee_education': employee_education,
            'bank': bank,
            'state': 'first',
            'nik_applicant': nik_applicant,
        })

    @http.route('''/job/success/''', type='http', auth="public", website=True, sitemap=True)
    def job_success_page_action(self, **rec):
        if not rec:
            return request.render('website_hr_recruitment.thankyou')
        else:
            data = []
            Applicant = request.env['hr.applicant']
            if request.params.get('nik', False):
                no_ktp = Applicant.sudo().search([('no_ktp', 'ilike', rec.get("nik"))])
                if no_ktp:
                    msg = 'No KTP sudah pernah digunakan pada pendaftaran.'
                    notification = json.dumps({'error_fields': {'nik': msg}})
                    return ValidationError(notification)
            file_ktp = rec.get("ktp_pict", False)
            file_ijazah = rec.get("foto_ijazah", False)
            file_skck = rec.get("foto_skck", False)
            image_applicant = rec.get("foto_profile", False)
            file_refrensi = rec.get("foto_refrensi", False)
            file_tabungan_image = rec.get("tabungan_image", False)
            file_foto_npwp = rec.get("foto_npwp", False)
            file_foto_bpjtk = rec.get("foto_bpjtk", False)
            file_foto_bpjsks = rec.get("foto_bpjsks", False)
            file_surat_sehat = rec.get("surat_sehat", False)
            file_foto_asuransi = rec.get("foto_asuransi", False)
            file_pict_vaksin = rec.get("pict_vaksin", False)
            file_kartu_keluarga = rec.get("foto_kk", False)
            vals = {
                'name': rec['partner_name'] + ' Application',
                'partner_name': rec['partner_name'],
                'partner_mobile': rec['partner_phone'],
                'job_id': int(rec['job_id']) or False,
                'department_id': rec['department_id'],
                'email_from': rec['email_from'],
                'no_ktp': rec['nik'],
                'ktp_address': rec['partner_address'],
                'ktp_city': int(rec['kota_ktp']) or False,
                'domicile_address': rec['partner_domicile'],
                'domicile_city': int(rec['kota_domisili']) or False,
                'province_id': rec['province_domisili'],
                'birth': rec['birth'],
                'place_of_birth': rec['kota_lahir'],
                'gender': rec['gender_employee'],
                'height': rec['height'],
                'weight': rec['weight'],
                'religion': rec['religion_employee'],
                'marital_status': rec['status_nikah'],
                'social_media': rec['social_media_name'],
                'education_id': rec['employee_education'],
                'major_education': rec['jurusan'],
                'bank_id': rec['bank_name'],
                'account_number': rec['rekening_number'],
                'account_name': rec['rekening_name'],
                'no_kk': rec['kk_number'],
                'no_npwp': rec['npwp_number'],
                'no_bpjsks': rec['nomor_bpjstk'],
                'no_bpkstk': rec['nomor_bpjstk'],
                'assurance': rec['asuransi'],
                'vaksin_status': rec['status_vaksin'],
                'emergency_name': rec['contact_emergency'],
                'emergency_mobile': rec['contact_emergency_number'],
                'emergency_relation': rec['jenis_relasi'],
                'husban_or_wife': rec['husband_or_wife'],
                'mother_name': rec['mother_name'],
                'first_child': rec['first_child_name'],
                'second_child': rec['second_child_name'],
                'third_child': rec['third_child_name'],
                'first_child_birth': False if rec['child_birth'] == '' else rec['child_birth'],
                'second_child_birth': False if rec['child_birth2'] == '' else rec['child_birth2'],
                'third_child_birth': False if rec['child_birth3'] == '' else rec['child_birth3'],
                'file_ktp': base64.b64encode(file_ktp.read()),
                'file_name_ktp': file_ktp.filename,
                'file_ijazah': base64.b64encode(file_ijazah.read()),
                'file_name_ijazah': file_ijazah.filename,
                'image_applicant': base64.b64encode(image_applicant.read()),
                'file_name_image_applicant': image_applicant.filename,
                'file_skck': base64.b64encode(file_skck.read()),
                'file_name_skck': file_skck.filename,
                'file_surat_refrensi': base64.b64encode(file_refrensi.read()),
                'file_name_surat_refrensi': file_refrensi.filename,
                'file_buku_tabungan': base64.b64encode(file_tabungan_image.read()),
                'file_name_buku_tabungan': file_tabungan_image.filename,
                'file_npwp': base64.b64encode(file_foto_npwp.read()),
                'file_name_npwp': file_foto_npwp.filename,
                'file_bpjstk': base64.b64encode(file_foto_bpjtk.read()),
                'file_name_bpjstk': file_foto_bpjtk.filename,
                'file_bpjsks': base64.b64encode(file_foto_bpjsks.read()),
                'file_name_bpjsks': file_foto_bpjsks.filename,
                'file_surat_sehat': base64.b64encode(file_surat_sehat.read()),
                'file_name_surat_sehat': file_surat_sehat.filename,
                'file_asuransi': base64.b64encode(file_foto_asuransi.read()),
                'file_name_asuransi': file_foto_asuransi.filename,
                'file_kartu_vaksin': base64.b64encode(file_pict_vaksin.read()),
                'file_name_kartu_vaksin': file_pict_vaksin.filename,
                'file_kk': base64.b64encode(file_kartu_keluarga.read()),
                'file_name_kk': file_kartu_keluarga.filename,
            }
            data.append(vals)
            new_applicant = request.env['hr.applicant'].sudo().create(data)
            return request.render("website_hr_recruitment.thankyou", {'new_applicant': new_applicant})
