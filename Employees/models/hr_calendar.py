from odoo import fields,api,models

class Employees_Calendar(models.Model):
    _inherit='resource.calendar'
    user_id=fields.Many2one('res.users')