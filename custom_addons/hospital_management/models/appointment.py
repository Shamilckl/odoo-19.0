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

    sale_order_count = fields.Integer(
        compute="_compute_sale_order_count"
    )

    state = fields.Selection([
        ('new', 'New'),
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
    ], default='new', string="Status", tracking=True)

    slot_id = fields.Many2one(
        "hospital.slot",
        string="Time Slot",
        domain="[('id', 'in', available_slot_ids)]"
    )

    available_slot_ids = fields.Many2many(
        "hospital.slot",
        compute="_compute_available_slots",
    )

    sale_order_ids = fields.One2many(
        "sale.order",
        "appointment_id",
        string="Sales Orders"
    )

    @api.depends('doctor_id', 'appointment_date')
    def _compute_available_slots(self):
        for rec in self:
            rec.available_slot_ids = [(5, 0, 0)]

            if rec.doctor_id and rec.appointment_date:
                day = rec.appointment_date.strftime('%A').lower()

                fee_lines = rec.doctor_id.consulting_fee_ids.filtered(
                    lambda x: x.day == day
                )

                slots = fee_lines.mapped('slot_ids')

                rec.available_slot_ids = [(6, 0, slots.ids)]

    def _compute_consultation_count(self):
        for rec in self:
            rec.consultation_count = self.env[
                "hospital.consultation"
            ].search_count([
                ("appointment_id", "=", rec.id)
            ])

    def _compute_sale_order_count(self):
        for rec in self:
            rec.sale_order_count = self.env[
                "sale.order"
            ].search_count([
                ("appointment_id", "=", rec.id)
            ])

    @api.onchange('doctor_id', 'appointment_date', 'slot_id')
    def _onchange_consulting_fee(self):
        for rec in self:

            rec.consulting_fee = 0

            if rec.doctor_id and rec.appointment_date:

                day = rec.appointment_date.strftime('%A').lower()

                fee_record = rec.doctor_id.consulting_fee_ids.filtered(
                    lambda x:(
                        x.day == day and
                        rec.slot_id in x.slot_ids
                    )
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

        consultation = self.env['hospital.consultation'].search(
            [('appointment_id', '=', self.id)],
             limit=1)

        if not consultation:
            self.env['hospital.consultation'].create({
                'patient_id': self.patient_id.id,
                'doctor_id': self.doctor_id.id,
                'appointment_id': self.id,
            })
        self.patient_id._create_customer()

        sale_order = self.env['sale.order'].search([
                ('appointment_id', '=', self.id)],
            limit=1)

        if not sale_order:
            sale_order = self.env['sale.order'].create({
                'partner_id': self.patient_id.partner_id.id,
                'appointment_id': self.id,
            })

            for product in self.doctor_id.product_ids:
                self.env['sale.order.line'].create({
                    'order_id': sale_order.id,
                    'product_id': product.id,
                    'product_uom_qty': 1,
                    'price_unit': product.lst_price,
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

    def action_view_sale_orders(self):
        self.ensure_one()

        sale_order = self.env["sale.order"].search(
            [("appointment_id", "=", self.id)],
            limit=1
        )

        if sale_order:
            return {
                "type": "ir.actions.act_window",
                "name": "Quotation",
                "res_model": "sale.order",
                "view_mode": "form",
                "res_id": sale_order.id,
                "target": "current",
            }
        return True
