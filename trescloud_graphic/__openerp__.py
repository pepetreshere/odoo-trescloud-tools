{
    'name' : 'Extra Graphic by Payment and Account Analityc',
    'version' : '1.1',
    'author' : 'TRESCloud S.A.',
    'category': 'Extra graphic',
    'website' : 'http://www.tresclod.com',
    'summary' : 'Voucher, Account Analityc',
    'description' : """
Este modulo agrega dos vistas mas graficas para pagos y cuentas analiticas

""",
    'depends' : [
        'base',
        'account',
        'account_voucher',
        
    ],
    'data' : [
        'trescloud_voucher_views.xml',
    ],
    'installable' : True,
    'auto_install': True,
}
