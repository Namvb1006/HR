from odoo import models,fields,api,_
from datetime import timedelta
from odoo.exceptions import UserError,ValidationError
class Employees_Project(models.Model):
    _name='employees.project'
    _description='Employees Project'
    name=fields.Char(string='Name Project',required=True)
    project_employees=fields.One2many('employees.information','project_id')
    validity=fields.Integer(default=7)
    date_deadline=fields.Date(compute="compute_total",store=True)
    user_id=fields.Many2one(related="project_employees.user_id",group="Employees.group_employees_manager")
    state=fields.Selection(selection=[('draft','Draft'),('in process','In Process'),('cancel','Cancel'),('finish','Finish')], default='draft')


    
    @api.depends("validity","create_date")
    def compute_total(self):
        for record in self:
            tmp=timedelta(days=record.validity)
            if record.create_date:
                record.date_deadline=record.create_date+tmp
            else:
                record.date_deadline=fields.Date.today()+tmp
                
    
    def action_in_process(self):
        for record in self:
            record.write({'state':'in process'})
    
    def action_cancel(self):
        for record in self:
            record.write({'state':'cancel'})
    
    def action_finish(self):
        for record in self:
            record.write({'state':'finish'})        
    

    def action_test(self):
       pass
    