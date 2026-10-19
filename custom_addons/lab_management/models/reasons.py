from odoo import api, fields, models, tools

class WrittenReasons(models.Model):
    _name = 'written.reasons'
    _description = 'Record Names'
    _rec_name = 'written_reasons'

    written_reasons = fields.Char(string='Written Reasons')

