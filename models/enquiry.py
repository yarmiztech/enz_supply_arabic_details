from odoo import fields, models, _, api
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp

class FinalCostSheet(models.TransientModel):
    _inherit = 'final.cost.sheet'

    discount_type = fields.Selection(
        [('percent', 'Percentage'), ('amount', 'Amount')],
        string='Discount type', default='percent')

    discount_rate = fields.Float('Discount Rate',
                                 digits=dp.get_precision('Account'))

    discount_amt = fields.Float()
    total_amt = fields.Float()

    @api.onchange('enquiry_id')
    def compute_sale_lines(self):
        if self.enquiry_id:
            sales = self.env['sale.order.line'].search(
                [('enquiry_line_id.enquiry_id', '=', self.enquiry_id.id), ('state', 'in', ['sale', 'done'])])
            sale_order = sales.mapped('order_id')
            order_list = []
            for order in sale_order:
                count = 1
                for line in order.order_line:
                    if count == 1:
                        order_line = (0, 0, {
                            'sale_id': order.id,
                            'partner_id': order.partner_id.id,
                            'product_id': line.product_id.id,
                            'name': line.name,
                            'product_uom_qty': line.product_uom_qty,
                            'price_unit': line.price_unit,
                            'tax_id': [(6, 0, line.tax_id.ids)],
                            'price_subtotal': line.product_uom_qty * line.price_unit,
                        })
                        order_list.append(order_line)
                        count += 1
                    else:
                        order_line = (0, 0, {
                            'sale_id': order.id,
                            'partner_id': order.partner_id.id,
                            'product_id': line.product_id.id,
                            'name': line.name,
                            'product_uom_qty': line.product_uom_qty,
                            'price_unit': line.price_unit,
                            'tax_id': [(6, 0, line.tax_id.ids)],
                            'price_subtotal': line.product_uom_qty * line.price_unit,
                            'make_inv': True,
                        })
                        order_list.append(order_line)
            self.sale_lines_ids = None
            self.sale_lines_ids = order_list

    @api.onchange('purchase_lines_ids')
    def compute_total_selling_price(self):
        self.total_expense = 0
        self.total_landed_cost = 0
        self.total_selling_price = 0
        self.profit = 0
        self.loss = 0
        self.discount_amt = 0
        self.total_amt = 0
        for line in self.purchase_lines_ids:
            if line.extra_charge == False:
                self.total_expense = self.total_expense + (line.expense * line.product_uom_qty)
                self.total_landed_cost = self.total_landed_cost + (line.landed_cost * line.product_uom_qty)
        # self.total_selling_price = self.total_selling_price + (line.selling_price * line.product_uom_qty)
        sales = self.sale_lines_ids.mapped('sale_id')
        for sale in sales:
            self.total_selling_price = self.total_selling_price + (sale.amount_untaxed/sale.currency_rate)
            self.discount_amt = self.discount_amt + (sale.amount_discount/sale.currency_rate)
            self.total_amt = self.total_amt + (sale.amount_untaxed/sale.currency_rate)
            if sale.discount_rate > 0:
                self.discount_type = sale.discount_type
                self.discount_rate = sale.discount_rate
        if self.total_landed_cost != 0:
            self.margin = self.total_selling_price / self.total_landed_cost
        profit = self.total_selling_price - self.total_landed_cost
        if profit >= 0:
            self.profit = profit
            self.loss = 0
        else:
            self.loss = profit
            self.profit = 0