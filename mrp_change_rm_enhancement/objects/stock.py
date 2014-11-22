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

from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp import netsvc
from openerp.tools import float_compare
import time

class stock_move(osv.osv):
    """
    Production Orders / Manufacturing Orders
    """
    _inherit = 'stock.move'
    
    def _calculate_cost(self, cr, uid, ids, name, args, context=None):
        res = {}
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
        'product_standard_price': fields.function(_calculate_cost_price, string='Product Price',digits_compute=dp.get_precision('Product Price'), type="float"),
        'cost_total': fields.function(_calculate_cost, string='Costo Total',digits_compute=dp.get_precision('Product Price'), type="float"),
        }
   
stock_move() 

class mrp_production(osv.osv):
    """
    Production Orders / Manufacturing Orders
    """
    _inherit = ['mrp.production','mail.thread', 'ir.needaction_mixin']
    _name = 'mrp.production'
    #===========================================================================
    # Metodo que calcula el costo real
    #===========================================================================
    def _calculate_total_cost(self, cr, uid, ids, name, args, context=None):
        res = {}
        area = 0.0
        movelines = []
        for object in self.browse(cr, uid, ids):
            if object.move_lines != []:
                movelines=object.move_lines
            elif object.move_lines2 != []:
                movelines=object.move_lines2
            for line in movelines:
                area += line.product_qty * line.product_standard_price
            res[object.id] = area
            area = 0.0
        return res
    
    def _calculate_unit_cost(self, cr, uid, ids, name, args, context=None):
        res = self._calculate_total_cost(cr, uid, ids, name, args, context)
        values_mrp = self.read(cr, uid, ids, ['product_qty'], context=context)
        product_qty = values_mrp[0]['product_qty']
        res[ids[0]] = res[ids[0]] / product_qty
        return res
    #===========================================================================
    # Metodo que setea el costo teorico del producto
    #===========================================================================
    def create(self, cr, uid, values, context=None):
        mrp_production_obj=self.pool.get('mrp.production')
        res = super(mrp_production, self).create(cr, uid, values, context=context)
        bom_read = mrp_production_obj.read(cr, uid, res, ['bom_id','product_qty'], context=context)
        bom_id= self.pool.get('mrp.bom').browse(cr, uid, bom_read['bom_id'][0])
        unit_cost = (bom_id.total_cost/bom_id.product_qty) 
        total_cost = unit_cost * bom_read['product_qty']
        mrp_production_obj.write(cr, uid, res, {'unit_cost' : unit_cost, 'total_cost' : total_cost}, context=context)
        return res
    
    #===========================================================================
    # Metodo para calcular la desviacion total del costo respecto real del teorico
    #===========================================================================
    
    def _calculate_total_deviation(self, cr, uid, ids, name, args, context=None):
        res = {}
        mrp_production_obj=self.pool.get('mrp.production')
        if ids == []:
            return False
        bom_read = mrp_production_obj.read(cr, uid, ids, ['total_cost','total_real_cost'], context=context)
        total_cost_show = bom_read[0]['total_real_cost']
        total_cost = bom_read[0]['total_cost']
        if total_cost == 0.0:
            res[ids[0]] = total_cost
            return res
        deviation = ((total_cost_show/total_cost) * 100) -100
        res[ids[0]] = deviation
        return res
    
    _columns = {
                'total_cost': fields.float('Total Cost', help="Total Cost of the Product", digits_compute=dp.get_precision('Product Price')),
                'unit_cost': fields.float('Unit Cost', help="Unit Cost of the product", digits_compute=dp.get_precision('Product Price')),
                'unit_real_cost': fields.function(_calculate_unit_cost, string='Unit Real Cost', help="Unit Real Cost of the product", digits_compute=dp.get_precision('Product Price')),
                'total_real_cost': fields.function(_calculate_total_cost, string='Total Real Cost', help="Total Real Cost of the product", digits_compute=dp.get_precision('Product Price'), type="float", store=True), 
                'total_deviation': fields.function(_calculate_total_deviation, type='float', help="Total Cost Deviation of the production", digits_compute=dp.get_precision('Product Price'),  string='Total Deviation'),
    }
    
    _defaults = {  
        'total_cost': 0.0,
        'unit_cost': 0.0,
        'unit_real_cost': 0.0,
        'total_real_cost': 0.0,
        'total_deviation': 0.0,
        }
    #===========================================================================
    # Metodo para actualizar todos los campos de calculados
    #===========================================================================
    
    def update_deviation(self, cr, uid, ids, context=None):
        res = {'unit_real_cost': 0.0, 'total_real_cost': 0.0, 'unit_deviation':0.0, 'total_deviation': 0.0 }
        treal_dict = self._calculate_total_cost(cr, uid, ids, '',[], context=context)
        tdev_dict = self._calculate_total_deviation(cr, uid, ids, '',[], context=context)
        values_mrp = self.read(cr, uid, ids, ['bom_id', 'product_qty'], context=context)
        ureal = treal_dict[ids[0]]/values_mrp[0]['product_qty']
        udev = tdev_dict[ids[0]]/values_mrp[0]['product_qty']
        self.bom_id_change(cr, uid, ids, values_mrp[0]['bom_id'][0], values_mrp[0]['product_qty'], context)
        res.update({
                    'unit_real_cost': ureal,
                    'total_real_cost': treal_dict[ids[0]],
                    'total_deviation': tdev_dict[ids[0]], 
                    })
        return self.write(cr, uid, ids, res)
    
    #===========================================================================
    # Metodo Onchange de bom_id
    #===========================================================================
    
    def bom_id_change(self, cr, uid, ids, bom_id, product_qty, context=None):
        res = super(mrp_production, self).bom_id_change(cr, uid, ids, bom_id, context=context)
        bom_ids = self.pool.get('mrp.bom').browse(cr, uid, bom_id)
        unit_cost = bom_ids.total_cost/bom_ids.product_qty
        res.update({
                    'unit_cost': unit_cost,
                    'total_cost': unit_cost * product_qty,
                    })
        return self.write(cr, uid, ids, res)
    
    #===========================================================================
    # Metodo Onchange de product_qty
    #===========================================================================
    
    def product_qty_change(self, cr, uid, ids,bom_id,product_qty, context=None):
        res = {'total_cost': 0.0}
        if bom_id in (None, False):
            return False 
        bom_ids = self.pool.get('mrp.bom').browse(cr, uid, bom_id)
        unit_cost = bom_ids.total_cost/bom_ids.product_qty
        res.update({
                     'total_cost': unit_cost * product_qty,
                    })
        return self.write(cr, uid, ids, res)
        
mrp_production()    
