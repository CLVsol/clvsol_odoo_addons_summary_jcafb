# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime
import pytz
import os
import base64

import xlwt

from odoo import api, fields, models, _
from odoo.exceptions import Warning
from odoo.tools import human_size

_logger = logging.getLogger(__name__)


class Residence(models.Model):
    _inherit = 'clv.residence'

    summary_id = fields.Many2one(
        comodel_name='clv.summary',
        string='Summary',
        ondelete='restrict',
        readonly='True'
    )
    date_summary = fields.Datetime(
        string='Summary Date',
        related='summary_id.date_summary',
        store=False
    )

    def _residence_summary_setup(self, dir_path, file_name):

        SummaryTemplate = self.env['clv.summary.template']
        Summary = self.env['clv.summary']

        model_name = 'clv.residence'

        for residence in self:

            _logger.info(u'%s %s', '>>>>> (residence):', residence.name)

            summary_templates = SummaryTemplate.search([
                ('model', '=', model_name),
            ])

            for summary_template in summary_templates:

                _logger.info(u'%s %s', '>>>>>>>>>> (summary_template):', summary_template.name)

                summary = Summary.with_context({'active_test': False}).search([
                    ('model', '=', model_name),
                    ('res_id', '=', residence.id),
                    ('action', '=', summary_template.action),
                ])

                if summary.id is False:

                    summary_values = {}
                    summary_values['model'] = model_name
                    summary_values['res_id'] = residence.id
                    # summary_values['method'] = summary_template.method
                    summary_values['action'] = summary_template.action
                    _logger.info(u'>>>>>>>>>>>>>>> %s %s',
                                 '(summary_values):', summary_values)
                    summary = Summary.create(summary_values)

                _logger.info(u'%s %s', '>>>>>>>>>>>>>>> (summary):', summary)

                residence.summary_id = summary.id

                action_call = 'self.env["clv.summary"].' + \
                    summary.action + \
                    '(summary, residence)'

                _logger.info(u'%s %s', '>>>>>>>>>>', action_call)

                if action_call:

                    # summary.state = 'Unknown'
                    # summary.outcome_text = False

                    exec(action_call)

            self.env.cr.commit()

            summary._residence_summary_export_xls(summary, residence, dir_path, file_name)


