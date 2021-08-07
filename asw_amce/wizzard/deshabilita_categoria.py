# -*- coding: utf-8 -*-
from openerp import models, fields, api


class asw_deshabilitacion_cateogira(models.TransientModel):
    _name = 'asw.deshabilitacion.categoria'

    def deshabilitar(self):
        context = self.env.context
        cat_ids = context.get('active_ids',[])
        profs = self.env['asw.categoria'].search([ ('id', 'in', cat_ids) ])
        profs.write({
            'active': False
        })