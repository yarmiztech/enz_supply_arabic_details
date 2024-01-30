# -*- coding: utf-8 -*-
{
    'name': "Enzapps Masar Arabic Details",
    'author':
        'ENZAPPS',
    'summary': """
This module is for Enzapps Low Price HighLight.
""",

    'description': """
        This module is for Low Price HighLight.
        Which Include Sales,Purchase,Expense,Inventory and Accounting.
        And the Corresponding Reports.
    """,
    'website': "",
    'category': 'base',
    'version': '16.0',
    'depends': ['base','contacts','account','stock','product','sale_management','purchase','hr_expense','opening_balance_customers_saudhi_branch','opening_balance_parent_child','enz_multi_branch','enz_purchase_barcode','enz_vencus_balance','sale_last_transactions','pro_forma_invoice','purchase_automatic_validation','sale_automatic_validation','report_xlsx','pending_sale','pending_purchase','pending_delivery','pending_receipt','enz_warranty','enztrading','hide_menu_user','enz_trading_extension','enz_trading_advanced','enz_trading_advanced_ext','enz_multi_branch_seq','enz_masar_updations','stock_landed_costs','enz_inventory_dashboard','enz_invoice_scrap','enz_supply_updations','enz_supply_updations_new','enz_cost_sheet','enz_assumption_cost_sheet','enz_cost_sheet_assumption_modification_one','enz_highlight_low_price','enz_change_branch_new','enz_masar_dec','enz_masar_jan','enz_dynamic_design_standard','product_brand_sale','enz_masar_jan_new','enz_masar_division','enz_tax_filter_report','enz_jan_update','enz_tax_filter_report_with_xlsx','enz_masar_jan_fifteen','purchase_stock','enz_slice_seq','enz_masar_jan_tt','enz_supply_seperate_margin'],
    "images": ['static/description/icon.png'],
    'data': [
        'reports/invoice.xml',
        'reports/pro_forma.xml',
        'reports/page_formate.xml',
        'views/purchase_order.xml',
        'views/company.xml',
        'views/enquiry.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
