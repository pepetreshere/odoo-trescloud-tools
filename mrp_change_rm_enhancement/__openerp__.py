# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 TRESCloud (<http://www.trescloud.com>)
#    Author: Santiago Orozco <santiago.orozco@trescloud.com>
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
    'name': 'Raw Material change in MO Enhancement',
    'version': '1.1',
    'author': 'Santiago Orozco',
    'website': 'http://www.openerp.com.cn',
    'category': 'Manufacturing',
    'sequence': 18,
    'summary': 'MRP support Add or Cancel the moves',
    'images': [],
    'depends': ['mrp_change_rm','mrp_bom_product_details_enhancement'],
    'description': """
            Add 6 fields for calculating the following indicators          
            The module allows you to:
                * Unit Cost : theorical cost
                * Total Cost : theorical total cost
                * Unit Real Cost : real cost
                * Total Real Cost : real total cost
                * Unit Cost Deviation : real cost/theorical cost *100
                * Total Cost Deviation : real total cost/theorical total cost *100

    """,
    'data': [
        'views/mrp_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
