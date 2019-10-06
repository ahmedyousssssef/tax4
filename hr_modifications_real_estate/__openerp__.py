# -*- coding: utf-8 -*-
{
    'name': "hr_modifications_real_estate",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base' ,'hr', 'hr_contract', 'hr_recruitment', 'hr_holidays', 'hr_payroll'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/hr_applicant_hr_inherit_view.xml',
        'views/hr_automated_actions_view.xml',
        'views/hr_inherit_job_positions_view.xml',
        'views/isky_hr_contract_view.xml',
        'views/isky_hr_employee_view.xml',
        'views/isky_hr_excuse_request_view.xml',
        'views/isky_hr_holidays_view.xml',
        'views/isky_hr_payroll_view.xml',
        'views/isky_recruitment_state_log_view.xml',
        'views/menu_item_view.xml',
        #data
        'data/social_insurance_salary_rule.xml',
        'data/contract_cron.xml',
        #reports
        "report/excuse_report_view.xml",
        "report/blue_collar_contract_report_view.xml",
        "report/acceptance_job_report_view.xml",
        "report/full_time_report_view.xml",
        "report/filing_tracker_report_view.xml",
        "report/hiring_checklist_report_view.xml",
        "report/part_time_report_view.xml",
        "report/all_reports_view.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}