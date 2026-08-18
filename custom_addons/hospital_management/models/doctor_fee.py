from odoo import models, fields

class HospitalDoctorFee(models.Model):
    _name = "hospital.doctor.fee"
    _description = "Doctor Fee"


    doctor_id = fields.Many2one(
        "hospital.doctor",
        string="Doctor",
        ondelete="cascade")

    day = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ], string="Day", required=True)


    fee = fields.Float(
        string="Consulting Fee",
        required=True)

    slot_ids = fields.Many2many(
        "hospital.slot",
        string="Slots")