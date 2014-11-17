# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source TRESCloud
#    Copyright (c) 2014-TRESCloud S.A. (<http://www.trescloud.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Product Msl',
    'version': '1.0',
    "summary": "Moisture Sensitive Level Management",
    'category': 'warehouse',
    'depends': ['base',
                'stock',
                'product_serial'
                ],
    'author': 'TRESCLOUD Henry Granada',
    'description': 
    """
    Moisture Sensitive Level
    Moisture sensitivity level relates to the packaging and handling precautions for some semiconductors. 
    The MSL is an electronic standard for the time period in which a moisture sensitive device can be exposed to ambient room conditions (approximately 30 °C/60%RH).
  
    This module adds:
    - - MSL definition in the product form
    - - Tracking of exposed time of a specific lot or serial number of the product
    - - Alarms
    Authors: 
    Henry Granada
    TRESCLOUD Cia Ltda
    """,
    'website': 'http://www.trescloud.com',
    'data': [
        'views/product_msl_view.xml',
        'views/product_view.xml',
        'wizard/wizard_product_msl_view.xml',
        'views/stock_view.xml',
        'data/product.msl.csv',
       # 'security/',
    ],
    'installable': True,
    'auto_install': False,
}
