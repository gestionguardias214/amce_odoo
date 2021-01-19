# -*- coding: utf-8 -*-
from openerp import api, models, fields
from odoo import exceptions

class asw_resp(models.Model):
    _name = 'asw.ap_respiratorio'
    _description = 'Ap. Respiratorio'
    _ord = 'resp_nombre'
    _rec_name = 'resp_nombre'    
    _inherit = ['asw.opcion_doble']

    resp_nombre = fields.Char(
        string = 'Nombre'
    )

    active = fields.Boolean(
        string = u'Está activo',
        default = True
    )

    @api.model
    def create(self, values):
        if 'resp_nombre' in values and values['resp_nombre'] not in [False, '']:
            cnt = self.env['asw.ap_respiratorio'].search_count([('resp_nombre', '=', values['resp_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo.''')

        result = super(asw_resp, self).create(values)

        return result

    @api.multi
    def write(self, values):
        if 'resp_nombre' in values and values['resp_nombre'] not in [False, '']:
            cnt = self.env['asw.ap_respiratorio'].search_count([('resp_nombre', '=', values['resp_nombre'])])
            if cnt > 0:
                raise exceptions.Warning('''El nombre provisto ya existe para otro registro.
                Por favor revise nuevamente y vuelva a intentarlo.''')

        result = super(asw_resp, self).write(values)

        return result