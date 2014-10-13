# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Serpent Consulting Services (<http://www.serpentcs.com>)
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

def rounding(f, r):
    import math
    if not r:
        return f
    return math.ceil(f / r) * r

class mrp_bom(osv.osv):
    """
    Defines bills of material for a product.
    """
    _inherit = 'mrp.bom'

    _columns = {
        'type': fields.selection([('normal','Normal BoM'),('phantom','Sets / Phantom'),('break_down_on_sale', 'Break down on Sale Order')], 'BoM Type', required=True,
                                 help= "If a by-product is used in several products, it can be useful to create its own BoM. "\
                                 "Though if you don't want separated production orders for this by-product, select Set/Phantom as BoM type. "\
                                 "If a Phantom BoM is used for a root product, it will be sold and shipped as a set of components, instead of being produced."),
        }

mrp_bom()

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'

    _columns = {
        'pack_depth': fields.integer('Depth', required=True, help='Depth of the product if it is part of a pack.'),
        'bom_line': fields.boolean('Bom Lines'),
    }
    _defaults={
        'pack_depth':0      
               }

sale_order_line()

class sale_order(osv.osv):
    _inherit = 'sale.order'

    def create_bom_line(self, cr, uid, line, order, sequence, main_discount=0.0, context=None):
        bom_obj = self.pool.get('mrp.bom')
        sale_line_obj = self.pool.get('sale.order.line')
        bom_ids = bom_obj.search(cr, uid, [('product_id', '=', line.product_id.id), ('type', '=', 'break_down_on_sale')])
        warnings = ''
        if bom_ids:
            bom_data = bom_obj.browse(cr, uid, bom_ids[0])
            factor = line.product_uos_qty / (bom_data.product_efficiency or 1.0)
            factor = rounding(factor, bom_data.product_rounding)
            if factor < bom_data.product_rounding:
                factor = bom_data.product_rounding
            for bom_line in bom_data.bom_lines:
                quantity = bom_line.product_qty * factor
                result = sale_line_obj.product_id_change(cr, uid, [], order.pricelist_id.id, bom_line.product_id.id, quantity, bom_line.product_id.uom_id.id, quantity, bom_line.product_id.uos_id.id, 
                            '', order.partner_id.id, False, True, order.date_order, False, order.fiscal_position.id, False, context=context)

                discount = result.get('value',{}).get('discount') or 0.0,
                
                if order.pricelist_id.visible_discount == True:
                    # if visible discount is installed and if enabled 
                    # use the discount provided by list price
                    discount = result.get('value',{}).get('discount') or 0.0
                else:
                    # we asume the visible discount is not enabled
                    # then we use as discount the discount of the main product.
                    print main_discount
                    discount = main_discount
                    
                warnings += result.get('warning') and result.get('warning').get('message') and \
                    "\nProduct :- " + bom_line.product_id.name + "\n" + result.get('warning').get('message') +"\n" or ''
                vals = {
                    'order_id': order.id,
                    'name': '%s%s' % ('>'* (line.pack_depth+1), result.get('value',{}).get('name')),
                    'sequence': sequence,
                    'delay': bom_line.product_id.sale_delay or 0.0,
                    'product_id': bom_line.product_id.id,
                    'price_unit': 0.0 ,#result.get('value',{}).get('price_unit'),
                    'tax_id': [(6,0,result.get('value',{}).get('tax_id'))],
                    'type': bom_line.product_id.procure_method,
                    'product_uom_qty': result.get('value',{}).get('product_uos_qty'),
                    'product_uom': result.get('value',{}).get('product_uom') or line.product_id.uom_id.id,
                    'product_uos_qty': result.get('value',{}).get('product_uos_qty'),
                    'product_uos': result.get('value',{}).get('product_uos') or line.product_id.uos_id.id,
                    'product_packaging': result.get('value',{}).get('product_packaging'),
                    'discount': discount,
                    'bom_line': True,
                    'th_weight': result.get('value',{}).get('th_weight'),
                    'pack_depth': line.pack_depth + 1,
                }
                sale_id = sale_line_obj.create(cr, uid, vals, context)
                line_data = sale_line_obj.browse(cr, uid, sale_id, context)
                warnings += self.create_bom_line(cr, uid, line_data, order, sequence, main_discount, context)

        return warnings

    def expand_bom(self, cr, uid, ids, context=None, depth=0):
        if context is None:
            context={}
        if depth == 10:
            return True
        if type(ids) in [int, long]:
            ids = [ids]
        sale_line_obj = self.pool.get('sale.order.line')
        warnings = ''
        for order in self.browse(cr, uid, ids, context):
            sequence = -1
            delete_line_ids = sale_line_obj.search(cr, uid, [('bom_line', '=', True), ('order_id', '=', order.id)])
            if delete_line_ids:
                sale_line_obj.unlink(cr, uid, delete_line_ids)
            for line in order.order_line:
                # el descuento del producto principal del combo
                main_discount = line.discount
                if line.product_id and line.state == 'draft':
                        sequence += 1
                        if sequence > line.sequence:
                            sale_line_obj.write(cr, uid, [line.id], {'sequence': sequence}, context)
                        else:
                            sequence = line.sequence
#                        for bom_line in bom_data.bom_lines:
                        sequence += 1
                warnings += self.create_bom_line(cr, uid, line, order, sequence, main_discount, context)
        context.update({'default_name': warnings})
        vals = True
        if warnings:
            vals = {
                    'name': ('Expand BOM Warnings'),
                    'context': context,
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'expand.bom.message',
                    'res_id': False,
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                }
        return vals

sale_order()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
