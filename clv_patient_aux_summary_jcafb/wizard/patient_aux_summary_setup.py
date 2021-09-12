# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PatientAuxSummarySetUp(models.TransientModel):
    _description = 'Patient (Aux) Summary SetUp'
    _name = 'clv.patient_aux.summary_setup'

    def _default_patient_aux_ids(self):
        return self._context.get('active_ids')
    patient_aux_ids = fields.Many2many(
        comodel_name='clv.patient_aux',
        relation='clv_patient_aux_summary_setup_rel',
        string='Patients (Aux)',
        default=_default_patient_aux_ids
    )

    def _default_dir_path(self):
        file_store_path = self.env['ir.config_parameter'].sudo().get_param(
            'clv.global_settings.current_filestore_path', '').strip()
        summary_files_directory = self.env['ir.config_parameter'].sudo().get_param(
            'clv.global_settings.current_summary_files_directory', '').strip()
        return file_store_path + '/' + summary_files_directory
    dir_path = fields.Char(
        string='Directory Path',
        required=True,
        help="Directory Path",
        default=_default_dir_path
    )

    def _default_file_name(self):
        summary_file_name = self.env['ir.config_parameter'].sudo().get_param(
            'clv.global_settings.current_summary_file_name', '').strip()
        return summary_file_name
    file_name = fields.Char(
        string='File Name',
        required=True,
        help="File Name",
        default=_default_file_name
    )

    def _reopen_form(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
        return action

    def do_patient_aux_summary_setup(self):
        self.ensure_one()

        for patient_aux in self.patient_aux_ids:

            _logger.info(u'%s %s', '>>>>>', patient_aux.name)

            patient_aux._patient_aux_summary_setup(self.dir_path, self.file_name)

        return True

    def do_populate_all_patient_auxs(self):
        self.ensure_one()

        PatientAux = self.env['clv.patient_aux']
        patient_auxs = PatientAux.search([])

        self.patient_aux_ids = patient_auxs

        return self._reopen_form()
