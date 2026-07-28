from odoo import models, fields, api

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    _rec_name = "name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Appointment No",
        required=True,
        copy=False,
        readonly=True,
        default="New"
    )

    patient_id = fields.Many2one("hospital.patient", string="Patient", tracking=True)
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", tracking=True)
    appointment_date = fields.Date(string="Appointment Date", tracking=True)
    fee = fields.Integer(string="Consultation Fee", tracking=True)

    consultation_count = fields.Integer(
        compute="_compute_consultation_count"
    )

    def _compute_consultation_count(self):
        for rec in self:
            rec.consultation_count = self.env[
                "hospital.consultation"
            ].search_count([
                ("appointment_id", "=", rec.id)
            ])

    state = fields.Selection([
        ('new', 'New'),
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
    ], default='new', string="Status", tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'hospital.appointment'
                ) or 'New'

        return super().create(vals_list)


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

    def action_view_consultation(self):
        self.ensure_one()

        consultation = self.env["hospital.consultation"].search(
            [("appointment_id", "=", self.id)],
            limit=1
        )

        if consultation:
            return {
                "type": "ir.actions.act_window",
                "name": "Consultation",
                "res_model": "hospital.consultation",
                "view_mode": "form",
                "res_id": consultation.id,
                "target": "current",
            }
        return True