# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Patient (Aux) Summary (for CLVhealth-JCAFB Solution)',
    'summary': 'Patient (Aux) Summary Module used in CLVhealth-JCAFB Solution.',
    'version': '14.0.5.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_patient_aux_jcafb',
        'clv_summary',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/patient_aux_summary.xml',
        'views/summary_view.xml',
        'wizard/patient_aux_summary_setup_view.xml',
    ],
    'demo': [],
    'test': [],
    'init_xml': [],
    'test': [],
    'update_xml': [],
    'installable': True,
    'application': False,
    'active': False,
    'css': [],
}
