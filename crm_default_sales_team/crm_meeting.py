from osv import fields,osv
from openerp.addons.base_status.base_state import base_state

class crm_meeting(base_state, osv.Model):
    """ Model for CRM meetings """
    _inherit = 'crm.meeting'
    
    def _get_user_default_sales_team(self, cr, uid, ids, context={}):
        user= self.pool.get('res.users').browse(cr,uid,uid)
        sale_team_id=user.default_section_id.id
        return sale_team_id or False
    _columns={
              'section_id': fields.many2one('crm.case.section', 'Sales Team'),
              }
    _defaults = {
                 'section_id': _get_user_default_sales_team,
                 }
    
crm_meeting()