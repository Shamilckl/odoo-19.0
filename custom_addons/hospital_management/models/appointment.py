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

    consulting_fee = fields.Float(
        string="Consulting Fee",
        store=True,
    )

    consultation_count = fields.Integer(
        compute="_compute_consultation_count"
    )

    state = fields.Selection([
        ('new', 'New'),
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
    ], default='new', string="Status", tracking=True)

    slot_id = fields.Many2one(
        "hospital.slot",
        string="Time Slot"
    )

    def _compute_consultation_count(self):
        for rec in self:
            rec.consultation_count = self.env[
                "hospital.consultation"
            ].search_count([
                ("appointment_id", "=", rec.id)
            ])

    @api.onchange('doctor_id', 'appointment_date')
    def _onchange_consulting_fee(self):
        for rec in self:

            rec.consulting_fee = 0

            if rec.doctor_id and rec.appointment_date:

                day = rec.appointment_date.strftime('%A').lower()

                fee_record = rec.doctor_id.consulting_fee_ids.filtered(
                    lambda x: x.day == day
                )

                if fee_record:
                    rec.consulting_fee = fee_record[0].fee

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

