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

from osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime


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

    def price_change(self, cr, uid, ids, price, discount, context=None):
        """
        Impedimos el cambio de precio y descuento, o registramos cambio y que se debe reexpandir.
        :param cr:
        :param uid:
        :param ids:
        :param price:
        :param discount:
        :return:
        """
        ids = ids if isinstance(ids, (list, tuple, set, frozenset)) else [ids]
        for obj in self.browse(cr, uid, ids, context):
            if not (obj.price_unit == price and obj.discount == discount) and obj.bom_line:
                return {
                    'value': {
                        'price_unit': obj.price_unit,
                        'discount': obj.discount
                    },
                    'warning': {
                        'title': 'Error!',
                        'message': 'No se puede cambiar el precio ni el descuento de una línea '
                                   'perteneciente a una receta'
                    }
                }
            else:
                if not obj.bom_line:
                    self.pool['sale.order'].write(cr, uid, [obj.order_id and obj.order_id.id], {}, context=dict(context or {}, should_expand=True))
                return {
                    'value': {}
                }
        return {
            'value': {}
        }

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if not context.get('sequence_preset', False):
            order_line_ids = self.pool['sale.order.line'].search(cr, uid, [('order_id', '=', vals['order_id'])], context=context)
            order_lines = self.pool['sale.order.line'].read(cr, uid, order_line_ids, fields=('sequence',), context=context)
            vals['sequence'] = max([obj['sequence'] if obj['sequence'] is not False else -1
                                    for obj in order_lines] or [-1]) + 1
        return super(sale_order_line, self).create(cr, uid, vals, context=context)

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
                          uom=False, qty_uos=0, uos=False, name='', partner_id=False,
                          lang=False, update_tax=True, date_order=False, packaging=False,
                          fiscal_position=False, flag=False, context=None):
        """
        Impedimos el cambio de producto y de cantidad, o registramos cambio y que se debe reexpandir.
        :param args:
        :param kwargs:
        :return:
        """
        result = {
            'warning': {},
            'value': {}
        }
        if not context:
            context = {}
        ids = ids if isinstance(ids, (list, tuple, set, frozenset)) else [ids]
        result = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty, uom,
                                                                qty_uos, uos, name, partner_id, lang, update_tax,
                                                                date_order, packaging, fiscal_position, flag,
                                                                context or {})
        for obj in self.browse(cr, uid, ids, context):
            if not (obj.product_id and obj.product_id.id == product and obj.product_uom_qty == qty) and obj.bom_line:
                result.setdefault('value', {})
                result['value'].update({
                    'product_uom_qty': obj.product_uom_qty,
                    'product_id': obj.product_id and obj.product_id.id
                })
                result.setdefault('warning', {})
                result['warning'].update({
                    'title': 'Error!',
                    'message': 'No se puede cambiar el producto ni la cantidad de una linea perteneciente a una receta'
                })
            else:
                if not obj.bom_line and not context.get('already_expanding', False):
                    self.pool['sale.order'].write(cr, uid, [obj.order_id and obj.order_id.id], {}, context=dict(context or {}, should_expand=True))
        return result
    
    def unlink(self, cr, uid, ids, context=None):
        """
        Desvincula desde el padre, jalando por cascade a los hijos
        :param cr:
        :param uid:
        :param ids:
        :param context:
        :return:
        """
        context = context or {}
        sale_order_line_obj = self.pool.get('sale.order.line')
        ids = ids if isinstance(ids, (list, tuple, set, frozenset)) else [ids]
        for line in sale_order_line_obj.browse(cr, uid, ids, context=context):
            # para cada objeto, navegamos hacia el padre superior
            if context.get('upwards', True):
                try:
                    while line.parent_sale_order_line:
                        line = line.parent_sale_order_line
                except ValueError:
                    # Absorbemos cualquier excepcion en este punto.
                    # Estas pueden darse por alguna cuestion relacionada a integridad referencial
                    #   ya que el objeto padre puede haberse borrado en alguna otra iteracion anterior.
                    pass

            try:
                super(sale_order_line, self).unlink(cr, uid, [line.id], context=context)
            except ValueError:
                # Absorbemos cualquier excepcion en este punto.
                # Estas pueden darse por alguna cuestion relacionada a integridad referencial
                #   ya que el objeto padre puede haberse borrado en alguna otra iteracion anterior.
                pass

    _columns = {
        'pack_depth': fields.integer('Depth', required=True, help='Depth of the product if it is part of a pack.'),
        'bom_line': fields.boolean('Bom Lines'),
        'parent_sale_order_line': fields.many2one('sale.order.line', string='Parent sale order line', required=False,
                                                  help='Depth of the product if it is part of a pack.',
                                                  ondelete="cascade")
    }
    _defaults = {
        'pack_depth': 0,
        'parent_sale_order_line': 0
    }

