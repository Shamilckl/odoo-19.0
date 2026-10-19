from odoo import fields, models

class LabDoctor(models.Model):
    _name = 'lab.doctor'
    _description = 'Lab Doctor'
    _rec_name = 'user_id'

    doctor_id = fields.Integer(string='Doctor ID')
    # doctor_name = fields.Char(string='Doctor Name')
    # profile_img = fields.Image(string='Profile Image')
    profile_img2 = fields.Image(string='Profile Image')
    specialization = fields.Char(string='Specialization')
    medical_license_number= fields.Integer(string='Medical Licence Number')

    user_id = fields.Many2one("res.users",string="User")