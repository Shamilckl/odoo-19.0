from odoo import models, fields, api


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _rec_name = "display_name"

    reference=fields.Char(
        string="Reference",
        required=True,
        copy=False,
        readonly=True,
        default="New")

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

    display_name = fields.Char(
        compute="_compute_display_name",
        store=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', 'New') == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code(
                    'hospital.patient'
                ) or 'New'

        return super().create(vals_list)

    @api.depends('name', 'reference')
    def _compute_display_name(self):
        for patient in self:
            patient.display_name = (
                f"{patient.name} - {patient.reference}"
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