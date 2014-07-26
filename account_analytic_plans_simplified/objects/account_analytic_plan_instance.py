# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2014 TRESCLOUD Cia Ltda (trescloud.com)
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
from openerp import netsvc
from openerp.tools.translate import _


class account_analytic_plan_instance(osv.osv):
    _inherit = "account.analytic.plan.instance"

    def name_get(self, cr, uid, ids, context=None):
        '''
        Al nombre original le agregamos la cadena completa de centros de costos involucrados
        '''       
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = super(account_analytic_plan_instance,self).name_get(cr, uid, ids, context=context)
        res2 = []
        account_analytic_plan_instance_line_obj = self.pool.get('account.analytic.plan.instance.line')
        account_analytic_plan_instance_lines_ids = account_analytic_plan_instance_line_obj.search(cr, uid, [('plan_id','in',ids)], limit=100, context=context)
        for account_analytic_plan_instance_id, name in res:
            analytic_plan_lines = account_analytic_plan_instance_line_obj.read(cr, uid, account_analytic_plan_instance_lines_ids, ['rate','analytic_account_id'], context=context)
            analytic_plan_lines_names = []
            for record in analytic_plan_lines:
                rate = str(record['rate']) + '% '
                analytic_account_name = (record['analytic_account_id'] and record['analytic_account_id'][1] + ' ' or '')
                analytic_plan_lines_names.append(rate + analytic_account_name)
            new_name = ', '.join(analytic_plan_lines_names) # + name # el nombre viejo ya no es importante
            res2.append((account_analytic_plan_instance_id, new_name))
        return res2

    def _distribute_100percent(self, cr, uid, ids, context=None):
        '''
        Valida que la suma de porcentajes sea 100%
        '''
        sum = 0.0
        account_analytic_plan_instance_line_obj = self.pool.get('account.analytic.plan.instance.line')
        account_analytic_plan_instance_lines_ids = account_analytic_plan_instance_line_obj.search(cr, uid, [('plan_id','in',ids)], limit=100, context=context)
        for lines in account_analytic_plan_instance_line_obj.browse(cr, uid, account_analytic_plan_instance_lines_ids, context=context):
            sum += lines.rate
        cien = 100.0
        if round(sum,2) == round(cien,2):
            return True
        return False 


     
    _constraints = [
                    (_distribute_100percent, _('Error: The cost distribution must match 100%, please review the percentages'), ['account_ids']),
                    ]
    
account_analytic_plan_instance()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
