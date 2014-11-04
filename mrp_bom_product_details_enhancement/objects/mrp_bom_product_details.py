# -*- coding: utf-8 -*-

##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 TRESCloud (<http://www.trescloud.com>)
#    Author: Santiago Orozco <santiago.orozco@trescloud.com>
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
    
    def _calculate_total_cost(self, cr, uid, ids, name, args, context=None):
        res = {}
        area = 0.0
        for object in self.browse(cr, uid, ids):
            for line in object.bom_lines:
                area += line.cost_total
            res[object.id] = area
            area = 0.0
        return res

    _columns ={
        'total_cost': fields.function(_calculate_total_cost, string='Total Cost of BOM', help="Total Cost of this Bill Of Materials", digits_compute=dp.get_precision('Product Price'), type="float", store=True),
    }
    

mrp_bom()