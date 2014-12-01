# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2013-Present Acespritech Solutions Pvt. Ltd.
#    (<http://www.acespritech.com>).
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
from openerp import netsvc
import time

# se crea vista temporal  para  actualizar o resetear tiempo y que se actualice con el guardado
class wizard_product_msl(osv.osv_memory):
    _name = 'wizard.product.msl'
    _columns = {
#        DR TODO: agregar campo para vista temporal 
    'last_baket_time': fields.datetime('last baket time', type='datetime',help="Last date that the component had been sent to bake."),
     
    }
    _defaults = {
        # se pone por defecto la hora actual para realizar la actualización del tiempo         
        'last_baket_time': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    
     # def save_time_msl(self, cr, user, ids, context=None):
     #Se busca el registro  asociado al campo de la base de datos para no confundir el numero de seriales
         
    def save_time_msl(self, cr, user, ids,  context=None):
        if context is None:
                context = {}
        #se crea el objeto de la clase  production.lot para ser ocupado en la actualización de la fecha         
        prodlot_obj = self.pool.get('stock.production.lot')
        # se interactua con la vista para poder ocupar  el serial unico asociado al producto
        prodlot_id = prodlot_obj.browse(cr,user,context.get('prodlot_id',False))
        # se guarda el tiempo actualizado del producto 
        prodlot_obj.write(cr, user, [prodlot_id.id], {'last_baket_time': context.get('last_baket_time',False)}, context=context)
        return True
  
wizard_product_msl()

