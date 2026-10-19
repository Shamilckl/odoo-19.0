from odoo import api, fields, models

class LabDepartment(models.Model):
    _name = 'lab.department'
    _description = 'Lab Department'
    _rec_name = 'department_name'

    department_name = fields.Char(string='Department Name')