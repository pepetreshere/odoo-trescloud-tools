  # -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 CodUP (<http://codup.com>).
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

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from tools.translate import _
from openerp import tools
import base64
class account_asset_asset(osv.osv):
    """
    Assets
    """
 
    _name = 'account.asset.asset'
    _inherit = ['mail.thread', 'account.asset.asset','ir.needaction_mixin']
    
    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image, avoid_resize_medium=True)
        return result

    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
    
    def write(self, cr, uid, ids, vals, context=None):
       """
       This function write an entry in the openchatter whenever we change important information
       """
       for asset in self.browse(cr, uid, ids, context):
           changes = []            
           if 'image' in vals and asset.image != vals['image']:
               newvalue = vals['image'] 
               oldvalue = asset.image or _('None')
               changes.append(_("Actualizado imagen de Activo"))
           if len(changes) > 0:
                self.message_post(cr, uid, [asset.id], body=", ".join(changes), context=context)    
       asset_id = super(account_asset_asset,self).write(cr, uid, ids, vals, context)
       
       return True

    _columns = {
              #INICIO AGREGANDO NUEVOS ATRIBUTOS A LOS FIELDS
                'name': fields.char('Name', size=64, required=True, select=1,track_visibility='onchange'), # agrego al field la trazabilidad para mensajes 
                'code': fields.char('Reference', size=32, readonly=True, states={'draft':[('readonly',False)]}, track_visibility='onchange'),# agrego al field la trazabilidad para mensajes 
                'parent_id': fields.many2one('account.asset.asset', 'Parent Asset', readonly=True, states={'draft':[('readonly',False)]},track_visibility='onchange'),# agrego al field la trazabilidad para mensajes
                'purchase_value': fields.float('Gross Value', required=True, readonly=True, states={'draft':[('readonly',False)]},track_visibility='onchange'),# agrego al field la trazabilidad para mensajes
             #   'value_residual': fields.function(_amount_residual, method=True, digits_compute=dp.get_precision('Account'), string='Residual Value',track_visibility='onchange'), # agrego al field la trazabilidad para mensajes
              #FIN AGREGANDO NUEVOS ATRIBUTOS A LOS FIELDS  
                
                #'property_stock_asset': fields.property('stock.location', type='many2one', relation='stock.location', string="Asset Location", view_load=True, help="This location will be used as the destination location for installed parts during asset life."),
                'property_stock_asset':fields.many2one('stock.location', 'Asset Location', required=False,track_visibility='onchange'), 
                'user_id': fields.many2one('hr.employee', 'Assigned to', track_visibility='onchange'),
                'model': fields.char('Model', size=64, track_visibility='onchange'),
                'manufacturer': fields.many2one('account.asset.manufacturer', 'Manufacturer',track_visibility='onchange'),# agrego al field la trazabilidad para mensajes
                'serial': fields.char('Serial no.', size=64, track_visibility='onchange'),
        # image: all image fields are base64 encoded and PIL-supported
                'image': fields.binary("Image", help="This field holds the image used as image for the asset, limited to 1024x1024px."),
                'image_medium': fields.function(_get_image, fnct_inv=_set_image,
            string="Medium-sized image", type="binary", multi="_get_image",
            store={
                'account.asset.asset': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized image of the asset. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved, "\
                 "only when the image exceeds one of those sizes. Use this field in form views or some kanban views."),
                'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Small-sized image", type="binary", multi="_get_image",
            store={
                'account.asset.asset': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Small-sized image of the asset. It is automatically "\
                 "resized as a 64x64px image, with aspect ratio preserved. "\
                 "Use this field anywhere a small image is required."),
    }
    
account_asset_asset()

class account_asset_manufacturer(osv.osv):
    """
    Manufacturer Assets
    """
 
    _name = 'account.asset.manufacturer'
    _inherit = ['mail.thread','ir.needaction_mixin']
    _columns = {
              #INICIO AGREGANDO NUEVOS ATRIBUTOS A LOS FIELDS
                'name': fields.char('Name', size=64, required=True, select=1,track_visibility='onchange'), # agrego al field la trazabilidad para mensajes 
    }
    
account_asset_manufacturer()
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
