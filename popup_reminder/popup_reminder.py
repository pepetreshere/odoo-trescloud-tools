# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from osv import osv, fields
from datetime import datetime
from tools import DEFAULT_SERVER_DATETIME_FORMAT

class popup_reminder(osv.Model):
    
    _name = 'popup.reminder'
    
    _description = 'Pop Up Alarms'
    
    def _links_get(self, cr, uid, context=None):
        
        if context and 'active_model' in context:
            name_object = context['active_model']
        else:
            context = {}
            name_object = 'crm.lead'
           
        obj = self.pool.get('res.request.link')
        ids = obj.search(cr, uid, [])
        res = obj.read(cr, uid, ids, ['object', 'name'], context=context)
        selection = [(r['object'], r['name']) for r in res]    
        selection.append((name_object, name_object))
        return selection
    
    _columns = {
        'name' : fields.char('Description', size=128, help="This field stores the description of the Alarm"),
        'alarm_date' : fields.datetime('Alarm Date', help="Date and time of Alarm"),
        'event_date' : fields.datetime('Event Date', help="Event date of Alarm"),
        'processed' : fields.boolean('Processed', help="If checked, indicates the alarm has already been shown"),
        'user_id' : fields.many2one('res.users', 'User', help="It indicates to whom the alarm should appear"),
        'alarm_ids' : fields.one2many('res.alarm', 'popup_reminder_id', 'Alarms'),
        'model_id' : fields.reference('Model', selection=_links_get, size=128),
        }
    
    _defaults = {
        'user_id' : lambda self, cr, uid, context=None: uid,
        }
    
    def open_alaram_popup(self, cr, uid, context=None):
        date_time_now = datetime.strftime(datetime.now(),DEFAULT_SERVER_DATETIME_FORMAT)
        reminder_ids = self.search(cr, uid, [('alarm_date', '<', date_time_now), ('processed', '=', False), ('user_id', '=', uid)])
        res = {}
        ir_model = self.pool.get("ir.model")
        res["reminder"] = []
        res["group"] = []
        res["ids"] = []
        model = []
        for reminder in self.read(cr, uid, reminder_ids, context = context):
            if reminder.get("model_id"):
                model_ids = ir_model.search(cr, uid, [("model", '=', reminder.get("model_id").split(",")[0])])
                model_name = ir_model.browse(cr, uid, model_ids[0], context=context).name
                if model_name not in model:
                    model.append(model_name)
                    res["group"].append({'name':reminder.get("model_id").split(",")[0], 'model_name':model_name})
                res["reminder"].append([reminder.get("model_id").split(",")[0], int(reminder.get("model_id").split(",")[1]), reminder.get("name"), reminder.get("event_date"), reminder.get("id")])
                res["ids"].append(reminder.get("id"))
        return res
    
    def accept_reminder(self, cr, uid, ids, context=None):
        if ids:
            self.write(cr, uid, ids, {'processed':True})
        return True
    
popup_reminder()

class res_alarm(osv.Model):
    
    _inherit = 'res.alarm'
    
    _columns = {
        'popup_reminder_id' : fields.many2one('popup.reminder', 'Alarm')
        }
    
res_alarm()

class crm_lead(osv.osv):
    
    _inherit = 'crm.lead'
    
    _columns = {
        'date_action': fields.datetime('Next Action Date', select=True),
        }
    
res_alarm()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: