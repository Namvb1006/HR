from datetime import datetime
from pytz import timezone, UTC
from dateutil.relativedelta import relativedelta

from odoo import fields,api,models
from odoo.exceptions import UserError,ValidationError
from pip._internal import self_outdated_check


class Employees_Attendance(models.Model):
    _name='employees.attendance'
    _description="Employees Attendance"
    _rec_name="employees_id"
    
    def default_employees(self):
        return self.env['employees.information'].search([('user_id','=', self.env.user.id)])
    
    employees_id=fields.Many2one('employees.information', readonly=True, default = default_employees )
    check_in=fields.Datetime(string="Check In",help="Check In Employees",readonly=True)
    check_out=fields.Datetime(string="Check Out",readonly=True)
    late_attendance_hours=fields.Float(string="Late Hours",compute="_compute_late_hours",store=True,readonly=True)
    early_attendance_hours=fields.Float(string="Early Hours",compute="_compute_early_hours",store=True,readonly=True)
    valid_worked_hours=fields.Float("Worked Hours",compute="_compute_worked_hours",readonly=True,store=True)
    user_id=fields.Many2one(comodel_name="res.users", related="employees_id.user_id")
    state = fields.Selection(selection=[('draft', 'Draft'), ('check_in','Check In'), ('check_out', 'Check Out')], string="State", default='draft')
    def check_time_in(self):
        time_now = fields.Datetime.now()
        self.check_in=time_now
        self.state = 'check_in'
            
    def check_time_out(self):
        time_now = fields.Datetime.now()
        self.check_out=time_now
        self.state = 'check_out'
    
    @api.constrains("check_in","check_out")
    def _check_in_out(self):
        for record in self:
            if  record.check_in and record.check_out:
                if record.check_in>record.check_out:
                    raise ValueError(_("The Check In Time cannot lower than Check out time"))

    @api.depends('check_in', 'check_out')
    def _compute_worked_hours(self):
        for record in self:
            if record.check_out and record.check_in:
                delta = record.check_out - record.check_in
                record.valid_worked_hours = delta.total_seconds() / 3600.0
            else:
                record.valid_worked_hours = False

    @api.depends("check_out")
    def _compute_early_hours(self):
        for record in self:
            if record.check_out:
                user_tz = self.env.user.tz or 'UTC'
                localized_dt = record.check_out.astimezone(timezone(user_tz))
                t=fields.Datetime.now().astimezone(timezone(user_tz)).replace(hour=17,minute=0,second=0)
                delta=localized_dt-t
                record.early_attendance_hours=delta.total_seconds() / 3600.0
                if record.early_attendance_hours<0:
                    record.early_attendance_hours=record.early_attendance_hours*(-1.0)
            else:
                record.check_out=False        
    
    @api.depends("check_in")
    def _compute_late_hours(self):
        for record in self:
            if record.check_in:
                user_tz = self.env.user.tz or 'UTC'
                localized_dt = record.check_in.astimezone(timezone(user_tz))
                t=fields.Datetime.now().astimezone(timezone(user_tz)).replace(hour=8,minute=0,second=0)
                delta=localized_dt-t
                record.late_attendance_hours=delta.total_seconds() / 3600.0
                if record.late_attendance_hours <0:
                    record.late_attendance_hours=record.late_attendance_hours*(-1.0)
            else:
                record.check_in=False
                
                
    def unlink(self):
        for record in self:
            if record.check_in<fields.datetime.today():
                raise UserError(_("You cannot delete the finish days"))
            return super(Employees_Attendance,self).unlink()