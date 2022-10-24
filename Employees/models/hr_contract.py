from odoo import models,fields,api
from datetime import timedelta

class Employees_Contract(models.Model):
    _name='employees.contract'
    _description='Employees Contract'
    name=fields.Char('Contract Name',required=True)
    employees_id=fields.Many2one('employees.information')
    validity=fields.Integer(default=7)
    end_date_contract=fields.Date(compute="compute_date",store=False)
    user_id=fields.Many2one('res.users')
    
    @api.depends("validity","create_date")
    def compute_date(self):
        for record in self:
            tmp=timedelta(record.validity)
            if record.create_date:
                record.end_date_contract=record.create_date+tmp
            else:
                record.end_date_contract=fields.Date.today()+tmp
    
    
    @api.model
    def create(self,vals):
        vals['name']=vals['name'].upper()
        res = super(Employees_Contract, self).create(vals)
        return res
    