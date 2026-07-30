from odoo import models, fields

class HospitalDoctorSlot(models.Model):
    _name = "hospital.doctor.slot"
    _description = "Doctor Time Slot"
    _rec_name = "doctor_id"

    doctor_id = fields.Many2one(
        "hospital.doctor",
        string="Doctor",
        required=True,
        ondelete="cascade"
    )

    start_time = fields.Datetime(
        string="Start Time",
        required=True,
    )

    end_time = fields.Datetime(
        string="End Time",
        required=True,
    )