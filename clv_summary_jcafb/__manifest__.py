# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Summary (customizations for CLVhealth-JCAFB Solution)',
    'summary': 'Summary Module customizations for CLVhealth-JCAFB Solution.',
    'version': '14.0.5.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_document_jcafb',
        'clv_lab_test_jcafb',
        'clv_event_jcafb',
        'clv_person_jcafb',
        'clv_summary',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/file_system.xml',
        'data/global_settings.xml',
        'views/summary_document_view.xml',
        'views/summary_lab_test_request_view.xml',
        'views/summary_lab_test_result_view.xml',
        'views/summary_lab_test_report_view.xml',
        'views/summary_event_view.xml',
        'views/summary_address_view.xml',
        'views/summary_family_view.xml',
        'views/summary_person_view.xml',
        'views/global_settings_view.xml',
        'wizard/summary_setup_view.xml',
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
