from osv import fields,osv

class crm_phonecall(osv.osv):
    _inherit='crm.phonecall'
    
    def _get_user_default_sales_team(self, cr, uid, ids, context={}):
        user= self.pool.get('res.users').browse(cr,uid,uid)
        sale_team_id=user.default_section_id.id
        return sale_team_id or False
    
    _defaults = {
                 'section_id': _get_user_default_sales_team,
                 }
    
crm_phonecall()