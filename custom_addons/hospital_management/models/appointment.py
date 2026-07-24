from odoo import models, fields

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    _rec_name = "patient_id"

    patient_id = fields.Many2one("hospital.patient", string="Patient")
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor")
    appointment_date = fields.Date(string="Appointment Date")
    fee = fields.Integer(string="Consultation Fee")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
    ], default='draft', string="Status")

    def action_draft(self):
        self.write({
            'state': 'draft'
        })

    def action_confirm(self):
        self.write({
            'state': 'confirm'
        })

        self.env['hospital.consultation'].create({
            'patient_id': self.patient_id.id,
            'doctor_id': self.doctor_id.id,
            'appointment_id': self.id,
        })