# © 2018 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Event',
    'version': '11.0.1.0.0',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'LGPL-3',
    'category': 'Project Management',
    'summary': 'Project Event module',
    'depends': [
        'base',
        'auditlog',
        'project',
        'mail',
        'hr',
        'project_resource_calendar',
        'web_widget_color',
    ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
        'data/auditlog_rule.xml',
        'data/channels.xml',
        'data/ir_sequence_data.xml',
        'data/task_categories.xml',
        'security/ir.model.access.csv',
        'security/project_security.xml',
        'views/auditlog_log.xml',
        'views/project_project_view.xml',
        'views/project_task_view.xml',
        'views/event_template_view.xml',
        'views/activity_template_view.xml',
        'views/task_template_view.xml',
        'templates/assets.xml',
        'wizard/project_event_wizard_view.xml',
        'wizard/reservation_validation_wiz_view.xml',
    ],
    'installable': True,
    'application': False,
}
