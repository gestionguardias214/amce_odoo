# -*- coding: utf-8 -*-
from openerp import models, fields, api


class asw_relacionar_cateogira(models.TransientModel):
    _name = 'asw.relacionar.categoria'

    cat_id = fields.Many2one(string='Categoria', comodel_name='asw.categoria', ondelete='restrict')
    grupo_id = fields.Many2one(string='Grupo', comodel_name='asw.grupo', ondelete='restrict')
            #    fields.Many2one(string=u'Grupo',comodel_name='asw.grupo', ondelete='restrict', track_visibility='onchange',group_expand='_read_group_grupo')    
    prof_ids = fields.Many2many('asw.profesionales', 'prof_categorias_wizzard', 'wiz_id', 'module_id',
                               string='Relacionar Profesionales_categoria')

    @api.model
    def default_get(self, vals):
        result = super(asw_relacionar_cateogira, self).default_get(vals)             
        cat_id = self.env.context.get('active_id')
        cat = self.cat_id.browse(cat_id)
        profesionales = self.prof_ids.search([('pro_grupo','=', cat.cat_grupo.id)])
        # import ipdb; ipdb.set_trace()
        result['cat_id'] = cat_id
        result['grupo_id'] = cat.cat_grupo.id
        result['prof_ids'] = [(6, 0, profesionales.ids)]
        return result 

    @api.multi
    def relacionar_profesionales(self):  
        self.cat_id.write({
            'cat_profesional' : [(6, 0, self.prof_ids.ids)]
        })      
   