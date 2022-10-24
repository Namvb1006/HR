from odoo import models,fields,api
from odoo.exceptions import UserError,ValidationError
from datetime import timedelta

class Employees_Payslip(models.Model):
        _name='employees.payslip'
        _description='Employees Payslip'
        name=fields.Char(string='Name',required=True)
        worked_hours=fields.Float(string='Worked hours',compute="_compute_total_hours")
        paid_rate=fields.Float(string='Paid rates')
        insurance_fee=fields.Float(string='Insurance fee')
        lunch_fee=fields.Float(string='Lunch fee',default=20000)
        lunch_days=fields.Integer(string='Lunch days',default=0)
        currency_id = fields.Many2one('res.currency', string='Currency')
        total_paid = fields.Monetary(string='Total Paid',store=True,currency_field='currency_id',compute='_compute_total_paid',default=0,group_operator="max")
        
        def default_employees(self):
            return self.env['employees.information'].search([('user_id','=', self.env.user.id)])
        
        employees_id=fields.Many2one('employees.information', default = default_employees)
        user_id=fields.Many2one('res.users', related = 'employees_id.user_id', group="Employees.group_employees_manager")
        _sql_constraints=[('check_total_paid','CHECK(total_paid>=0)','The Total Paid have to greater than zero')]
        
        @api.depends('employees_id')
        def _compute_total_hours(self):
            for record in self:
                if record.employees_id:
                    count_worked_hours=self.env['employees.attendance'].search([('employees_id','=',record.employees_id.id)])
                    record.worked_hours=sum(count_worked_hours.mapped('valid_worked_hours'))
                else:
                    record.worked_hours=0.0
            
        @api.depends('worked_hours','paid_rate','insurance_fee','lunch_fee','lunch_days')
        def _compute_total_paid(self):
            for record in self:
                record.total_paid=(record.worked_hours*record.paid_rate)-(record.lunch_days*record.lunch_fee)-record.insurance_fee