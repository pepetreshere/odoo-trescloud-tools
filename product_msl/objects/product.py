# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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

from osv import fields,osv


class product_product(osv.osv):
    _inherit = 'product.product'
    _name = 'product.product' 
    _columns = {
        
    'msl_id': fields.many2one('product.msl','MSL',
                              select=True,
                              help="Moisture Sensitivity Level relates to the packaging and handling precautions for some semiconductors"),
    'open_time': fields.related('msl_id', 'open_time', type="float", relation="product.msl",
                                string="Open Time in hours",
                                store=False,
                                help="Maximum period of time that the component can be used, after that time the component must be sent to bake."),     
                }
    #===========================================================================
    # def _default_msl(self,cr,uid,ids,context=None):
    #     res = self.pool.get('product.msl').search(cr,uid,[('control','=', True)],context=context)
    #     return res[0]
    # _defaults = {  
    #     'msl_id': _default_msl,  
    #     }
    #===========================================================================

product_product()