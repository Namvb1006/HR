from odoo import models,api,fields

class Employees_Add_Department_Wizard(models.TransientModel):
    _name='add.department.wizard'
    _description='Add Department Wizard'
    department=fields.Many2one('employees.department')
    def action_confirm(self):
        employees_id=self.env["employees.information"].browse(self.env.context['active_ids'])
        new_data={}
        if self.department:
            new_data.update({"department":self.department})
            employees_id.write(new_data)
        
    