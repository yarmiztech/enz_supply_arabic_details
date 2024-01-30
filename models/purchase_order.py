from odoo import fields,models,api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    converted_to_po = fields.Boolean()

    def converted_to_po_in_rfq(self):
        if self.rfq_ids:
            for line in self.rfq_ids:
                rfqs = self.env['purchase.order'].search([('name','=',line.name)])
                if rfqs:
                    for rfq in rfqs:
                        rfq.converted_to_po = True

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        self.converted_to_po_in_rfq()
        return res

    @api.onchange('cost_expense_details_lines_ids', 'cost_bill_details_lines_ids', 'assumption_cost_lines_ids',
                  'margin', 'order_line')
    def compute_expense_landes_cost_selling_price(self):
        cost = 0
        if self.rfq == True:
            cost = sum(self.assumption_cost_lines_ids.mapped('amount'))
        else:
            for line in self.cost_expense_details_lines_ids:
                if line.state in ['approved', 'done']:
                    cost = cost + (line.total_amount / line.currency_rate)
            for line in self.cost_bill_details_lines_ids:
                if line.move_id.state == 'posted':
                    cost = cost + (line.price_subtotal / line.currency_rate)
            # cost = cost + sum(self.cost_bill_details_lines_ids.mapped('price_subtotal'))
        quantity = 0
        if self.order_line:
            for order in self.order_line:
                if order.extra_charge == False:
                    if order.order_id.rfq == True:
                        if order.check == True:
                            quantity = quantity + order.product_qty
                    else:
                        quantity = quantity + order.product_qty
        if self.rfq == True:
            amount_untaxed = sum(
                self.order_line.filtered(lambda product_line: product_line.check == True).mapped('price_subtotal'))
            extra_charge = sum(
                self.order_line.filtered(lambda product_line: product_line.extra_charge == True).mapped('price_subtotal'))
            cost_of_material = amount_untaxed / self.currency_rate
            extra_charge_cost = extra_charge / self.currency_rate
        else:
            amount_untaxed = sum(
                self.order_line.filtered(lambda product_line: product_line.extra_charge == False).mapped('price_subtotal'))
            extra_charge = sum(
                self.order_line.filtered(lambda product_line: product_line.extra_charge == True).mapped(
                    'price_subtotal'))
            cost_of_material = amount_untaxed / self.currency_rate
            extra_charge_cost = extra_charge / self.currency_rate
        if quantity > 0:
            # cost_material = cost_of_material / quantity
            if self.order_line:
                for line in self.order_line:
                    if line.extra_charge == False:
                        if self.rfq == True:
                            if line.check == True:
                                if self.amount_untaxed > 0:
                                    line.expense = ((line.price_unit / self.currency_rate) / cost_of_material) * (cost + extra_charge_cost)
                                    line.landed_cost = (line.price_unit / self.currency_rate) + line.expense
                                    line.selling_price = line.landed_cost * line.margin
                            else:
                                line.expense = 0
                                line.landed_cost = 0
                                line.selling_price = 0
                        else:
                            if self.amount_untaxed > 0:
                                line.expense = ((line.price_unit / self.currency_rate) / cost_of_material) * (cost + extra_charge_cost)
                                line.landed_cost = (line.price_unit / self.currency_rate) + line.expense
                                if line.landed_cost != 0:
                                    line.margin = line.selling_price / line.landed_cost
                                    # line.selling_price = line.landed_cost * line.margin
                    else:
                        line.expense = 0
                        line.landed_cost = 0
                        line.selling_price = 0
        else:
            if self.order_line:
                for line in self.order_line:
                    line.expense = 0
                    line.landed_cost = 0
                    line.selling_price = 0
