from odoo import fields,models

class ResCompany(models.Model):
    _inherit = "res.company"


    check_upselling_delete = fields.Boolean()