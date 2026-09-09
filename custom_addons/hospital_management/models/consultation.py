from odoo import models, fields, api

class HospitalConsultation(models.Model):
    _name = "hospital.consultation"
    _description = "Consultation"
    _rec_name = "name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Consultation No",
        required=True,
        copy=False,
        readonly=True,
        default="New"
    )

    appointment_id = fields.Many2one(
        "hospital.appointment", tracking=True
    )

    patient_id = fields.Many2one(
        "hospital.patient", tracking=True
    )

    doctor_id = fields.Many2one(
        "hospital.doctor", tracking=True
    )

    diagnosis = fields.Text()

    medicine_line_ids = fields.One2many(
        "hospital.consultation.line",
        "consultation_id",
        string="Medicines", tracking=True
    )

    state = fields.Selection([
        ('new', 'New'),
        ('consultation', 'Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], default='new', string="Status", tracking=True)

    sale_order_count = fields.Integer(
        compute="_compute_sale_order_count"
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'hospital.consultation'
                ) or 'New'
    
        return super().create(vals_list)

    def action_done(self):
        self.write({
            'state': 'done'
        })

        sale_order = self.env['sale.order'].search([
            ('consultation_id', '=', self.id)],
            limit=1)

        if not sale_order:
            sale_order = self.env['sale.order'].create({
                'partner_id': self.patient_id.partner_id.id,
                'consultation_id': self.id,
            })

            for product in self.doctor_id.product_ids:
                self.env['sale.order.line'].create({
                    'order_id': sale_order.id,
                    'product_id': product.id,
                    'product_uom_qty': 1,
                    'price_unit': product.lst_price,
                })

            for medicine_line in self.medicine_line_ids:
                self.env['sale.order.line'].create({
                    'order_id': sale_order.id,
                    'product_id': medicine_line.medicine_id.id,
                    'product_uom_qty': medicine_line.quantity,
                    'price_unit': medicine_line.medicine_id.lst_price,
                    'dosage': medicine_line.dosage,
                })

            sale_order.action_confirm()
            sale_order._create_invoices()

    def action_cancel(self):
        self.write({
            'state': 'cancel'
        })

    def action_consultation(self):
        self.write({
            'state': 'consultation'
        })

    def _compute_sale_order_count(self):
        for rec in self:
            rec.sale_order_count = self.env[
                "sale.order"
            ].search_count([
                ("consultation_id", "=", rec.id)
            ])

    def action_view_sale_orders(self):
        self.ensure_one()

        sale_order = self.env["sale.order"].search(
            [("consultation_id", "=", self.id)],
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
