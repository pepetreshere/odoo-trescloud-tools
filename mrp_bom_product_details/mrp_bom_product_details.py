# -*- coding: utf-8 -*-

##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Solutions Libergia inc. (<http://www.libergia.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
import decimal_precision as dp
from openerp.tools.translate import _

class mrp_bom(osv.osv):
    _inherit = 'mrp.bom'
    
    def _calculate_cost(self, cr, uid, ids, name, args, context=None):
        res = {}
        area=0.0
        for object in self.browse(cr, uid, ids):
            area = object.product_qty * object.product_standard_price
            res[object.id] = area
        return res
    
    def _calculate_cost_price(self, cr, uid, ids, name, args, context=None):
        res = {}
        for object in self.browse(cr, uid, ids):
            area = object.product_id.standard_price * object.product_uom.factor_inv
            res[object.id] = area
        return res

    _columns ={
        'product_standard_price': fields.related('product_id', 'standard_price', type='float',digits_compute=dp.get_precision('Product Price'), string='Cost Price', readonly=True),
        'product_qty_available': fields.related('product_id', 'qty_available', type='float',digits_compute=dp.get_precision('Account'),string='Quantity On Hand', readonly=True),
        'product_standard_price': fields.function(_calculate_cost_price, string='Product Price',digits_compute=dp.get_precision('Product Price'), type="float"),
        'cost_total': fields.function(_calculate_cost, string='Costo Total',digits_compute=dp.get_precision('Product Price'), type="float")
        
    }
    _defaults = {
    }
    

mrp_bom()