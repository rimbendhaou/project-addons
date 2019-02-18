# @ 2018 Savoir-failre Linux
# License LGPL-3.0 or Later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta


class ProjectActivityWizard(models.TransientModel):
    """Wizard Event Activity Creation from template"""
    _name = 'project.activity.wizard'
    _description = __doc__

    event_wizard_id = fields.Many2one(
        'project.event.wizard',
        string='Event Wizard',
    )
    template_id = fields.Many2one(
        'activity.template',
        string='Activity Template',
    )
    name = fields.Char(
        string='Activity Title',
    )
    activity_resp_id = fields.Many2one(
        'res.partner',
        string='Responsible',
    )
    activity_partner_id = fields.Many2one(
        'res.partner',
        string='Client',
    )
    category_id = fields.Many2one(
        'task.category',
        string='Category',
    )
    room_id = fields.Many2one(
        'resource.calendar.room',
        string='Room',
    )
    date_start = fields.Datetime(
        string='Starting Date',
        default=fields.Datetime.now,
    )
    date_end = fields.Datetime(
        string='Ending Date',
    )
    description = fields.Html(
        string='Description',
    )
    notes = fields.Html(
        string='Notes',
    )
    task_line_ids = fields.One2many(
        'project.task.wizard',
        'activity_wiz_id',
        string='Tasks to Edit',
    )

    @api.onchange('template_id')
    def _onchange_template_id(self):
        if self.template_id:
            self.name = self.template_id.name
            self.activity_resp_id = self.template_id.temp_resp_id
            self.category_id = self.template_id.category_id
            self.room_id = self.template_id.room_id
            self.description = self.template_id.description
            self.notes = self.template_id.notes

    @api.multi
    def add_flexible_tasks(self):
        self.ensure_one()
        view = self.env.ref(
            'project_event.view_project_task_wizard_activity')

        for task in self.template_id.task_template_ids:
            task_vals = {
                'template_id': task.id,
                'activity_wiz_id': self.id,
                'task_name': task.name,
                'task_resp_id': task.temp_resp_id.id,
                'category_id': task.category_id.id,
                'resource_type': task.resource_type,
                'equipment_id': task.equipment_id.id,
                'room_id': task.room_id.id,
                'department_id': task.department_id.id,
                'employee_ids': [(4, e.id) for e in task.employee_ids],
                'duration': task.duration,
                'start_time': task.start_time,
                'description': task.description,
                'notes': task.notes,
            }
            self.env['project.task.wizard'].create(task_vals)

        return {
            'name': _('Tasks Wizard'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': self._name,
            'views': [(view.id, 'form')],
            'target': 'new',
            'res_id': self.id,
        }

    @api.multi
    def create_activity_from_template(self):
        self.ensure_one()
        tasks = self.env['project.task.wizard'].search([
            ('activity_wiz_id', '=', self.id)])
        activity_vals = {
            'name': self.name,
            'responsible_id': self.activity_resp_id.id,
            'partner_id': self.activity_partner_id.id,
            'category_id': self.category_id.id,
            'activity_task_type': 'activity',
            'room_id': self.room_id.id,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'description': self.description,
            'notes': self.notes,
            'is_from_template': True,
            'child_ids': [
                (0,
                 0,
                 {
                     'name': task.task_name,
                     'activity_task_type': 'task',
                     'responsible_id': task.task_resp_id.id,
                     'partner_id': task.task_partner_id.id,
                     'category_id': task.category_id.id,
                     'department_id': task.department_id.id,
                     'employee_ids': [(4, e.id) for e in task.employee_ids],
                     'resource_type': task.resource_type,
                     'equipment_id': task.equipment_id.id,
                     'room_id': task.room_id.id,
                     'date_start': (
                         fields.Datetime.from_string(
                             self.date_start) + relativedelta(
                             minutes=task.start_time)
                     ),
                     'date_end': (
                         fields.Datetime.from_string(
                             self.date_start) + relativedelta(
                             minutes=task.start_time + task.duration)
                     ),
                     'notes': task.notes,
                     'description': task.description,
                     'is_from_template': True,
                     'is_main_task': task.template_id.is_main_task,
                 }
                 ) for task in tasks],
        }
        self.env['project.task'].create(activity_vals)
