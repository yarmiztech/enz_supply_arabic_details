from odoo import fields, models


class StockImmediateTransfer(models.TransientModel):
    _inherit = "stock.immediate.transfer"

    def check_upselling_delete(self):
        for picking in self.pick_ids:
            if picking.company_id.check_upselling_delete == True:
                sale_orders = set(picking.move_ids_without_package.mapped('sale_advance_line_id.order_id'))
                for order in sale_orders:
                    for order_line in order.order_line:
                        if order_line.product_uom_qty == 0:
                            order_line.state = 'draft'
                            order_line.sudo().unlink()

    def check_purchase_sale_recieve(self):
        sale_count = 0
        for picking in self.pick_ids:
            for move in picking.move_ids_without_package:
                if move.purchase_advance_line_id.id:
                    move.purchase_advance_line_id.qty_received = move.purchase_advance_line_id.qty_received + move.product_uom_qty
                    move.purchase_advance_line_id.quantity_recieved = move.purchase_advance_line_id.quantity_recieved + move.product_uom_qty
                    move.purchase_advance_line_id.enquiry_line_id.recieved_po_qty = move.purchase_advance_line_id.enquiry_line_id.recieved_po_qty + move.product_uom_qty
                if move.sale_advance_line_id.id:
                    # move.sale_advance_line_id.qty_delivered = move.sale_advance_line_id.qty_delivered + move.product_uom_qty
                    move.sale_advance_line_id.quantity_delivered = move.sale_advance_line_id.quantity_delivered + move.product_uom_qty
                    move.sale_advance_line_id.enquiry_line_id.delivered_so_qty = move.sale_advance_line_id.enquiry_line_id.delivered_so_qty + move.product_uom_qty
                    sale_count += 1
            if picking.purchase_order_ids.ids:
                for purchase in picking.purchase_order_ids:
                    complete = 0
                    for order in purchase.order_line:
                        if order.qty_received != order.product_qty:
                            complete += 1
                    if complete == 0:
                        purchase.complete = True
            if picking.sale_order_ids.ids:
                for sales in picking.sale_order_ids:
                    complete = 0
                    for order in sales.order_line:
                        if order.qty_delivered != order.product_uom_qty:
                            complete += 1
                    if complete == 0:
                        sales.complete = True
            if sale_count != 0:
                self.check_upselling_delete()
