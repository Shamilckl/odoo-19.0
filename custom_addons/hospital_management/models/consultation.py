from odoo import models, fields

class HospitalConsultation(models.Model):
    _name = "hospital.consultation"
    _description = "Consultation"
    _rec_name = "patient_id"

    appointment_id = fields.Many2one(
        "hospital.appointment"
    )

    patient_id = fields.Many2one(
        "hospital.patient"
    )

    doctor_id = fields.Many2one(
        "hospital.doctor"
    )

    diagnosis = fields.Text()

    medicine_line_ids = fields.One2many(
        "hospital.consultation.line",
        "consultation_id",
        string="Medicines"
    )

    state = fields.Selection([
        ('cancel', 'Cancel'),
        ('consulted', 'Consulted'),
    ], default='cancel', string="Status")

    def action_draft(self):
        self.write({
            'state': 'cancel'
        })

    def action_confirm(self):
        self.write({
            'state': 'consulted'
        })