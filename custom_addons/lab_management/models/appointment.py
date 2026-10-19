from odoo import fields, models, api


class LabAppointment(models.Model):
    _name = 'lab.appointment'
    _description = 'Lab Appointment'

    name = fields.Char(string="Appointment Sequence", readonly=True,
                       index='trigram', copy=False,
                       default=lambda self: self.env['ir.sequence'].next_by_code('lab.appointment'))

    patient_name = fields.Many2one("lab.patient", string="Patient")
    patient_number = fields.Char(string="Phone Number")
    # department_name = fields.Char(string="Department")
    department_name2 = fields.Many2one("lab.department", string="Department")
    doctor_name = fields.Many2one("lab.doctor", string="Doctor")
    consultation_date = fields.Date(string="Consultation Date")
    time_slot = fields.Datetime(string="Time Slot")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_consultation', 'In Consultation'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='draft', string="Status")

    many = fields.Many2many('lab.patient', 'patient_name')

    def action_draft(self):
        self.write({
            'state': 'draft'
        })

    def action_confirmed(self):
        self.write({
            'state': 'confirmed'
        })

    def action_in_consultation(self):
        self.write({
            'state': 'in_consultation'
        })

    def action_completed(self):
        self.write({
            'state': 'completed'
        })

    def action_cancelled(self):
        self.write({
            'state': 'cancelled'
        })

    def action_prescription(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment',
            'res_model': 'created.appointment',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_name': self.patient_name.id,
                'default_doctor_name': self.doctor_name.id,
                'default_consultation_date': self.consultation_date,
            },
        }

    def action_exel_report(self):
        self.ensure_one()
        return self.env.ref('lab_management.appointment_report_xlsx').report_action(self)

    def action_view_patients(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "lab.patient",
            "name": ("Patients"),
            "view_mode": "form",
            "res_id": self.patient_name.id,
            "target": "current",
        }

    @api.model
    def auto_cancel_expired_appointments(self):
        now = fields.Datetime.now()
        appointments = self.search([('state', '=', 'draft'), ('time_slot', '<', now), ])
        appointments.write({'state': 'cancelled'})