class Summary(models.Model):
    _inherit = 'clv.summary'

    def _residence_summary(self, summary, model_object):

        _logger.info(u'%s %s', '>>>>>>>>>>>>>>> (model_object):', model_object.name)

        date_summary = datetime.now()

        Document = self.env['clv.document']
        SummaryDocument = self.env['clv.summary.document']
        LabTestRequest = self.env['clv.lab_test.request']
        LabTestResult = self.env['clv.lab_test.result']
        LabTestReport = self.env['clv.lab_test.report']
        SummaryLabTestRequest = self.env['clv.summary.lab_test.request']
        SummaryLabTestResult = self.env['clv.summary.lab_test.result']
        SummaryLabTestReport = self.env['clv.summary.lab_test.report']
        SummaryEvent = self.env['clv.summary.event']
        Patient = self.env['clv.patient']
        SummaryPatient = self.env['clv.summary.patient']

        summary_documents = SummaryDocument.search([
            ('summary_id', '=', summary.id),
        ])
        summary_documents.unlink()

        summary_lab_test_requests = SummaryLabTestRequest.search([
            ('summary_id', '=', summary.id),
        ])
        summary_lab_test_requests.unlink()

        summary_lab_test_results = SummaryLabTestResult.search([
            ('summary_id', '=', summary.id),
        ])
        summary_lab_test_results.unlink()

        summary_lab_test_reports = SummaryLabTestReport.search([
            ('summary_id', '=', summary.id),
        ])
        summary_lab_test_reports.unlink()

        summary_events = SummaryEvent.search([
            ('summary_id', '=', summary.id),
        ])
        summary_events.unlink()

        summary_patients = SummaryPatient.search([
            ('summary_id', '=', summary.id),
        ])
        summary_patients.unlink()

        search_domain = [
            ('ref_id', '=', model_object._name + ',' + str(model_object.id)),
        ]
        documents = Document.search(search_domain)
        lab_test_requests = LabTestRequest.search(search_domain)
        lab_test_results = LabTestResult.search(search_domain)
        lab_test_reports = LabTestReport.search(search_domain)

        search_domain = [
            ('residence_id', '=', model_object.id),
        ]
        patients = Patient.search(search_domain)

        for document in documents:

            if document.phase_id.id == model_object.phase_id.id:

                values = {
                    'summary_id': summary.id,
                    'document_id': document.id,
                }
                SummaryDocument.create(values)

        for lab_test_request in lab_test_requests:

            if lab_test_request.phase_id.id == model_object.phase_id.id:

                values = {
                    'summary_id': summary.id,
                    'lab_test_request_id': lab_test_request.id,
                }
                SummaryLabTestRequest.create(values)

        for lab_test_result in lab_test_results:

            if lab_test_result.phase_id.id == model_object.phase_id.id:

                values = {
                    'summary_id': summary.id,
                    'lab_test_result_id': lab_test_result.id,
                }
                SummaryLabTestResult.create(values)

        for lab_test_report in lab_test_reports:

            if lab_test_report.phase_id.id == model_object.phase_id.id:

                values = {
                    'summary_id': summary.id,
                    'lab_test_report_id': lab_test_report.id,
                }
                SummaryLabTestReport.create(values)

        for patient in patients:

            if patient.state not in ['unavailable']:

                values = {
                    'summary_id': summary.id,
                    'patient_id': patient.id,
                }
                SummaryPatient.create(values)

                search_domain = [
                    ('ref_id', '=', 'clv.patient' + ',' + str(patient.id)),
                ]
                documents = Document.search(search_domain)
                lab_test_requests = LabTestRequest.search(search_domain)

                for document in documents:

                    if document.phase_id.id == patient.phase_id.id:

                        values = {
                            'summary_id': summary.id,
                            'document_id': document.id,
                        }
                        SummaryDocument.create(values)

                for lab_test_request in lab_test_requests:

                    if lab_test_request.phase_id.id == patient.phase_id.id:

                        values = {
                            'summary_id': summary.id,
                            'lab_test_request_id': lab_test_request.id,
                        }
                        SummaryLabTestRequest.create(values)

        summary_values = {}
        summary_values['date_summary'] = date_summary
        summary.write(summary_values)

    def _residence_summary_export_xls(self, summary, model_object, dir_path, file_name):

        _logger.info(u'%s %s', '>>>>>>>>>>>>>>> (model_object):', model_object.name)

        model_object_name = model_object._name.replace('.', '_')
        model_object_code = model_object.code

        FileSystemDirectory = self.env['clv.file_system.directory']
        file_system_directory = FileSystemDirectory.search([
            ('directory', '=', dir_path),
        ])

        file_name = file_name.replace('<model>', model_object_name).replace('<code>', model_object_code)
        file_path = dir_path + '/' + file_name
        wbook = xlwt.Workbook()
        sheet = wbook.add_sheet(file_name[8:])

        for i in range(12):
            sheet.col(i).width = 256 * 7
        sheet.show_grid = False

        row_nr = 0

        row_nr += 1
        row = sheet.row(row_nr)
        row.write(0, 'Summary for:')
        row.write(3, self.reference_name)
        row_nr += 1
        row = sheet.row(row_nr)
        row.write(0, 'Summary date:')

        # user_tz = self.env.user.tz
        user_tz = 'America/Argentina/Buenos_Aires'
        local = pytz.timezone(user_tz)
        date_summary_utc = pytz.utc.localize(self.date_summary)
        date_summary_local = date_summary_utc.astimezone(local)
        date_summary_local_str = datetime.strftime(date_summary_local, '%d-%m-%Y %H:%M:%S')

        row.write(3, date_summary_local_str)
        row_nr += 1
        row = sheet.row(row_nr)
        row.write(0, 'Responsible Employee:')
        row.write(3, model_object.employee_id.name)
        row_nr += 1

        row_nr += 1
        row = sheet.row(row_nr)
        row.write(0, 'Residence:')
        row.write(3, model_object.name)
        row_nr += 1
        row = sheet.row(row_nr)
        row.write(3, model_object.district)
        row_nr += 1
        row = sheet.row(row_nr)
        row.write(0, 'Residence Categories:')
        row.write(3, model_object.category_ids.name)
        row_nr += 1
        row = sheet.row(row_nr)
        row.write(0, 'Residence Code:')
        row.write(3, model_object.code)
        row_nr += 1
        row = sheet.row(row_nr)
        row.write(0, 'Residence State:')
        row.write(3, model_object.state)
        row_nr += 1

        row_nr += 1
        row = sheet.row(row_nr)
        row.write(0, 'Patient ')
        row.write(5, 'Code')
        row.write(7, 'Birthday')
        # row.write(8, 'Reference Age')
        # row.write(10, 'Categories')
        # row.write(12, 'Status')
        row.write(9, 'Categories')
        row.write(11, 'Status')
        row_nr += 1
        sheet.row(row_nr).height_mismatch = True
        sheet.row(row_nr).height = 20 * 4
        row_nr += 1

        for summary_patient in self.summary_patient_ids:

            row = sheet.row(row_nr)
            row.write(0, summary_patient.patient_id.name)
            row.write(5, summary_patient.patient_id.code)

            if summary_patient.patient_id.birthday is not False:
                row.write(7, datetime.strftime(summary_patient.patient_id.birthday, '%d-%m-%Y'))
            # if summary_patient.patient_id.age_reference is not False:
            #     row.write(8, summary_patient.patient_id.age_reference)
            # if summary_patient.patient_category_ids.name is not False:
            #     row.write(10, summary_patient.patient_category_ids.name)
            # row.write(12, summary_patient.patient_state)
            if summary_patient.patient_category_ids.name is not False:
                row.write(9, summary_patient.patient_category_ids.name)
            row.write(11, summary_patient.patient_state)
            row_nr += 1

        row_nr += 1
        row = sheet.row(row_nr)
        row.write(0, 'Document ')
        row.write(2, 'Code')
        row.write(4, 'Categories')
        row_nr += 1
        sheet.row(row_nr).height_mismatch = True
        sheet.row(row_nr).height = 20 * 4
        row_nr += 1

        for summary_document in self.summary_document_ids:

            row = sheet.row(row_nr)
            row.write(0, summary_document.document_id.document_type_id.name)
            row.write(2, summary_document.document_id.code)
            row.write(4, summary_document.document_category_ids.name)
            row_nr += 1

        row_nr += 1
        row = sheet.row(row_nr)
        row.write(0, 'Lab Test Type ')
        row.write(8, 'Lab Test Request')
        row_nr += 1
        sheet.row(row_nr).height_mismatch = True
        sheet.row(row_nr).height = 20 * 4
        row_nr += 1

        for summary_lab_test_request in self.summary_lab_test_request_ids:

            row = sheet.row(row_nr)
            row.write(0, summary_lab_test_request.lab_test_type_ids.name)
            row.write(8, summary_lab_test_request.lab_test_request_id.code)
            row_nr += 1

        wbook.save(file_path)

        self.directory_id = file_system_directory.id
        self.file_name = file_name
        self.stored_file_name = file_name

        model_object.directory_id = file_system_directory.id
        model_object.file_name = file_name
        model_object.stored_file_name = file_name


