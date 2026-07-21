from odoo import models, fields, api

class HospitalBilling(models.Model):
    _name = "hospital.billing"
    _description = "Hospital Billing"
    _rec_name = "patient_id"

    patient_id = fields.Many2one(
        "hospital.patient",
        string="Patient"
    )

    consultation_fee = fields.Float(string="Consultation Fee")

    room_rent = fields.Float(string="Room Rent")

    medicine_total = fields.Float(string="Medicine Total")

    laboratory_charge = fields.Float(string="Laboratory Charge")

    total_amount = fields.Float(
        string="Bill Amount",
        compute="_compute_total",
        store=True
    )

    @api.depends(
        "consultation_fee",
        "room_rent",
        "medicine_total",
        "laboratory_charge"
    )
    def _compute_total(self):
        for record in self:
            record.total_amount = (
                record.consultation_fee
                + record.room_rent
                + record.medicine_total
                + record.laboratory_charge
            )