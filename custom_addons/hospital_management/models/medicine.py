from odoo import fields, models

class HospitalMedicine(models.Model):
    _name = "hospital.medicine"
    _description = "Hospital Medicine"
    _rec_name = "patient_id"

    patient_id= fields.Many2one("hospital.patient",string="Patient")
    doctor_id= fields.Many2one("hospital.doctor",string="Doctor")

    medicine= fields.Char(string="Medicine Name",required=True)
    qty = fields.Integer(string="Quantity")
    price = fields.Float(string="Price")