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
    .
    """
    _inherit = 'product.product'
    _columns = {
        'spec_id': fields.many2one('product.spec', 'Spec'),
        'density':fields.char('Density',size=10),
                }

product_product()

class product_spec(osv.osv):
    _name = 'product.spec'
    _columns = {
                   'name'          : fields.char('Name', size=64, required=True, readonly=False),
                   'description'   : fields.text('Description'), 
             } 
product_spec()

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        res=super(sale_order_line,self).product_id_change(cr, uid, ids, pricelist, product, qty,
            uom, qty_uos, uos, name, partner_id,
            lang, update_tax, date_order, packaging, fiscal_position, flag, context)
       
        if product:
            product_objs= self.pool.get('product.product')
            product_obj=product_objs.browse(cr,uid,product)
            res['value']['name'] = ""
            if product_obj.default_code:
                res['value']['name'] = unicode(product_obj.default_code) + " /"
            if product_obj.categ_id:
                res['value']['name'] += unicode(product_obj.categ_id.name)
            if product_obj.name:
                res['value']['name'] +=" /" +unicode(product_obj.name)    
            if product_obj.brand_id:
                res['value']['name'] +=" /"+unicode(product_obj.brand_id.name)
            if  product_obj.thickness:
                res['value']['name']+=" /"+unicode(product_obj.thickness)
            if  product_obj.measure:
                res['value']['name']+=" /"+unicode(product_obj.measure)    
            if  product_obj.density:
                res['value']['name']+=" /"+unicode(product_obj.density) 
            if  product_obj.country_id:
                res['value']['name']+=" /"+"Origen: "+unicode(product_obj.country_id.name)       
        return res
sale_order_line()    

class product_product(osv.osv):
    _inherit = 'product.product'

    def name_get(self, cr, uid, ids, context=None):
        return_val = super(product_product, self).name_get(cr, uid, ids, context=context)
        res = []
        if isinstance(ids, (int, long)):
            ids = [ids]
        for product in self.browse(cr, uid, ids, context=context):
            nombre = "["
            if product.default_code :
                nombre += unicode(product.default_code)+ " "
            if product.categ_id.name :
                nombre += product.categ_id.name +"] "+product.name
            
            res.append((product.id, (nombre)))
        return res or return_val   

product_product()


