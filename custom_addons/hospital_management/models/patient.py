from odoo import models, fields


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _rec_name = "name"

    name = fields.Char(
        string="Patient Name",
        required=True
    )

    age = fields.Integer(string="Age")

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")

    phone = fields.Char(string="Phone")

    address = fields.Text(string="Address")

    partner_id = fields.Many2one(
        "res.partner",
        string="Customer"
    )

    def _create_customer(self):
        for patient in self:
            if not patient.partner_id:
                partner = self.env["res.partner"].create({
                    "name": patient.name,
                    "phone": patient.phone,
                    "street": patient.address,
                    "customer_rank": 1,
                })

                patient.partner_id = partner.id