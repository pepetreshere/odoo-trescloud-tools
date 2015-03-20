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

from __future__ import division
from openerp.osv import fields, orm, osv
from openerp.tools.translate import _
import time
from datetime import *
import math
from openerp.tools import float_compare

import pytz

#===============================================================================
# INCOMPLETO FALTA UNA PARTE
# class stock_picking(osv.osv):
#     _inherit = 'stock.picking'
#     
#     def draft_force_assign(self, cr, uid, ids, *args):
#         res = super(stock_picking, self).draft_force_assign(cr, uid, ids, *args)
#         for pick in self.browse(cr, uid, ids):
#             for move in pick.move_lines:
#                 if move.product_id == move.prodlot_id.product_id and move.product_id:
#                     if 
#                
#             wf_service.trg_validate(uid, 'stock.picking', pick.id,
#                 'button_confirm', cr)
#         return res
# stock_picking()
#===============================================================================

class stock_production_lot(osv.osv):
    
    _inherit = 'stock.production.lot'
    _name = 'stock.production.lot'
    
    # Array que contiene los estados de los niveles de humedad
    
    _MSL_STATUS=[('ready', 'Ready'),
             ('alert', 'Alert'),
             ('donotuse','Don\'t Use')]

    #Metodo que da el nombre de los seriales
    def name_get(self, cr, uid, ids, context=None):
        result = []
        for record in self.browse(cr, uid, ids, context=context):
            name = record.name
            for status in self._MSL_STATUS:
                if status[0] == record.msl_status:
                    name +=  ' [' + status[1] + ']'
            result.append((record.id,name))
        return result
    
    # Metodo que analiza el estado en que se encuentra el serial
    def _msl_calculate(self, cr, uid, ids, name, args, context=None):
        res = {}      
        for lot in self.browse(cr,uid,ids):
            res[lot.id] = {'msl_status':''} 
            control = False
            #===============================================================
            # cr.execute('select moisture_exposed_time from stock_production_lot where id=%s', (lot.id,))
            # time_read = map(lambda x: x[0], cr.fetchall())
            #===============================================================
            met, factor, open_time = 0.0, 0.0, 0.0
            # Si existe serial se busca sus variables asociadas al msl
            # las condiciones estan dadas por los porcentajes de humedad que soporte el producto
            # segun su msl 
            if lot.moisture_exposed_time:
                met = lot.moisture_exposed_time
            elif context is not None and 'moisture_exposed_time' in context:
                met = context.get('moisture_exposed_time', 0.0)
                #===========================================================
                # if met == 0.0:
                #     met = time_read[0]
                #===========================================================
            if lot.product_id.msl_id:
                factor = lot.product_id.msl_id.alarm_percentage/100
                control = lot.product_id.msl_id.control
            if lot.open_time:
                open_time = lot.open_time
            if control:
                res[lot.id] = 'ready'
            elif met == 0.0 and factor == 0.0 and open_time == 0.0:
                res[lot.id] = 'ready'
            elif met < factor * open_time:
                res[lot.id] = 'ready'
            elif met > factor * open_time and met < open_time:
                res[lot.id] = 'alert'
            elif met >= open_time:
                res[lot.id] = 'donotuse'
        return res
    
    # Se busca todos los stock.moves que tengan humedad su bodega origen ya que es el fin del movimiento
    # ademas debe ser mayor que la fecha de last baked time, y que tenga los mismos seriales el movimiento
     
    def _moisture_exposed_time_calculate(self, cr, uid, ids, name, args, context=None):           
        res = {}
        time_baked = "1900-01-01 00:00:00"
        move_pool = self.pool.get('stock.move')
        picking_pool = self.pool.get('stock.picking')
        move_ids = move_pool.search(cr, uid, [('prodlot_id', 'not in', [0.0])],context=context)
        for lot in self.browse(cr,uid,ids):
            res[lot.id] = 0.0
            if lot.product_id.msl_id:
                moisture_exposed_time = 0.0
                for move_id in move_ids:
                    move = move_pool.browse(cr,uid,move_id)
                    if lot.last_baket_time:
                        time_baked = lot.last_baket_time
                    if lot == move.prodlot_id and move.location_id.hasmoisture and datetime.strptime(move.date, "%Y-%m-%d %H:%M:%S") > datetime.strptime(time_baked, "%Y-%m-%d %H:%M:%S"):
                        moisture_exposed_time += move.duration                        
                res[lot.id] = moisture_exposed_time
                context.update({'moisture_exposed_time':moisture_exposed_time})
            if res[lot.id] == 0.0:
                picking_ids = picking_pool.search(cr, uid, [
                                ('state', '=', 'done'),
                                ('type', '=', 'internal')],context=context)
                prev_move_ids = move_pool.search(cr, uid, [
                                                      ('state', '=', 'done'),
                                                      ('location_dest_id.hasmoisture', '=', True),
                                                      ('prodlot_id', '=', lot.id),
                                                      ('picking_id','in', picking_ids), 
                                                      ('date', '>', (lot.last_baket_time if lot.last_baket_time else time_baked))],
                                            order='date desc', context=context)
                if prev_move_ids:
                    timeNow = datetime.now()
                    timeRest = (timeNow - datetime.strptime(
                        move_pool.browse(cr, uid, prev_move_ids[0]).date, '%Y-%m-%d %H:%M:%S'
                        ))
                    real_time = move_pool.total_seconds(timeRest) / 60.0 / 60.0
                    res[lot.id] = real_time 
        return res
    
    # obtiene los lotes que estan siendo modificados las variables, ver _store_rules
    def _get_lots(self, cr, uid, ids, context=None):
        lot_ids = []
        for lot in self.browse(cr, uid, ids, context=context):
                lot_ids.append(lot.id) 
        return lot_ids
    
    # obtiene los lotes que estan siendo modificados de los stock.moves, ver _store_rules
    def _get_by_moves(self, cr, uid, ids, context=None):
        lot_ids = []
        move_ids = []
        for move in self.browse(cr, uid, ids, context=context):
            if move.prodlot_id and move.prodlot_id.id not in lot_ids:               
                lot_ids.append(move.prodlot_id.id) 
        return lot_ids
    
    # obtiene los lotes que estan siendo modificados product ver _store_rules
    def _get_msl(self, cr, uid, ids, context=None):
        lot_ids = []
        lot_pool = self.pool.get('stock.production.lot')
        product_id = False
        for product in self.browse(cr, uid, ids, context=context):
            lot_ids = lot_pool.search(cr,uid,[('product_id','=',product.id)]) 
        return lot_ids
    
    # obtiene los lotes que estan siendo modificados product.msl ver _store_rules
    def _get_prod_msl(self, cr, uid, ids, context=None):
        lot_ids = []
        lot_pool = self.pool.get('stock.production.lot')
        product_pool = self.pool.get('product.product')
        product_id = False
        for product_msl in self.browse(cr, uid, ids, context=context):
            product_ids = product_pool.search(cr,uid,[('msl_id','=', product_msl.id)]) 
            lot_ids = lot_pool.search(cr,uid,[('product_id','in',product_ids)]) 
        return lot_ids
                     
    _store_rules = {
                    'product.product': (_get_msl, ['msl_id'],0),
                    'product.msl': (_get_prod_msl, ['open_time'],0),
                    'stock.production.lot': (_get_lots, ['product_id', 'moisture_exposed_time', 'last_baket_time', 'move_ids', 'msl_id','open_time'], 0),
                    'stock.move': (_get_by_moves, ['duration'], 0),
                    }

    _columns = {
                'msl_status': fields.function(_msl_calculate, 
                                              method=True, 
                                              type='selection', 
                                              selection=_MSL_STATUS, 
                                              string='MSL Status',  
                                              help="Ready, Alerted or Don't Use. If state is in alerted or don't use you should send the lot to baking"),
                'moisture_exposed_time': fields.function(_moisture_exposed_time_calculate,
                                                         method=True, type='float', 
                                                         string='Moisture exposed time', 
                                                         digits=(15,2), 
                                                         help="The time this specific lot has been exposed to moisture, is calculated according to the times in the related stock moves in locations with moisture."),                
                'msl_id': fields.related('product_id', 'msl_id', type='many2one', relation='product.msl', string="MSL", help="Moisture Sensitivity Level relates to the packaging and handling precautions for some semiconductors"),
                'open_time': fields.related('product_id', 'open_time', type='float', relation='product.product', string="Open Time in hours", help="Maximum period of time that the component can be used, after that time the component must be sent to bake."),
                'last_baket_time': fields.datetime('Last Baked Time', type='datetime',help="Last date that the component had been sent to bake."),                
                }
    
    _default = {
                'msl_status': 'ready',
                'last_baket_time': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
                }