sale_order_line()


class sale_order(osv.osv):
    _inherit = 'sale.order'

    _columns = {
        'should_expand': fields.boolean(string='Should Expand BoM', required=True)
    }

    _defaults = {
        'should_expand': lambda *a, **kwa: False
    }

    def create_bom_line(self, cr, uid, line, order, main_discount=0.0, hierarchy=(), context=None):
        bom_obj = self.pool.get('mrp.bom')
        sale_line_obj = self.pool.get('sale.order.line')
        bom_ids = bom_obj.search(cr, uid, [('product_id', '=', line.product_id.id), ('type', '=', 'break_down_on_sale')])
        warnings = ''
        hierarchy = hierarchy + (line.product_id.id,)
        if bom_ids:
            bom_data = bom_obj.browse(cr, uid, bom_ids[0])
            factor = line.product_uos_qty / (bom_data.product_efficiency or 1.0)
            factor = rounding(factor, bom_data.product_rounding)
            if factor < bom_data.product_rounding:
                factor = bom_data.product_rounding
            for bom_line in bom_data.bom_lines:
                quantity = bom_line.product_qty * factor
                date_start = bom_line.date_start
                date_stop = bom_line.date_stop

                now = datetime.now().date()

                if date_start:
                    date_start = datetime.strptime(date_start, DEFAULT_SERVER_DATE_FORMAT).date()
                    if date_start > now:
                        continue

                if date_stop:
                    date_stop = datetime.strptime(date_stop, DEFAULT_SERVER_DATE_FORMAT).date()
                    if date_stop < now:
                        continue

                result = sale_line_obj.product_id_change(cr, uid, [], order.pricelist_id.id, bom_line.product_id.id,
                                                         quantity, bom_line.product_id.uom_id.id, quantity,
                                                         bom_line.product_id.uos_id.id, '', order.partner_id.id, False,
                                                         True, order.date_order, False, order.fiscal_position.id, False,
                                                         context=context or {})

                discount = result.get('value', {}).get('discount') or 0.0,
                
                if order.pricelist_id.visible_discount == True:
                    # if visible discount is installed and if enabled 
                    # use the discount provided by list price
                    discount = result.get('value', {}).get('discount') or 0.0
                else:
                    # we asume the visible discount is not enabled
                    # then we use as discount the discount of the main product.
                    print main_discount
                    discount = main_discount

                if bom_line.product_id.id in hierarchy:

                    pass
                    # comentamos el mensaje que agregamos porque a los de SF no les va a gustar ver esto asi.
                    # sin embargo, el codigo de abajo NO es erroneo.
                    ###########################################################################################
                    # warnings += """
                    #             Cannot expand BoM line for product: [%d] %s. Such product is misconfigured since it belongs to a BoM hierarchy it's also an ancestor for.
                    #             """ % (line.product_id.id, line.product_id.name)

                else:

                    warnings += result.get('warning') and result.get('warning').get('message') and \
                        "\nProduct :- %s\n%s\n" % (bom_line.product_id.name, result.get('warning').get('message')) or ''
                    vals = {
                        'order_id': order.id,
                        'name': '%s%s' % ('>' * (line.pack_depth+1), result.get('value', {}).get('name')),
                        'sequence': context['_shared']['sequence'],
                        'delay': bom_line.product_id.sale_delay or 0.0,
                        'product_id': bom_line.product_id.id,
                        # TODO: Esta funcionalidad deberia ser parametrizable
                        'price_unit': 0.0,  # result.get('value',{}).get('price_unit'),
                        'tax_id': [(6, 0, result.get('value', {}).get('tax_id'))],
                        'type': bom_line.product_id.procure_method,
                        'product_uom_qty': result.get('value', {}).get('product_uos_qty'),
                        'product_uom': result.get('value', {}).get('product_uom') or line.product_id.uom_id.id,
                        'product_uos_qty': result.get('value', {}).get('product_uos_qty'),
                        'product_uos': result.get('value', {}).get('product_uos') or line.product_id.uos_id.id,
                        'product_packaging': result.get('value', {}).get('product_packaging'),
                        'discount': discount,
                        'bom_line': True,
                        'th_weight': result.get('value',{}).get('th_weight'),
                        'pack_depth': line.pack_depth + 1,
                        'parent_sale_order_line': line.id
                    }

                    sale_id = sale_line_obj.create(cr, uid, vals, dict(context or {}, sequence_preset=True))
                    line_data = sale_line_obj.browse(cr, uid, sale_id, context)
                    context['_shared']['sequence'] += 1
                    warnings += self.create_bom_line(cr, uid, line_data, order, main_discount, hierarchy,
                                                     context)

        return warnings

    def expand_bom(self, cr, uid, ids, context=None, depth=0):
        if context is None:
            context = {}
        context.update({
            '_shared': {
                'sequence': 0
            }
        })
        if depth == 10:
            return True
        if type(ids) in [int, long]:
            ids = [ids]
        sale_line_obj = self.pool.get('sale.order.line')
        warnings = ''
        for order in self.browse(cr, uid, ids, context):
            delete_line_ids = sale_line_obj.search(cr, uid, [('bom_line', '=', True), 
                                                             ('order_id', '=', order.id)])
            if delete_line_ids:
                sale_line_obj.unlink(cr, uid, delete_line_ids, context=dict(context, upwards=False))
            for line in sale_line_obj.browse(cr, uid, sale_line_obj.search(cr, uid, [('order_id', '=', order.id)], order='sequence', context=context), context=context):
                # el descuento del producto principal del combo
                main_discount = line.discount
                if line.product_id and line.state == 'draft':
                    sale_line_obj.write(cr, uid, [line.id], {'sequence': context['_shared']['sequence']}, dict(context, already_expanding=True))
                context['_shared']['sequence'] += 1
                warnings += self.create_bom_line(cr, uid, line, order, main_discount, hierarchy=(), context=dict(context, already_expanding=True))
        context.update({'default_name': warnings})
        context.pop('_shared', None)
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
    
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        res = super(sale_order, self).create(cr, uid, vals, context=context)
        self.expand_bom(cr, uid, [res], context=context, depth=0)
        return res
    
    def write(self, cr, uid, ids, vals, context=None):
        """
        Debemos contemplar que, al guardar, puede que la guardada sea autonoma y que
          tengamos que refrescar todo el contenido, si así fue encargado. Si la guardada
          NO es autonoma, sino que pertenece a algun cambio registrado, entonces invocamos
          que se guarde y se marque para expandir.
        :param cr:
        :param uid:
        :param ids:
        :param vals:
        :param context:
        :return:
        """
        if context is None:
            context = {}

        # Nos quedamos con los elementos que existan en la base de datos. LA RAZON ES QUE si no filtramos asi,
        #   vamos a tener elementos para el WRITE que se refiere a elementos que no estan en la base de datos,
        #   y vamos a tener un bonito error.
        #
        # OJO tambien conservamos los nuevos eeh.
        existent_lines = self.pool['sale.order.line'].search(cr, uid, [('order_id', 'in', ids)], context=context)
        if 'order_line' in vals:
            vals['order_line'] = [e for e in vals.get('order_line', []) if (e[0] == 0 or e[1] in existent_lines)]

        # nos quedamos con los elementos NUEVOS de sale.order.line
        new_order_lines = [e for e in vals.get('order_line', []) if e[0] == 0]

        if not context.get('should_expand', False):
            """
            Entramos aca si cualquiera de las dos condiciones se cumple:
            1. Es una guardada normal (es decir, no es una guardada que preguarda la indicación de expandir.
               En este sentido, ya que no estamos preindicando, lo que nos toca es revisar si teniamos anteriormente
                 una preindicacion para expandir, y obedecerla.
            2. Es una guardada que modifica las lineas que existen en la orden de venta. En tal caso deberiamos
                 forzar una expansion, como si hubieramos tenido la indicacion de expandir puesta explicitamente.
            """

            ids = ids if isinstance(ids, (list, tuple, set, frozenset)) else [ids]
            for values in self.read(cr, uid, ids, fields=('id', 'should_expand'), context=context):
                if values['should_expand'] or new_order_lines:
                    super(sale_order, self).write(cr, uid, [values['id']], dict(vals, should_expand=False), context)
                    self.expand_bom(cr, uid, [values['id']], context=context, depth=0)
                else:
                    super(sale_order, self).write(cr, uid, [values['id']], vals, context)
        else:
            # Esta llamada se realiza cuando guardamos mediante write() con el contexto explicito.
            super(sale_order, self).write(cr, uid, ids, dict(vals, should_expand=True), context)

        return True
sale_order()

