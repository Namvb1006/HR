from odoo import models,fields,api
from odoo.exceptions import UserError,ValidationError
class Employees_Information(models.Model):
    _name='employees.information'
    _description='Employees Information'
    
    
    name=fields.Char('Name')
    active=fields.Boolean(group="Employees.group_employees_manager",default=True)
    avatar=fields.Image(string='Avatar',max_width=128, max_height=128)
    first_name=fields.Char("First Name")
    last_name=fields.Char("Last Name")
    age=fields.Float(string='Age',compute='_compute_age')
    job_tittles=fields.Char('Job Tittle',required=True)
    id_employees=fields.Char('ID Employees',required=True)
    gender=fields.Selection(selection=[('Male','Male'),('Female','Female'),('Other','Other')])
    date_of_birth=fields.Date('Date Of Birth')
    nationality=fields.Char('Nationality')
    identification_no=fields.Char('Identification')
    email=fields.Char('Email')
    phone=fields.Char('Phone')
    holidays_count=fields.Integer(compute="_compute_holidays_count")
    attendance_count=fields.Integer(compute="_compute_attendance_count")
    address=fields.Char('Address',default="VietNam")
    department=fields.Many2one('employees.department')
    partner=fields.Many2one('res.partner')
    employees_types=fields.Selection(selection=[('employee','Employee'),('student','Student'),('trainee','Trainee'),('contractor','Contractor'),('freelance','Freelance')])
    work_location=fields.Many2one('res.partner')
    project_id=fields.Many2one('employees.project')
    project_name = fields.Char(related='project_id.name')
    project_date_deadline = fields.Date(related='project_id.date_deadline')
    manager=fields.Many2one('res.users')
    user_id=fields.Many2one('res.users',group="Employees.group_employees_manager")
    update_days=fields.Datetime('The Lastest Update')
    _sql_constraints=[('check_ids_employees','unique(ids_employees)','The ID Employees has been created')]
    holidays_ids=fields.One2many('employees.leave','employees_id')
    attendance_ids=fields.One2many(comodel_name="employees.attendance",inverse_name="employees_id")
    
    
    @api.depends("date_of_birth")
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                record.age=float(fields.date.today().year)-(record.date_of_birth.year)
            else:
                record.age=False
    def name_get(self):
        res=[]
        for employees in self:
            b = employees.name +" " +employees.job_tittles
            res.append((employees.id, b))
        return res
    
    def action_open_attendance_view(self):
        action = self.env['ir.actions.act_window']._for_xml_id('Employees.Employees_Attendance_Action')
        action['domain'] = "[('employees_id','=', {})]".format(self.id)
        return action
    
    def action_open_holidays_view(self):
        action = self.env['ir.actions.act_window']._for_xml_id('Employees.employees_leave_actions')
        action['domain'] = "[('employees_id','=',{})]".format(self.id)
        return action
    
    @api.depends("attendance_ids")
    def _compute_attendance_count(self):
        for record in self:
            if record.attendance_ids:
                record.attendance_count=len(record.attendance_ids)
            else:
                record.attendance_count=False
            
    
    @api.depends("holidays_ids")
    def _compute_holidays_count(self):
        for record in self:
            if record.holidays_ids:
                record.holidays_count=len(record.holidays_ids)
            else:
                record.holidays_count=False
                
    # @api.model
    def create(self,vals):
        vals['name']=vals['first_name']+" "+vals['last_name']
        return super(Employees_Information,self).create(vals)

    # def test(self):
    #     public_user=self.env.ref('Employees.group_employees_user')
    #     ids=public_user.read()[0]['users']
    #     list_users=self.env['res.users'].browse(ids).exists()
    #     public_information=self.with_user(public_user)
    #     print(public_information.read())
    # def write(self,vals):
    #     if 'first_name' in vals and 'last_name' not in vals:
    #         vals['name']=vals['first_name']+" "+self.last_name
    #     elif 'first_name' not in vals and 'last_name' in vals:
    #         vals['name']=self.first_name+" "+vals['last_name']
    #
    #     elif 'first_name' in vals and 'last_name' in vals:
    #         vals['name']=vals['first_name']+" "+vals['last_name']
    #
    #     res = super(Employees_Information,self).write(vals)
    #     if not self._context.get('write_update', False):
    #         for r in self:
    #             r = r.with_context(write_update=True)
    #             r.update_days=fields.Datetime.now()




    
    
    