stock_production_lot()

class stock_partial_picking(osv.osv):
    
    _inherit = 'stock.partial.picking.line'
    _name = 'stock.partial.picking.line' 
    
    # Ochange de lotes en esta clase alerta para que se mande este producto al horno
    def onchange_prodlot_id(self, cr, uid, ids, prodlot_id, product_id, context=None):
        prod_id = self.pool.get('product.product').browse(cr, uid, product_id)
        lot = False
        value = {'prodlot_id': prodlot_id}
        warning = {}
        if prod_id.msl_id:
            if prodlot_id:
                    lot = self.pool.get('stock.production.lot').browse(cr, uid, prodlot_id)
            if lot:
                if lot.msl_status and lot.msl_status != 'ready':
                    warning = {
                               'title': 'Warning Production',
                               'message': "You must send this product lot to bake."
                    }
                    return {'warning': warning, 'value': value }
            else:
                return {'value': value}
        return {'warning': warning, 'value': value }

stock_partial_picking()

class stock_move(osv.osv):
    
    _inherit = 'stock.move'
    _name = 'stock.move' 
    
    def float_time_convert(self, float_val):
        hours = math.floor(abs(float_val))
        mins = abs(float_val) - hours
        mins = round(mins * 60)
        if mins >= 60.0:
            hours = hours + 1
            mins = 0.0
        float_time = '%02d:%02d' % (hours,mins)
        return float_time

    def float_to_datetime(self, float_val):
        str_float = self.float_time_convert(float_val)
        hours = int(str_float.split(':')[0])
        minutes = int(str_float.split(':')[1])
        days = 1
        if hours / 24 > 0:
            days += hours / 24
            hours = hours % 24
        return datetime(1900, 1, int(days), hours, minutes)

    def float_to_timedelta(self, float_val):
        str_time = self.float_time_convert(float_val)
        return timedelta(0, int(str_time.split(':')[0]) * 60.0*60.0
            + int(str_time.split(':')[1]) * 60.0)
    
    def total_seconds(self, td):
        return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6     
    
    # Obtiene el tiempo de exposicion a humedad de las seriales
    def _get_expose_duration(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        zone = False
        if 'tz' in context and context.get("tz","UTC"):
            zone = context.get("tz","UTC") 
        else: 
            zone = "UTC"
        active_tz = pytz.timezone(zone)
        move_pool = self.pool.get('stock.move')
        picking_pool = self.pool.get('stock.picking')
        str_now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        for move_id in ids:
            duration = 0.0
            move = self.browse(cr, uid, move_id, context=context)
            res[move.id] = {}
            
            # fecha en que termina la transaccion
            move_ends = datetime.strptime(
                move.date, '%Y-%m-%d %H:%M:%S'
                ).replace(tzinfo=pytz.utc).astimezone(active_tz)
            prev_move_date = str_now
            prev_move_ids = False
            
            # se buscan las transacciones que esten listas y ademas que tengan los movimientos 
            # en bodegas sean internal, los movimientos previos son los que cumplan con estas condiciones
            # y se lo ordena por fechas desc 
            if move.location_id:
                picking_ids = picking_pool.search(cr, uid, [
                                            ('state', '=', 'done'),
                                            ('type', '=', 'internal')],context=context)
                prev_move_ids = self.search(cr, uid, [
                                                      ('state', '=', 'done'),
                                                      ('location_dest_id', '=', move.location_id.id),
                                                      ('prodlot_id', '=', move.prodlot_id.id),
                                                      ('picking_id','in', picking_ids),
                                                      ('date', '<', move.date)], order='date desc', context=context)
                
                # si no hay movimientos previos iguala las fechas de inicio y fin de movimiento
                if not prev_move_ids:
                    prev_move_date = move.date
                else:
                    #Si hay movimientos se toma el inmediato anteriros que cumpla con las condiciones
                    prev_move = self.browse(cr, uid, prev_move_ids[0], context=context)
                    prev_move_date = prev_move.date
                move_begins = datetime.strptime(
                    prev_move_date, '%Y-%m-%d %H:%M:%S'
                    ).replace(tzinfo=pytz.utc).astimezone(active_tz)
                duration_delta = move_ends - move_begins 
                duration = self.total_seconds(duration_delta) / 60.0 / 60.0
                
            #Calculo de la duracion
            res[move.id]['duration'] = duration
            res[move.id]['end_datetime'] = prev_move_date
        return res

    _columns = {
        'duration': fields.function(_get_expose_duration, 
                                    method=True, 
                                    multi='duration', 
                                    string="Exposed Duration",
                                    store=False),
        'end_datetime': fields.function(_get_expose_duration, 
                                        method=True, 
                                        multi='duration', 
                                        type="datetime", 
                                        string="End date time",
                                        store=True),
        'dummy_field': fields.char('Dummy field',
                                   help="Used to cause a write that updates the stored function fields")
    }
    # Funcion que permite  validar que los productos que tienen  asociados seriales  puedan transferir productos de diferentes bodegas
    # ademas se informa  que se pueda transferir todo el lote  de bodegas del mismo tipo
    # las alertas  se informan cuando la cantidad es menor y mayor a la confirmada
    def _check_location(self, cr, uid, ids, context=None):
        for record in self.browse(cr, uid, ids, context=context):
            if record.prodlot_id:
                if record.location_id.usage == record.location_dest_id.usage:
                    if record.product_qty > record.prodlot_id.stock_available:
                        raise osv.except_osv(_('Error'), _('You cannot move the product %s because the quantity you plan to move is greater than the quantity available, you have to move the whole quantity of serial.')% (record.product_id.name))
                        #raise osv.except_osv(_('Error'), _('You cannot move the product, the amount is greater than the available.')% (record.product_id.name, record.location_id.name))
                    elif record.product_qty < record.prodlot_id.stock_available:
                        raise osv.except_osv(_('Error'), _('You cannot move the product %s because the quantity you plan to move is less than the quantity available, you have to move the whole quantity of serial')% (record.product_id.name))
        return True
    
    _constraints = [
       (_check_location, 'You cannot move products from this location to another.',
           ['location_id','location_dest_id'])]
    
    # Onchange de los seriales para que indique que el serial tiene que mandarse al horno en stock.move                         
    def onchange_lot_id(self, cr, uid, ids, prodlot_id=False, product_qty=False,
                        loc_id=False, product_id=False, uom_id=False, context=None):
        """ On change of production lot gives a warning message.
        @param prodlot_id: Changed production lot id
        @param product_qty: Quantity of product
        @param loc_id: Location id
        @param product_id: Product id
        @return: Warning message
        """
        warning = super(stock_move,self).onchange_lot_id(cr, uid, ids, prodlot_id, product_qty,
                        loc_id, product_id, uom_id, context)
        message=''
        if warning and warning['warning'] and warning['warning']['message']:
                    message = warning['warning']['message']
        if not prodlot_id:
            return {'warning': warning}
        product_obj = self.pool.get('product.product')
        product_id = product_obj.browse(cr, uid, product_id, context)
        prodlot = self.pool.get('stock.production.lot').browse(cr, uid, prodlot_id, context)
        if product_id.msl_id:
            if prodlot and prodlot.msl_status and prodlot.msl_status != 'ready':
                
                warning = {
                           'title': 'Warning!',
                           'message': message + "\nYou must send this product lot to bake."
                }
                return {'warning': warning}
        if warning is {}:
            return {'warning': warning}
        else:
            return warning
    
stock_move()

class stock_location(osv.osv):
    
    _inherit = 'stock.location'
    _name = 'stock.location'
    
    _columns = {
            'hasmoisture':fields.boolean('Has Moisture', required=False, help='Check this, if the location has moisture.'),
                    }
stock_location()