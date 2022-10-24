from odoo import fields,api,models

class Employees_Leave_Type(models.Model):
    _name="employees.leave.type"
    _description="Employees Leave Type"
    _order='sequence'
    name=fields.Char(string="Name",required=True)
    sequence = fields.Integer(default=100,
                              help='The type with the smallest sequence is the default value in time off request',
                              readonly=True,invisible=True)