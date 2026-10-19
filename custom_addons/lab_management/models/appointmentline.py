from odoo import fields,models,api

class AppointmentLine(models.TransientModel):
    _name = 'appointment.line'
    _description = 'Appointment Line'

    appointment_relation=fields.Many2one("created.appointment",string="Relation" )

    product_name=fields.Many2one('product.template',string="Product")
    comment=fields.Char(string="Comment")
    days=fields.Integer(string="Days")
    quantity=fields.Integer(string="Quantity",default=1)
    unit_price=fields.Float(string="Price", related="product_name.list_price")
    subtotal=fields.Float(string="Subtotal",compute="_compute_subtotal")
    price_total = fields.Float(
        string="Total",
        compute='_compute_amount')

    @api.depends('quantity','unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal= line.unit_price * line.quantity

    @api.depends('subtotal')
    def _compute_amount(self):
        for line in self:
            line.price_total = line.subtotal


