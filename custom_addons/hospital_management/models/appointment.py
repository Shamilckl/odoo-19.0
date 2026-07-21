from odoo import models, fields

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _rec_name = "appointment_date"

    patient_id = fields.Many2one("hospital.patient", string="Patient")

    doctor_id = fields.Many2one("hospital.doctor", string="Doctor")

    appointment_date = fields.Date(string="Appointment Date")

    fee = fields.Float(string="Consultation Fee")

    remarks = fields.Text(string="Remark")