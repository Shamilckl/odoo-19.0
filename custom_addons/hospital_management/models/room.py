from odoo import models, fields

class HospitalRoom(models.Model):
    _name = 'hospital.room'
    _description = 'Hospital Room'
    _rec_name = "room_id"

    patient_id = fields.Many2one("hospital.patient",string="Patient")

    room_id = fields.Integer(string="Room Number")

    rent = fields.Float(string="Room Rent")

