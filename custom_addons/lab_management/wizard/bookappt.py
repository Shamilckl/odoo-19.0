from odoo import api, fields, models

class BookAppt(models.TransientModel):
    _name = 'book.appt'
    _description = 'Book Appt'

    patient_name = fields.Many2one('lab.patient',string='patient')
    doctor_name = fields.Many2one('lab.doctor',string='Doctor')

    def action_create_appointment(self):

        self.env['lab.appointment'].create({
            'patient_name': self.patient_name.id,
            'doctor_name':self.doctor_name.id,
        })

        return