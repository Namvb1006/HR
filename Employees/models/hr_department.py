from odoo import models,fields,api
from odoo.exceptions import ValidationError
class Employees_Department(models.Model):
    _name="employees.department"
    _description="Employees Department"
    name=fields.Char('Department',required=True,trim=True)
    id_employees=fields.One2many('employees.information','department')
    parent_id=fields.Many2one('employees.department',string='Parent Department',index=True)
    child_ids=fields.One2many('employees.department','parent_id',string='Child Department')
    _sql_constraints=[('check_name','unique(name)','The Name of Department has been created')]
    @api.constrains('parent_id')
    def check_parent_id(self):
         if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive departments.'))
    
    
    
  