class Residence_2(models.Model):
    _inherit = "clv.residence"

    file_name = fields.Char(string='File Name')
    file_content = fields.Binary(
        string='File Content',
        compute='_compute_file'
    )
    stored_file_name = fields.Char(string='Stored File Name')
    directory_id = fields.Many2one(
        comodel_name='clv.file_system.directory',
        string='Directory'
    )

    def _file_read(self, fname, bin_size=False):

        def file_not_found(fname):
            raise Warning(_(
                '''Error while reading file %s.
                Maybe it was removed or permission is changed.
                Please refresh the list.''' % fname))

        self.ensure_one()
        r = ''
        directory = self.directory_id.get_dir() or ''
        full_path = directory + fname
        if not (directory and os.path.isfile(full_path)):
            # file_not_found(fname)
            return False
        try:
            if bin_size:
                r = human_size(os.path.getsize(full_path))
            else:
                # r = open(full_path, 'rb').read().encode('base64')
                r = base64.b64encode(open(full_path, 'rb').read())
        except (IOError, OSError):
            _logger.info("_read_file reading %s", fname, exc_info=True)
        return r

    @api.depends('stored_file_name')
    def _compute_file(self):
        bin_size = self._context.get('bin_size')
        for file in self:
            content = False
            if file.stored_file_name:
                content = file._file_read(file.stored_file_name, bin_size)
            file.file_content = content
