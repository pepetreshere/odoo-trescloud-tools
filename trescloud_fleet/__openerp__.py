{
    'name' : 'Fleet Management TRESCloud',
    'version' : '1.1',
    'author' : 'TRESCloud S.A. David Jacobo Romero Calderon',
    'category': 'Managing vehicles and contracts',
    'website' : 'http://www.tresclod.com',
    'summary' : 'Vehicle, leasing, insurances, costs',
    'description' : """
Vehicle, leasing, insurances, cost
==================================
""",
    'depends' : [
        'base',
        'fleet',
        'decimal_precision',
    ],
    'data' : [
        'trescloud_fleet_views.xml',
        'data/trescloud_data_partner_title.xml',
        'trescloud_partner.xml',
    ],
    'update_xml' : ['security/ir.model.access.csv'],
    'installable' : True,
    'auto_install': True,
}
