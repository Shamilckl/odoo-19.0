from odoo import models, fields

class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Hospital Doctor"
    _rec_name = "name"

    name = fields.Char(string="Doctor Name", required=True)

    consulting_fee_ids = fields.One2many(
        "hospital.doctor.fee",
        "doctor_id",
        string="Consulting Fees"
    )

    age = fields.Integer(string="Age")

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")

    specialization = fields.Char(string="Specialization")

    phone = fields.Char(string="Phone")