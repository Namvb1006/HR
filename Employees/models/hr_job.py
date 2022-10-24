from odoo import models,fields,api

class Employees_Job(models.Model):
    _name='employees.job'
    _description='job Description'
    name=fields.Char('Name')
   
    workplace=fields.Char('Work place')