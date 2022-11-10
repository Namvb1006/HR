
from datetime import timedelta
import pytz 
from pytz import timezone, UTC


from odoo.exceptions import UserError,ValidationError
from odoo import fields,api,models,_
class Employees_Leave(models.Model):    
    _name="employees.leave"
    _description="Employees Leave"
    _rec_name="id"
    leave_type_ids=fields.Many2one("employees.leave.type")
    date_from=fields.Date("Start Off")
    date_to=fields.Date("End Off")
    number_of_days=fields.Float(string="Duration",compute="_compute_total_days",store=True)
    number_of_hours=fields.Float(string="Duration",compute="_compute_number_of_hours",store=True)
    name=fields.Text(string="Description")
    def default_employees(self):
        return self.env['employees.information'].search([('user_id','=', self.env.user.id)])
    
    employees_id=fields.Many2one("employees.information", default = default_employees,readonly=True)
    user_id=fields.Many2one(related="employees_id.user_id", group="Employees.group_employees_manager")
    manager=fields.Many2one(related="employees_id.manager",group="Employees.group_employees_manager")
    state=fields.Selection(selection=[('Draft','Draft'),('Confirm','To Approve'),('Refuse','Refuse'),('Validate','Second Approval'),('Validate1','Approved')],
                           default='Draft')
    request_hour_from = fields.Selection([
        ('0', '12:00 AM'), ('0.5', '12:30 AM'),
        ('1', '1:00 AM'), ('1.5', '1:30 AM'),
        ('2', '2:00 AM'), ('2.5', '2:30 AM'),
        ('3', '3:00 AM'), ('3.5', '3:30 AM'),
        ('4', '4:00 AM'), ('4.5', '4:30 AM'),
        ('5', '5:00 AM'), ('5.5', '5:30 AM'),
        ('6', '6:00 AM'), ('6.5', '6:30 AM'),
        ('7', '7:00 AM'), ('7.5', '7:30 AM'),
        ('8', '8:00 AM'), ('8.5', '8:30 AM'),
        ('9', '9:00 AM'), ('9.5', '9:30 AM'),
        ('10', '10:00 AM'), ('10.5', '10:30 AM'),
        ('11', '11:00 AM'), ('11.5', '11:30 AM'),
        ('12', '12:00 PM'), ('12.5', '12:30 PM'),
        ('13', '1:00 PM'), ('13.5', '1:30 PM'),
        ('14', '2:00 PM'), ('14.5', '2:30 PM'),
        ('15', '3:00 PM'), ('15.5', '3:30 PM'),
        ('16', '4:00 PM'), ('16.5', '4:30 PM'),
        ('17', '5:00 PM'), ('17.5', '5:30 PM'),
        ('18', '6:00 PM'), ('18.5', '6:30 PM'),
        ('19', '7:00 PM'), ('19.5', '7:30 PM'),
        ('20', '8:00 PM'), ('20.5', '8:30 PM'),
        ('21', '9:00 PM'), ('21.5', '9:30 PM'),
        ('22', '10:00 PM'), ('22.5', '10:30 PM'),
        ('23', '11:00 PM'), ('23.5', '11:30 PM')], string='Hour from')
    request_hour_to = fields.Selection([
        ('0', '12:00 AM'), ('0.5', '12:30 AM'),
        ('1', '1:00 AM'), ('1.5', '1:30 AM'),
        ('2', '2:00 AM'), ('2.5', '2:30 AM'),
        ('3', '3:00 AM'), ('3.5', '3:30 AM'),
        ('4', '4:00 AM'), ('4.5', '4:30 AM'),
        ('5', '5:00 AM'), ('5.5', '5:30 AM'),
        ('6', '6:00 AM'), ('6.5', '6:30 AM'),
        ('7', '7:00 AM'), ('7.5', '7:30 AM'),
        ('8', '8:00 AM'), ('8.5', '8:30 AM'),
        ('9', '9:00 AM'), ('9.5', '9:30 AM'),
        ('10', '10:00 AM'), ('10.5', '10:30 AM'),
        ('11', '11:00 AM'), ('11.5', '11:30 AM'),
        ('12', '12:00 PM'), ('12.5', '12:30 PM'),
        ('13', '1:00 PM'), ('13.5', '1:30 PM'),
        ('14', '2:00 PM'), ('14.5', '2:30 PM'),
        ('15', '3:00 PM'), ('15.5', '3:30 PM'),
        ('16', '4:00 PM'), ('16.5', '4:30 PM'),
        ('17', '5:00 PM'), ('17.5', '5:30 PM'),
        ('18', '6:00 PM'), ('18.5', '6:30 PM'),
        ('19', '7:00 PM'), ('19.5', '7:30 PM'),
        ('20', '8:00 PM'), ('20.5', '8:30 PM'),
        ('21', '9:00 PM'), ('21.5', '9:30 PM'),
        ('22', '10:00 PM'), ('22.5', '10:30 PM'),
        ('23', '11:00 PM'), ('23.5', '11:30 PM')], string='Hour to')
    # used only when the leave is taken in half days
    request_date_from_period = fields.Selection([
        ('am', 'Morning'), ('pm', 'Afternoon')],
        string="Date Period Start", default='am')
    # request type
    request_unit_half = fields.Boolean('Half Day', compute='_compute_request_unit_half', store=True, readonly=False)
    request_unit_hours = fields.Boolean('Custom Hours', compute='_compute_request_unit_hours', store=True, readonly=False)
    request_unit_custom = fields.Boolean('Days-long custom hours', compute='_compute_request_unit_custom', store=True, readonly=False)
    number_of_days_display = fields.Float(
        'Duration in days', compute='_compute_number_of_days_display', readonly=True,
        help='Number of days of the time off request according to your working schedule. Used for interface.')
    number_of_hours_display = fields.Float(
        'Duration in hours', compute='_compute_number_of_hours_display', readonly=True,
        help='Number of hours of the time off request according to your working schedule. Used for interface.')
    
    
    
    @api.depends('leave_type_ids', 'request_unit_hours', 'request_unit_custom')
    def _compute_request_unit_half(self):
        for record in self:
            if record.leave_type_ids or record.request_unit_hours or record.request_unit_custom:
                record.request_unit_half = False

    @api.depends('leave_type_ids', 'request_unit_half', 'request_unit_custom')
    def _compute_request_unit_hours(self):
        for record in self:
            if record.leave_type_ids or record.request_unit_half or record.request_unit_custom:
                record.request_unit_hours = False

    @api.depends('leave_type_ids', 'request_unit_half', 'request_unit_hours')
    def _compute_request_unit_custom(self):
        for record in self:
            if record.leave_type_ids or record.request_unit_half or record.request_unit_hours:
                record.request_unit_custom = False
    
 
    @api.constrains("date_from","date_to")
    def _check_date(self):
        for record in self:
            if record.date_from<fields.Date.today():
                raise ValidationError(_("YOU CANNOT CHOOSSE DATE IN THE PAST"))
            elif record.date_to<record.date_from:
                raise ValidationError(_("THE END CANNOT LOWER THAN THE START DATE "))
    
    @api.depends("date_from","date_to")
    def _compute_total_days(self):
        for record in self:
            if record.date_from and record.date_to:
                tmp=record.date_to-record.date_from
                record.number_of_days=float(tmp.days)
            else:
                record.number_of_days=False
    
    @api.depends("number_of_days")
    def _compute_number_of_days_display(self):
        for record in self:
            record.number_of_days_display=record.number_of_days
    
    @api.depends("number_of_hours")
    def _compute_number_of_hours_display(self):
        for record in self:
            record.number_of_hours_display=record.number_of_hours
   
    @api.depends("request_hour_from","request_hour_to","request_unit_hours")
    def _compute_number_of_hours(self):
        for record in self:
            # if record.request_unit_half:
            #     record.number_of_hours=4
            if record.request_unit_hours:
                if record.request_hour_from and record.request_hour_to:
                    record.number_of_hours=float(record.request_hour_to)-float(record.request_hour_from)
            else:
                record.number_of_hours=False
    
    @api.onchange("request_unit_half")
    def _onchange_request_unit_half(self):
        if self.request_unit_half:
            self.number_of_hours=4

    
    @api.constrains('date_from', 'date_to', 'employees_id')
    def _check_date_employees(self):
        for record in self.filtered('employees_id'):
            domain=[
                ('date_from', '<', record.date_to),
                ('date_to', '>', record.date_from),
                ('employees_id', '=', record.employees_id.id),
                ('id', '!=', record.id),
                ('state', '!=', 'Refuse')
                ]
            nholidays = self.search_count(domain)
            if nholidays:
                raise ValidationError(
                    _('You can not set 2 time off that overlaps on the same day for the same employee.') )
    
    def unlink(self):
        for record in self:
            if record.date_to<fields.date.today():
                raise UserError(_("You cannot delete the finish holidays"))
            return super(Employees_Leave,self).unlink()
    
    def action_refuse(self):
        for record in self:
            record.write({'state':'Refuse'})
            
            
    def action_approved(self):
        for record in self:
            record.write({'state':'Validate1'})
    #
    # def test(self):
    #     self._onchange_request_unit_half()    