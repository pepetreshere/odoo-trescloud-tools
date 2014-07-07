# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 TRESCloud (<http://www.trescloud.com>)
#    Copyright (C) 2004-2010 OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from osv import fields,osv

class product_product(osv.osv):
    """
    Modulo que agregaa caracteristicas de medidas a un producto
    """
    _inherit = 'product.product'
 
    def _product_measure(self, cr, uid, ids, name, arg, context=None):
        res = {}
        if context is None:
            context = {}
        measure=""
        product=self.browse(cr,uid,ids)[0]
        long_p = product.long_p
        width = product.width
        thickness = product.thickness
        if long_p:
            measure+=str(long_p)
        if long_p and (width or thickness) :    
            measure+='x'
        if width:
            measure+=str(width)
        if width and thickness:    
            measure+='x'
        
        if thickness:
            measure+=str(thickness)
         
        res[ids[0]]=measure
        return res
    
    _columns = {
        'long_p':fields.float('Long (mm)'),
        'width':fields.float('Width (mm)'),
        'thickness':fields.float('Thickness (mm)'),
        'measure': fields.function(_product_measure, method=True, type='char', string='Measurement', store=True), 
                }

product_product()


 
